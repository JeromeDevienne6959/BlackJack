from pickletools import string1
import random
import string
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import json
import os

with open('strat.json') as fic:
    jsonFile = json.load(fic)


compteur = 1
nombreDeJeux = 20
doPrint = False
compteurTour = 0

def myPrint(string):
    if(doPrint):
        print(string)

class Joueur:
    nom = ""
    cagnotte = 0
    status = ""
    historiqueCagnotte = []
    strategie = ""
    miseInitial = 0

    def __init__(self,cave,nom,strat) -> None:
        self.cagnotte = cave
        self.nom = nom
        self.status = "OK"
        self.historiqueCagnotte = [self.cagnotte]
        self.strategie = strat
        self.miseInitial = 0.05 * self.cagnotte

    def jouer(self):
        self.historiqueCagnotte.append(self.cagnotte)
        mise = input(f"{self.nom} Votre mise s'il vous plait")
        while(mise>self.cagnotte):
            myPrint("Vous n'avez pas assez")
            mise = input(f"{self.nom} Votre mise s'il vous plait")
        jeu = Jeu(self,mise,[])
        self.cagnotte -= mise
        listeDesMains.ajouterJeu(jeu)

    def eliminer(self):
        self.status = "Eliminé"

    def __str__(self) -> str:
        return (
            f"Nom Joueur : {self.nom}"
            +"\n"
            +f"Cagnotte = {self.cagnotte}"
            +"\n"
            +f"Status : {self.status}")

class JeuCroupier:
    nombreDeCartes = 0
    listeDeCartes = []
    sommeDesCartes = 0
    sommeAlter = 0
    status = ""
    
    def __init__(self) -> None:
        self.nombreDeCartes = 0
        self.listeDeCartes = []
        self.sommeDesCartes = 0
        self.status = "OK"

    def afficherJeuEntier(self):
        
        exitString = (
            "\n"
            +"JEU CROUPIER :\n"
            +f"Nombre de cartes = {self.nombreDeCartes}"
            +"\n"
        )
        if(
            (self.sommeAlter < 22)
            and
            (1 in self.listeDeCartes)
        ):
            exitString = exitString + (
                f"Somme des cartes = {self.sommeDesCartes}/{self.sommeAlter}\n"
            )
        else:
            exitString = exitString + (
                f"Somme des cartes = {self.sommeDesCartes}\n"
            )
            
        exitString = exitString + (
            
            f"Liste des cartes = {self.listeDeCartes}"
            +"\n"
        )
        
        myPrint(exitString)
        
    def afficherJeuTronque(self):
        myPrint(
            "\n"
            f"Jeu Croupier :\n Carte visible = {self.listeDeCartes[0]}\n"
        )
        return (self.listeDeCartes[0])
    
    def tirer(self):
        self.listeDeCartes.append(jeuDeCarte.tirerUneCarte())
        self.nombreDeCartes = self.calcNbCard()
        self.sommeDesCartes = self.calculerSommeJeu()
        self.sommeAlter = self.calculerSommeJeuAlter()
        
    def calculerSommeJeu(self):
        somme = 0
        for i in self.listeDeCartes:
            somme += i
        return somme
    
    def calculerSommeJeuAlter(self):
        if 1 in self.listeDeCartes:
            return self.calculerSommeJeu() +10
        else:
            return self.calculerSommeJeu()
    
    def calcNbCard(self):
        return len(self.listeDeCartes)
    
    def setState(self,state):
        self.status = state

    def testerTirageCroupier(self):
        if(
            (16 < self.sommeAlter < 22)
            or
            (16 < self.sommeDesCartes )
            ):
            test = False
        else:
            test = True
        return test
        
