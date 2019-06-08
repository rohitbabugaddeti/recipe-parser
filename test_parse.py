import recipe_parser
import pprint
import os
from pathlib import Path

class test_parse():
    def test_with_prase_obj(self):
        dirname = os.path.dirname(__file__)
        arg = Path(dirname + '/bevvy-irish-coffee.html')
        pprint.pprint(recipe_parser.parse(arg))
        print('---------------------------------------')
    def test_with_file_obj(self):
        dirname = os.path.dirname(__file__)
        arg = Path(dirname + '/bevvy-irish-coffee.html')
        f = open(arg, 'rt')
        pprint.pprint(recipe_parser.parse(f))
        f.close()
        print('----------------------------------------')
    def test_with_filePath(self):
        pprint.pprint(recipe_parser.parse('D:/GitHub/recipe-parser/bevvy-irish-coffee.html'))
        print('----------------------------------------')


test_parse().test_with_file_obj()
