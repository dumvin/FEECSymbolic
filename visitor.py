import complex 
import form as Form
from graphviz import Digraph, Graph

#We define the different function that needs to be done by our Visitor on the nodes

#The most general Visitor class
class Visitor(object):
    """this class implement a tree visitor for our form"""
    def __init__(self):
        self.handler_dict = {Form.OperatorForm:(self.func_op_fo,{}),Form.TerminalForm:(lambda x: x,{})}

    #Operator form 
    def func_op_fo(self, form, children=None):
        """function when an operator form is found"""
        if children:    
            return form.reconstruct(children)
        else:
            return form

    def _visit_preorder(self, form):
        """the intern preorder method for visiting the tree"""
        new_form = self.find_method(form)(form)
        new_children = map(self._visit_preorder, form.forms)
        return new_form.reconstruct(new_children)


    def visit_preorder(self, form):
        """the preorder method for visiting the tree"""
        return(self._visit_preorder(form))

    def _visit_postorder(self, form):
        """the intern postorder method for visiting the tree"""
        new_children = map(self._visit_postorder, form.forms)
        new_form = self.find_method(form)(form)
        return new_form.reconstruct(new_children)

            
    def visit_postorder(self, form):
        """the postorder method for visiting the tree"""
        return(self._visit_postorder(form))
        
    def find_method(self, form, H=None, D=None):
        """This method enables to choose the method that we want
        to apply to a specific node"""
        if D is None:
            D = self.handler_dict
           
        for typ, val in D.items():
             
            if isinstance(form, typ):
                
                return (self.find_method(form, *val)) #or H
        return(H)

#The Visitor class to get all the bottom children in a tree
class VisitorChildren(Visitor):
    """The Visitor class to get all the bottom children in a tree"""
    def __init__(self):
        self.handler_dict = {Form.OperatorForm:(self.func_op_fo,{}),Form.TerminalForm:(func_term_form,{})}
        self.list = []

    def func_term_form(self, form):
        self.list.append(form)
        return form
    
    def func_op_fo(self, form):
        """function when an operator form is found"""
        if children:    
            return form.reconstruct(children)
        else:
            return form

    def visit_preorder(self, form):
        """the preorder method for visiting the tree"""
        visit = (self._visit_preorder(form))
        return visit.list
            
    def visit_postorder(self, form):
        """the postorder method for visiting the tree"""
        visit = (self._visit_postorder(form))
        return visit.list

