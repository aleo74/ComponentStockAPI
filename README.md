# ComponentStockAPI

L'API ElectroStockAPI est une solution de gestion de stocks de composants électroniques conçue pour simplifier la gestion, le suivi et le contrôle des stocks de composants électroniques. Que vous soyez un passionné d'électronique, un étudiant, un ingénieur électronique ou une petite entreprise, cette API vous permet de garder une trace efficace de vos composants électroniques, d'optimiser les réapprovisionnements et d'améliorer la gestion de projets électroniques.

## Fonctionnalités clés

- Création de listes de composants électroniques.
- Ajout, mise à jour et suppression de composants.
- Suivi des mouvements de stock (entrées, sorties, achats, ventes, etc.).
- Notifications de réapprovisionnement.
- Recherche et filtrage avancés.

## Installation

Suivez ces étapes pour installer et exécuter ComponentStockAPI sur votre environnement local.

### Prérequis

- Python 3.x
- MongoDB (avec une base de données préalablement créée)

### Instructions

1. Clonez le référentiel depuis GitHub :

   ```bash
   git clone https://github.com/aleo74/ComponentStockAPI
   cd ComponentStockAPI

2. Créez un environnement virtuel (recommandé) :

        python -m venv venv
        source venv/bin/activate  # Pour Linux/macOS
        .\venv\Scripts\activate  # Pour Windows


3. Installez les dépendances Python avec pip :

        pip install -r requirements.txt

4. Configurez les variables d'environnement en copiant, modifiant er en renomant le fichier .env.example en .env à la racine du projet.


Assurez-vous de personnaliser les valeurs des variables d'environnement en fonction de votre configuration.

5. Lancez l'application :

        flask run

L'API sera accessible à l'adresse http://127.0.0.1:5000/ par défaut. Vous pouvez accéder à l'API à l'aide d'outils tels que Postman ou cURL.