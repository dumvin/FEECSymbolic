class Visitor(object):
    """this class implement a tree visitor for our form"""
    def __init__():
        self.handler_dict = {OperatorForm:(HO,DO),TerminalForm:(HT,DT)}

    def visit(self, form):
        """for the moment we will do a preorder """
        if not isinstance(form,TerminalForm):
            self.find_method(form)
            self.visit(node.left, visitor)
            self.visit(node.right, visitor)
        self.find_method(form)
        
    def find_method(self, form, H=None, D=None):
        """This method enables to choose the method that we wamt to apply to a specific node"""
        if D is None:
            D = self.handler_dict
        for type, val in D.items():
            if isinstance(form,type):
                return self.find_method(self,form,*val) or H
            return(H)