#The class that draw a graph of our form, and store pre and post visits in a 
#table
class VisitorGraph(Visitor):
    """this class implement a tree visitor for our form"""
    def __init__(self):
        self.handler_dict = {Form.OperatorForm:(self.func_op_fo,{Form.D: (self.diff, {})\
							, Form.Wedge: (self.wed, {}), Form.Add: (self.add,{}), \
							Form.Hodge: (self.hod, {}),Form.Pullback: (self.pull, {}) }),\
							Form.TerminalForm:(self.func_term_fo,{})}
        self.dot = Graph(comment='Tree of our form')#Digraph(comment='Tree of our form') #to store the dot for vizgraph
        self.edges = [] #to store the edge for the graph
        self.post = [] #to store the post order traversal
        self.pre = [] # to store the pre order traversal
        self.comp = 0 #to differentiate the edge

    #D form
    def diff(self, form, children=None):
        """function when a diff operation is made"""
        if form.scalar == 1:
            return( 'd')
        elif form.scalar == -1:
            return( "-d" )
        else:
            return( "{}d ".format(form.scalar)  )
    
    #Wedge
    def wed(self, form, children=None):
        """function when a wedge operation is made"""
        if form.scalar == 1:
            return( '^')
        elif form.scalar == -1:
            return( "-^" )
        else:
            return( "{}^ ".format(form.scalar)  )
                    
    #Add
    def add(self, form, children=None):
        """function when a add operation is made"""
        if form.scalar == 1:
            return( '+')
        elif form.scalar == -1:
            return( "-+" )
        else:
            return( "{}+ ".format(form.scalar)  )
                    
    #Hodge
    def hod(self, form, children=None):
        """function when a hodge star operation is made"""
        if form.scalar == 1:
            return( '*')
        elif form.scalar == -1:
            return( "-*" )
        else:
            return( "{}* ".format(form.scalar)  )
    
    #Pullback
    def pull(self, form, children=None):
        """function when a hodge star operation is made"""
        if form.scalar == 1:
            return("phi")

        else:
            return( "{}phi ".format(form.scalar)  )

    #TerminalForm
    def func_term_fo(self, form):
        """function that print a terminal Form"""
        if form.scalar == 1:
            return( form.name)
        elif form.scalar == -1:
            return( "-{} ".format(form.name)  )
        else:
            return( "{}{} ".format(form.scalar, form.name)  )


    def _visit_preorder(self, form):
        """the intern preorder method for visiting the tree"""
        if not isinstance(form,Form.TerminalForm):
            children=form.forms
            inter = self.find_method(form)(form)
            self.pre.append(inter)
            for fo in children:
                self._visit_preorder(fo)
            #in post order the find_method will be there
        else:
            inter = self.find_method(form)(form)
            self.pre.append(inter)

    def visit_preorder(self, form):
        """the preorder method for visiting the tree"""
        self.pre=[]
        self._visit_preorder(form)
        return self.pre

    def _visit_postorder(self, form):
        """the intern postorder method for visiting the tree"""
        if not isinstance(form,Form.TerminalForm):
            children=form.forms
            for fo in children:
                self._visit_postorder(fo)
            inter = self.find_method(form)(form)
            self.post.append(inter)
        else:
            inter = self.find_method(form)(form)
            self.post.append(inter)
            
    def visit_postorder(self, form):
        """the postorder method for visiting the tree"""
        self.post=[]
        self._visit_postorder(form)
        return self.post

    def _create_graph(self, form, parent_name=""):
        """the method for creating a graph of the tree, the edges are store inside the edges attribute"""
        if not isinstance(form,Form.TerminalForm):
            children = form.forms
            node = (self.find_method(form)(form))
            nbr1 = str(self.comp)
            self.comp+=1
            name = nbr1
            self.dot.node(name, node)
            
            if parent_name is not "":
                inter=parent_name+name                
                self.edges.append(inter)
                self.dot.edge(parent_name, name)

            parent_name=name
            for fo in children:
                self._create_graph(fo,parent_name)
            
        else:
            node = (self.find_method(form)(form))
            nbr1 = str(self.comp)
            self.comp+=1
            name = nbr1
            #~ print(name)
            self.dot.node(name,node)
            if parent_name is not "":
                inter = parent_name+name                
                self.edges.append(inter)
                self.dot.edge(parent_name, name)
 
    def draw_graph(self, form, name='sample'):
        """the method for drawing a graph of the tree, name is the file
		name under which we want to save it"""
        self.dot = Graph(comment='Tree of our form')#Digraph(comment='Tree of our form')
        self.edges = []
        self.comp = 0
        self._create_graph(form)
        namefile='drawing/'+name+'.gv'
        self.dot.render(namefile, view=True)

