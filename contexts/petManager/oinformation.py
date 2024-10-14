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
    def __filter_types(*args)->tuple:
        """
        This method filters out arguments that are of type None or bool.
        It returns a list of arguments that are not of these types.
        """
        filtered_array = []
        for arg in args:
            arg_type = type(arg)
            if arg_type in [type(None),bool]:
                continue
            if arg_type in [list,tuple,set]:
                filtered_array.append(OInformation.__filter_types(*arg))
                continue
            
            if arg_type in [dict]:
                filtered_array.append((None,*OInformation.__filter_types(*[item for item in arg.items() if item[1] is not None ])))
                continue

            filtered_array.append(arg)

        return tuple(filtered_array)

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
        schema_copy = self.__schema.copy()
        for item in schema_copy:
            if type(item) is tuple and None in item:
                item = dict(item[1::])
            yield item   
    

if __name__ == "__main__":
    import time
    
    def test_o_information():
        start_time = time.time()
        
        # Test case 1: Adding arguments to the schema
        info = OInformation("dog", "brown", "friendly", "Max")
        assert set(info.get()) == {"dog", "brown", "friendly", "Max"}

        # Test case 2: Setting the schema with new arguments
        info.set("cat", "white", "playful", "Whiskers")
        assert set(info.get()) == {"cat", "white", "playful", "Whiskers"}

        # Test case 3: Filtering out None and bool types
        info.set(None, True, "bird", "blue", "intelligent", "Sunny")
        assert set(info.get()) == {"bird", "blue", "intelligent", "Sunny"}

        # Test case 4: Retrieving a copy of the schema
        schema_copy = set(info.get())
        assert isinstance(schema_copy, set)
        assert not schema_copy == {"cat", "white", "playful", "Whiskers", "bird", "blue", "intelligent", "Sunny"}

        # Test case 5 : Sub info
        info = OInformation(1,2,3,(4,5,6),{"key":"value",'1':2,"3":None})
        schema_copy = tuple(info.get())
        print(f"{schema_copy=}")
        
        for item in (1, 2, 3, (4, 5, 6), {"key": "value", '1': 2}):
            assert item in schema_copy
            
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"All tests passed successfully. Total time elapsed: {elapsed_time:.2f} seconds.")
    test_o_information()
