# Bonjour et bienvenu dans ce programme de simulation de BlackJack 

---

Premierement je vais présenter les règles spécifiques avec lesquels ce programme joue 

- Le croupier tire à 16 et reste à 17 
- pas de présence de +3 
- BlackJack paye 3 pour 2 

---

## Initialisation du programme : 
Vous serons demander dans l'ordre 

- Nombre de joueur (réels ou virtuels) (int)
Pour chaques joueurs 
- Nomination (string)
- Cave = Mise initial (int)
- Stratégie : le programme permets de jouer manuellement ou de suivre une stratégie 
Entrez 'Strat' pour utiliser la stratégie automatique enregistrée 
Entrez 'Manuel' pour jouer manuellement

---

## Comment utiliser le programme

**Ce programme peut vous permettre de jouer au black jack contre le croupier en ligne de commande**

les commandes en mode manuel sont : 

- tirer => tirer 
- rester => rester 
- doubler => double 
- split => double jeu 

**Ce programme peut vous permettre de jouer au BlackJack en suivant une stratégie près enregistrée**

Forme de la stratégie : 

La stratégie se présente sous forme de fichier JSON contenant la marche à suivre celon chaque situation 
les marches à suivres se présentent sous même forme que les actions en ligne de commande soit 

- tirer => tirer 
- rester => rester
- doubler => doubler 
- split => double jeu

L'architecture du JSON de stratégie est la suivante (exemple ci joint)
```
{
    "nom" : "Nom de la strat",
    "provenance" : "Lien de la strat obligatoire mais pas utile ",
    "assurance" : "1", *// REMARQUE : 1 si assurance 0 sinon, pas de gestion des assurancs en fonction des cas*
    "double": [ *// REMARQUE : correspond à la réaction si double en main*
        {
            "1": [ REMARQUE : correspond à la carte doublé
                {
                    "1": "split", REMARQUE : correspond à la carte visible du croupier 
                    "2": "split",
                    ...
                }],
            "2": [{...}],
            ...
            "10": [{...}],
          
        }
    ],
    "asPlusElse": [ REMARQUE : correspond à avoir un As en main
        {
            "2": [ REMARQUE : carte en plus de l'as, pas de 1 car As et As sont dans la catégorie double
                {
                    "1": "split", REMARQUE : correspond à la carte visible du croupier
                    "2": "split",
                    ...
                }],
            "3": [{...}],
            ... 
            "10": [{...}]
        }
    ],
    "sum": [ *// REMARQUE : correspond aux reste des cas et/ou si l'on tire plus d'une carte*
        {
            "5": [ *// REMARQUE : correpond à la somme des cartes en main commence à 5 car sinon soit double soit As + qqch d'autre* 
                {
                    "1": "split", *// REMARQUE : correspond à la carte visible du croupier* 
                    "2": "split",
                    ...
                }],
            "6": [{...}],
            ...
            "21": [{...}]
        }
    ]
}
```

---

**Pour enregistrer une stratégie :**

*/!\ IL NE PEUT Y AVOIR QU'UNE STRATEGIE AUTOMATIQUE EN COURS* 
*IL NE PEUT PAS Y AVOIR PLUSIEURS strat.json DANS LE DOSSIER ET SEUL LA STRATEGIE strat.json SERA UTILISEE*


creer un fichier strat.json dans le dossier courant contenant le JSON corespondant à votre stratégie 


Une fois la partie (manuel ou automatique) terminée un graphique apparaitra avec les courbes des gains de chaque joueurs (Attention si trop de joueur d'un coup le graphique sera illisible)
Un fichier 'nomDeStrat.json' sera crée avec les données suivantes de la partie 
- date 
- mise de départ
- nombre de tours tenus 
- cagnotte max
- tour de cagnotte max
- dernier tour avec gain positif ou nul
- historique des gains

En relancant une partie avec la même stratégie les données de la nouvelle partie seront ajoutées à la fin du json
 
*/!\ Utilisez le versionning sur vos noms de stratégie afin de ne pas mélanger les résultats après modifications des stratégies*