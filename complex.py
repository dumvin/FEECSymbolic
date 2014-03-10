
class Complex:
	"""This class represent a Complex, which is needed to define a form.
	For the moment a complex has only a dimension attribute, we will then add the spaces that define the complex"""
	def __init__(self,dimension=0):
		"""This constructor needs a dimension(default value is 0), which is the dimension of our complex"""
		self.dimension=dimension
	def __repr__(self):
		return "This a complex of dimension: {}".format(self.dimension)
	def __str__(self):
		return "This a complex of dimension: {}".format(self.dimension)