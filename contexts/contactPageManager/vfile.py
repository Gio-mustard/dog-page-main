
class VirtualFile:
    def __init__(self,firtsLine:str=None,use_strict:bool=False) -> None:
        """
        Initializes a VirtualFile object.
        * The VirtualFile class is designed to manage a virtual file system. 
        * It allows adding, removing, and clearing lines of text, 
        * and provides options for strict line handling and custom separators.
        Args:
            firtsLine (str, optional): The first line of the virtual file. Defaults to None.
            use_strict (bool, optional): Indicates if the file should use strict line handling. Defaults to False.
        """
        self.__raw = list()
        self.__use_strict = use_strict
        if firtsLine is not None:
            self.add(firtsLine)

    def _apply_rules(self, line:str)->str|tuple:
        """
        In strict mode, the VirtualFile class treats each newline character ('\n') as a delimiter for a new line.
        When adding a line, if the line contains a newline character, it is split into multiple lines and each line is added separately.
        This allows for precise control over the content of the virtual file, ensuring that each line is treated as a distinct entity.
        """
        if not line: return line
        if self.__use_strict:
            return tuple(line.split('\n')) if '\n' in line else line
        else:
            return line.replace("\n", " ")

    @staticmethod
    def __check_line_type(line):
        if type(line) is not str:
            raise TypeError("The line on the VirtualFile must be a String.")
        
    def add(self,line:str,index:int=None):
        VirtualFile.__check_line_type(line)
        final_line = self._apply_rules(line)
        if index is not None:
            self.__raw.insert(abs(index), final_line)
        elif type(final_line) is str:
            self.__raw.append(final_line)
        elif type(final_line) in [tuple,list]:
            for inline in final_line:
                self.add(inline)

    def remove(self,line:str=None,index:int=None):
        """
        Removes a line from the virtual file based on the provided parameters.
        This method can remove a line by its content or by its index. If both parameters are provided, the index takes precedence.
        Args:
            line (str, optional): The content of the line to be removed. Defaults to None.
            index (int, optional): The index of the line to be removed. Defaults to None.
        Raises:
            SyntaxError: If neither line nor index is provided, or if the line or index does not exist in the virtual file.
        """
        if index is not None:
            self.__raw.pop(abs(index))
            
        elif line is not None:
            self.__raw.remove(line)
        
        else:
            raise SyntaxError("To remove a line on virtual file that's need a line to match or index line,but you give nothing.")


    def clear(self):
        self.__raw = list()

    def get(self,sep:str = "\n")->str:
        if sep == "for-each-line":
            return self.__raw
            
        return f"{sep}".join(self.__raw)

    def num_of_lines(self):
        return len(self.__raw)