"""
Command-line interface for the scientific suite
"""
import argparse
import sys
import cmd
from core.equation_parser import EquationParser
from core.solvers.algebraic import AlgebraicSolver
from core.solvers.numerical import NumericalMethods
from visualization.plotter import Plotter
from visualization.graph_types import GraphTypes
import numpy as np

class ScientificCLI(cmd.Cmd):
    """Interactive command-line interface"""
    
    intro = """
    ============================================
    Scientific Computing Suite - Interactive CLI
    ============================================
    Type 'help' for available commands or 'exit' to quit.
    """
    prompt = 'sci> '
    
    def __init__(self):
        super().__init__()
        self.parser = EquationParser()
        self.algebraic_solver = AlgebraicSolver()
        self.numerical = NumericalMethods()
        self.plotter = Plotter()
        self.graph_types = GraphTypes()
        self.variables = {}
        
    def do_solve(self, arg):
        """Solve equation: solve equation [variable]
        Example: solve x**2 - 4 = 0 x"""
        args = arg.split()
        if len(args) < 2:
            print("Usage: solve equation variable")
            return
        
        equation = ' '.join(args[:-1])
        variable = args[-1]
        
        try:
            expr = self.parser.validate_equation(equation)
            solutions = self.algebraic_solver.solve_symbolic(expr, variable)
            if solutions:
                print(f"Solutions: {solutions}")
            else:
                # Try numerical solving
                func = lambda x: float(expr.subs({variable: x}))
                guess = 0
                solution = self.numerical.find_roots(func, (-10, 10))
                print(f"Numerical solution: {solution}")
        except Exception as e:
            print(f"Error: {e}")
    
    def do_plot(self, arg):
        """Plot function: plot expression [xmin xmax]
        Example: plot sin(x) -2 2"""
        args = arg.split()
        if len(args) < 1:
            print("Usage: plot expression [xmin xmax]")
            return
        
        expression = args[0]
        xmin = float(args[1]) if len(args) > 1 else -10
        xmax = float(args[2]) if len(args) > 2 else 10
        
        try:
            expr = self.parser.parse_expression(expression)
            func = lambda x: float(expr.subs('x', x))
            self.plotter.function_plot(func, (xmin, xmax), title=expression)
            self.plotter.show_plot()
        except Exception as e:
            print(f"Error: {e}")
    
    def do_integrate(self, arg):
        """Numerical integration: integrate expression a b
        Example: integrate x**2 0 1"""
        args = arg.split()
        if len(args) < 3:
            print("Usage: integrate expression a b")
            return
        
        expression = args[0]
        a = float(args[1])
        b = float(args[2])
        
        try:
            expr = self.parser.parse_expression(expression)
            func = lambda x: float(expr.subs('x', x))
            result, error = self.numerical.integrate_1d(func, a, b)
            print(f"Result: {result}")
            print(f"Estimated error: {error}")
        except Exception as e:
            print(f"Error: {e}")
    
    def do_derivative(self, arg):
        """Numerical derivative: derivative expression x [h]
        Example: derivative sin(x) 1.0"""
        args = arg.split()
        if len(args) < 2:
            print("Usage: derivative expression x [h]")
            return
        
        expression = args[0]
        x = float(args[1])
        h = float(args[2]) if len(args) > 2 else 1e-5
        
        try:
            expr = self.parser.parse_expression(expression)
            func = lambda x: float(expr.subs('x', x))
            result = self.numerical.differentiate(func, x, h)
            print(f"Derivative at x={x}: {result}")
        except Exception as e:
            print(f"Error: {e}")
    
    def do_define(self, arg):
        """Define variable: define var = value
        Example: define pi = 3.14159"""
        try:
            var, expr = arg.split('=')
            var = var.strip()
            value = eval(expr.strip())
            self.variables[var] = value
            print(f"{var} = {value}")
        except Exception as e:
            print(f"Error: {e}")
    
    def do_clear(self, arg):
        """Clear variables"""
        self.variables.clear()
        print("Variables cleared")
    
    def do_show(self, arg):
        """Show defined variables"""
        if self.variables:
            for var, val in self.variables.items():
                print(f"{var} = {val}")
        else:
            print("No variables defined")
    
    def do_quadratic(self, arg):
        """Plot quadratic: quadratic a b c [xmin xmax]
        Example: quadratic 1 -2 1 -5 5"""
        args = arg.split()
        if len(args) < 3:
            print("Usage: quadratic a b c [xmin xmax]")
            return
        
        a = float(args[0])
        b = float(args[1])
        c = float(args[2])
        xmin = float(args[3]) if len(args) > 3 else -10
        xmax = float(args[4]) if len(args) > 4 else 10
        
        try:
            fig = self.graph_types.quadratic_plot(a, b, c, (xmin, xmax))
            plt.show()
        except Exception as e:
            print(f"Error: {e}")
    
    def do_trig(self, arg):
        """Plot trig function: trig type amplitude freq phase [xmin xmax]
        Example: trig sin 2 1 0 -5 5"""
        args = arg.split()
        if len(args) < 4:
            print("Usage: trig type amplitude freq phase [xmin xmax]")
            return
        
        func_type = args[0]
        amplitude = float(args[1])
        frequency = float(args[2])
        phase = float(args[3])
        xmin = float(args[4]) if len(args) > 4 else 0
        xmax = float(args[5]) if len(args) > 5 else 4*np.pi
        
        try:
            fig = self.graph_types.trigonometric_plot(func_type, amplitude, 
                                                      frequency, phase, (xmin, xmax))
            plt.show()
        except Exception as e:
            print(f"Error: {e}")
    
    def do_save(self, arg):
        """Save current plot: save filename
        Example: save myplot.png"""
        if arg:
            self.plotter.save_plot(arg)
        else:
            print("Usage: save filename")
    
    def do_exit(self, arg):
        """Exit the program"""
        print("Goodbye!")
        return True
    
    def do_help(self, arg):
        """Show help"""
        print("""
Available commands:
  solve       - Solve equation
  plot        - Plot function
  integrate   - Numerical integration
  derivative  - Numerical derivative
  define      - Define variable
  quadratic   - Plot quadratic function
  trig        - Plot trigonometric function
  show        - Show defined variables
  clear       - Clear all variables
  save        - Save current plot
  exit        - Exit program
  
For detailed help: help <command>
        """)

def main():
    """Main CLI entry point"""
    if len(sys.argv) > 1:
        # Non-interactive mode - process single command
        parser = argparse.ArgumentParser(description='Scientific Computing Suite')
        parser.add_argument('command', help='Command to execute')
        parser.add_argument('args', nargs='*', help='Command arguments')
        args = parser.parse_args()
        
        # Execute single command
        cli = ScientificCLI()
        cmd_name = f'do_{args.command}'
        if hasattr(cli, cmd_name):
            getattr(cli, cmd_name)(' '.join(args.args))
        else:
            print(f"Unknown command: {args.command}")
    else:
        # Interactive mode
        ScientificCLI().cmdloop()

if __name__ == '__main__':
    main()