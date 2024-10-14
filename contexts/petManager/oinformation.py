class OInformation:
    def __init__(self,*args) -> None:
        """
        This class represents a collection of information that can be dynamically added or set.
        It filters out arguments of type None or bool to ensure the integrity of the data.
        The schema can be retrieved as a copy for read-only purposes.
        """
        self.__schema = set()
        self.add(*args)

    @staticmethod
    def __filter_types(*args):
        """
        This method filters out arguments that are of type None or bool.
        It returns a list of arguments that are not of these types.
        """

        return [arg for arg in args if type(arg) not in [type(None), bool] ]

    def add(self, *args) -> None:
        """
        This method adds arguments to the schema after filtering out None and bool types.
        """
        filtered_args = self.__filter_types(*args)
        self.__schema.update(filtered_args)

    def set(self, *args) -> None:
        """
        This method sets the schema to the provided arguments after filtering out None and bool types.
        """
        filtered_args = self.__filter_types(*args)
        self.__schema = set(filtered_args)

    def get(self) -> set:
        """
        This method returns a copy of the schema. 
        It is not a reference to the original object, 
        and is intended for read-only purposes.
        """
        return self.__schema.copy()
    

if __name__ == "__main__":
    import time
    
    def test_o_information():
        start_time = time.time()
        
        # Test case 1: Adding arguments to the schema
        info = OInformation("dog", "brown", "friendly", "Max")
        assert info.get() == {"dog", "brown", "friendly", "Max"}

        # Test case 2: Setting the schema with new arguments
        info.set("cat", "white", "playful", "Whiskers")
        assert info.get() == {"cat", "white", "playful", "Whiskers"}

        # Test case 3: Filtering out None and bool types
        info.set(None, True, "bird", "blue", "intelligent", "Sunny")
        assert info.get() == {"bird", "blue", "intelligent", "Sunny"}

        # Test case 4: Retrieving a copy of the schema
        schema_copy = info.get()
        assert isinstance(schema_copy, set)
        assert not schema_copy == {"cat", "white", "playful", "Whiskers", "bird", "blue", "intelligent", "Sunny"}

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"All tests passed successfully. Total time elapsed: {elapsed_time:.2f} seconds.")
    test_o_information()
