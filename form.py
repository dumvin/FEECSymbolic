import itertools
import copy
import visitor


scalar_precedence=50

def parenthesize(func):
 
    def _parenthesize(self, parent_precedence=0):
        """This defines the decorator to parenthesize or not in the LaTeX rep of the form"""
        if self.scalar!=1:
            obj_precedence=scalar_precedence
        else:
            obj_precedence=self.precedence

        if parent_precedence > obj_precedence:
            return "("+func(self, parent_precedence)+")"
        else:
            return func(self, parent_precedence)

    return _parenthesize

class Form(object):
    """This class is the parent class where you define a form thanks to
    a complex and a rank"""

    def __init__(self, complex, rank,scalar=1):
        self.rank=rank
        self.complex=complex
        self.scalar=scalar


    def d(self):
        """This defines the differentiation of an operator"""
        if self.rank==self.complex.dimension:
            return Zero(self.complex,0)
        return D(self)

    def wedge(self,formBis):
        """this does the wedges of self by formBis, the sense is very important, if formBis is an int it does the scalar multiplication
        If the other way is wanted do formBis.wedge(self)"""

        if self.rank+formBis.rank>self.complex.dimension:
            return "The sum of the rank of the two form in the wedge must be less or equal to the complex in which they are described"
        elif self.complex!=formBis.complex:
            return "The two forms have to be defined with the same complex"
        return Wedge(self,formBis)

    def __add__(self,form):
        """This is a method to add two forms"""
        if self.rank!=form.rank:
            return "to be added, the forms must have the same rank"
        elif self.complex!=form.complex:
            return "The two forms have to be defined with the same complex"
        return Add(self,form)

    def __radd__(self,form):
        """We define this method so that A+B=B+A"""
        return self.add(form)
        
    def __rmul__(self,sca):
        """We define the scalar multiplication"""
        formb=copy.copy(self)
        formb.scalar=sca
        return formb

    def hodge(self):
        """This defines the Hodge operation"""
        if self.rank==self.complex.dimension:
            return Zero(self.complex,0)
        return Hodge(self)

    def pullback(self):
        """This defines the Hodge operation"""
        return Pullback(self)
        
    def __sub__(self,form):
        """This method defines the difference between txo forms of the same rank"""

        formb=copy.copy(form)
        formb.scalar=-form.scalar
        return(self+formb)

        """if self.rank!=form.rank:
            return "to be added, the forms must have the same rank"
        elif self.complex!=form.complex:
            return "The two forms have to be defined with the same complex"
        return Sub(self,form)"""


class TerminalForm(Form):
    """This define a terminal form which is in its basic representation, 
    e.g. it is not represented by a sequence of operation on forms"""
    def __init__(self, complex, rank, name="form", scalar=1):
        """A terminal Form is defined by a complex, a rank (need to be an int) and a name
        The rank has to be lower than the dimension of the complex"""

        if rank>complex.dimension:
            """ Test to check if the rank of the form is not higher than the dimension"""
            print ("impossible to create a form of rank higher than the dimension of the complex generating the form")

        else:
            self.complex = complex
            self.rank = rank
            self.name = name
            self.scalar = scalar
            self.pullbkack = False #to know if this is a pullbacked form or not yet 
            self.forms = []
            self.transformed = False #True if this terminal form was created from another form in a hodge decomposition operation
            self.originalForm = None #not None if this term form is issued from the form store inside this attribute
            
    precedence=100 #We define the precedence to be the higher for terminal forms.
    
    def reconstruct(self, *children):
        r = TerminalForm(self.complex, self.rank, self.name, self.scalar)
        return r
        
    def decompose(self):
        if self.rank == 0:
            return self
        else:
            f = lambda x : self.complex.basis[x]
            A =  [map(f,x) for x in itertools.combinations(range(self.complex.dimension),self.rank)]
            coefficients = [TerminalForm(self.complex,0,self.name+str(x)) for x in range(len(A))]
            new_decomposition = [0 for x in range(len(A))]
            i = 0
            for x in A:
                for y in x:
                    if new_decomposition[i] == 0:
                        new_decomposition[i] = y
                    else:
                        new_decomposition[i] = new_decomposition[i].wedge(y)
                i = i+1
            new_form = 0
            inter = [x.wedge(y) for x,y in zip(coefficients, new_decomposition) ]
            for x in inter:
                if new_form == 0:
                    new_form = x
                else:
                    new_form = new_form + x
            new_form.scalar = self.scalar
            return new_form


    def __repr__(self):
        if self.scalar==1:
            return self.name
        return "{}.{}".format(self.scalar,self.name) 
        
    @parenthesize    
    def __str__(self,parent_precedence=0):
        if self.scalar==1:
            return self.name
        return "{}{}".format(self.scalar,self.name)
    
    @parenthesize    
    def _to_latex(self,parent_precedence=0):
        if self.scalar==1:
            return self.name
        return "{}{}".format(self.scalar,self.name)        
    
    def to_latex(self):
        """Return the latex representation"""
        return "$ {} $".format(self._to_latex())
        

