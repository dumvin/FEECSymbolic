"""Test class for the main files"""
"""py.test testOpertationForm.py"""
import form
import complex
import visitor
import pytest

class TestClass:

    def test_add(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        assert str(a+b) == "a+b"

    def test_add_rule_samerank(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 2, "b")
        assert str(a+b) == "to be added, the forms must have the same rank"

    def test_hodge(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        assert str(a.hodge()) == "*a"

    def test_scalarmult(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        assert str(2*a) == "2a"

    def test_diff(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        assert str(a.d()) == "da"

    def test_wedge(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        assert str(a.wedge(b)) == "a^b"

 
    def test_preorder(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        V = visitor.VisitorGraph()
        form1 = (a+b).wedge(a)+(a+b).hodge()
        V.visit_preorder(form1)
        test = V.pre
        assert test == ['+', '^', '+', 'a', 'b', 'a', '*', '+', 'a', 'b']

    def test_postorder(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        V = visitor.VisitorGraph()
        form1 = (a+b).wedge(a)+(a+b).hodge()
        V.visit_postorder(form1)
        test = V.post
        assert test == ['a', 'b', '+', 'a', '^', 'a', 'b', '+', '*', '+']

    def test_drawgraph(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        V = visitor.VisitorGraph()
        form1 = (4*(a+b)).wedge(-2*a)+(a-3*b).hodge()
        V.draw_graph(form1)
        test = str(V.dot.source)
        assert test == '// Tree of our form\ngraph {\n\t0 [label="+"]\n\t1 [label="^"]\n\t\t0 -- 1\n\t2 [label="4+ "]\n\t\t1 -- 2\n\t3 [label=a]\n\t\t2 -- 3\n\t4 [label=b]\n\t\t2 -- 4\n\t5 [label="-2a "]\n\t\t1 -- 5\n\t6 [label="*"]\n\t\t0 -- 6\n\t7 [label="+"]\n\t\t6 -- 7\n\t8 [label=a]\n\t\t7 -- 8\n\t9 [label="-3b "]\n\t\t7 -- 9\n}'
    
    #Pullback step 2
    #@pytest.mark.xfail
    def test_pullback_terminal(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        V = visitor.VisitorPullback()
        real = (a.pullback()).d()
        test = V._visit_preorder((a.d()).pullback())
        assert str(real) == str(test)


    #Distribution of the sum on the hodge star
    def test_visitor_hodge_distribution(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        V = visitor.HodgeDistribution()
        real = a.hodge()+b.hodge()
        test = V._visit_preorder((a+b).hodge())
        assert str(real) == str(test)
        
    def test_visitor_hodge_distribution(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        V = visitor.VisitorHodgeDistribution()
        real = a.hodge()+b.hodge()+b.wedge(a)
        test = V._visit_preorder((a+b).hodge()+b.wedge(a))
        assert str(real) == str(test)
