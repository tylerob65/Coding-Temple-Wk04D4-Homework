import requests, json, os

def create_pokemon_dict_from_api(from_api):
    # Check if have name cached
    pokemon = dict()
    # Add abilities
    pokemon['abilities'] = []
    for ability in from_api["abilities"]:
        pokemon['abilities'].append(ability['ability']["name"])

    # Add Base Experience
    pokemon['base_experience'] = from_api['base_experience']

    # Add Stats
    pokemon['stats'] = dict()
    for stat in from_api['stats']:
        stat_val = stat['base_stat']
        stat_name = stat['stat']['name']
        pokemon['stats'][stat_name] = stat_val

    # Add Shiny Sprite
    pokemon['shiny_sprite_url'] = from_api['sprites']['front_shiny']
    return pokemon

def PokePrint():
    print("Welcome to PokePrint")
    print("You can leave at any time by typing 'leave'")
    wants_to_continue = True
    while wants_to_continue:
        print("Please enter the name of a pokemon you would like to look up?")
        name = input().strip().lower()

        if name == "leave":
            print("Thanks! I hope you use PokePrint sometime again soon")
            return

        # Check if have record of name
        if f"{name}.json" in os.listdir("pokemon/"):
            # If have record get pokemon dictionary
            with open(f'pokemon/{name}.json','r') as openfile:
                pokemon = json.load(openfile)
        else:
            url = f"https://pokeapi.co/api/v2/pokemon/{name}"
            response = requests.get(url)
            if not response.ok or not name:
                print("Sorry, that was not a valid pokemon name")
                print("Please try again or enter 'leave' to quit")
                continue
            
            # Gets a slimmed down pokemon dictionary
            pokemon = create_pokemon_dict_from_api(response.json())

            # Adds stored slimmed down pokemon dictionary for future use
            with open(f"pokemon/{name}.json","w") as outfile:
                outfile.write(json.dumps(pokemon))
        print(f"Pokemon's name is {name}")
        print()
        print("Pokemon's abilities are....")
        # Lists Abilitites
        for ability in pokemon["abilities"]:
            print(ability)

        # Base Experience
        print("\nPokemon's base experience")
        print(pokemon['base_experience'])

        # "Lists Stats"
        print("\nPokemon's base stats are...")
        for stat_name,stat_val in pokemon['stats'].items():
            print(f"{stat_name}: {stat_val}")

        # Shiny Image
        print("\nURL to front_shiny sprite")
        print(pokemon['shiny_sprite_url'])
        print()


if __name__ == "__main__":
    PokePrint()