class Zero(TerminalForm):
    """This define the zero for each form"""
    def __init__(self,complex,rank):
        if rank>complex.dimension:
            """ Test to check if the rank of the form is not higher than the dimension"""
            print( "impossible to create a form of rank higher than the dimension of the complex generating the form")
        else:
            self.complex = complex
            self.rank = rank
            self.name = "0_" + str(rank)
            self.scalar = 1
            self.forms = []
    precedence=100
    
    
class Basis(TerminalForm):
    """This define the zero for each form"""
    def __init__(self, complex, index=1):
            self.complex = complex
            self.rank = 1
            self.name = "dx_"+str(index)
            self.index = index #% complex.dimension
            self.scalar = 1
            self.forms = []
    precedence=100
    
    def decompose(self):
        return self
    
    
    
class OperatorForm(Form):
    """This class is the parent class of all the operation class, We need a representation of the form"""
    def __init__(self,forms,rank,scalar=1):

        self.forms=forms
        self.rank=rank
        self.complex=forms[0].complex
        self.scalar=scalar
        
    def reconstruct(self, children):
        r = self.__class__(*children)
        r.scalar = self.scalar
        return r
        

class D(OperatorForm):
    """ This class is the differentiation operator"""
    def __init__(self,forme):
        """the differentiation operates on a form """
        super(D,self).__init__([forme],forme.rank+1)

    precedence = 70   
    def d(self):
        """ the differentiation of a differentiate form is 0"""
        return Zero(self.complex, self.rank+1)

    def __repr__(self):
        if self.scalar==1:
            return "({}).d()".format(repr(self.forms)) 
        return "{}.({}).d()".format(str(self.scalar),repr(self.forms)) 

    @parenthesize
    def __str__(self,parent_precedence=0):
        if self.scalar==1:
            return "d{}".format(self.forms[0].__str__(self.precedence))
        return "{}d{}".format(self.scalar,self.forms[0].__str__(self.precedence))
        
    @parenthesize
    def _to_latex(self,parent_precedence=0):
        """This function permits to write the the term of latex operator"""      
        if self.scalar==1:
            return "d{}".format(self.forms[0]._to_latex(self.precedence))
        return "{}d{}".format(self.scalar,self.forms[0]._to_latex(self.precedence))
  
    def to_latex(self):    
        """Return the latex representation"""
        return "${}$".format(self._to_latex())


class Wedge(OperatorForm):
    """this class takes for attributes two forms and return their wedge product"""
    def __init__(self,formA,formB):
        """We define the two attributes of our wedge product, the sense is important"""
        #forma=copy.copy(formA)
        super(Wedge,self).__init__([formA,formB],formA.rank+formB.rank)

    precedence=30 

    def __repr__(self):
        if     (self.scalar)==1:
            return "({}).wedge({})".format(repr(self.forms[0]),repr(self.forms[1])) 
        return "{}.({}).wedge({})".format(self.scalar,repr(self.forms[0]),repr(self.forms[1])) 
    @parenthesize
    def __str__(self,parent_precedence=0):
        if     (self.scalar)==1:
            return "{}^{}".format(self.forms[0].__str__(self.precedence),self.forms[1].__str__(self.precedence))
        return "{}({}^{})".format(self.scalar,self.forms[0].__str__(self.precedence),self.forms[1].__str__(self.precedence))
        
    @parenthesize
    def _to_latex(self,parent_precedence=0):
        """This function permits to write the the term of latex operator"""
        if     (self.scalar)==1:
            return "{} \wedge {}".format(self.forms[0]._to_latex(self.precedence),self.forms[1]._to_latex(self.precedence))
        return "{}({} \wedge {})".format(self.scalar,self.forms[0]._to_latex(self.precedence),self.forms[1]._to_latex(self.precedence))
    def to_latex(self):
        return "${}$".format(self._to_latex())

class Add(OperatorForm):
    """ this class creates a form which is the sum of two forms, of the same rank"""
    def __init__(self,formA,formB):
        """we define our sum, the sense is not important"""
        super(Add,self).__init__([formA,formB],formA.rank)
    precedence=10 
    def __repr__(self):
        if self.scalar==1:
            return "({}).add({})".format(repr(self.forms[0]),repr(self.forms[1])) 
        return "{}.({}).add({})".format(str(self.scalar),repr(self.forms[0]),repr(self.forms[1])) 

    @parenthesize
    def __str__(self,parent_precedence=0):
        if self.scalar==1:
            return "{}+{}".format(self.forms[0].__str__(self.precedence),self.forms[1].__str__(self.precedence))  
        return "{}({}+{})".format(self.scalar,self.forms[0].__str__(self.precedence),self.forms[1].__str__(self.precedence))
        
    @parenthesize
    def _to_latex(self,parent_precedence=0):
        """This function permits to write the the term of latex operator"""
        if self.scalar==1:
            return "{}+{}".format(self.forms[0]._to_latex(self.precedence),self.forms[1]._to_latex(self.precedence))  
        return "{}({}+{})".format(self.scalar,self.forms[0]._to_latex(self.precedence),self.forms[1]._to_latex(self.precedence))
        
    def to_latex(self):
        """Return the latex representation"""
        return "${}$".format(self._to_latex())

class Sub(OperatorForm):
    """ this class creates a form which is the sum of two forms, of the same rank"""
    def __init__(self,formA,formB):
        """we define our sum, the sense is not important"""
        super(Sub,self).__init__([formA,formB],formA.rank)

    precedence=10 
    def __repr__(self):
        if self.scalar==1:
            return "({}).sub({})".format(repr(self.forms[0]),repr(self.forms[1])) 
        return "({}).sub({})".format(repr(self.forms[0]),repr(self.forms[1])) 
        
    @parenthesize
    def __str__(self,parent_precedence=0):
        if self.scalar==1:
            return "{}-{}".format(self.forms[0].__str__(self.precedence),self.forms[1].__str__(self.precedence))  
        return"{}({}-{})".format(self.scalar,self.forms[0].__str__(self.precedence),self.forms[1].__str__(self.precedence))

    @parenthesize
    def _to_latex(self,parent_precedence=0):
        """This function permits to write the the term of latex operator"""
        if self.scalar==1:
            return "{}-{}".format(self.forms[0]._to_latex(self.precedence),self.forms[1]._to_latex(self.precedence))  
        return"{}({}-{})".format(self.scalar,self.forms[0]._to_latex(self.precedence),self.forms[1]._to_latex(self.precedence))
        
    def to_latex(self):
        """Return the latex representation"""
        return "${}$".format(str(self))


class Hodge(OperatorForm):
    """ this class creates the hodge star of a form"""
    def __init__(self,form):
        """the differentiation operates on a form """
        super(Hodge,self).__init__([form],form.complex.dimension-form.rank)

    _index = 0 #used when needed to create a terminalform in a hodge star
    precedence=70
    def transform(self,name="H"):
        """function to transform the form inside the hodge star when it is not a terminal form"""
        if not isinstance(self.forms[0], TerminalForm):
            new_Ter = TerminalForm(self.complex, self.complex.dimension-self.rank,"H"+str(0))#str(_index))  
            new_Ter.transformed = True
            new_Ter.originalForm = self.forms[0]
            self.forms[0] = new_Ter
            #_index=_index+1
        else:
            pass

    def __repr__(self):
        if self.scalar==1:
            return "({}).hodge()".format(repr(self.forms)) 
        return "{}.({}).hodge()".format(str(self.scalar),repr(self.forms)) 

    @parenthesize    
    def __str__(self,parent_precedence=0):
        if self.scalar==1:
            return "*{}".format(self.forms[0].__str__(self.precedence))
        return "{}*{}".format(self.scalar,self.forms[0].__str__(self.precedence))

    @parenthesize    
    def _to_latex(self,parent_precedence=0):
        """This function permits to write the the term of latex operator"""
        if self.scalar==1:
            return "\ast {}".format(self.forms[0]._to_latex(self.precedence))
        return "{}\ast {}".format(self.scalar,self.forms[0]._to_latex(self.precedence))
        
    def to_latex(self):
        """Return the latex representation"""
        return "${}$".format(self._to_latex())


class Pullback(OperatorForm):
    """this class is the pullback of a form"""
    """ this class creates the hodge star of a form"""
    def __init__(self,form):
        """the differentiation operates on a form """
        super(Pullback,self).__init__([form],form.rank)

    precedence=110 
    def __repr__(self):
        if self.scalar==1:
            return "phi({})".format(repr(self.forms)) 
        return "phit({}.({}))".format(str(self.scalar),repr(self.forms)) 

    @parenthesize    
    def __str__(self,parent_precedence=0):
        if self.scalar==1:
            return "phi{}".format(self.forms[0].__str__(self.precedence))
        return "phi{}.{}".format(self.scalar,self.forms[0].__str__(self.precedence))

    @parenthesize    
    def _to_latex(self,parent_precedence=0):
        """This function enables to write the the term of latex operator"""
        if self.scalar==1:
            return "\ast \phi {}".format(self.forms[0]._to_latex(self.precedence))
        return "{}\ast \phi {}".format(self.scalar,self.forms[0]._to_latex(self.precedence))
        
    def to_latex(self):
        """Return the latex representation"""
        return "${}$".format(self._to_latex())
