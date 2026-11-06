"""
Numerical methods for various mathematical operations
"""
import numpy as np
from scipy import integrate, optimize, interpolate
from scipy import linalg, special

class NumericalMethods:
    def __init__(self, precision=1e-6):
        self.precision = precision
        
    # Integration Methods
    def integrate_1d(self, func, a, b, method='quad'):
        """1D numerical integration"""
        if method == 'quad':
            result, error = integrate.quad(func, a, b)
            return result, error
        elif method == 'romberg':
            return integrate.romberg(func, a, b)
        elif method == 'simpson':
            x = np.linspace(a, b, 100)
            y = func(x)
            return integrate.simps(y, x)
    
    def integrate_2d(self, func, x_bounds, y_bounds):
        """2D numerical integration"""
        def f(y, x):
            return func(x, y)
        return integrate.dblquad(f, x_bounds[0], x_bounds[1], 
                                 lambda x: y_bounds[0], lambda x: y_bounds[1])
    
    def monte_carlo_integrate(self, func, bounds, n_points=10000):
        """Monte Carlo integration"""
        dim = len(bounds)
        points = np.random.uniform(
            [b[0] for b in bounds], 
            [b[1] for b in bounds], 
            (n_points, dim)
        )
        values = np.array([func(*p) for p in points])
        volume = np.prod([b[1]-b[0] for b in bounds])
        return volume * np.mean(values), volume * np.std(values)/np.sqrt(n_points)
    
    # Differentiation Methods
    def differentiate(self, func, x, h=1e-5, method='central'):
        """Numerical differentiation"""
        if method == 'forward':
            return (func(x + h) - func(x)) / h
        elif method == 'backward':
            return (func(x) - func(x - h)) / h
        elif method == 'central':
            return (func(x + h) - func(x - h)) / (2*h)
        elif method == 'fourth_order':
            return (-func(x + 2*h) + 8*func(x + h) - 8*func(x - h) + func(x - 2*h)) / (12*h)
    
    def jacobian(self, func, x, h=1e-5):
        """Compute Jacobian matrix"""
        n = len(x)
        m = len(func(x))
        J = np.zeros((m, n))
        for i in range(n):
            x_plus = x.copy()
            x_plus[i] += h
            J[:, i] = (func(x_plus) - func(x)) / h
        return J
    
    # Interpolation Methods
    def interpolate(self, x, y, kind='cubic'):
        """Interpolate data points"""
        if kind == 'linear':
            return interpolate.interp1d(x, y, kind='linear')
        elif kind == 'cubic':
            return interpolate.interp1d(x, y, kind='cubic')
        elif kind == 'spline':
            return interpolate.UnivariateSpline(x, y)
        elif kind == 'polynomial':
            return np.poly1d(np.polyfit(x, y, min(len(x)-1, 5)))
    
    # Root Finding
    def find_roots(self, func, interval, method='bisection'):
        """Find roots in interval"""
        if method == 'bisection':
            from scipy.optimize import bisect
            return bisect(func, interval[0], interval[1])
        elif method == 'newton':
            from scipy.optimize import newton
            return newton(func, (interval[0] + interval[1])/2)
    
    # Series Expansions
    def taylor_series(self, func, x0, n_terms, x_range):
        """Compute Taylor series approximation"""
        coeffs = []
        for i in range(n_terms):
            # Numerical approximation of derivatives
            if i == 0:
                coeffs.append(func(x0))
            else:
                # Approximate derivative using finite differences
                h = 1e-5
                derivative = self.differentiate(func, x0, h, 'central')
                for _ in range(i-1):
                    derivative = self.differentiate(derivative, x0, h, 'central')
                coeffs.append(derivative / np.math.factorial(i))
        
        def taylor_func(x):
            result = 0
            for i, coeff in enumerate(coeffs):
                result += coeff * (x - x0)**i
            return result
        
        return taylor_func