#The class to push the pullback to the bottom
class VisitorPullback(Visitor):
    """ visitor to pass the pullback up to the bottom of our tree"""
    def __init__(self):
        self.handler_dict = {Form.OperatorForm: (self.func_op_fo ,{Form.D: (self.diff , {})\
							, Form.Add: (self.add, {}), Form.Wedge: (self.wed , {}), Form.Pullback: (self.pull ,{}) }), \
							Form.TerminalForm: (self.func_term_fo ,{})}
        self.pullback = False;
    
    #D form
    def diff(self, form, children=None):
        """function when a diff operation is made"""
        if self.pullback:
            return form.scalar*(self._visit_preorder(form.forms[0].pullback())).d()
        else:
            return form

    #Wedge
    def wed(self, form, children=None):
        """function when a wedge operation is made"""
        if self.pullback:
            a=(self._visit_preorder(form.forms[0].pullback()))
            b=(self._visit_preorder(form.forms[1].pullback()))
            return form.scalar * a.wedge(b)
        else:
            return form

    #Add
    def add(self, form, children=None):
        """function when a add operation is made"""
        if self.pullback:
            a=(self._visit_preorder(form.forms[0].pullback()))
            b=(self._visit_preorder(form.forms[1].pullback()))
            return form.scalar * (a+b)
        else:
            return form
            
    #TerminalForm
    def func_term_fo(self, form):
        """function that print a terminal Form"""
        if self.pullback:
            return form.pullback()
        else:
            return form
    #Operator form 
    def func_op_fo(self, form, children=None):
        """function when an operator form is found"""    
        if self.pullback:
            self.pullback=False
            formb = form.scalar * (self._visit_preorder(form).pullback())
            return formb
        else:
            return form
            
    #Pullback
    def pull(self, form, children=None):
        """function when a hodge star operation is made"""
        self.pullback = True
        formb = map(self._visit_preorder, form.forms)
        self.pullback = False
        return formb[0]
        
    def _visit_preorder(self, form):
        """the intern preorder method for visiting the tree"""
        new_form = self.find_method(form)(form)
        if not isinstance(form, Form.TerminalForm):
            new_children = map(self._visit_preorder, new_form.forms)
        else:
            new_children = new_form.forms
            if self.pullback:
                new_children = [form]
        return new_form.reconstruct(new_children)
        
    def draw_graph(self , form, name='sample'):
        """function that draw the graph"""
        formb = self.visit_preorder(form)
        VG = VisitorGraph()
        VG.draw_graph(formb, name)

class VisitorSimplification(Visitor):
    """ visitor to tansform the pullback of Terminalforms into pullbacked forms
    the ' sign shows it"""
    def __init__(self):
        self.handler_dict = {Form.OperatorForm: (self.func_op_fo ,{Form.Pullback: (self.pull ,{})}), Form.TerminalForm: (self.func_term_fo ,{})}
            
    #Operator form

    def func_op_fo (self, form, children=None):
        """function when an operator form is found"""    
        return form
        
    #TerminalForm
    def func_term_fo(self, form):
        """function that print a terminal Form"""
        return form
            
    #Pullback
    def pull(self, form, children=None):
        """function when a pullback operation is made"""
        if isinstance(form.forms[0], Form.TerminalForm):
            na = form.forms[0].name+"'"
            new = Form.TerminalForm(form.forms[0].complex, form.forms[0].rank, na, form.forms[0].scalar)
            return new
        else:
            return form
        
    def draw_graph(self , form, name='sample'):
        """function that draw the graph"""
        formb = self.visit_preorder(form)
        VG = VisitorGraph()
        VG.draw_graph(formb, name)

#~ #The class to push the pullback to the bottom
#~ class VisitorCleanHodgeStar(Visitor):
    #~ """ visitor to tansform the form under a hodge star when they are not for """
    #~ def __init__(self):
        #~ self.handler_dict = {Form.OperatorForm: (self.func_op_fo ,{Form.Pullback: (self.pull ,{})}), Form.TerminalForm: (self.func_term_fo ,{})}
            #~ 
    #~ #Operator form
#~ 
    #~ def func_op_fo (self, form, children=None):
        #~ """function when an operator form is found"""    
        #~ return form
        #~ 
    #~ #TerminalForm
    #~ def func_term_fo(self, form):
        #~ """function that print a terminal Form"""
        #~ return form
            #~ 
    #~ #Pullback
    #~ def pull(self, form, children=None):
        #~ """function when a pullback operation is made"""
        #~ if isinstance(form.forms[0], Form.Hodge):
            #~ child = form.forms[0].forms[0]
            #~ if isinstance(child, Form.TerminalForm):
                #~ new = form
            #~ else:    
                #~ new = form.forms[0].transform()
            #~ return new
        #~ else:
            #~ return form
        #~ 
    #~ def draw_graph(self , form, name='sample'):
        #~ """function that draw the graph"""
        #~ formb = self.visit_preorder(form)
        #~ VG = VisitorGraph()
        #~ VG.draw_graph(formb, name)
        #~ 
