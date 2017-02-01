import json;

#Cargamos los ficheros de configuración
with open('config.json') as data_file:
    data = json.load(data_file)
with open('repos_config.json') as repos_data_file:
    repos_data = json.load(repos_data_file)
with open('provision_config.json') as provision_data_file:
    provis_data = json.load(provision_data_file)

tab = "    "

#La función que modifica el fichero repos.yml
def modify_repos(repos_vars):
    #Abrimos el archivo repos.yml, usando la ruta especificada en la configuración
    repos = open(data["repos_route"], 'w')
    new_repos_content = data["repos_header"]

    #Creamos el nuevo contenido de repos.yml, usando la cabecera especificada en la configuración y los checkboxes marcados.
    #La configuración por defecto mantiene el mismo formato del archivo en github.
    for name in repos_vars:
        if repos_vars[name].get() == 1:
            repos_line = tab + name + ":\n"
            repos_line += tab * 2 + "repo: " + data["github"] + repos_data[name] + "\n"
            repos_line += tab * 2 + "version: " + data["version"] + "\n"
            repos_line += tab * 2 + "force: " + data["force"] + "\n"
            new_repos_content = new_repos_content + repos_line

    repos.write(new_repos_content)
    print(new_repos_content)

#La función que modifica los ficheros de vagrant provision
def modify_provision(server, is_base):
    #Cargamos el contenido nuevo
    config_new = open(provis_data["config"][server], 'r').read()
    vagrant_new = open(provis_data["vagrantfile"][server], 'r').read()
    if(is_base == 1):
        playbook_new = open(provis_data["playbook"]["base"], 'r').read()
    else:
        playbook_new = open(provis_data["playbook"][server], 'r').read()

    #El destino del contenido nuevo
    config_file = open(provis_data["root"] + "config.yml", 'w')
    playbook_file = open(provis_data["root"] + "playbook.yml", 'w')
    vagrant_file = open(provis_data["root"] + "Vagrantfile", 'w')

    #Escritura del nuevo contenido en el destino
    config_file.write(config_new)
    playbook_file.write(playbook_new)
    vagrant_file.write(vagrant_new)