import argparse
# import requests
# from bs4 import BeautifulSoup

commands = {
    'RECHERCHER': lambda params: search_content(params),
    'RECUPERER': lambda params: retrieve_content(params),
    'SAUVEGARDER': lambda params: save_content(params)
}

content = ""

def search_content(params):
    search = params['termes']
    from_dt = params['depuis']
    to_dt = params["jusqu'a"]
    mode = params["mode"]

    # Effectuer la search et extraire le content
    # ...

def retrieve_content(params):
    css_selector = params['partie']

    # Récupérer le content en utilisant le sélecteur CSS et l'enregistrer dans une variable
    # ...

def save_content(params):
    export_file = params['dans']

    with open('./exports/' + export_file, '+wt') as file:
        file.write(content)

parser = argparse.ArgumentParser(description='Micro-langage pour extraction de content web')
parser.add_argument('script', help='Script contenant les commandes à exécuter')
args = parser.parse_args()

with open(args.script, 'r') as script_file:
    script_lines = script_file.readlines()

for line in script_lines:
    line = line.strip()
    if line:
        command_parts = line.split(' ', maxsplit=1)
        command_name = command_parts[0].upper()
        command_params = {}

        if len(command_parts) > 1:
            param_parts = command_parts[1].split('"')
            param_parts = [part.strip() for part in param_parts if part.strip()]

            if len(param_parts) % 2 == 0:
                for i in range(0, len(param_parts), 2):
                    param_name = param_parts[i].strip().lower()
                    param_value = param_parts[i+1].strip()
                    command_params[param_name] = param_value
            else:
                print('Erreur de format des paramètres dans la ligne:', line)
                continue

        if command_name in commands:
            commands[command_name](command_params)
        else:
            print('Commande inconnue:', command_name)
