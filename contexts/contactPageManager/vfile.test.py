if __name__ == "__main__":
    import unittest
    from vfile import VirtualFile
    import colorama
    colorama.init()
    print(colorama.Fore.GREEN + "Aqui empiezan los test de VirtualFile" + colorama.Style.RESET_ALL)
    class TestVirtualFile(unittest.TestCase):

        def test_init(self):
            vf = VirtualFile()
            self.assertEqual(vf.num_of_lines(), 0)

        def test_init_with_line(self):
            vf = VirtualFile("Hello World")
            self.assertEqual(vf.num_of_lines(), 1)
            self.assertEqual(vf.get(), "Hello World")

        def test_add(self):
            vf = VirtualFile()
            vf.add("Hello World")
            self.assertEqual(vf.num_of_lines(), 1)
            self.assertEqual(vf.get(), "Hello World")

        def test_add_with_index(self):
            vf = VirtualFile()
            vf.add("Hello World", 0)
            self.assertEqual(vf.num_of_lines(), 1)
            self.assertEqual(vf.get(), "Hello World")

        def test_remove(self):
            vf = VirtualFile("Hello World")
            vf.remove("Hello World")
            self.assertEqual(vf.num_of_lines(), 0)

        def test_remove_with_index(self):
            vf = VirtualFile("Hello World")
            vf.remove(index=0)
            self.assertEqual(vf.num_of_lines(), 0)

        def test_clear(self):
            vf = VirtualFile("Hello World")
            vf.clear()
            self.assertEqual(vf.num_of_lines(), 0)

        def test_get_without_strict(self):
            # default
            vf = VirtualFile("Hello\nWorld",use_strict=False)
            self.assertEqual(vf.get(), "Hello World")

        def test_get_strict(self):
            vf = VirtualFile("Hello\nWorld", use_strict=True)
            self.assertEqual(vf.get(), "Hello\nWorld")

        def test_get_with_sep(self):
            vf = VirtualFile("Hello\nWorld")
            self.assertEqual(vf.get(sep=" "), "Hello World")

        def test_get_for_each_line(self):
            vf = VirtualFile("Hello\nWorld")
            self.assertEqual(vf.get(sep="for-each-line"), ["Hello World"])

        def test_get_for_each_line_with_strict(self):
            vf = VirtualFile("Hello\nWorld", use_strict=True)
            self.assertEqual(vf.get(sep="for-each-line"), ["Hello", "World"])

        def test_num_of_lines(self):
            vf = VirtualFile("Hello\nWorld",use_strict=True)
            self.assertEqual(vf.num_of_lines(), 2)
    unittest.main()