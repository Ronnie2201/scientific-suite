"""
Mathematical constants and configuration
"""
import numpy as np
import math

# Mathematical Constants
class MathConstants:
    """Common mathematical constants"""
    PI = math.pi
    E = math.e
    TAU = 2 * math.pi
    GOLDEN_RATIO = (1 + math.sqrt(5)) / 2
    EULER_MASCHERONI = 0.57721566490153286060651209008240243104215933593992
    CATALAN = 0.915965594177219015054603514932384110774
    INFINITY = float('inf')
    NAN = float('nan')
    
    # Physical Constants
    SPEED_OF_LIGHT = 299792458  # m/s
    PLANCK_CONSTANT = 6.62607015e-34  # J⋅s
    GRAVITATIONAL_CONSTANT = 6.67430e-11  # m³/kg/s²
    ELECTRON_MASS = 9.10938356e-31  # kg
    PROTON_MASS = 1.6726219e-27  # kg
    BOLTZMANN_CONSTANT = 1.380649e-23  # J/K
    AVOGADRO_NUMBER = 6.02214076e23  # mol⁻¹
    GAS_CONSTANT = 8.314462618  # J/(mol·K)
    
    # Astronomical Constants
    ASTRONOMICAL_UNIT = 149597870700  # m
    LIGHT_YEAR = 9460730472580800  # m
    PARSEC = 3.08567758149137e16  # m
    SOLAR_MASS = 1.9885e30  # kg
    SOLAR_RADIUS = 696340000  # m
    EARTH_MASS = 5.97237e24  # kg
    EARTH_RADIUS = 6371000  # m

class PlottingDefaults:
    """Default settings for plotting"""
    FIGURE_SIZE = (10, 6)
    DPI = 100
    COLORS = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    LINE_STYLES = ['-', '--', '-.', ':']
    MARKERS = ['o', 's', '^', 'D', 'v', '<', '>', 'p']
    FONT_SIZE = 12
    TITLE_FONT_SIZE = 14
    LEGEND_FONT_SIZE = 10
    
    # Color maps
    COLORMAPS = {
        'sequential': ['viridis', 'plasma', 'inferno', 'magma', 'cividis'],
        'diverging': ['RdBu', 'PiYG', 'PRGn', 'BrBG', 'PuOr'],
        'qualitative': ['Set1', 'Set2', 'Set3', 'Pastel1', 'Pastel2']
    }

class SolverDefaults:
    """Default settings for solvers"""
    MAX_ITERATIONS = 1000
    TOLERANCE = 1e-6
    STEP_SIZE = 1e-5
    DEFAULT_GUESS = 0.0
    DEFAULT_BRACKET = (-10, 10)
    
    # Integration settings
    INTEGRATION_METHODS = ['quad', 'romberg', 'simpson', 'monte_carlo']
    DEFAULT_INTEGRATION_METHOD = 'quad'
    
    # ODE settings
    ODE_METHODS = ['RK45', 'RK23', 'DOP853', 'Radau', 'BDF']
    DEFAULT_ODE_METHOD = 'RK45'

class ErrorMessages:
    """Standard error messages"""
    INVALID_EXPRESSION = "Invalid mathematical expression"
    NO_SOLUTION_FOUND = "No solution found"
    DIVERGENCE = "Solution diverged"
    INVALID_INPUT = "Invalid input provided"
    FILE_NOT_FOUND = "File not found"
    UNSUPPORTED_OPERATION = "Operation not supported"
    DOMAIN_ERROR = "Value outside function domain"
    NUMERICAL_ERROR = "Numerical error in computation"

class FileFormats:
    """Supported file formats"""
    DATA_FORMATS = {
        'csv': {'extension': '.csv', 'description': 'CSV file'},
        'json': {'extension': '.json', 'description': 'JSON file'},
        'npy': {'extension': '.npy', 'description': 'NumPy array'},
        'pkl': {'extension': '.pkl', 'description': 'Pickle file'},
        'txt': {'extension': '.txt', 'description': 'Text file'},
        'xlsx': {'extension': '.xlsx', 'description': 'Excel file'}
    }
    
    IMAGE_FORMATS = {
        'png': {'extension': '.png', 'description': 'PNG image'},
        'pdf': {'extension': '.pdf', 'description': 'PDF document'},
        'svg': {'extension': '.svg', 'description': 'SVG vector'},
        'jpg': {'extension': '.jpg', 'description': 'JPEG image'}
    }
    
    SESSION_FORMATS = {
        'sci': {'extension': '.sci', 'description': 'Scientific session file'}
    }

# Configuration settings
CONFIG = {
    'app_name': 'Scientific Computing Suite',
    'version': '1.0.0',
    'author': 'Your Name',
    'preferences': {
        'default_precision': 6,
        'auto_save': True,
        'auto_save_interval': 300,  # seconds
        'theme': 'light',  # light/dark
        'language': 'en'
    },
    'paths': {
        'workspace': './workspace',
        'exports': './exports',
        'sessions': './sessions',
        'temp': './temp'
    }
}