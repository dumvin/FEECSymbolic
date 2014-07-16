import form
class Complex:
    """This class represent a Complex, which is needed to define a form.
    For the moment a complex has only a dimension attribute, we will then add the spaces that define the complex"""
    def __init__(self, dimension=0):
        """This constructor needs a dimension(default value is 0), which is the dimension of our complex"""
        self.dimension = dimension
        self.basis = [form.Basis(self, i) for i in range(dimension)]
        #~ self.basis2=[]
        #~ for i in range(dimension):
            #~ if i+1<dimension:
                #~ for j in range(i+1,dimension): 
                    #~ self.basis2.append((self.basis[i]).wedge(self.basis[j]))
#~ 
        #~ self.basis3 = []
        #~ for i in range(len(self.basis2)):
                #~ for j in range(i+2,dimension):
                    #~ self.basis3.append(self.basis2[i].wedge(self.basis[j]))
                    #~ 
        #~ self.basis4 = []
        #~ for i in range(len(self.basis3)):
                #~ for j in range(i+3,dimension):
                    #~ self.basis4.append(self.basis3[i].wedge(self.basis[j]))
                    #~ 
        #~ self.basis2 = []
        #~ for a in self.basis:
            #~ for b in self.basis:
                #~ if b!=a:
                    #~ self.basis2.append(a.wedge(b)) 
        #~ self.basis3 = []
        #~ for a in self.basis2:
            #~ for b in self.basis:
                #~ if b not in a.forms:
                    #~ self.basis3.append(a.wedge(b))
        #~ if self.dimension>3:
            #~ self.basis4 = []
            #~ for a in self.basis4:
                #~ for b in self.basis:
                    #~ for c in a.forms:
                        #~ if b not in c.forms:
                            #~ self.basis4.append(a.wedge(b))
                            

    def __repr__(self):
        return "This a complex of dimension: {}".format(self.dimension)
    def __str__(self):
        return "This a complex of dimension: {}".format(self.dimension)
