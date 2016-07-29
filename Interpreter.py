import re
from numbers import Number as allnumbertypes
from time import sleep
NUMBER = 1
FUNCTION = 2
PAIR = 4
LIST = 8

REQUIRED = 1
OPTIONAL = 2

functions = {}

def register(name, arity = 0):
    def register_function(function):
        functions[name] = Function(name, function, arity)
        return function
    return register_function

class Argument:
    def __init__(self, value, flags = REQUIRED):
        self._argval = value
        self._argflags = flags
    
    def __getattr__(self, name):
        return getattr(self._argval,name)
    
    def get_Flags(self): return self._argflags
    
class Function:
    #onexecute: takes in {dictionary} of scoped Functions, followed by argstring.
    #Returns an array of return values, followed by the remainder of the argstring.
    def __init__(self, name, onexecute, arity, **kwargs):
        self._name = name
        self.execute = onexecute
        self._arity = arity
        for k, v in kwargs:
            setattr(self, k, v)
    
    def coalesce_arity(self, dict, argstring, *args, defaultval="i"):
        #print("coalescing arity for", self._name)
        if isinstance(self._arity, allnumbertypes):
            arity = self._arity
            numargs = 0
            #print(argstring)
            while numargs < self._arity and len(argstring) > 0:
                arg1, rest = argstring[0].coalesce_arity(dict, argstring[1:], *args)
                #print(self._name, self._arity, numargs, arg1, rest)
                argstring = rest
                arity = arity + arg1
                numargs=numargs+1
            #print(self._name, "_arity", self._arity, "numargs", numargs, arity, argstring)
                
            while numargs < self._arity:
                #print(self._name, numargs, "<", self._arity, "def", defaultval)
                arity = arity + dict.get(defaultval).coalesce_arity(dict,[])[0]
                numargs = numargs + 1
            #sleep(10)
            return [arity, argstring]
        print("arityisnotnumber")
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
    def truthy(self):
        return not self._value == 0
    def get_Type(self):
        return NUMBER
    def __str__(self):
        return str(self._value)

class Boolean:
    def __init__(self, value):
        self._value = value
        
    def set_Value(self, value):
        self._value = value
    def get_Value(self):
        return 1 if self._value else 0
    def execute(self, *args):
        return self.get_Value()
    def truthy(self):
        return self._value
    def get_Type(self):
        return NUMBER
    def __str__(self):
        return str(self._value)

'''TODO'''
def cons(first, next):
    if next is empty or next.get_Type() & PAIR:
        return List(first, next)
    return pair(first, next)
#def makePair(first, next):
#    if isinstance(next, list) or next is empty:
#        return list(first, next)
#    return pair(first, next)

class pair:
    def __init__(self, car = None, cdr = None):
        self._car = first
        self._cdr = next    
    def __str__(self):
        return "("+str(self._car)+" . "+str(self._cdr)+")"
    def car(self):
        return self._car
    def cdr(self):
        return self._cdr

empty = 0
'''TODO'''
class List:
    
    def __init__(self, first = None, next = empty):
        self._first = first
        self._next = next
    def append(self, item):
        pass
    def car(self):
        return self._first
    def cdr(self):
        return self._next
    def truthy(self):
        return True
    def __str__(self):
        return "("+str(self._first) +  " " + self._next._str() + ")"
    def _str(self):
        try: next = self._next._str() 
        except: next = ""
        return str(self._first) + next
    def get_Type(self):
        return LIST + PAIR
#        self.first = first
#        self.next = next

'''TODO'''
def length(list):
    try:
        return 1 + length(list.cdr())
    except:
        return 0

def truthy(value):
    if value is empty: return False
    return value.truthy()

'''Default expansion parameter i'''
def retrieveParams(minargs, dict, *args, defaultval="i", getuntil=False):
    arg = []
    rest = args
    string = rest[0]
    while len(arg) < minargs and len(string) > 0:
        #print(rest)
        
        arg1, rest = string[0].execute(dict, string[1:], *args[1:])
        string = rest[0]
        arg = arg + arg1
    while len(arg) < minargs:
        arg = arg + dict.get(defaultval).execute(dict)[0]
    return [arg,rest]
    #print("arg1, arg2:")
    #print(arg1, arg2)

@register("y",1)    
def decrement(dict, *args):
    arg = retrieveParams(1, dict, *args)
    return [[Argument(Number(arg[0][0].get_Value()-1))],arg[1]]    

@register("?",3)
def ifelse(dict, *args):
    arg1, rest = retrieveParams(1, dict, *args)
    
    if truthy(arg1[0]):
        #print("truthy", arg1[0])
        if len(arg1)>1:  return ([arg1[1]]+arg1[3:], rest) 
        else:
            #print("rest", rest)
            arg, rest = retrieveParams(1,dict, *rest)
            #print("rest after retrieve", rest)
            return (arg, (rest[0][0] if len(rest[0])>0 else dict.get("i")).coalesce_arity(dict, rest[0][1:], *rest[1:])[1:])
    if len(arg1) > 2: return (arg1[2:], rest) 
    else:
        
        #print("functions",[y.get_Name() for y in rest[0]])
        #print("rest of rest", rest[1:])
        past = rest[0][0].coalesce_arity(dict, rest[0], *rest[1:])[1]
        #print("coalesced_arity", past)
        x = retrieveParams(1,dict,past[1:])
        #print([y.get_Value() for y in x[0]],x)
        return x

@register("0")
def zero(*args):
    #print(args)
    return [[Argument(Number(0))], args[1:]]

@register("1")
def one(*args):
    #print(args)
    return [[Argument(Number(1))], args[1:]]

