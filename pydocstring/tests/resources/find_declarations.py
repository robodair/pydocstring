# normal method
def method_norm():
    pass

# method with params
def method_params(p1, p2):
    pass

# old-style class
class OldClass():
    pass

# new-style class
class NewClass(object):
    pass

    def __init__(self, c1, c2: int):
        pass

    # Method within a class - should ignore the self parameter
    def class_method(self):
        pass

# multi-line method
def method_multiline(param1,
            param2):
    pass

#def method_in_a_comment():
#    pass

"""
def method_in_a_string():
"""

# method with args and keyword args (FAILS!!!!)
def method_ag_kw_normal(p1, p2, ls=[1], st="string", tup=(1, 2), di={"key", "value"}):
    pass

# method with keyword args of all types (no spaces) and single quotes
def method_kw_normal(ls=[1], st='string', tup=(1, 2), di={'key', 'value'}):
    pass

# method with keyword args of all types (with spaces)
def method_kw_space(ls = [ 1 ], st = "string", tup = (1, 2), di = {"key", "value"}):
    pass

# method with keyword args of all types (mixed spaces)
def method_kw_mixed_space(ls= [1 ], st ="string", tup= (1, 2), di ={"key", "value"}):
    pass

# method with type definitions
def method_type(p1: str, p2: list) -> dict:
    pass

# method with the *args **kwargs syntax
def method_expand(*args, **kwargs):
    pass

# method with no trailing newline
def no_trailing_newline():
    pass