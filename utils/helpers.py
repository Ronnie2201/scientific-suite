"""
Helper functions and utilities
"""
import numpy as np
import sympy as sp
from typing import Union, List, Tuple, Callable
import math
import re

class MathHelpers:
    """Mathematical helper functions"""
    
    @staticmethod
    def is_number(s: str) -> bool:
        """Check if string is a number"""
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def round_sig(x: float, sig: int = 4) -> float:
        """Round to significant figures"""
        if x == 0:
            return 0
        return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)
    
    @staticmethod
    def vectorize_function(func: Callable) -> Callable:
        """Convert function to work with numpy arrays"""
        return np.vectorize(func)
    
    @staticmethod
    def find_nearest(array: np.ndarray, value: float) -> Tuple[float, int]:
        """Find nearest value in array"""
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx], idx
    
    @staticmethod
    def linspace_with_center(start: float, end: float, num: int, center: float = 0) -> np.ndarray:
        """Create linspace with more points near center"""
        x = np.linspace(0, 1, num)
        # Transform to have more density near center
        x = np.sign(x - 0.5) * np.abs(x - 0.5)**0.5 + 0.5
        return start + (end - start) * x
    
    @staticmethod
    def is_power_of_two(n: int) -> bool:
        """Check if number is power of two"""
        return n & (n-1) == 0 and n != 0

class StringHelpers:
    """String manipulation helpers"""
    
    @staticmethod
    def extract_numbers(text: str) -> List[float]:
        """Extract all numbers from string"""
        return [float(x) for x in re.findall(r'-?\d+\.?\d*', text)]
    
    @staticmethod
    def format_equation(equation: str) -> str:
        """Format equation nicely"""
        # Add spaces around operators
        equation = re.sub(r'([\+\-\*/=])', r' \1 ', equation)
        # Clean up multiple spaces
        equation = re.sub(r'\s+', ' ', equation)
        return equation.strip()
    
    @staticmethod
    def latex_to_sympy(latex_str: str) -> str:
        """Convert LaTeX to sympy readable string (basic)"""
        # This is a simplified version - consider using latex2sympy for production
        replacements = [
            (r'\sin', 'sin'),
            (r'\cos', 'cos'),
            (r'\tan', 'tan'),
            (r'\log', 'log'),
            (r'\exp', 'exp'),
            (r'\sqrt', 'sqrt'),
            (r'\{', '('),
            (r'\}', ')'),
            (r'\^', '**'),
        ]
        for latex, sympy in replacements:
            latex_str = latex_str.replace(latex, sympy)
        return latex_str
    
    @staticmethod
    def sympy_to_latex(expr: sp.Expr) -> str:
        """Convert sympy expression to LaTeX"""
        return sp.latex(expr)

class FileHelpers:
    """File operation helpers"""
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """Get file extension"""
        return filename.split('.')[-1].lower() if '.' in filename else ''
    
    @staticmethod
    def validate_filename(filename: str, allowed_extensions: List[str]) -> bool:
        """Validate filename extension"""
        ext = FileHelpers.get_file_extension(filename)
        return ext in allowed_extensions
    
    @staticmethod
    def generate_filename(base: str, extension: str, timestamp: bool = True) -> str:
        """Generate filename with optional timestamp"""
        if timestamp:
            from datetime import datetime
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{base}_{timestamp_str}.{extension}"
        return f"{base}.{extension}"

def timer_decorator(func):
    """Decorator to time function execution"""
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper