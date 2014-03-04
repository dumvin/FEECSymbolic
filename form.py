from complexe import *

class Form:
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

		if self.rank!=form.rank:
			return "to be added, the forms must have the same rank"
		elif self.complex!=form.complex:
			return "The two forms have to be defined with the same complex"
		return Sub(self,form)
	
		
class TerminalForm(Form):
	"""This define a terminal form which is in its basic representation, 
	e.g. it is not represented by a sequence of operation on forms"""
	def __init__(self,complex,rank,name="form"):
		"""A terminal Form is defined by a complex, a rank (need to be an int) and a name
		The rank has to be lower than the dimension of the complex"""
		
		if rank>complex.dimension:
			""" Test to check if the rank of the form is not higher than the dimension"""
			print ("impossible to create a form of rank higher than the dimension of the complex generating the form")
		
		else:
			self.complex=complex
			self.rank=rank
			self.name=name
		
	def __repr__(self):
		return self.name
	
	def __str__(self):
		
		return self.name
		
	def toLatex(self):
		"""Return the latex representation"""

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



class OperatorForm(Form):
	"""This class is the parent class of all the operation class, We need a representation of the form"""
	def __init__(self,forms,rank):
		
		self.forms=forms
		self.rank=rank
		self.complex=forms[0].complex
	

class D(OperatorForm):
	""" This class is the differentiation operator"""
	def __init__(self,forme):
		"""the differentiation operates on a form """
		super(D,self).__init__([forme],forme.rank)
	def d(self):
		""" the differentiation of a differentiate form is 0"""
		return Zero(self.complex,self.rank+1)
		
	def __repr__(self):
		return "({}).d()".format(repr(self.forms)) 
		
	def __str__(self):
		if isinstance(self.forms[0],TerminalForm):
			return "d{}".format(str(self.forms))
		return "d({})".format(str(self.forms))
		
	def toLatex(self):
		"""Return the latex representation"""
	
class Wedge(OperatorForm):
	"""this class takes for attributes two forms and return their wedge product"""
	def __init__(self,formA,formB):
		"""We define the two attributes of our wedge product, the sense is important"""
		super(Wedge,self).__init__([formA,formB],formA.rank+formB.rank)
		
	
	def __repr__(self):
		return "({}).wedge({})".format(repr(self.forms[0]),repr(self.forms[1])) 
		
	def __str__(self):
		if isinstance(self.forms[0],TerminalForm):
			if isinstance(self.forms[1],TerminalForm):
				return "{}^{} ".format(str(self.forms[0]),str(self.forms[1]))
			else :
				return "{}^({}) ".format(str(self.forms[0]),str(self.forms[1]))
		if isinstance(self.forms[1],TerminalForm):
				return "({})^{} ".format(str(self.forms[0]),str(self.forms[1]))
		return "({})^({}) ".format(str(self.forms[0]),str(self.forms[1]))
	def toLatex(self):
		"""Return the latex representation"""
		
class Add(OperatorForm):
	""" this class creates a form which is the sum of two forms, of the same rank"""
	def __init__(self,formA,formB):
		"""we define our sum, the sense is not important"""
		super(Add,self).__init__([formA,formB],formA.rank)
		
		
	
	def __repr__(self):
		return "{}.add({})".format(repr(self.forms[0]),repr(self.forms[1])) 
	def __str__(self):
	
		return "{}+{}".format(str(self.forms[0]),str(self.forms[1])) 
	
	def toLatex(self):
		"""Return the latex representation"""

class Sub(OperatorForm):
	""" this class creates a form which is the sum of two forms, of the same rank"""
	def __init__(self,formA,formB):
		"""we define our sum, the sense is not important"""
		super(Sub,self).__init__([formA,formB],formA.rank)

	
	def __repr__(self):
		return "({}).sub({})".format(repr(self.forms[0]),repr(self.forms[1])) 
	def __str__(self):
	
		return "{}-{}".format(str(self.forms[0]),str(self.forms[1])) 
	
	def toLatex(self):
		"""Return the latex representation"""

class Hodge(OperatorForm):
	""" this class creates the hodge star of a form"""
	def __init__(self,form):
		"""the differentiation operates on a form """
		super(Hodge,self).__init__([form],form.complex.dimension-form.rank)
		
	def __repr__(self):
		return "({}).hodge()".format(repr(self.forms)) 
		
	def __str__(self):
		if isinstance(self.forms[0],TerminalForm):
			return "*{}".format(str(self.forms[0]))
		return "*({})".format(str(self.forms[0]))
		
	def toLatex(self):
		"""Return the latex representation"""
		
