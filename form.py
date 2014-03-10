from complexe import *
import copy
#from decorator import decorator
#Importer la classe decorator...

scalar_precedence=50
   
def parenthesize(func):
 
	def _parenthesize(self ,parent_precedence=0):
		"""This defines the decorator to parenthesize or not in the LaTeX rep of the form"""
		if self.scalar!=1:
			obj_precedence=scalar_precedence
		else:
			obj_precedence=self.precedence
		
		if parent_precedence > obj_precedence:
			return "("+func(self,parent_precedence)+")"
		else:
			return func(self,parent_precedence)

	return _parenthesize

class Form(object):
	"""This class is the parent class where you define a form thanks to
	a complex and a rank"""
	
	def __init__(self, complex, rank):
		self.rank=rank
		self.complex=complex
		
		
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
		
	def hodge(self):
		"""This defines the Hodge operation"""
		if self.rank==self.complex.dimension:
			return Zero(self.complex,0)
		return Hodge(self)
		
	def __sub__(self,form):
		"""This method defines the difference between txo forms of the same rank"""

		formb=copy.copy(form)
		formb.sclar=-1
		return(self+formb)

		"""if self.rank!=form.rank:
			return "to be added, the forms must have the same rank"
		elif self.complex!=form.complex:
			return "The two forms have to be defined with the same complex"
		return Sub(self,form)"""
	
		
class TerminalForm(Form):
	"""This define a terminal form which is in its basic representation, 
	e.g. it is not represented by a sequence of operation on forms"""
	def __init__(self,complex,rank,name="form",scalar=1):
		"""A terminal Form is defined by a complex, a rank (need to be an int) and a name
		The rank has to be lower than the dimension of the complex"""
		
		if rank>complex.dimension:
			""" Test to check if the rank of the form is not higher than the dimension"""
			print ("impossible to create a form of rank higher than the dimension of the complex generating the form")
		
		else:
			self.complex=complex
			self.rank=rank
			self.name=name
			self.scalar=scalar
	precedence=100#We define the precedence to be the higher for terminal forms.
	def __repr__(self):
		if self.scalar==1:
			return self.name
		return "{}.{}".format(self.scalar,self.name) 
		
	def __str__(self,parent_precedence):
		return self.name
		
	def to_latex(self,parent_precedence):
		"""Return the latex representation"""
		return "$ {} $".format(self.name)
		
class Zero(TerminalForm):
	"""This define the zero for each form"""
	def __init__(self,complex,rank):
		if rank>complex.dimension:
			""" Test to check if the rank of the form is not higher than the dimension"""
			print( "impossible to create a form of rank higher than the dimension of the complex generating the form")
		else:
			self.complex=complex
			self.rank=rank
			self.name="0_"+str(rank)
			self.scalar=1
	precedence=100

class OperatorForm(Form):
	"""This class is the parent class of all the operation class, We need a representation of the form"""
	def __init__(self,forms,rank,scalar=1):
		
		self.forms=forms
		self.rank=rank
		self.complex=forms[0].complex
		self.scalar=scalar

class D(OperatorForm):
	""" This class is the differentiation operator"""
	def __init__(self,forme):
		"""the differentiation operates on a form """
		scalar=forme.scalar
		formb=forme
		formb.scalar=1
		super(D,self).__init__([formb],forme.rank,scalar)
		
	precedence=70 #To be defined	
	def d(self):
		""" the differentiation of a differentiate form is 0"""
		return Zero(self.complex,self.rank+1)
		
	def __repr__(self):
		return "({}).d()".format(repr(self.forms)) 
	
	@parenthesize
	def __str__(self,parent_precedence=0):
		return "d{}".format(self.forms[0].__str__(self.precedence))
	
	def to_latex(self):
		"""Return the latex representation"""
		return "${}$".format(str(self))

	
class Wedge(OperatorForm):
	"""this class takes for attributes two forms and return their wedge product"""
	def __init__(self,formA,formB):
		"""We define the two attributes of our wedge product, the sense is important"""
		#forma=copy.copy(formA)
		super(Wedge,self).__init__([formA,formB],formA.rank+formB.rank)
		
	precedence=30 
	
	def __repr__(self):
		if 	(self.scalar)==1:
			return "({}).wedge({})".format(repr(self.forms[0]),repr(self.forms[1])) 
		return "{}.({}).wedge({})".format(self.scalar,repr(self.forms[0]),repr(self.forms[1])) 
	@parenthesize
	def __str__(self,parent_precedence=0):
		return "{}^{}".format(self.forms[0].__str__(self.precedence),self.forms[1].__str__(self.precedence))
	
	def to_latex(self):
		return "${}$".format(str(self))
		
class Add(OperatorForm):
	""" this class creates a form which is the sum of two forms, of the same rank"""
	def __init__(self,formA,formB):
		"""we define our sum, the sense is not important"""
		super(Add,self).__init__([formA,formB],formA.rank)
	precedence=10 #To be defined	
	def __repr__(self):
		if self.scalar==1:
			return "({}).add({})".format(repr(self.forms[0]),repr(self.forms[1])) 
		return "{}.({}).add({})".format(str(self.scalar),repr(self.forms[0]),repr(self.forms[1])) 
		
	@parenthesize
	def __str__(self,parent_precedence=0):
		return "{}+{}".format(self.forms[0].__str__(self.precedence),self.forms[1].__str__(self.precedence))  
		
	def to_latex(self):
		"""Return the latex representation"""
		return "${}$".format(str(self))

class Sub(OperatorForm):
	""" this class creates a form which is the sum of two forms, of the same rank"""
	def __init__(self,formA,formB):
		"""we define our sum, the sense is not important"""
		super(Sub,self).__init__([formA,formB],formA.rank)
		
	precedence=10 #To be defined
	def __repr__(self):
		if self.scalar==1:
			return "({}).sub({})".format(repr(self.forms[0]),repr(self.forms[1])) 
		return "({}).sub({})".format(repr(self.forms[0]),repr(self.forms[1])) 
	@parenthesize
	def __str__(self,parent_precedence=0):
		return "{}-{}".format(self.forms[0].__str__(self.precedence),self.forms[1].__str__(self.precedence))  
		
	def to_latex(self):
		"""Return the latex representation"""
		return "${}$".format(str(self))
		
		
class Hodge(OperatorForm):
	""" this class creates the hodge star of a form"""
	def __init__(self,form):
		"""the differentiation operates on a form """
		super(Hodge,self).__init__([form],form.complex.dimension-form.rank)
		
	precedence=70 #To be defined	
	def __repr__(self):
		if self.scalar==1:
			return "({}).hodge()".format(repr(self.forms)) 
		return "{}.({}).hodge()".format(str(self.scalar),repr(self.forms)) 
	
	@parenthesize	
	def __str__(self,parent_precedence=0):
		return "*{}".format(self.forms[0].__str__(self.precedence))
		
		
	def to_latex(self):
		"""Return the latex representation"""
		return "${}$".format(str(self))

		
