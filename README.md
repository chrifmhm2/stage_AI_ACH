
# Test ACH

## Vue d'ensemble

Ce projet est une application web basée sur Django conçue pour gérer et générer des modèles XML pour des transactions. L'application inclut des fonctionnalités telles que l'enregistrement des utilisateurs, la gestion des comptes, et la possibilité de créer et de finaliser plusieurs transactions au sein d'une même session.

## Fonctionnalités

- **Génération de transactions** : Génération de fichiers XML pour les transactions en fonction des saisies utilisateur et des données provenant d'une base de données MySQL connectée.
- **Transactions multiples** : Les utilisateurs peuvent ajouter plusieurs transactions et les finaliser en une seule fois.
- **Contenu dynamique** : L'application charge dynamiquement les options de compte en fonction de la banque sélectionnée.
- **Interface utilisateur stylée** : L'interface inclut des pages stylisées avec des images de fond, des polices personnalisées et des boutons réactifs.

## Technologies utilisées

- **Django** : Framework web Python utilisé pour le backend.
- **MySQL** : Base de données utilisée pour stocker les données des utilisateurs et des transactions.
- **HTML/CSS** : Pour structurer et styliser les pages web.
- **JavaScript (jQuery)** : Pour le chargement dynamique de contenu (AJAX).
- **Faker** : Bibliothèque Python utilisée pour générer des données aléatoires pour les tests.
- **XML/XSD** : Pour la génération et la validation des modèles de transaction.

## Prérequis

Avant de commencer, assurez-vous d'avoir respecté les prérequis suivants :

- Python 3.8 ou une version ultérieure installée.
- Django 3.0 ou une version ultérieure installée.
- Serveur MySQL installé et en cours d'exécution.
- Git installé pour cloner le dépôt.

## Installation

1. **Cloner le dépôt :**

    ```bash
    git clone https://github.com/votre-nom-utilisateur/votre-repo.git
    cd votre-repo
    ```

2. **Configurer un environnement virtuel :**

    ```bash
    python -m venv venv
    venv\Scripts\activate  # Sur linux\macOs utilisez `source venv/bin/activate`
    ```

3. **Installer les paquets requis :**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configurer la base de données :**

    - Créez une base de données MySQL pour le projet. "mydjangodb"
    - Mettez à jour la configuration `DATABASES` dans `mydjangosite/settings.py` avec les détails de votre base de données.
    - Appliquez les migrations :

    ```bash
    python manage.py migrate
    ```

5. **Charger les données initiales :**

    Si vous avez une commande `load_data` ou un fichier de données, exécutez-le pour peupler la base de données :

    ```bash
    python manage.py load_data
    ```

6. **Lancer le serveur de développement :**

    ```bash
    python manage.py runserver
    ```

7. **Accéder à l'application :**

    Ouvrez votre navigateur et allez à l'adresse `http://127.0.0.1:8000/`.

## Utilisation

1. **Page principale** :
   - La page d'accueil fournit un lien pour générer un nouveau modèle de transaction.
   
2. **Générer un modèle** :
   - Sélectionnez une banque et un compte, spécifiez le montant et choisissez un identifiant de compte.
   - Ajoutez la transaction et finalisez-la lorsque vous êtes prêt.

3. **Interface d'administration** :
   - Accédez à l'interface d'administration Django à `/admin/` pour gérer les utilisateurs, les comptes et les transactions.

## Contribuer

Pour contribuer à ce projet, suivez ces étapes :

1. Forkez le dépôt.
2. Créez une nouvelle branche : `git checkout -b feature/votre-nom-de-fonctionnalité`.
3. Apportez vos modifications et validez-les : `git commit -m 'Ajout d'une fonctionnalité'`.
4. Poussez vers la branche : `git push origin feature/votre-nom-de-fonctionnalité`.
5. Soumettez une pull request.






