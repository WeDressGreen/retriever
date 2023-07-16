import argparse
import requests
import json

commands = {
    'RECHERCHER': lambda params: search_content(params),
    'AFFICHER': lambda params: show_content(),
    'SAUVEGARDER': lambda params: save_content(params)
}

author = ""
authorEmail = ""
writtenAt = ""
content = ""

def search_content(params):
    global author
    global authorEmail
    global writtenAt
    global content

    search = params['termes']
    from_dt = params['depuis'] if 'depuis' in params else None
    to_dt = params["jusqu'a"] if "jusqu'a" in params else None

    reqParams = { "search": search }

    if from_dt and to_dt:
        reqParams["from"] = from_dt
        reqParams["to"] = to_dt

    headers = {'Content-Type': 'application/json'}

    res = requests.post("https://retriever.dynamored.com/search", data=json.dumps(reqParams), headers=headers)

    if res.status_code == 200:
        resContent = res.json()["data"]

        content = resContent['content']
        author = resContent['author']
        authorEmail = resContent['authorEmail']
        writtenAt = resContent['writtenAt']
    else:
        content = "Aucun résultat trouvé"

def show_content():
    global author
    global authorEmail
    global writtenAt
    global content

    print(author + " <" + authorEmail + ">")
    print(writtenAt)
    print(content)

def save_content(params):
    global author
    global authorEmail
    global writtenAt
    global content

    export_file = params['dans']

    with open('./exports/' + export_file, '+wt', encoding="utf-8") as file:
        file.write(author + " <" + authorEmail + ">\n")
        file.write(writtenAt + "\n\n")
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
