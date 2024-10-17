import sys
import os
from information_manager.main import get
import click
from entry_point_response_manager.main import make_page
from command_line_interface import prints as print
import json

DATA = {
    "pet_schema":None,
    "pet_description":None,
    "owner_schema":None,
    "pet_photos":None
}


def show_data()->None:
    print.question(json.dumps(DATA, indent=4))
    return [False,""]

def save_data()->None:
    with open('data_test.json', 'w') as file:
        json.dump(DATA, file, indent=4)
    return [False,""]

PET_PATTERN = "race, color, name"
OWNER_PATTERN = "name,addres,phone_number,email"

def set_data_of_pet()->bool:
    print.title("Describe a tu mascota",decorator="*")
    print.title("Cosas que deberias de mencionar (Puede extender la descripcion todo lo que quieras)...")
    properties = (
        "Nombre",
        "Raza",
        "Caracteristicas",
        "Color de pelo"
    )
    for property in properties:
        print.question("*",end=". ")
        print._(property)
    
    description = print.inp(":")
    schema = get(description,PET_PATTERN)
    DATA['pet_schema'] = schema
    return True

def confirm_data_of_pet()->bool:
    print.question(json.dumps(DATA['pet_schema'], indent=4))
    response = print.inp("La informacion es correcta?? S/N : ").lower()
    if response == 'n':
        reset_steps()
        return False 
    return True

def confirm_data_of_owner()->bool:
    print.question(json.dumps(DATA['owner_schema'], indent=4))
    response = print.inp("La informacion es correcta?? S/N : ").lower()
    if response == 'n':
        reset_steps()
        return False 
    return True

def set_data_of_owner()->bool:
    print.title("Describete a ti",decorator="-")
    print.title("Cosas que deberias de mencionar (Puede extender la descripcion todo lo que quieras)...")
    properties = (
        "Tu Nombre",
        "Tu email",
        "Tu direccion aproximada",
        "Tu numero de telefono"
    )
    for property in properties:
        print.question("*",end=". ")
        print._(property)
    
    description = print.inp(":")
    schema = get(description,OWNER_PATTERN)
    DATA['owner_schema'] = schema
    return True

def reset_steps()->None:
    for step in STEPS:
        step['completed'] = False
    return [False,""]

STEPS = [
    {"completed":False,"content":"Dar una descripcion de tu mascota",'make':set_data_of_pet},
    {"completed":False,"content":"Confirmar descripcion de tu mascota","make":confirm_data_of_pet},
    {"completed":False,"content":"Dar tu informacion de contacto","make":set_data_of_owner},
    {"completed":False,"content":"Confirmar tu informacion de contacto","make":confirm_data_of_owner},
]
try:
    with open('data_test.json', 'r') as file:
        DATA = json.load(file)
    for step in STEPS:
        step['completed'] = True
except:
    pass
def print_instructions()->None:
    print.title("Description",decorator='-')
    description = ""
    print._(description)
    print.title("Instructions",decorator='-')
    for index,step in enumerate(STEPS):
        print.title(f"{index+1}.",end="")
        if step['completed']:
            print.title("✔",end="")
        print._(f"\t{step['content']}")
    print._("-"*32)



def show_command_list()->None:
    print.title("Commands", decorator='-')
    for command in COMMANDS:
        print._(command)
    return [False,""]

def clear():
    click.clear()
    print_instructions()
    return [False,""]

def make_next_step():
    for index,step in enumerate(STEPS):
        if not step['completed']:
            mark_completed = step['make']()
            if mark_completed:
                STEPS[index]['completed'] = True
            break
    return [False,""]

COMMANDS = {
    "--clear":clear,
    '--exit':lambda : sys.exit(0),
    '--help':show_command_list,
    "--make-next-step":make_next_step,
    "--reset":reset_steps,
    "--add-photos":lambda:[False,""],
    "--add-description":lambda:[False,""],
    '--show-data':show_data,
    '--save':save_data
}



def send_to_make_a_page()->None|str:
    if not all(step['completed'] for step in STEPS):
        return [True,"Make you sure are completed all steps on instructions"]
    pet_info = DATA["pet_schema"]
    pet_info['description'] = DATA["pet_description"]
    owner_info = DATA["owner_schema"]
    if DATA['pet_photos'] is not None:
        pet_info['extra']['photos'] = DATA["pet_photos"]
    __download_page,__open_on_browser = make_page(
        pet_info=pet_info,
        owner_info=owner_info
    )
    COMMANDS['--download'] = lambda : download(__download_page)
    COMMANDS['--open'] = lambda : [False,__open_on_browser()]
    return [False,""]


def download(callback)->None:
    path = None
    while path is None:
        path = print.inp("Enter the path to save the project:").replace("/","\\")
        if len(path) == 0 or  "\\" not in path:
            print.warning("Path cannot be empty")
            path = None
    try:
        callback(path,on_spa=True)
        return [False,None]
    except Exception as e:
        return [True,str(e)]

def main():
    COMMANDS['--make-page'] = send_to_make_a_page
    COMMANDS['--clear']()
    while True:
        command = print.inp().lower().replace(" ","")
        if command in COMMANDS:
            has_error,message = COMMANDS[command]()
            if has_error:
                print.warning(message)