class Jeu(JeuCroupier):
    
    mise = 0
    joueurDApartenance = None
    id = 0
    assure = ""
    
    def __init__(self,player,bet,cardList):
        global compteur
        self.id = compteur
        compteur += 1
        self.joueurDApartenance = player
        self.mise = bet
        if(len(cardList) == 2):
            self.listeDeCartes = []
            myPrint(f"Nouveau jeu ICI : {self}")
            self.listeDeCartes.append(cardList[0])
            self.tirer()
            myPrint(f"Nouveau jeu LABAS : {self}")
        else:
            self.listeDeCartes = cardList
        self.nombreDeCartes = self.calcNbCard()
        self.sommeDesCartes = self.calculerSommeJeu()
        player.cagnotte -= bet
        self.status = "OK"
        self.assure = "N"
    
    def split(self):
        nouveauJeu = Jeu(self.joueurDApartenance,self.mise,self.listeDeCartes)
        listeDesMains.ajouterJeu(nouveauJeu)
        self.listeDeCartes.pop(0)
        self.tirer()
        myPrint(f"Nouveau jeu : {nouveauJeu}")
        
    def assurer(self):
        self.assure = "Y"

    def __str__(self) -> string:
        
        sommeCarte = self.sommeDesCartes
        if(1 in self.listeDeCartes):
            sommeAlter = sommeCarte+10
        

        exitString = (
            f"JEU N°{self.id}"
            +"\n"
            +f"Nombre de cartes = {self.nombreDeCartes}"
            +"\n"
            +f"Liste des cartes = {self.listeDeCartes}"
            +"\n"
        )
        
        if(
            (self.sommeAlter < 22)
            and
            (1 in self.listeDeCartes)
        ):
            exitString = exitString + (
                f"Somme des cartes = {sommeCarte}/{sommeAlter}"
            )
        else:
            exitString = exitString + (
                f"Somme des cartes = {sommeCarte}"
            )
                    
        exitString = exitString + (
            "\n"
            +f"Mise = {self.mise}"
            +"\n"
            +f"Appartient au joueur : {self.joueurDApartenance.nom}"
            +"\n"
            +f"Status du jeu : {self.status}"
        )

        return(exitString)

    def ajoutGain(self, gain):
        self.joueurDApartenance.cagnotte += gain
        self.joueurDApartenance.historiqueCagnotte.append(self.joueurDApartenance.cagnotte)
    
        
class ListeDesJeux:
    listeDesJeux=[]

    def __init__(self) -> None:
        self.listeDesJeux = []
    

    def afficher(self):
        for i in range (len(self.listeDesJeux)):
            myPrint("\n")
            myPrint(f"JEU N°{i+1}")
            myPrint(self.listeDesJeux[i])
            myPrint("\n")

    def ajouterJeu(self,jeu):
        self.listeDesJeux.append(jeu)

class ListeJoueurs:
    listeDesJoueurs=[]

    def __init__(self) -> None:
        self.listeDesJoueurs = []

    def afficher(self):
        for i in range (len(self.listeDesJoueurs)):
            myPrint("\n")
            myPrint(f"JOUEURS N°{i}")
            myPrint(self.listeDesJoueurs[i])
            myPrint("\n")

    def ajouterJoueur(self,je):
        self.listeDesJoueurs.append(je)
        
    def joueursEnLice(self):
        test = False
        for i in self.listeDesJoueurs:
            if i.status == "OK":
                test = True
        return test

class Paquet:
    paquetDeCarte = []

    def initaliser(self):
        self.paquetDeCarte=[1,2,3,4,5,6,7,8,9,10,10,10,10]
        self.paquetDeCarte = nombreDeJeux*self.paquetDeCarte*4
        self.paquetDeCarte.append(0)
        random.shuffle(self.paquetDeCarte) 
    
    def afficher(self):
        print(self.paquetDeCarte)
    
    def tirerUneCarte(self):
        carte = self.paquetDeCarte[0]
        while (carte == 0):
            self.initaliser()
            carte = self.paquetDeCarte[0]
        self.paquetDeCarte.pop(0)
        return carte


def isChoixCorrect(nombre, liste):
    if nombre in liste:
        return True
    else:
        return False

def inscriptionDesJoueurs():
    for i in range(nbJoueurs):
        print("\n")
        print(f"Entrer les donnees du joueurs N°{i+1} :")
        nom = input(f"Entrer le nom du joueur N°{i+1}\n")
        cave = float(input(f"Entrer la cave de {nom} ?\n"))
        strat = ""
        while(strat not in ["Strat","Manuel"]):
            print(
                "\n"
                +f"Manuel- Jeu Manuel"
                +"\n"
                +f"Strat- Jeu automatique strategie issue d'un JSON  "
            )
            strat = input("Entrer la stratégie du joueur\n")
        joueur = Joueur(cave,nom,strat)
        listeDesJoueurs.ajouterJoueur(joueur)
        print("\n")
        
