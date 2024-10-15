from vfile import VirtualFile
class HTML(VirtualFile):
    HEAD_TAG = "head"
    BODY_TAG = "body"
    def __init__(self, content: str = None,use_strict:bool=True) -> None:
        """
        This class is a subclass of VirtualFile and is used to manage HTML content.
        It provides methods to insert content between specific tags in the HTML and add tag line by line.
        """
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
        """
        This method inserts the content between the specified tag in the HTML.
        If the content is None, it raises a SyntaxError.
        If the tag is not found, it raises a SyntaxError.
        If on_end is True, the content is inserted at the end of the tag.
        Otherwise, it is inserted at the beginning of the tag.
        """
        if (content is None) or (type(content) is not str):
            raise SyntaxError("The content must be a string.")
        start_index, end_index = self.__find_range_index_by(between)
        if start_index == -1 :
            raise SyntaxError("The tag not found.")
        if on_end:
            index_to_insert = end_index
        else:
            index_to_insert = start_index+1

        self.add(content, index=index_to_insert)
