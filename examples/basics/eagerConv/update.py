#parsed

from pymoult.highlevel.updates import EagerConversionUpdate
import sys

main = sys.modules["__main__"]

class ItemV2(object):
    def __init__(self,name,color,commentary):
        self.name =name
        self.color = color
        self.commentary = commentary

    def display(self):
        print("An item named "+self.name+" of color "+self.color)
        print("Its labels says : "+self.commentary)
    
    def change(self,color):
        self.color = color

    def comment(self,commentary):
        self.commentary = commentary


def transformer(obj):
    mapping = {"apple":"tasty","banana":"always bring one to parties","mango":"it's a mango!"}
    if obj.name in mapping.keys():
        obj.commentary = mapping[obj.name]


update = EagerConversionUpdate(main.Item,ItemV2,transformer)
main.manager.add_update(update)


