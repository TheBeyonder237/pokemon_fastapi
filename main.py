from dataclasses import dataclass, asdict
from typing import Union
import json
from fastapi import FastAPI, Path, HTTPException
import math

# -------------- Structure de données : Dictionnaire indexé par pokemon id ----------------

with open('pokemon.json', 'r') as f:
    pokemon_lists = json.load(f)
    
list_pokemons = {k+1:v for k, v in enumerate(pokemon_lists)}

# -----------------------------------------------------------------------------------------
@dataclass
class Pokemon():
    id: int
    name: str
    types: list[str]
    total: int
    hp: int
    attack: int
    defense: int
    attack_special: int
    defense_special: int
    speed: int
    evolution_id: Union[int, None] = None
# -----------------------------------------------------------------------------------------


app = FastAPI()

@app.get("/")
def root():
    return {'message': "Hello Les gars !"}

@app.get("/total_pokemons")
def get_total_pokemons() -> dict:
    """Recupération du nombre total de pokémons

    Returns:
        dict: Un dictionnaire avec le nomnbre total de pokémon
    """
    return {"total": len(list_pokemons)}


@app.get("/pokemons")
def get_all_pokemons() -> list[Pokemon]:
    """Affichage intégral des pokémons

    Returns:
        list[Pokemon]: Une liste contenant tous les pokemons
    """
    res = []
    for id in list_pokemons:
        res.append(Pokemon(**list_pokemons[id]))
    return res


@app.get("/pokemon/{id}")
def get_pokemon_by_id(id: int = Path(ge=1)) -> Pokemon:
    """Recupération d'un pokemon grace à son id

    Args:
        id (int, optional): id unique d'un pokemon. Defaults to Path(ge=1).

    Raises:
        HTTPException: Statut code 404 retourné en cas d'id inexistant

    Returns:
        Pokemon: Affiche l'object pokemon affilié à l'id
    """
    if id not in list_pokemons:
        raise HTTPException(status_code=404, detail="Ce pokemon n'existe pas")
    
    return Pokemon(**list_pokemons[id])


@app.post("/pokemon/")
def create_pokemon(pokemon: Pokemon) -> Pokemon:
    """Création d'un pokémon

    Args:
        pokemon (Pokemon): Objet pokémon possédant les mêmes caractéristiques que le classe Pokémon

    Raises:
        HTTPException: retourne un statut code 404 au cas où un id passé pour un pokemon est déjà présent

    Returns:
        Pokemon: Retourne l'objet pokemon qui a été crée
    """
    if pokemon.id in list_pokemons:
        raise HTTPException(status_code=404, detail=f"Le pokemon avec l'id {pokemon.id}, existe déjà")
    
    list_pokemons[pokemon.id] = asdict(pokemon)
    return pokemon


@app.put("/pokemon/{id}")
def update_pokemon_by_id(pokemon:Pokemon, id: int = Path(ge=1)) -> Pokemon:
    """Mettre à jour un pokemon

    Args:
        pokemon (Pokemon): Objet pokemon avec les attributs de la classe pokemon
        id (int, optional): identifiant unique d'un pokemon. Defaults to Path(ge=1).

    Raises:
        HTTPException: retourne un statut code 404 si l'id passé en paramètre n'existe pas

    Returns:
        Pokemon: Retourne l'objet pokemon avec les modifications effectuées
    """
    if id not in list_pokemons:
        raise HTTPException(status_code=404, detail="Ce pokemon n'existe pas")
    
    list_pokemons[id] = asdict(pokemon)
    return pokemon


@app.delete("/pokemon/{id}")
def delete_pokemon(id:int = Path(ge=1)) -> Pokemon:
    """Suppressionn d'un pokemon

    Args:
        id (int, optional): Identifiant unique d'un pokemon. Defaults to Path(ge=1).

    Raises:
        HTTPException: retourne un statut code 404 si l'id passé en paramètre n'existe pas

    Returns:
        Pokemon: Retourne l'objet ayant été supprimé
    """
    if id in list_pokemons:
        pokemon = Pokemon(**list_pokemons[id])
        del list_pokemons[id]
        return pokemon
    
    raise HTTPException(status_code=404, detail="Ce pokemon n'existe pas")