def depotDesMises():
    for i in listeDesJoueurs.listeDesJoueurs:
        if(i.status == "OK"):
            strat = i.strategie
            match strat:
                case "Manuel":
                    mise = float(input(f"Bonjour {i.nom}, merci d'entrer votre mise (cagnotte = {i.cagnotte})\n"))
                    while mise>i.cagnotte:
                        myPrint("Attention, le casino ne fait pas crédit")
                        mise = float(input(f"Bonjour {i.nom}, merci d'entrer votre mise (cagnotte = {i.cagnotte})\n"))
                    i.historiqueCagnotte.append(i.cagnotte)
                case "Strat":
                    mise = i.miseInitial
                    if mise>i.cagnotte:
                        mise = i.cagnotte
            jeu = Jeu(i,mise,[])
            listeDesMains.ajouterJeu(jeu)
        
def distribuerCartes():
    for j in range(2):
        for i in range (len(listeDesMains.listeDesJeux)):
            listeDesMains.listeDesJeux[i].tirer()
        jeuCroupier.tirer()
        
def blackJack(tab):
    return(
        (len(tab) == 2)
        and
        (1 in tab)
        and
        (10 in tab))

def choixManuel(jeu):
    listeChoixCorects=[]
    choix = 10
    while not isChoixCorrect(choix,listeChoixCorects):
        myPrint("Veuillez jouer")
        myPrint("tirer- Tirer")
        myPrint("rester- Arreter Ici")
        listeChoixCorects = ["tirer","rester"]
        if(
            (len(jeu.listeDeCartes) == 2)
            and
            (jeu.joueurDApartenance.cagnotte >= jeu.mise)
            ):
            myPrint("double- Doubler")
            listeChoixCorects = ["tirer","rester","doubler"]
        if (
            ((len(jeu.listeDeCartes)) == 2)
            and
            (jeu.listeDeCartes[0] == jeu.listeDeCartes[1])
            and
            (jeu.joueurDApartenance.cagnotte >= jeu.mise)
            ):
            myPrint("split- Spliter")
            listeChoixCorects = ["tirer","rester","doubler","split"]
        choix = input("Votre Choix ? \n")
        return choix

def choixStratJson(jeu,jeuCroupier,data):
    carteCroupier = str(jeuCroupier.listeDeCartes[0])
    if(jeu.listeDeCartes[0] == jeu.listeDeCartes[1]):
        carteJoueurEnDouble = str(jeu.listeDeCartes[0])
        choix = data['double'][0][carteJoueurEnDouble][0][carteCroupier]
    elif(
        (jeu.listeDeCartes[0] == 1)
        or
        (jeu.listeDeCartes[1] == 1)
        and
        (jeu.listeDeCartes[0] != jeu.listeDeCartes[1])
    ):
        if(jeu.listeDeCartes[0] == 1):
            autreCarte = str(jeu.listeDeCartes[1])
        else:
            autreCarte = str(jeu.listeDeCartes[0])
        choix = data['asPlusElse'][0][autreCarte][0][carteCroupier]
        
    else:
        somme = str(sommeOuSommeAlter(jeu.sommeDesCartes, jeu.sommeAlter))
        choix = data['sum'][0][somme][0][carteCroupier]
    return choix
       
def sommeOuSommeAlter(somme, sommeAlter):
    if(16>sommeAlter>22):
        return sommeAlter
    else :
        return somme

def tour(jeu):
    while(jeu.status == "OK"):
        myPrint(jeu)
        if blackJack(jeu.listeDeCartes):
            myPrint("BLACK JACK")
            jeu.setState("BJ")
            choix = "rester"
            listeChoixCorects = ["tirer","rester","double","split"]
        else:
            
            strategie = jeu.joueurDApartenance.strategie
            
            match strategie:
                case "Manuel" :
                    choix = choixManuel(jeu)
                case "Strat":
                    choix = choixStratJson(jeu,jeuCroupier,jsonFile)
                case _ :
                    myPrint("/!\ Strategie inconnue choix manuel aplique /!\\")
                    choix = choixManuel(jeu)
                    
                    
            listeChoixCorects = ["tirer","rester"]
            if(
                (len(jeu.listeDeCartes) == 2)
                and
                (jeu.joueurDApartenance.cagnotte >= jeu.mise)
                ):
                listeChoixCorects = ["tirer","rester","double"]
            if (
                ((len(jeu.listeDeCartes)) == 2)
                and
                (jeu.listeDeCartes[0] == jeu.listeDeCartes[1])
                and
                (jeu.joueurDApartenance.cagnotte >= jeu.mise)
            ):
                listeChoixCorects = ["tirer","rester","double","split"]
                
        if (not isChoixCorrect(choix, listeChoixCorects)):
            choix = "rester"

        
        
        
        myPrint("\n")
        
        match choix:
            case "tirer" :
                jeu.tirer()
                if (jeu.sommeDesCartes > 21):
                    myPrint(jeu)
                    jeu.setState("Burn")
            case "rester" :
                jeu.setState("Stop")
            case "double" :
                jeu.joueurDApartenance.cagnotte -= jeu.mise
                jeu.mise *= 2
                jeu.tirer()
                jeu.setState("Stop")
                myPrint(jeu)
            case "split" :
                myPrint("Creation du double jeu")
                jeu.split()

