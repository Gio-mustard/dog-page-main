import sys
import subprocess
import os
import glob

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from contactPageManager.contactPage import ConctactPage as FilesManager
from petManager.petinformation import Manager as PetManager

class IResponse:
    def __init__(self,file_manager:FilesManager,data:dict) -> None:
        if type(file_manager) != FilesManager: raise TypeError('file_manager must be a FilesManager')
        if type(data) != dict: raise TypeError('data must be a dict')
        self.__file_manager = file_manager
        self.__data = data

    def get_project(self) -> tuple[str]:
        """
        This method retrieves the project files from the file manager and returns them as a tuple.
        The tuple contains the HTML, CSS, and JavaScript files of the project.

        @return [html : str , css : str , js : str]        
        """
        return (
            self.__file_manager.get_html(),
            self.__file_manager.get_css(),
            self.__file_manager.get_js()
        )

    def get_on_single_page(self) -> str:
        return self.__file_manager.make_project().get()
    
    @property
    def data(self) -> dict:
        return self.__data.copy()

class I:
    """
    This class is the main interface for the contact page. It initializes the file manager and pet manager.
    It also provides methods to add pet and owner information, and to get the response.
    """
    def __init__(self) -> None:
        self.__files_manager = FilesManager()
        self.__pet_manager = PetManager()

    def __add_info(self, info: dict,identify:str,function,keys:tuple[str]) -> None:
        if type(info) != dict: raise TypeError(f'{identify} must be a dict')
        values = list(info.get(key) for key in keys)
        if 'extra' in keys: 
            del values[keys.index('extra')]
            values.extend(info.get('extra',[]))
        function(*values)


    def add_pet_info(self, info: dict) -> None:
        self.__add_info(info, 
                        'pet_info',
                        self.__pet_manager.add_pet, 
                        ('race', 'color', 'description', 'name', 'extra'))

    def add_owner_info(self, info: dict) -> None:
        self.__add_info(info,
                        'owner_info',
                        self.__pet_manager.add_owner,
                        ('name', 'address', 'phone_number', 'email', 'extra'))


    def get_response(self) -> IResponse:
        """
        This method generates a response object containing the file manager and the prepared object data.
        It orchestrates the process of preparing the directory, executing commands, preparing object data, saving JSON,
        and adding HTML, styles, and scripts to the file manager. The method returns an IResponse object.

        @return IResponse: An object containing the file manager and the prepared object data.
        """
        path = self.__get_directory()
        self.__execute_commands(path)
        path+= "/dist/"
        
        object_data = self.__prepare_object_data()

        self.__save_json(path, object_data)

        self.__add_html_to_file_manager(path)

        self.__add_styles_to_file_manager(path)

        self.__add_scripts_to_file_manager(path)

        return IResponse(file_manager=self.__files_manager, data=object_data)


    def __get_directory(self) -> str:
        path = r"./template-page/"
        path = os.path.abspath(path)
        path = path.replace("\\", "/")
        print(f'JSON:{path=}')
        return path

    def __execute_commands(self, path: str)->None:
        """
        This function executes a series of commands in the specified directory to prepare the environment for the project.
        It pulls the latest code from the main branch of a Git repository, lists the directory contents, installs Node.js dependencies,
        and builds the project using npm. The output of the commands is captured and printed to the console.
        """
        self.__execute_git_pull(path)
        self.__list_directory_contents(path)
        self.__install_node_dependencies(path)
        self.__build_project(path)

    def __execute_git_pull(self, path: str)->None:
        comando = ["cmd", "/c", "git pull origin main"]
        resultado = subprocess.run(comando, cwd=path, text=True, capture_output=True)
        print("Salida del comando git pull:", resultado.stdout)

    def __list_directory_contents(self, path: str)->None:
        comando = ["cmd", "/c", "dir"]
        resultado = subprocess.run(comando, cwd=path, text=True, capture_output=True)
        print("Salida del comando dir:", resultado.stdout)

    def __install_node_dependencies(self, path: str)->None:
        comando = ["cmd", "/c", "npm install"]
        resultado = subprocess.run(comando, cwd=path, text=True, capture_output=True)
        print("Salida del comando npm install:", resultado.stdout)

    def __build_project(self, path: str)->None:
        comando = ["cmd", "/c", "npm run build"]
        resultado = subprocess.run(comando, cwd=path, text=True, capture_output=True)
        print("Salida del comando npm run build:", resultado.stdout)

    def __prepare_object_data(self) -> dict:
        pet_info = [{
            "title": item,
            "children": None,
        } if type(item) is not dict else {
            "title": list(item.keys())[0],
            "children": list(item.values())[0],
        } for item in tuple(self.__pet_manager.information.pet.info.get())]

        owner_info = [{
            "title": item,
            "children": None,
        } if type(item) is not dict else {
            "title": list(item.keys())[0],
            "children": list(item.values())[0],
        } for item in tuple(self.__pet_manager.information.owner.info.get())]

        return {
            "pet": {
                "name": self.__pet_manager.information.pet.name,
                "race": self.__pet_manager.information.pet.race,
                "color": self.__pet_manager.information.pet.color,
                "description": self.__pet_manager.information.pet.description,
                "properties": pet_info
            },
            "owner": {
                "name": self.__pet_manager.information.owner.name,
                "address": self.__pet_manager.information.owner.address,
                "phone_number": self.__pet_manager.information.owner.phone_number,
                "email": self.__pet_manager.information.owner.email,
                "extra": owner_info
            }
        }

    def __save_json(self, path: str, object_data: dict)->None:
        with open(path + 'info.json', 'w') as file:
            import json
            json.dump(object_data, file, indent=4)

    def __add_html_to_file_manager(self, path: str)->None:
        with open(path + 'index.html', 'r') as file:
            self.__files_manager.add_tag(file.read())

    def __add_styles_to_file_manager(self, path: str)->None:
        css_files = glob.glob(path + 'assets/*.css')
        if css_files:
            styles = ''
            for style_file in css_files:
                with open(style_file, 'r') as file:
                    styles += file.read() + '\n'
            self.__files_manager.set_style(styles)

    def __add_scripts_to_file_manager(self, path: str)->None:
        js_files = glob.glob(path + 'assets/*.js')
        if js_files:
            for script_file in js_files:
                with open(script_file, 'r') as file:
                    self.__files_manager.add_script(file.read())

    