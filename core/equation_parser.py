"""
Mathematical expression parser and validator
"""
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

class EquationParser:
    def __init__(self):
        self.transformations = (standard_transformations + (implicit_multiplication_application,))
        self.variables = {}
        self.functions = {}
        
    def parse_expression(self, expression_str):
        """Convert string to sympy expression"""
        try:
            expr = parse_expr(expression_str, transformations=self.transformations)
            return expr
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")
    
    def validate_equation(self, equation_str):
        """Check if equation is valid"""
        # Handle both '=' and '=='
        if '=' in equation_str:
            left, right = equation_str.replace('==', '=').split('=')
            return sp.Eq(self.parse_expression(left), self.parse_expression(right))
        return self.parse_expression(equation_str)
    
    def extract_variables(self, expression):
        """Get all variables in expression"""
        return list(expression.free_symbols)
    
    def substitute_values(self, expression, variable_values):
        """Substitute numerical values for variables"""
        return expression.subs(variable_values)
    
    def define_function(self, name, expression_str):
        """Define custom function"""
        expr = self.parse_expression(expression_str)
        self.functions[name] = expr
        return expr
    
    def evaluate_at_point(self, expression_str, point_dict):
        """Evaluate expression at given point"""
        expr = self.parse_expression(expression_str)
        return float(expr.subs(point_dict))
    
    def get_function_string(self, expression):
        """Get readable string representation"""
        return str(expression)