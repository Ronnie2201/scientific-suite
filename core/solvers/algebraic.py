"""
Algebraic equation solvers
"""
import sympy as sp
import numpy as np
from scipy.optimize import fsolve, root

class AlgebraicSolver:
    def __init__(self):
        self.solutions = []
        
    def solve_symbolic(self, equation, variable):
        """Solve equation symbolically using SymPy"""
        try:
            solutions = sp.solve(equation, variable)
            return [float(sol) if sol.is_real else sol for sol in solutions]
        except:
            return None
    
    def solve_numerical(self, function, guess, bounds=None):
        """Solve equation numerically using SciPy"""
        try:
            if bounds:
                # Bounded solver
                solution = root(function, guess, bounds=bounds)
            else:
                # Unbounded solver
                solution = fsolve(function, guess)
            return solution.x
        except Exception as e:
            raise ValueError(f"Numerical solver failed: {e}")
    
    def solve_linear_system(self, equations, variables):
        """Solve system of linear equations"""
        try:
            solution = sp.linsolve(equations, variables)
            return solution
        except:
            # Fallback to numpy for numerical
            A = np.array([[float(coeff) for coeff in eq.lhs.as_coefficients_dict().values()] 
                         for eq in equations])
            b = np.array([float(eq.rhs) for eq in equations])
            return np.linalg.solve(A, b)
    
    def solve_polynomial(self, coefficients):
        """Solve polynomial given coefficients"""
        return np.roots(coefficients)
    
    def solve_trigonometric(self, equation, variable, domain=(0, 2*np.pi)):
        """Solve trig equations within domain"""
        solutions = sp.solveset(equation, variable, domain=sp.Interval(*domain))
        return list(solutions)