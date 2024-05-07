# LineGest
Projet de test de gestion de lignes

## Installation des dépendances back-end

Ce projet utilise l'outil pipenv pour gérer ses dépendances back-end. S'il n'est pas
déjà installé sur votre ordinateur, vous pouvez l'installer à l'aide de la commande
`pip install pipenv`.

Une fois pipenv installé, il vous suffit de suivre les instructions suivantes:
- Si vous avez décidé d'utiliser Postgresql, lancer la base de donnée à l'aide de `docker-compose up -d`
- Exécuter les migrations avec `pipenv run python manage.py migrate`
- Créer un super-utilisateur avec `pipenv run python manage.py createsuperuser`


## Installation des dépendances front-end

Pour les dépendances frontend, il est également nécessaire d'installer Node.js sur votre
ordinateur. Vous vouvez le faire en téléchargeant le binaire d'installation [directement
depuis cette page](https://nodejs.org/en/download), en l'exécutant et en suivant les
instructions. Node.js installera la commande npm qui vous permettra d'installer
les dépendances pour CSS et Javascript.

Une fois que node est installé, rendez-vous dans le sous-répertoire frontend du projet
et exécuter la commande `npm install`.

Un fois les dépendances installées, vous pouvez utiliser la commande `npm run start` pour
développer, ou `npm run build` pour compiler les fichiers de production.


## Generation des données

 - Périodes : `pipenv run python manage.py load_period 2023`
 - Catégories des labels : `pipenv run python manage.py load_category`
 - Labels : `pipenv run python manage.py load_label`
 - Status de taxations des ligne : `pipenv run python manage.py load_status_taxa_line`
 - Data exemple : `pipenv run python manage.py load_data .\linegest\phoneline\management\commands\data_exemples.csv`

=> a faire dans cette ordre


## Requêtes qui fonctionnent 
Non de ligne pour chaque status par label de taxation : 
Obtention de la liste des labels taxants : `list_label_taxant = Label.objects.filter(category__tag='CENTRE_TAXA')`
Sous requêtes pour les status de ligne :
 - Ligne taxant oui `taxant_oui = Count('line_phones', filter=Q(line_phones__status_taxa_line__name='TAXANT_OUI'))`
 - Ligne taxant non `taxant_non = Count('line_phones', filter=Q(line_phones__status_taxa_line__name='TAXANT_NON'))`
 - ligne taxant nd `taxant_nd = Count('line_phones', filter=Q(line_phones__status_taxa_line__name='NOT_DEFINE'))`

Compte par label sur l'ensemble des données changées
`labels=Label.objects.filter(category__tag='CENTRE_TAXA').annotate(taxant_oui=taxant_oui).annotate(taxant_non=taxant_non).annotate(taxant_nd=taxant_nd)
for label in labels:
    print(label, label.taxant_oui, label.taxant_non, label.taxant_nd)`


Compte des données par label et par période
`
for period in Period.objects.all():
    labels=Label.objects.filter(category__tag='CENTRE_TAXA').filter(line_phones__period__period_date=period.period_date).annotate(taxant_oui=taxant_oui).annotate(taxant_non=taxant_non).annotate(taxant_nd=taxant_nd)
    for label in labels:
        print(label, period, label.taxant_oui, label.taxant_non, label.taxant_nd)
`

## Requête rechercher 
Requête permettant d'avoir une sortie du type : 
`{'label_1':
    {'Janvier_2023': {'taxant_oui' : 5, 'taxant_non': 1, 'taxant_nd': 1},
    'Février_2023': {'taxant_oui' : 5, 'taxant_non': 1, 'taxant_nd': 1},
    'Mars_2023': {'taxant_oui' : 5, 'taxant_non': 1, 'taxant_nd': 1},
    'Avril_2023': {'taxant_oui' : 3, 'taxant_non': 0, 'taxant_nd': 0},
    'Mai_2023': {'taxant_oui' : 8, 'taxant_non': 1, 'taxant_nd': 1},
    'Juin_2023': {'taxant_oui' : 4, 'taxant_non': 1, 'taxant_nd': 1}},
'label_2':
    {'Janvier_2023': {'taxant_oui' : 1, 'taxant_non': 1, 'taxant_nd': 0},
    'Février_2023': {'taxant_oui' : 2, 'taxant_non': 1, 'taxant_nd': 0},
    'Mars_2023': {'taxant_oui' : 2, 'taxant_non': 1, 'taxant_nd': 0},
    'Avril_2023': {'taxant_oui' : 2, 'taxant_non': 1, 'taxant_nd': 0},
    'Mai_2023': {'taxant_oui' : 3, 'taxant_non': 2, 'taxant_nd': 0},
    'Juin_2023': {'taxant_oui' : 1, 'taxant_non': 1, 'taxant_nd': 0}},
'label_3':
    {'Janvier_2023': {'taxant_oui' : 0, 'taxant_non': 2, 'taxant_nd': 0},
    'Février_2023': {'taxant_oui' : 0, 'taxant_non': 2, 'taxant_nd': 0},
    'Mars_2023': {'taxant_oui' : 0, 'taxant_non': 2, 'taxant_nd': 0},
    'Avril_2023': {'taxant_oui' : 0, 'taxant_non': 2, 'taxant_nd': 0},
    'Mai_2023': {'taxant_oui' : 0, 'taxant_non': 4, 'taxant_nd': 0},
    'Juin_2023': {'taxant_oui' : 0, 'taxant_non': 2, 'taxant_nd': 0}}
}`
        