class VisitorExpansion(Visitor):
    """ visitor to replace the terminalForm in their basis decomposition"""
    def __init__(self):
        self.handler_dict = {Form.OperatorForm: (self.func_op_fo ,{}), Form.TerminalForm: (self.func_term_fo ,{})}
        self.decompose = False    
    #Operator form

    def func_op_fo (self, form, children=None):
        """function when an operator form is found"""
        return form
        
    #TerminalForm
    def func_term_fo(self, form):
        """function that print a terminal Form"""
        #~ if not (form.decompose().rank == 0):
            #~ return form.decompose() #(self._visit_preorder(form.decompose()))
        #~ else:
            #~ return form
        return form.decompose()
        
    def _visit_preorder(self, form):
        """the intern preorder method for visiting the tree"""
        new_form = self.find_method(form)(form)
        new_children = map(self._visit_preorder, new_form.forms)
        return new_form.reconstruct(new_children)
    
    def draw_graph(self , form, name='sample'):
        """function that draw the graph"""
        formb = self.visit_preorder(form)
        VG = VisitorGraph()
        VG.draw_graph(formb, name)
        
class VisitorHodgeDistribution(Visitor):
    """ visitor to distribute the Hodge star on the addition"""
    """and maybe in a futher on the wedge product and the diff one"""
    def __init__(self):
        self.handler_dict = {Form.OperatorForm: (self.func_op_fo ,{Form.Hodge : (self.hodge, {}), Form.D : (self.d, {})}), Form.TerminalForm: (self.func_term_fo ,{})}
        self.decompose = False    
        
    #Operator form
    def func_op_fo (self, form, children=None):
        """function when an operator form is found"""
        return form
        
    #TerminalForm
    def func_term_fo(self, form):
        """function that print a terminal Form"""
        return form
    
    def d(self, form):
        """ we applied the leibniz rule each time we hit a diff of a wedge form"""
        return form.leibniz()

    #Hodge Star
    def hodge(self, form):
        new = form
        new.scalar = form.scalar
        if isinstance(form.forms[0], Form.Add):
            child = form.forms[0].forms
            print "child", child
            new = form.forms[0].scalar * form.scalar * (self._visit_preorder( child[0].hodge()) + self._visit_preorder(child[1].hodge()))
            print "new",new
        elif isinstance(form.forms[0], Form.Hodge):
            k = form.forms[0].forms[0].rank 
            N = form.complex.dimension 
            new = form.scalar * form.forms[0].scalar * (-1)** (k*( N-k))*form.forms[0].forms[0]
            new = self._visit_preorder(new)
        else:
            children = map(self._visit_preorder, form.forms)
            new.reconstruct(children)
        return new

    def _visit_preorder(self, form):
        """the intern preorder method for visiting the tree"""
        print form
        new_form = self.find_method(form)(form)
        print "new form", new_form
        if not isinstance(form, Form.TerminalForm):
            new_children = map(self._visit_preorder, new_form.forms)
        else:
            new_children = form.forms
        return new_form.reconstruct(new_children)
        
    def draw_graph(self, form, name='sample'):
        """function that draw the graph"""
        formb = self.visit_preorder(form)
        VG = VisitorGraph()
        VG.draw_graph(formb, name)

class VisitorHodgeEvaluation(Visitor):
    """ visitor to transofrm the hodge star of a basis into basis functions"""
    """"""
    def __init__(self):
        self.handler_dict = {Form.OperatorForm: (self.func_op_fo ,{Form.Hodge : (self.hodge, {})}), Form.TerminalForm: (self.func_term_fo ,{})}
        self.decompose = False    
        
    #Operator form
    def func_op_fo (self, form, children=None):
        """function when an operator form is found"""    
        return form
        
    #TerminalForm
    def func_term_fo(self, form):
        """function that print a terminal Form"""
        return form
        
    #Hodge Star
    def hodge(self, form):
        new = form
        if isinstance(form.forms[0], Form.Add):
            child = form.forms[0].forms
            new = child[0].hodge() + child[1].hodge()
        return new

    def _visit_preorder(self, form):
        """the intern preorder method for visiting the tree"""
        new_form = self.find_method(form)(form)
        if not isinstance(form, Form.TerminalForm):
            new_children = map(self._visit_preorder, new_form.forms)
        else:
            new_children = new_form.forms
        return new_form.reconstruct(new_children)
        
    def draw_graph(self, form, name='sample'):
        """function that draw the graph"""
        formb = self.visit_preorder(form)
        VG = VisitorGraph()
        VG.draw_graph(formb, name)
