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
        form1 = -2*((4*(a+b)).wedge(-2*a))+5*(a-3*b+(2*a+5*b).d().hodge()).hodge()
        V.draw_graph(form1, "originalform")
        test = str(V.dot.source)
        assert test == '// Tree of our form\ngraph {\n\t0 [label="+"]\n\t1 [label="-2^ "]\n\t\t0 -- 1\n\t2 [label="4+ "]\n\t\t1 -- 2\n\t3 [label=a]\n\t\t2 -- 3\n\t4 [label=b]\n\t\t2 -- 4\n\t5 [label="-2a "]\n\t\t1 -- 5\n\t6 [label="5* "]\n\t\t0 -- 6\n\t7 [label="+"]\n\t\t6 -- 7\n\t8 [label="+"]\n\t\t7 -- 8\n\t9 [label=a]\n\t\t8 -- 9\n\t10 [label="-3b "]\n\t\t8 -- 10\n\t11 [label="*"]\n\t\t7 -- 11\n\t12 [label=d]\n\t\t11 -- 12\n\t13 [label="+"]\n\t\t12 -- 13\n\t14 [label="2a "]\n\t\t13 -- 14\n\t15 [label="5b "]\n\t\t13 -- 15\n}'
    
    #Pullback step 2
    #@pytest.mark.xfail
    def test_pullback_terminal(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        V = visitor.VisitorPullback()
        real = (a.pullback()).d()
        test = V._visit_preorder((a.d()).pullback())
        assert str(real) == str(test)
    
    def test_pullback_draw(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        V = visitor.VisitorPullback()
        form1 = (-2*((4*(a+b)).wedge(-2*a))+5*(a-3*b+(2*a+5*b).d().hodge()).hodge()).pullback()
        V.draw_graph(form1, "Pulled")
        test = (V.visit_preorder(form1))
        assert str(test) != '-2(4(phi(a)+phi(b))^phi(-2a))+phi5.(5*(a+-3b+*d(2a+5b)))'

    #cleaning step
    def test_clean_draw(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        V = visitor.VisitorPullback()
        form1 = (-2*((4*(a+b)).wedge(-2*a))+5*(a-3*b+(2*a+5*b).d().hodge()).hodge()).pullback()
        form1 = V.visit_preorder(form1)
        Vi = visitor.VisitorSimplification()
        Vi.draw_graph(form1, "cleaned")
        test = (V.visit_preorder(form1))
        assert str(test) != "-2(4(phi(a)+phi(b))^phi(-2a))+phi5.(5*(a+-3b+*d(2a+5b)))"
        
    #basis decomp
    def test_basisde_draw(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        V = visitor.VisitorPullback()
        form1 = (-2*((4*(a+b)).wedge(-2*a))+5*(a-3*b+(2*a+5*b).d().hodge()).hodge()).pullback()
        form1 = V.visit_preorder(form1)
        Vi = visitor.VisitorSimplification()
        form1 = Vi.visit_preorder(form1)
        Vii = visitor.VisitorExpansion()
        Vii.draw_graph(form1, "decomposed")
        test = (Vii.visit_preorder(form1))
        test = str(test)
        assert test != "-2(4(a'0^dx_0+a'1^dx_1+a'2^dx_2+b'0^dx_0+b'1^dx_1+b'2^dx_2)^-2(a'0^dx_0+a'1^dx_1+a'2^dx_2))+phi5.(5*(a0^dx_0+a1^dx_1+a2^dx_2+-3(b0^dx_0+b1^dx_1+b2^dx_2)+*d(2(a0^dx_0+a1^dx_1+a2^dx_2)+5(b0^dx_0+b1^dx_1+b2^dx_2))))"
    

    #Distribution of the sum on the hodge star
    def test_visitor_hodge_distribution(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        V = visitor.VisitorHodgeDistribution()
        real = 3*((2*a).hodge()+(5*b).hodge())
        test = V._visit_preorder(3*(2*a+5*b).hodge())
        V.draw_graph(test, "Essai")
        assert str(real) == str(test)

    #Leibniz/add
    def test_visitor_d_distribution(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        V = visitor.VisitorHodgeDistribution()
        real = 3*((2*a).d()+(5*b).d())
        test = V._visit_preorder(3*(2*a+5*b).d())
        V.draw_graph(test, "Essai2")
        assert str(real) == str(test)
        
    #Leibniz/wedge
    def test_visitor_wedgeD_distribution(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        V = visitor.VisitorHodgeDistribution()
        real = 3*((2*a).d().wedge(5*b)-(2*a).wedge((5*b).d()))
        test = V._visit_preorder(3*((2*a).wedge(5*b)).d())
        V.draw_graph(test, "Essai3")
        assert str(real) == str(test)
        
    def test_visitor_hodge_distribution2(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        V = visitor.VisitorHodgeDistribution()
        real = a.hodge()+b.hodge()+b.wedge(a)
        test = V._visit_preorder((a+b).hodge()+b.wedge(a))
        assert str(real) == str(test)
        
    def test_hodgeexpansion_draw(self):
        C = complex.Complex(3)
        a = form.TerminalForm(C, 1, "a")
        b = form.TerminalForm(C, 1, "b")
        V = visitor.VisitorPullback()
        form1 = (-2*((4*(a+b)).wedge(-2*a))+5*(a-3*b+(2*a+5*b).d().hodge()).hodge()).pullback()
        form1 = V.visit_preorder(form1)
        Vi = visitor.VisitorSimplification()
        form1 = Vi.visit_preorder(form1)
        Vii = visitor.VisitorExpansion()
        form1 = Vii.visit_preorder(form1)
        Viii = visitor.VisitorHodgeDistribution()
        Viii.draw_graph(form1, "HodgeDistribution")
        test = (Viii.visit_preorder(form1)) 
        test = str(test)
        assert test!= "a"

