# EpicEvents CRM

L'application Django Epic Events CRM est créée dans le cadre d'un projet du parcours **Développeur d'application - Python** d'openclassrooms.

## Description

EpicEvents CRM présente une architecture back-end sécurisée permettant la gestion d'employés, clients, contrats et évènements via des endpoints d'API REST dédiés. 

Les points de terminaison sont développés conformément au cahier des charges. 
Trois groupes d'utilisateurs sont définis: Management, Sales et Support. Chaque groupe dispose de droits d'accès et de modification qui lui sont propres.

## Sécurité

La prévention des vulnérabilités auxquelles sont exposées les API a été prise en compte à travers le respect des recommandations de l'OWASP, notamment via le processus AAA (Authentication, Authorization, Accounting) des protocoles réseau.

- Authentication : Utilisation de tokens JWT
- Autorisation : Différentes règles restreignent l'accès des personnes non autorisés aux ressources exposées à travers les API.
- Accès : Les accès aux modifications et suppression des ressources sont également contraints selon le statut des utilisateurs identifiés.

## Configuration requise
- Python 3.x
- Django 3.x

## Configuration de la base de données
EECRM utilise un SGBDR installé localement. Postgre-sql est recommandé.
Afin de le configurer correctement, créez un fichier env.py à la racine de votre projet et alimentez-le avec les éléments suivants:
```
DATABASES = {
    "default": {
        "ENGINE": "your_engine",
        "NAME": "EECRM",
        "USER": "your_username",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

### Fonctionnement de l'application en local.

L'application est lancée en local, sur un serveur de développement.

1. Créez un dossier dédié à l'application. 

2. Clônez le dépôt Git dans votre répertoire local:
`git clone https://github.com/kcardon/EECRM.git`

3. Créez et lancez un environnement virtuel:
`python -m venv env`
`.\env\Scripts\Activate.ps1`

4. Installez les dépendances prérequises:
`pip install requirements.txt`

5. Créez la base de données:
`python manage.py migrate`

6. Lancez l'application:
`cd .\EECRM\`
`python manage.py runserver`

7. Utilisez la documentation POSTMAN pour effectuer les requêtes appropriées auprès des points de terminaison requis:
`https://documenter.getpostman.com/view/25029281/2s946e9t3c`

