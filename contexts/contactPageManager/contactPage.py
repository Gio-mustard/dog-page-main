from vfile import VirtualFile
from vfile_html import HTML

class ConctactPage:
    def __init__(self) -> None:
        self._id = id(self) 
        self.__html = HTML()
        self.__css = VirtualFile()
        self.__js = VirtualFile()

    def add_tag(self,line)->None:
        self.__html.add(line)

    def set_style(self, css:str)->None:
        self.__css.add(css)

    def add_script(self, js:str)->None:
        self.__js.add(js)

    def make_project(self)->HTML:
        js = self.get_js()
        self.__html.insert(
            between=self.__html.BODY_TAG,
            content=f"<script>{js}</script>",
            on_end=True
        )
        css = self.get_css()
        self.__html.insert(
            between=self.__html.HEAD_TAG,
            content=f"<style>{css}</style>",
            on_end=True
        )
        return self.__html
        

    def get_js(self)->str:
        return self.__js.get(sep="\n")
    
    def get_css(self)->str:
        return self.__css.get(sep=" ")
    
    def get_html(self)->str:
        return self.__html.get(sep="\n")
    

import unittest

class TestConctactPage(unittest.TestCase):

    def setUp(self):
        self.contact_page = ConctactPage()

    def test_init(self):
        self.assertIsNotNone(self.contact_page._id)

    def test_add_tag(self):
        # TODO: implement test for add_tag method
        self.html_content = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <h1>Hello world</h1>
        </body>
        </html>"""
        self.contact_page.add_tag(self.html_content)

    def test_set_style(self):
        css = "body { background-color: #f2f2f2; }"
        self.contact_page.set_style(css)
        self.assertEqual(self.contact_page.get_css(), css)

    def test_add_script(self):
        js = "console.log('Hello World!');"
        self.contact_page.add_script(js)
        self.contact_page.add_script(js)
        self.assertEqual(self.contact_page.get_js(), js+'\n'+js)

    def test_make_project(self):
        # TODO: implement test for make_project method
        self.test_add_tag()
        self.test_add_script()
        self.test_get_css()
        new_html = self.contact_page.make_project()
        print( new_html.get())

    def test_get_js(self):
        js = "console.log('Hello World!');"
        self.contact_page.add_script(js)
        self.assertEqual(self.contact_page.get_js(), js)

    def test_get_css(self):
        css = "body { background-color: #f2f2f2; }"
        self.contact_page.set_style(css)
        self.assertEqual(self.contact_page.get_css(), css)

    def test_get_html(self):
        # TODO: implement test for get_html method
        pass

if __name__ == "__main__":
    unittest.main()

