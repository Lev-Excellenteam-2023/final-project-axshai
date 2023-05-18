# from lecture_parser import PresentationParser
#
# p = PresentationParser(r"C:\Users\User\Downloads\asyncio-intro.pptx")
# for part in p.get_lecture_parts():
#     x = p.parse_lecture_part(part)
#     print(x)

class Person:
    def __new__(cls, *args, **kwargs):
        print("new")
        obj = object.__new__(cls)
        return obj
    def __init__(self):
        print("init")

p = Person()
p1 = Person()