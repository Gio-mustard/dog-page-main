from oinformation import OInformation
class Owner:
    # this class is read only
    def __init__(self,name:str,addres:str,phone_number:str,info:OInformation,email:str) -> None:
        self.__name = name
        self.__address = addres
        self.__phone_number = phone_number
        self.__info = info
        self.__email = email

    @property
    def name(self) -> str:
        return self.__name

    @property
    def address(self) -> str:
        return self.__address

    @property
    def phone_number(self) -> str:
        return self.__phone_number

    @property
    def info(self) -> OInformation:
        return self.__info

    @property
    def email(self) -> str:
        return self.__email
    
    def __str__(self) -> str:
        return f"Name: {self.__name}, Address: {self.__address}, Phone Number: {self.__phone_number}, Email: {self.__email}"
    


if __name__ == "__main__":
    import unittest
    class TestOwner(unittest.TestCase):
        def setUp(self):
            self.owner = Owner("John Doe", "123 Main St", "123-456-7890", OInformation("dog", "brown", "friendly", "Max"), "johndoe@example.com")

        def test_owner_properties(self):
            self.assertEqual(self.owner.name, "John Doe")
            self.assertEqual(self.owner.address, "123 Main St")
            self.assertEqual(self.owner.phone_number, "123-456-7890")
            self.assertEqual(self.owner.info.get(), {"dog", "brown", "friendly", "Max"})
            self.assertEqual(self.owner.email, "johndoe@example.com")

        def test_owner_read_only(self):
            with self.assertRaises(AttributeError):
                self.owner.name = "Jane Doe"
            with self.assertRaises(AttributeError):
                self.owner.address = "456 Elm St"
            with self.assertRaises(AttributeError):
                self.owner.phone_number = "987-654-3210"
            with self.assertRaises(AttributeError):
                self.owner.info = OInformation("cat", "white", "playful", "Whiskers")
            with self.assertRaises(AttributeError):
                self.owner.email = "janedoe@example.com"

        def test_owner_str(self):
            self.assertEqual(str(self.owner), "Name: John Doe, Address: 123 Main St, Phone Number: 123-456-7890, Email: johndoe@example.com")

    unittest.main()