def distributionDesGains(jeu):
    sommeNormale = jeu.sommeDesCartes
    sommeAlter = jeu.sommeAlter
    if(
        (sommeAlter >sommeNormale)
        and
        (sommeAlter < 22)
    ):
        jeu.sommeDesCartes = sommeAlter
                
    resultatCroupier = 0
    if(
        (jeuCroupier.sommeAlter < 22)
        and
        (jeuCroupier.sommeAlter > jeuCroupier.sommeDesCartes)
    ):
        resultatCroupier = jeuCroupier.sommeAlter
    else:
        resultatCroupier = jeuCroupier.sommeDesCartes
        
    myPrint(
        f"{jeu.joueurDApartenance.nom} Vous obtenez {jeu.sommeDesCartes}"
        +"\n"
        +f"Le croupier fait {resultatCroupier}"
    )
    
    if(jeuCroupier.status == "BJ"):
        if(jeu.sommeDesCartes == 21):
            myPrint(f"Egalité, Vous recuperez {1 * jeu.mise} \n\n")
            jeu.ajoutGain(
                1 * jeu.mise
            )
            
        elif(jeu.assure == "Y"):
            myPrint(f"Le croupier Gagne vous perdez {jeu.mise}. Mais vous récuperez le double de l'assurance = {jeu.mise}\n\n")
            jeu.ajoutGain(
                1 * jeu.mise
            )
        elif(jeu.assure == "N"):
            myPrint(f"Le croupier Gagne vous perdez {jeu.mise}.\n\n")
            jeu.ajoutGain(
                0 * jeu.mise
            )
            if(jeu.joueurDApartenance.cagnotte == 0):
                jeu.joueurDApartenance.eliminer()

    else:
        resultat = jeu.status
        match resultat:
            case "BJ":
                myPrint(f"BLACK JACK VOUS GAGNEZ {2.5 * jeu.mise} \n\n")
                jeu.ajoutGain(
                    2.5 * jeu.mise
                )
            case "Burn":
                myPrint(f"BURN vous perdez {jeu.mise}\n\n")
                jeu.ajoutGain(
                    0 * jeu.mise
                )
                if(jeu.joueurDApartenance.cagnotte == 0):
                    jeu.joueurDApartenance.eliminer()
                
            case "Stop":
                
                if(
                    (resultatCroupier > 21)
                    or
                    (resultatCroupier < jeu.sommeDesCartes)
                ):
                    myPrint(f"Vous Gagnez {2*jeu.mise} face au croupier\n\n")
                    jeu.ajoutGain(
                        2 * jeu.mise
                    )
                elif(resultatCroupier == jeu.sommeDesCartes):
                    myPrint(f"Egalité, Vous recuperez {1 * jeu.mise} \n\n")
                    jeu.ajoutGain(
                        1 * jeu.mise
                    )
                else: 
                    myPrint(f"Le croupier Gagne vous perdez {jeu.mise} \n\n")
                    jeu.ajoutGain(
                        0 * jeu.mise
                    )
                    if(jeu.joueurDApartenance.cagnotte == 0):
                        jeu.joueurDApartenance.eliminer()
            
def testerTirageCroupier(jeu):
    if(
        (16 < jeu.sommeAlter < 22)
        or
        (16 < jeu.sommeDesCartes )
        ):
        test = False
    else:
        test = True
    return test

def tourCroupier(jeu):
    if(
        (jeu.nombreDeCartes==2)
        and
        (jeu.sommeAlter == 21)
        ):
        jeu.setState("BJ")
    test = jeu.testerTirageCroupier()
    while(test):        
        jeu.tirer()
        test = jeu.testerTirageCroupier()

def creerAbs(tab):
    absTab = []
    for i in range(len(tab)):
        absTab.append(i)
    return absTab

