from pet import Pet
from owner import Owner
from oinformation import OInformation

class PetInformation:
    def __init__(self) -> None:
        self.__id = id(self)
        self.__owner:Owner
        self.__pet:Pet

    def set_owner(self, name: str, address: str, phone_number: str, email: str, *info):
        self.__owner = Owner(name=name, address=address, phone_number=phone_number, email=email, info=OInformation(*info))

    def set_pet(self, race: str, color: str, description: str, name: str, *info):
        self.__pet = Pet(race=race, color=color, description=description, name=name, info=OInformation(*info))

    @property
    def id(self):
        return self.__id
    
    @property
    def owner(self) -> Owner:
        return self.__owner

    @property
    def pet(self) -> Pet:
        return self.__pet
    
    def __str__(self) -> str:
        return f"ID: {self.id}, Owner: {self.owner}, Pet: {self.pet}"
    

class Manager:
    def __init__(self) -> None:
        self.__pet_information:PetInformation = PetInformation()

    def add_pet(self, race: str, color: str, description: str, name: str, *info) -> None:
        self.__pet_information.set_pet(race,color,description,name,*info)

    def add_owner(self, name: str, address: str, phone_number: str, email: str, *info) -> None:
        self.__pet_information.set_owner(name,address,phone_number,email,*info)

    @property
    def information(self) -> PetInformation:
        return self.__pet_information
    

if __name__ == "__main__":
    import unittest
    import colorama
    colorama.init()
    class TestManager(unittest.TestCase):
        def setUp(self):
            self.manager = Manager()
        def test_add_pet(self):
            print(colorama.Fore.GREEN + "Starting test: test_add_pet")
            try:
                self.manager.add_pet("Golden Retriever", "Golden", "Friendly and energetic", "Buddy", "dog", "brown", "friendly", "Max")
                self.assertIsNotNone(self.manager.information.pet, "The pet should not be None after adding")
            except AssertionError as e:
                print(colorama.Fore.RED + str(e))
            print(colorama.Fore.GREEN + "Ending test: test_add_pet")
        def test_add_owner(self):
            print(colorama.Fore.GREEN + "Starting test: test_add_owner")
            try:
                self.manager.add_owner("John Doe", "123 Main St", "123-456-7890", "johndoe@example.com", "dog", "brown", "friendly", "Max")
                self.assertIsNotNone(self.manager.information.owner, "The owner should not be None after adding")
            except AssertionError as e:
                print(colorama.Fore.RED + str(e))
            print(colorama.Fore.GREEN + "Ending test: test_add_owner")
    unittest.main()
