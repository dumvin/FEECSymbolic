import complex 
import form as Form
#We define the different function that needs to be done by our Visitor on the nodes
def func_term_fo(form):
    """function that print a terminal Form"""
    if form.scalar == 1:
        print( form.name)
    else:
        print( "{}{} ".format(form.scalar,form.name)  )

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
    
dic_op_fo = {Form.D: (diff, {}), Form.Wedge: (wed, {}), Form.Add: (add,{}), Form.Hodge: (hod, {}) }

class Visitor(object):
    """this class implement a tree visitor for our form"""
    def __init__(self):
        self.handler_dict = {Form.OperatorForm:(func_op_fo,dic_op_fo),Form.TerminalForm:(func_term_fo,dic_term_fo)}

    def visit_preorder(self, form):
        """the preorder method for visiting the tree"""
        if not isinstance(form,Form.TerminalForm):
            children=form.forms
            self.find_method(form)(form)
            for fo in children:
                self.visit_preorder(fo)
            #in post order the find_method will be there
        else:
            self.find_method(form)(form)
    
    def visit_postorder(self, form):
        """the postorder method for visiting the tree"""
        if not isinstance(form,Form.TerminalForm):
            children=form.forms
            for fo in children:
                self.visit_postorder(fo)
            self.find_method(form)(form)
        else:
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
                
                return (self.find_method(form, *val)) #or H
        return(H)
