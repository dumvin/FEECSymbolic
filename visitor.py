import complex 
import form as Form
from graphviz import Digraph, Graph

#We define the different function that needs to be done by our Visitor on the nodes
#Opertaor form 

def func_op_fo(form, children=None):
    """function when an operator form is found"""
    if children:    
        return form.reconstruct(children)
    else:
        return form
    return ['Operator form','Operator form']
    #print("Operator form")

#The most general Visitor class
class Visitor(object):
    """this class implement a tree visitor for our form"""
    def __init__(self):
        self.handler_dict = {Form.OperatorForm:(func_op_fo,{}),Form.TerminalForm:(lambda x: x,{})}

    def _visit_preorder(self, form):
        """the intern preorder method for visiting the tree"""
        new_form = self.find_method(form)(form)
        if not isinstance(new_form,Form.TerminalForm):
            children = new_form.forms
            new_children = []
            for fo in children:
                new_children.append(self._visit_preorder(fo))
            new_form.reconstruct(new_children)
            #in post order the find_method will be there
        return new_form

    def visit_preorder(self, form):
        """the preorder method for visiting the tree"""
        self._visit_preorder(form)

    def _visit_postorder(self, form):
        """the intern postorder method for visiting the tree"""
        if not isinstance(form,Form.TerminalForm):
            children=form.forms
            new_children = []
            for fo in children:
                new_children = self._visit_postorder(fo)
            return self.find_method(form)(form, children)
        else:
            return self.find_method(form)(form)
            
    def visit_postorder(self, form):
        """the postorder method for visiting the tree"""
        self._visit_postorder(form)
        
    def find_method(self, form, H=None, D=None):
        """This method enables to choose the method that we want
        to apply to a specific node"""
        if D is None:
            D = self.handler_dict
           
        for typ, val in D.items():
             
            if isinstance(form, typ):
                
                return (self.find_method(form, *val)) #or H
        return(H)

#The class that draw a graph of our form, and store pre and post visits in a 
#table
class VisitorGraph(Visitor):
    """this class implement a tree visitor for our form"""
    def __init__(self):
        self.handler_dict = {Form.OperatorForm:(func_op_fo,{Form.D: (VisitorGraph.diff, {})\
							, Form.Wedge: (VisitorGraph.wed, {}), Form.Add: (VisitorGraph.add,{}), \
							Form.Hodge: (VisitorGraph.hod, {}) }),\
							Form.TerminalForm:(VisitorGraph.func_term_fo,{})}
        self.dot = Graph(comment='Tree of our form')#Digraph(comment='Tree of our form') #to store the dot for vizgraph
        self.edges = [] #to store the edge for the graph
        self.post = [] #to store the post order traversal
        self.pre = [] # to store the pre order traversal
        self.comp = 0 #to differentiate the edge
        
    @staticmethod
    def plus(form, children):
        pass
	
    #D form
    @staticmethod
    def diff(form, children=None):
        """function when a diff operation is made"""
        if form.scalar == 1:
            return( 'd')
        elif form.scalar == -1:
            return( "-d" )
        else:
            return( "{}d ".format(form.scalar)  )
        #print("d ")
    
    #Wedge
    @staticmethod
    def wed(form, children=None):
        """function when a wedge operation is made"""
        if form.scalar == 1:
            return( '^')
        elif form.scalar == -1:
            return( "-^" )
        else:
            return( "{}^ ".format(form.scalar)  )

        #print("^ ")
                    
    #Add
    @staticmethod
    def add(form, children=None):
        """function when a add operation is made"""
        if form.scalar == 1:
            return( '+')
        elif form.scalar == -1:
            return( "-+" )
        else:
            return( "{}+ ".format(form.scalar)  )

        #print("+ ")
                    
    #Hodge
    @staticmethod
    def hod(form, children=None):
        """function when a hodge star operation is made"""
        if form.scalar == 1:
            return( '*')
        elif form.scalar == -1:
            return( "-*" )
        else:
            return( "{}* ".format(form.scalar)  )
        #print("* ")

    #TerminalForm
    @staticmethod
    def func_term_fo(form):
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
            print(name)
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