@register("2")
def two(*args):
    #print(args)
    return [[Argument(Number(2))], args[1:]]

@register("3")
def three(*args):
    #print(args)
    return [[Argument(Number(3))], args[1:]]

@register("4")
def four(*args):
    #print(args)
    return [[Argument(Number(4))], args[1:]]

@register("5")
def five(*args):
    #print(args)
    return [[Argument(Number(5))], args[1:]]

@register("6")
def six(*args):
    #print(args)
    return [[Argument(Number(6))], args[1:]]

@register("7")
def seven(*args):
    #print(args)
    return [[Argument(Number(7))], args[1:]]

@register("8")
def eight(*args):
    #print(args)
    return [[Argument(Number(8))], args[1:]]

@register("9")
def nine(*args):
    #print(args)
    return [[Argument(Number(9))], args[1:]]

@register("_", 1)
def negate(dict, *args):
    arg1, rest = retrieveParams(1, dict, *args)
    return [[Argument(Boolean(not truthy(arg1[0])))]+arg1[1:], rest]
                      
@register("+", 2)
def sum(dict, *args):
    
    arg1, rest = retrieveParams(2, dict, *args)
    sum = arg1[0]
    #print("sum, arg1[1:]")
    #print(sum, arg1[1:])
    if sum.get_Type() & NUMBER:
        if arg1[1].get_Type() & NUMBER:  sum.set_Value(sum.get_Value() + arg1[1].get_Value())
        elif arg1[1].get_Type & LIST:    sum = cons(sum,arg1[1])
    elif sum.get_Type() & LIST:
        sum.append(arg1[1])
    last_used = len(arg1)
    for index, item in enumerate(arg1[2:]):
        if item.get_Flags() & OPTIONAL: 
            last_used = index + 2
            break
        if sum.get_Type() & NUMBER:
            if item.get_Type() & NUMBER:  sum.set_Value(sum.get_Value() + item.get_Value())
            elif item.get_Type & LIST:    sum = cons(sum,item)
        elif sum.get_Type() & LIST:
            sum.append(item)
    #print("Returned ",[[sum],string])
    return [[sum]+arg1[last_used:],rest]

@register("M", 2)
def product(dict, *args):
    #print(args)
    arg1, rest = retrieveParams(2, dict, *args)

    if arg1[0].get_Type() & NUMBER:
        product = Number(arg1[0].get_Value()*arg1[1].get_Value())
        last_used = len(arg1)
        for index, item in enumerate(arg1[2:]):
            if item.get_Flags() & OPTIONAL: 
                last_used = index + 2
                break
            product.set_Value(product.get_Value() * item.get_Value())
    else: product = [] # TODO cartesian product
    return [[product]+arg1[last_used:], rest]

@register("-", 2)
def difference(dict, *args):
    
    arg1, rest = retrieveParams(2, dict, *args)
    diff = arg1[0]
    #print("sum, arg1[1:]")
    #print(sum, arg1[1:])
    if diff.get_Type() & NUMBER: diff.set_Value(diff.get_Value() - arg1[1].get_Value())
    elif diff.get_Type() & LIST: pass
        #for arg in arg1[1]:
            
    last_used = len(arg1)
    for index, item in enumerate(arg1[2:]):
        if item.get_Flags() & OPTIONAL: 
            last_used = index + 2
            break
        if diff.get_Type() & NUMBER: diff.set_Value(diff.get_Value() - item.get_Value())
        elif diff.get_Type() & LIST: pass
    
    return [[diff]+arg1[last_used:],rest]

@register("/", 2)
def difference(dict, *args):
    arg1, rest = retrieveParams(2, dict, *args)
    div = arg1[0]
    #print("sum, arg1[1:]")
    #print(sum, arg1[1:])
    if div.get_Type() & NUMBER: div.set_Value(div.get_Value() / arg1[1].get_Value())
    elif div.get_Type() & LIST: pass
        #for arg in arg1[1]:
            
    last_used = len(arg1)
    for index, item in enumerate(arg1[2:]):
        if item.get_Flags() & OPTIONAL: 
            last_used = index + 2
            break
        if div.get_Type() & NUMBER: div.set_Value(div.get_Value() / item.get_Value())
        elif div.get_Type() & LIST: pass
    
    return [[div]+arg1[last_used:],rest]

'''TODO'''
@register("c")
def difference(dict, *args):
    pass

def interpret(program, i):
    scope = functions.copy()
    def Input(*args):
        return [[i],args[1:]]
    def Recurse(dict, *args):
        arg = retrieveParams(1, dict, *args)
        return [interpret(program, arg[0][0]),arg[1]]
    scope['i'] = Function('i',Input, 0)
    scope['R'] = Function('R',Recurse,1)
    processed = preprocess(scope,program)
    x, rest = processed[0].execute(scope, processed[1:])
    #print(x, rest)
    while len(rest[0]) > 0:
        y, rest = rest[0][0].execute(scope,rest[0][1:], *rest[1:])
        x = x + y
    return x

def run():
    program, i = (input("Program:\n"), evaluate(input("input:\n")))
    x = interpret(program, i)
    for output in x:
        print(output.get_Value())


def preprocess(scope, program):
    processed = []
    for symbol in program:
        try: processed.append(scope.get(symbol))
        except: processed.append(symbol)
    if len(processed) == 0: processed.append(scope.get("i"))
    return processed
    
def evaluate(i):
    if re.compile(r"[1234567890]+(.[1234567890]+)?").match(i):
        try:
            return Number(int(i))
        except ValueError:
            return Number(float(i))
    '''TODO: Check for listiness'''
    return str(i)

#print("it compiles!")
while True:
    run()
