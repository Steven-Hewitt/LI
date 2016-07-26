import re

NUMBER = 1
FUNCTION = 2

functions = {}

def register(name):
    def register_function(function):
        functions[name] = Function(name, function)
        return function
    return register_function

class Function:
    #onexecute: takes in {dictionary} of scoped Functions, followed by argstring.
    #Returns an array of return values, followed by the remainder of the argstring.
    def __init__(self, name, onexecute, **kwargs):
        self._name = name
        self.execute = onexecute
        for k, v in kwargs:
            setattr(self, k, v)
        
    def get_Name(self):
        return self._name
    
    def get_Type(self):
        return FUNCTION
  
class Number:
    def __init__(self, value):
        self._value = value
        
    def set_Value(self, value):
        self._value = value
    def get_Value(self):
        return self._value
    def execute(self, *args):
        return self.get_Value()
    def get_Type(self):
        return NUMBER
    def __str__(self):
        return str(self._value)

@register("1")
def one(*args):
    #print(args)
    return [[Number(1)], args[1:]]

@register("2")
def two(*args):
    #print(args)
    return [[Number(2)], args[1:]]

@register("3")
def three(*args):
    #print(args)
    return [[Number(3)], args[1:]]

@register("4")
def four(*args):
    #print(args)
    return [[Number(4)], args[1:]]

@register("5")
def five(*args):
    #print(args)
    return [[Number(5)], args[1:]]

@register("6")
def six(*args):
    #print(args)
    return [[Number(6)], args[1:]]

@register("7")
def seven(*args):
    #print(args)
    return [[Number(7)], args[1:]]

@register("8")
def eight(*args):
    #print(args)
    return [[Number(8)], args[1:]]

@register("9")
def nine(*args):
    #print(args)
    return [[Number(9)], args[1:]]

@register("+")
def sum(dict, *args):
    
    #print("args:")
    #print(args)
    arg1, rest = args[0][0].execute(dict, args[0][1:])
    #print("rest (arg1):")
    #print(rest)
    string = rest[0]
    if len(arg1) <= 1:
        (arg2, rest) = string[0].execute(dict, string[1:])
    #print("rest (arg2):")
    #print(rest)
    string = rest[0]
    #print("arg1, arg2:")
    #print(arg1, arg2)
    arg1.append(arg2)
    sum = arg1[0]
    #print("sum, arg1[1:]")
    #print(sum, arg1[1:])
    for item in arg1[1:][0]:
        if sum.get_Type() & NUMBER:
            if item.get_Type() & NUMBER:  sum.set_Value(sum.get_Value() + item.get_Value())
            elif item.get_Type & LIST:    sum = cons(sum,item)
        elif sum.get_Type & LIST:
            sum.append(item)
    #print("Returned ",[[sum],string])
    return [[sum],rest]
functions["+"] = Function("+",sum)

'''TODO'''
def cons(first, next):
    pass
#def makePair(first, next):
#    if isinstance(next, list) or next is empty:
#        return list(first, next)
#    return pair(first, next)

#class pair:
#    def __init__(self, first = None, next = None):
#        self.first = first
#        self.next = next
 
'''TODO'''
class list:
    empty = 0
    
    def __init__(self, first = None, next = empty):
        pass
    def append(self, item):
        pass
    def __str__(self):
        return str(self._value)
#        self.first = first
#        self.next = next

'''TODO'''
#def length(list):
#    return 0 if list is empty else 1 + length(list.next)


def interpret(program, i):
    processed = preprocess(program)
    x = processed[0].execute(functions, processed[1:])
    for output in x[0]:
        print(output.get_Value())


def preprocess(program):
    processed = []
    for symbol in program:
        processed.append(functions[symbol])
    return processed
    
def evaluate(i):
    if re.compile(r"[1234567890]+(.[1234567890]+)?").match(i):
        return Number(i)
    return str(i)

print("it compiles!")
while True:
    interpret(input("Program:"), evaluate(input("input:")))
