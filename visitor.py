from complex import *
from form import *
#We define the different function that needs to be done by our Visitor on the nodes
def func_term_fo(form):
    """function that print a terminal Form"""
    if form.scalar == 1:
        return form.name
    return "{}{} ".format(form.scalar,form.name)  

dic_term_fo = {}    

#Opertaor form

def func_op_fo(form):
    """function when an operator form is found"""
    #return "Operator form"
    print("Operator form")

#D form

def diff(form):
    """function when a diff operation is made"""
    #return "d "
    print("d ")
    
#Wedge

def wed(form):
    """function when a wed operation is made"""
    #return "^ "
    print("^ ")
    
#Add
    
def add(form):
    """function when a wed operation is made"""
    #return "+ "
    print("+ ")
    
#Hodge

def hod(form):
    """function when a wed operation is made"""
    #return "* "
    print("* ")
    
dic_op_fo = {D: (diff, {}), Wedge: (wed, {}), Add: (add,{}), Hodge: (hod, {}) }

class Visitor(object):
    """this class implement a tree visitor for our form"""
    def __init__(self):
        self.handler_dict = {OperatorForm:(func_op_fo,dic_op_fo),TerminalForm:(func_term_fo,dic_term_fo)}

    def visit(self, form):
        """for the moment we will do a preorder """
        if not isinstance(form,TerminalForm):
            children=form.forms
            self.find_method(form)(form)
            for fo in children:
                self.visit(fo)
            #in post order the find_method will be there
        self.find_method(form)(form)
        
    def find_method(self, form, H=None, D=None):
        """This method enables to choose the method that we wamt to apply to a specific node"""
        if D is None:
            D = self.handler_dict
        for typ, val in D.items():
            #m = __import__("form")
            #m = getattr( m, typ)
            #I do not know if there is a nicer way to what i just did
            if isinstance(form, typ):
                print(typ)
                return self.find_method(form, val) or H
            return(H)