def tracerCourbe(ListeDesJoueurs):
    for i in ListeDesJoueurs:
        absTab = creerAbs(i.historiqueCagnotte)
        plt.plot(absTab,i.historiqueCagnotte, label = f"Cagnotte de {i.nom}")
        plt.legend()
        myPrint(f" Joueur : {i.nom} a jouer {len(absTab)} mains avec la strategie ")
    plt.show()

def tourAssurance(listeDesJeux,jsonFile):
    for jeu in listeDesJeux:
        listeChoixCorects = [1,2]
        choix = 3
        while not isChoixCorrect(choix,listeChoixCorects):
            if(jeu.joueurDApartenance.strategie != "Manuel"):
                choix = jsonFile["assurance"]
                choix = int(choix)
            else :
                myPrint(f"{jeu.joueurDApartenance.nom} Voulez vous assurer votre jeu ?\n") 
                myPrint(jeu)
                myPrint(
                    "1- Assurer"
                    +"\n"
                    +"2- NE PAS Assurer"
                )
                choix = int(input())
        if choix == 1:
            jeu.assurer()
            jeu.joueurDApartenance.cagnotte -= (0.5 * jeu.mise)   

def findTourSansRetour(tab,valeurCritique):
    pos = 0
    for i in range(len(tab)):
        if(tab[i] == valeurCritique):
            pos = i
    return pos

def statJeu(joueur,nomStrat):
    date = str(datetime.now())
    listeDeCagnotte = joueur.historiqueCagnotte
    miseDepart = listeDeCagnotte[0]
    cagnotteMax = max(listeDeCagnotte)
    tourDeCagnotteMax = listeDeCagnotte.index(cagnotteMax)
    nombreDeTour = len(listeDeCagnotte)
    tourSansRetour = findTourSansRetour(listeDeCagnotte,cagnotteMax)
    objetStat = {
        "date" : date,
        "mise de depart" : miseDepart,
        "nombre de tours tenus" : nombreDeTour,
        "cagnotte max" : cagnotteMax,
        "tour de cagnotte max" : tourDeCagnotteMax,
        "Dernier tour a gain positif ou nul" : tourSansRetour,
        "historique des gains" : listeDeCagnotte,   
    }
    
    string = nomStrat + ".json"
    
    try:
        jsonFile = open(string,"r")
    except:
        jsonFile = open(string,"w")
        obj = {"tab" : []}
        json.dump(obj,jsonFile)
        jsonFile.close()
        jsonFile = open(string,"r")
        
    objJson = json.load(jsonFile)
    objJson["tab"].append(objetStat)
    jsonFile.close()
    os.remove(string)
    
    jsonFile = open(string,"w")
    json.dump(objJson, jsonFile)
    jsonFile.close()
    pass
#######  PROGRAMME PRINCIPALE #######


jeuDeCarte = Paquet()
jeuDeCarte.initaliser()

listeDesMains = ListeDesJeux()

listeDesJoueurs = ListeJoueurs()

nbJoueurs = int(input("Combien de joueurs vont jouer ?"))
while(0 >= nbJoueurs):
    myPrint("Entré eronée")
    nbJoueurs = input("Combien de joueurs vont jouer ?")
    
inscriptionDesJoueurs()

jeuCroupier = JeuCroupier()



myPrint("Let's get our gambling freak on !!\n\n")

test = True
while (listeDesJoueurs.joueursEnLice()):
    
    print(f"TOUR N°{compteurTour}")
    
    jeuCroupier = JeuCroupier()
    listeDesMains = ListeDesJeux()
    

    depotDesMises()     
    distribuerCartes()
    carteCroupier = jeuCroupier.afficherJeuTronque()
    
    if(carteCroupier) == 1:
        myPrint("ASSURANCE")
        tourAssurance(listeDesMains.listeDesJeux,jsonFile)
        

    for i in listeDesMains.listeDesJeux:
        
        myPrint("\n")
        tour(i)
        
    tourCroupier(jeuCroupier)
    
    jeuCroupier.afficherJeuEntier()

    for i in listeDesMains.listeDesJeux:
        distributionDesGains(i)
    
    if(compteurTour % 1000 == 0 and compteurTour != 0):
        tracerCourbe(listeDesJoueurs.listeDesJoueurs)
    compteurTour += 1

for i in (listeDesJoueurs.listeDesJoueurs):
    statJeu(i,jsonFile["nom"])
    pass
tracerCourbe(listeDesJoueurs.listeDesJoueurs)