@app.get("/types")
def get_all_types() -> list[str]:
    """Récupère tous les types de pokémon existants

    Returns:
        list[str]: Retourne une liste d'entiers avec les différents types
    """
    types = []
    for pokemon in pokemon_lists:
        for type in pokemon["types"]:
            if type not in types:
                types.append(type)
    types.sort()
    return types


@app.get("/pokemons/search/")
def search_pokemons(
    types: Union[str, None] = None,
    evo: Union[str, None] = None,
    totalgt: Union[int, None] = None,
    totallt: Union[int, None] = None,
    sortby: Union[str, None] = None,
    order: Union[str, None] = None,
) -> Union[list[Pokemon], None] : 
    """Recherche d'un ou plusieurs pokemon en fonction des critères

    Args:
        types (Union[str, None], optional): type d'un pokemon. Defaults to None.
        evo (Union[str, None], optional): possibilité d'évolution. Defaults to None.
        totalgt (Union[int, None], optional): total de gt. Defaults to None.
        totallt (Union[int, None], optional): total de lt. Defaults to None.
        sortby (Union[str, None], optional): trier par ordre. Defaults to None.
        order (Union[str, None], optional): le type d'ordre. Defaults to None.

    Raises:
        HTTPException: retourne un statut code 404 si aucun pokemon ne correspond aux critères

    Returns:
        Union[list[Pokemon], None]: Retourne soit une liste de Pokemon soit rien en fonction des critères passés en paramètres
    """
    
    filtered_list = []
    res = []
    
    # Filtrage sur les types
    if types is not None:
        for pokemon in pokemon_lists:
            if set(types.split(",")).issubset(pokemon["types"]) : 
                filtered_list.append(pokemon)
                
    # Filtrage sur les évolutions
    if evo is not None:
        tmp = filtered_list if filtered_list else pokemon_lists
        new = []
        
        for pokemon in tmp:
            if evo == "true" and "evolution_id" in pokemon:
                new.append(pokemon)
            if evo == "false" and "evolution_id" not in pokemon:
                new.append(pokemon)
                
        filtered_list = new 
    
    # Filtrage sur greater than total
    if totalgt is not None:
        tmp = filtered_list if filtered_list else pokemon_lists
        new = []
        
        for pokemon in tmp:
            if pokemon["total"] > totalgt:
                new.append(pokemon) 
                
        filtered_list = new
        
    # Filtrage sur less than total
    if totallt is not None:
        tmp = filtered_list if filtered_list else pokemon_lists
        new = []
           
        for pokemon in tmp:
            if pokemon["total"] < totallt:
                new.append(pokemon)
                   
        filtered_list = new
        
    # Gestion du tri   
    if sortby is not None and sortby in ["id", "name", "totam"]:
        filtered_list = filtered_list if filtered_list else pokemon_lists
        sorting_order = False
        if order == "asc" : sorting_order = False
        if order == "desc" : sorting_order = True
        
        filtered_list = sorted(filtered_list, key= lambda d: d[sortby], reverse=sorting_order)
        
    # Réponse de l'API 
    if filtered_list:
        for pokemon in filtered_list:
            res.append(Pokemon(**pokemon))
        return res
    
    raise HTTPException(status_code=404, detail="Aucun Pokemon ne réponds aux critères de rcherce")


@app.get("/pokemons2/")
def get_all_pokemons(page: int=1, items: int=10) -> list[Pokemon]:
    """Affichage des pokemons avec pagination

    Args:
        page (int, optional): Rangé à laquelle on veut commencer l'affichage. Defaults to 1.
        items (int, optional): Nombre d'élements à afficher. Defaults to 10.

    Returns:
        list[Pokemon]: Retourne une liste de pokemon
    """
    items = min(items, 20)
    max_page = math.ceil(len(list_pokemons) / items)
    current_page = min(page, max_page)
    start = (current_page-1)*items
    stop = start + items if start + items <= len(list_pokemons) else len(list_pokemons)
    sublist = (list(list_pokemons))[start:stop]

    res = []

    for id in sublist :
        res.append(Pokemon(**list_pokemons[id]))
    
    return res