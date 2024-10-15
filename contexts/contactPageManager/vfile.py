import unittest

class VirtualFile:
    def __init__(self,firtsLine:str=None,use_strict:bool=False) -> None:
        self.__raw = list()
        self.__use_strict = use_strict
        if firtsLine is not None:
            self.add(firtsLine)

    def _apply_rules(self, line:str)->str|tuple:
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



    

class HTML(VirtualFile):
    HEAD_TAG = "head"
    BODY_TAG = "body"
    def __init__(self, content: str = None,use_strict:bool=True) -> None:
        super().__init__(use_strict=use_strict)
        if content:
            for line in content.split('\n'):
                self.add(line)

    def __find_range_index_by(self,tag:str = 'head') -> tuple[int,int]:
        """
        This method finds the indices of the tag tag in the VirtualFile.
        It returns a tuple containing the start and end indices of the tag.
        If no tag is found, it returns (-1, -1).
    
        * Example of a result:
        The method would return (0, 7) indicating that the tag starts at index 0 and ends at index 7.
        """
        start_index = -1
        end_index = -1
        for i, line in enumerate(self.get('for-each-line')):
            if f"<{tag}" in line:
                start_index = i
            elif f"</{tag}" in line:
                end_index = i
                break
        return (start_index, end_index)
    
    def insert(self,between:str = HEAD_TAG,content:str = None,on_end:bool=False):
        if content is None:
            raise SyntaxError("The content must be a string.")
        start_index, end_index = self.__find_range_index_by(between)
        if start_index == -1 :
            raise SyntaxError("The tag not found.")
        if on_end:
            index_to_insert = end_index
        else:
            index_to_insert = start_index

        self.add(content, index=index_to_insert)
