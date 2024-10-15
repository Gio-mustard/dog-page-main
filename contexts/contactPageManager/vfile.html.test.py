if __name__ == "__main__":
    from vfile_html import HTML
    import unittest
    import colorama
    colorama.init()
    print(colorama.Fore.GREEN + "Aqui empiezan los test de HTML" + colorama.Style.RESET_ALL)
    
    class TestHTMLClass(unittest.TestCase):
        def setUp(self):
            self.html_content = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <h1>Hello world</h1>"""
            self.html = HTML(self.html_content,use_strict=True)
    
        def test_a(self):
            content = "</body>\n</html>"
            self.html.add(content)
            self.html_content+=('\n'+content)
            self.assertEqual(self.html.get(),self.html_content)
            
        def test_b(self):
            self.html.add("</body>\n</html>")
            self.html.insert(between='body',content="<p>hello</p>",on_end=True)    
            self.html_content+='\n'+"<p>hello</p>"+"\n</body>\n</html>"
            self.assertEqual(self.html.get(),self.html_content )
    
    class OrderedTests(unittest.TestSuite):
        def __init__(self):
            super().__init__()
            self.addTest(TestHTMLClass('test_a'))
            self.addTest(TestHTMLClass('test_b'))
           
    runner = unittest.TextTestRunner()
    runner.run(OrderedTests())
    
    