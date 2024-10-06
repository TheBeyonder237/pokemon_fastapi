# Pokémon API

Ce projet est une API basée sur FastAPI qui permet de gérer une collection de Pokémon. Il permet de récupérer, créer, mettre à jour, supprimer et rechercher des Pokémon en fonction de divers critères. Les données des Pokémon sont stockées dans un fichier JSON local (`pokemon.json`).

## Fonctionnalités

- **Lister tous les Pokémon** : Obtenez la liste complète de tous les Pokémon disponibles.
- **Récupérer un Pokémon par ID** : Accédez à un Pokémon spécifique en utilisant son identifiant unique.
- **Créer un nouveau Pokémon** : Ajoutez un nouveau Pokémon à la collection.
- **Mettre à jour un Pokémon existant** : Modifiez les détails d’un Pokémon en fonction de son ID.
- **Supprimer un Pokémon** : Supprimez un Pokémon de la collection.
- **Rechercher des Pokémon** : Cherchez des Pokémon en fonction de plusieurs critères (types, évolution, statistiques totales, etc.).
- **Pagination** : Affichez les Pokémon avec pagination.
- **Récupérer les types de Pokémon** : Obtenez tous les types de Pokémon uniques.

## Endpoints

### Racine
- `GET /`  
  Retourne un message de bienvenue.

### Gestion des Pokémon
- `GET /total_pokemons`  
  Retourne le nombre total de Pokémon dans la collection.
  
- `GET /pokemons`  
  Récupère la liste complète de tous les Pokémon.
  
- `GET /pokemon/{id}`  
  Récupère un Pokémon en fonction de son identifiant unique.

- `POST /pokemon/`  
  Crée un nouveau Pokémon à partir des données fournies.

- `PUT /pokemon/{id}`  
  Met à jour un Pokémon existant selon son identifiant.

- `DELETE /pokemon/{id}`  
  Supprime un Pokémon en fonction de son identifiant.

### Recherche et Filtres
- `GET /pokemons/search/`  
  Permet de rechercher des Pokémon en fonction de critères comme le type, l'évolution, les statistiques totales et les options de tri.

### Pagination
- `GET /pokemons2/?page={page}&items={items}`  
  Récupère les Pokémon avec pagination. Spécifiez le numéro de page et le nombre d'éléments par page (par défaut 10, maximum 20).

### Types de Pokémon
- `GET /types`  
  Retourne une liste de tous les types de Pokémon uniques.

## Structure des Données

### Classe Pokémon

L'API utilise une classe `Pokemon`, définie à l'aide de `dataclass` pour représenter les données de manière structurée.

- `id`: (int) Identifiant du Pokémon
- `name`: (str) Nom du Pokémon
- `types`: (list de str) Types du Pokémon
- `total`: (int) Statistiques totales de base du Pokémon
- `hp`: (int) Points de vie (HP)
- `attack`: (int) Attaque
- `defense`: (int) Défense
- `attack_special`: (int) Attaque spéciale
- `defense_special`: (int) Défense spéciale
- `speed`: (int) Vitesse
- `evolution_id`: (int ou None) ID de l'évolution (le cas échéant)

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/TheBeyonder237/pokemon_fastapi.git
   cd pokemon_fastapi
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Lancez l'application :
   ```bash
   uvicorn main:app --reload
   ```

4. Accédez à la documentation de l'API :
   ```
   http://127.0.0.1:8000/docs
   ```

## Format des Données JSON

Le fichier `pokemon.json` est une liste de dictionnaires, où chaque dictionnaire représente un Pokémon avec ses attributs associés (ID, nom, types, statistiques, etc.).

Exemple d'entrée pour un Pokémon :
```json
{
  "id": 1,
  "name": "Bulbizarre",
  "types": ["Plante", "Poison"],
  "total": 318,
  "hp": 45,
  "attack": 49,
  "defense": 49,
  "attack_special": 65,
  "defense_special": 65,
  "speed": 45,
  "evolution_id": 2
}
```

## Licence

Ce projet est sous licence MIT.