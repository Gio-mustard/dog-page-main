import sys
import os
from PIL import Image
from tkinter import filedialog
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from colorama import Fore, Style

from contexts.IContactPage.interface import I as __I

def __make_qr(url):

    import qrcode
    # Datos que quieres convertir en QR
    data = url

    # Crear el objeto QRCode
    qr = qrcode.QRCode(
        version=2,  # Controla el tamaño del código QR, puede ser de 1 a 40
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nivel de corrección de errores
        box_size=100,  # Tamaño de cada cuadrado del QR
        border=4,  # Tamaño del borde (4 es el mínimo recomendado)
    )

    # Añadir datos al QR
    qr.add_data(data)
    qr.make(fit=True)

    # Crear la imagen del QR
    img = qr.make_image(fill="black", back_color="white")
    img.show()
    return img


def __init(owner_info, pet_info):
    i = __I()
    i.add_owner_info(owner_info)
    i.add_pet_info(pet_info)
    return i

def __download(response, on_spa:bool,initial_path:str = None):
    # ----------------------------------------------------------
    abs_path = filedialog.askdirectory() if initial_path is None else os.path.abspath(initial_path)

    print(f"{Fore.CYAN}Path to save : {abs_path}{Style.RESET_ALL}")
    def find_photos()->dict|None:
        for item in response.data['pet']['properties']:
            if item['title'] == 'photos':
                return [url for url in item['children']]

    photos = find_photos()
    content = []
    # ----------------------------------------------------------

    if on_spa:
        html_content = response.get_on_single_page()
        content.append(html_content)
    else:
        html_content,css_content,js_content = response.get_project()
        content.append(html_content)
        content.append(css_content)
        content.append(js_content)
    # ----------------------------------------------------------

    for index,item in enumerate(content):
        filename = ''
        match index:
            case 0:
                  filename = 'index.html'
            case 1:
                  filename = f'assets\\style_{index}.css'
            case 2:
                  filename = f'assets\\script_{index}.js'
        path = abs_path +"\\"
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        path +=  filename
        if not os.path.exists(path):
            mode = 'x'
        else:
             mode = 'w'
        with open(path, mode,encoding='utf8') as file:
            print('*'*10)
            print(f"{Fore.GREEN}Saved {Style.RESET_ALL}:{path=}")
            print('*'*10)
            if ".html" in path:
                item += '\n<link rel="stylesheet" crossorigin href="./assets/index_1.css">'
                item += '\n<script type="module" crossorigin src="./assets/index_2.js"></script>'
            file.write(item)

    # ----------------------------------------------------------

    if photos is not None:
        photos_paths = []
        for file in photos:
            photo_path = __copy_file(file.replace("/",'\\'), abs_path+'\\' + 'assets\\')
            photos_paths.append(photo_path)

        for item in response.data['pet']['properties']:
            if item['title'] == 'photos':
                response.data['pet']['properties'].remove(item)

        response.data['pet']['properties'].insert(0, {
            "title": "photos",
            "children": photos_paths
        })
    # ----------------------------------------------------------

    import json
    path = abs_path + "\\" + 'public\\'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    path += "info.json"
    if not os.path.exists(path):
        mode = 'x'
    else:
        mode = 'w'
    print('*'*10)
    print(f"{Fore.GREEN}Saved {Style.RESET_ALL}:{path=}")
    print('*'*10)
    with open(path,mode=mode,encoding="utf8") as file:
        json.dump(response.data, file,indent=4)
    # ----------------------------------------------------------

def __copy_file(source_path: str, destination_path: str) -> None:
    """
    Copies the contents of a file from a source path to a destination path.

    Args:
        source_path (str): The path of the source file.
        destination_path (str): The path where the file will be copied.

    Raises:
        FileNotFoundError: If the source file does not exist.
        IOError: If there is an issue reading or writing the file.
    """
    
    im = Image.open(source_path)
    if not os.path.exists(destination_path):
        os.makedirs(destination_path, exist_ok=True)
    filename = destination_path + os.path.basename(source_path)
    im.save(filename)
    print('*'*10)
    print(f"{Fore.GREEN}Saved {Style.RESET_ALL}:{filename=}")
    print('*'*10)
    return ".\\assets\\"+os.path.basename(source_path)

def __open_on_browser(response):
    import tempfile
    from  threading import Thread
    with tempfile.TemporaryDirectory() as temp_dir:
        # Your code here
        __download(response, on_spa=True, initial_path=temp_dir)
        PORT = 2307
        import os
        os.chdir(temp_dir)
        import subprocess
        
        with open(os.path.join(temp_dir, 'script.py'), 'w') as file:
            file.write(
                f"""import http.server
import socketserver
import webbrowser

with socketserver.TCPServer(("", {PORT}), http.server.SimpleHTTPRequestHandler) as httpd:
    print("serving at port", {PORT})
    webbrowser.open(f'http://localhost:{PORT}/index.html')
    httpd.serve_forever()
"""
            )

        subprocess.Popen(f"start cmd /k python {os.path.join(temp_dir, 'script.py')}", shell=True)
        import time
        time.sleep(5)
        subprocess.Popen(f"start cmd /k C:\cloudflared\cloudflared.exe tunnel --url http://localhost:{PORT}/index.html",shell=True)
        input(":")


def make_page(owner_info, pet_info):
    """ Example of how to write owner and pet info objects\n
     owner_info = {
         'name': 'John Doe',
         'address': '123 Main St',
         'phone_number': '555-1234',
         'email': 'john@example.com',
         'extra': ['No extra information']
     }\n
     pet_info = {
         'race': 'Golden Retriever',
         'color': 'Golden',
         'description': 'A friendly dog',
         'name': 'Buddy',
         'extra': ['Vaccinations up to date',
                    {
                        "title":"photos",
                        "content":["C:/Users/sergio morquecho/Pictures/perro.jpg", "C:/Users/sergio morquecho/Pictures/34-w-Metro.jpg"]
                    }
                   ]
     }
    """
    i = __init(owner_info, pet_info)
    response = i.get_response()
    return (
        lambda path=None,on_spa=True: __download(response,on_spa,path),
        lambda : __open_on_browser(response),
    )