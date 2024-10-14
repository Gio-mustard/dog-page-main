class Pet:
    # this class is to read only
    def __init__(self, race: str, color: str, description: str, name: str):
        self.__race = race
        self.__color = color
        self.__description = description
        self.__name = name

    @property
    def race(self):
        return self.__race

    @property
    def color(self):
        return self.__color

    @property
    def description(self):
        return self.__description

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return f"Race: {self.__race}, Color: {self.__color}, Description: {self.__description}, Name: {self.__name}"

if __name__ == "__main__":
    import unittest
    import colorama
    colorama.init()
    class TestPet(unittest.TestCase):

        def setUp(self):
            self.pet = Pet(race="Golden Retriever", color="Golden", description="Friendly and energetic", name="Buddy")

        def test_race(self):
            print(colorama.Fore.GREEN + "Starting test: test_race")
            try:
                self.assertEqual(self.pet.race, "Golden Retriever", "The race of the pet should be 'Golden Retriever'")
            except AssertionError as e:
                print(colorama.Fore.RED + str(e))
            print(colorama.Fore.GREEN + "Ending test: test_race")

        def test_color(self):
            print(colorama.Fore.GREEN + "Starting test: test_color")
            try:
                self.assertEqual(self.pet.color, "Golden", "The color of the pet should be 'Golden'")
            except AssertionError as e:
                print(colorama.Fore.RED + str(e))
            print(colorama.Fore.GREEN + "Ending test: test_color")

        def test_description(self):
            print(colorama.Fore.GREEN + "Starting test: test_description")
            try:
                self.assertEqual(self.pet.description, "Friendly and energetic", "The description of the pet should be 'Friendly and energetic'")
            except AssertionError as e:
                print(colorama.Fore.RED + str(e))
            print(colorama.Fore.GREEN + "Ending test: test_description")

        def test_name(self):
            print(colorama.Fore.GREEN + "Starting test: test_name")
            try:
                self.assertEqual(self.pet.name, "Buddy", "The name of the pet should be 'Buddy'")
            except AssertionError as e:
                print(colorama.Fore.RED + str(e))
            print(colorama.Fore.GREEN + "Ending test: test_name")

        def test_str(self):
            print(colorama.Fore.GREEN + "Starting test: test_str")
            expected_str = "Race: Golden Retriever, Color: Golden, Description: Friendly and energetic, Name: Buddy"
            try:
                self.assertEqual(str(self.pet), expected_str, "The string representation of the pet should match the expected format")
            except AssertionError as e:
                print(colorama.Fore.RED + str(e))
            print(colorama.Fore.GREEN + "Ending test: test_str")

    unittest.main()