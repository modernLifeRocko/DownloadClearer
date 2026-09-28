import unittest
import clearer
import os


class TestClearer(unittest.TestCase):
    def setUp(self):
        # create files with extensions in every class
        proot = os.getcwd()
        open('tests/Downloads/img.jpg', 'w').close()
        open('tests/Downloads/book.epub', 'w').close()
        open('tests/Downloads/vid.mov', 'w').close()
        open('tests/Downloads/mus.mp3', 'w').close()
        open('tests/Downloads/bin.deb', 'w').close()
        clearer.main(test=True)
        os.chdir(proot)

    def testebook(self):
        self.assertTrue(os.path.exists('tests/Library/book.epub'))
        self.assertFalse(os.path.exists('tests/Downloads/book.epub'))

    def testimg(self):
        self.assertTrue(os.path.exists('tests/Pictures/img.jpg'))
        self.assertFalse(os.path.exists('tests/Downloads/img.jpg'))

    def testvid(self):
        self.assertTrue(os.path.exists('tests/Movies/vid.mov'))
        self.assertFalse(os.path.exists('tests/Downloads/img.jpg'))

    def testmusic(self):
        self.assertTrue(os.path.exists('tests/Music/mus.mp3'))
        self.assertFalse(os.path.exists('tests/Downloads/mus.mp3'))

    def testInstallers(self):
        self.assertFalse(os.path.exists('tests/Downloads/bin.deb'))
        self.assertFalse(os.path.exists('tests/Documents/bin.deb'))
        self.assertFalse(os.path.exists('tests/Library/bin.deb'))
        self.assertFalse(os.path.exists('tests/Music/bin.deb'))
        self.assertFalse(os.path.exists('tests/Pictures/bin.deb'))
        self.assertFalse(os.path.exists('tests/Movies/bin.deb'))

    def tearDown(self):
        # clear all test directories
        os.system('find tests -mindepth 2 -delete')


if __name__ == '__main__':
    unittest.main()
