"""
Specialized graph types and functions
"""
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch, Circle
import matplotlib.patches as mpatches

class GraphTypes:
    def __init__(self):
        self.fig = None
        self.ax = None
        
    def quadratic_plot(self, a, b, c, x_range=(-10, 10)):
        """Plot quadratic function ax² + bx + c"""
        x = np.linspace(x_range[0], x_range[1], 1000)
        y = a*x**2 + b*x + c
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, y, 'b-', label=f'{a}x² + {b}x + {c}')
        
        # Find vertex
        vertex_x = -b/(2*a)
        vertex_y = a*vertex_x**2 + b*vertex_x + c
        ax.plot(vertex_x, vertex_y, 'ro', label='Vertex')
        
        # Find roots if real
        discriminant = b**2 - 4*a*c
        if discriminant >= 0:
            root1 = (-b + np.sqrt(discriminant))/(2*a)
            root2 = (-b - np.sqrt(discriminant))/(2*a)
            ax.plot([root1, root2], [0, 0], 'go', label='Roots')
        
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_title(f'Quadratic: {a}x² + {b}x + {c}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        
        return fig
    
    def trigonometric_plot(self, func_type='sin', amplitude=1, frequency=1, phase=0, 
                           x_range=(0, 4*np.pi)):
        """Plot trigonometric functions"""
        x = np.linspace(x_range[0], x_range[1], 1000)
        
        if func_type == 'sin':
            y = amplitude * np.sin(frequency*x + phase)
            func_name = 'sin'
        elif func_type == 'cos':
            y = amplitude * np.cos(frequency*x + phase)
            func_name = 'cos'
        elif func_type == 'tan':
            y = amplitude * np.tan(frequency*x + phase)
            func_name = 'tan'
        elif func_type == 'csc':
            y = amplitude / np.sin(frequency*x + phase)
            func_name = 'csc'
        elif func_type == 'sec':
            y = amplitude / np.cos(frequency*x + phase)
            func_name = 'sec'
        elif func_type == 'cot':
            y = amplitude / np.tan(frequency*x + phase)
            func_name = 'cot'
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(x, y, 'b-', label=f'{amplitude} {func_name}({frequency}x + {phase})')
        
        # Add horizontal lines
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax.axhline(y=amplitude, color='r', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.axhline(y=-amplitude, color='r', linestyle='--', linewidth=0.5, alpha=0.5)
        
        # Add vertical lines at asymptotes for tan, csc, sec, cot
        if func_type in ['tan', 'csc', 'sec', 'cot']:
            # Add asymptote markers (simplified)
            pass
        
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_title(f'Trigonometric: {func_name} function')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_ylim(-amplitude*2, amplitude*2)
        
        return fig
    
    def exponential_plot(self, base, coefficient=1, x_range=(-5, 5)):
        """Plot exponential functions"""
        x = np.linspace(x_range[0], x_range[1], 1000)
        y = coefficient * base**x
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, y, 'b-', label=f'{coefficient} * {base}^x')
        
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_title(f'Exponential: {coefficient} * {base}^x')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        
        return fig
    
    def logarithmic_plot(self, base=10, coefficient=1, x_range=(0.1, 10)):
        """Plot logarithmic functions"""
        x = np.linspace(x_range[0], x_range[1], 1000)
        y = coefficient * np.log(x) / np.log(base)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, y, 'b-', label=f'{coefficient} * log_{base}(x)')
        
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax.axvline(x=0, color='k', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_title(f'Logarithmic: log_{base}(x)')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        
        return fig
    
    def parametric_plot(self, x_func, y_func, t_range=(0, 2*np.pi), num_points=1000):
        """Plot parametric equations"""
        t = np.linspace(t_range[0], t_range[1], num_points)
        x = x_func(t)
        y = y_func(t)
        
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(x, y, 'b-')
        
        # Add arrow to show direction
        mid = len(t)//2
        ax.arrow(x[mid], y[mid], x[mid+1]-x[mid], y[mid+1]-y[mid], 
                head_width=0.1, head_length=0.1, fc='red', ec='red')
        
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.set_title('Parametric Plot')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.axis('equal')
        
        return fig
    
    def polar_function_plot(self, r_func, theta_range=(0, 2*np.pi), num_points=1000):
        """Plot polar functions"""
        theta = np.linspace(theta_range[0], theta_range[1], num_points)
        r = r_func(theta)
        
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='polar')
        
        ax.plot(theta, r, 'b-')
        ax.set_title('Polar Plot')
        ax.grid(True)
        
        return fig
    
    def vector_field_plot(self, X, Y, U, V, title="Vector Field"):
        """Plot vector field"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        ax.quiver(X, Y, U, V, alpha=0.6)
        ax.set_title(title)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        
        return fig
    
    def network_graph(self, adjacency_matrix, node_labels=None, title="Network Graph"):
        """Plot network/graph"""
        G = nx.from_numpy_array(adjacency_matrix)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=node_labels is not None, 
               node_color='lightblue', node_size=500,
               font_size=10, font_weight='bold')
        
        if node_labels:
            labels = {i: label for i, label in enumerate(node_labels)}
            nx.draw_networkx_labels(G, pos, labels)
        
        ax.set_title(title)
        
        return fig
    
    def phase_portrait(self, dx_func, dy_func, x_range=(-2, 2), y_range=(-2, 2), 
                       density=20, title="Phase Portrait"):
        """Plot phase portrait of dynamical system"""
        x = np.linspace(x_range[0], x_range[1], density)
        y = np.linspace(y_range[0], y_range[1], density)
        X, Y = np.meshgrid(x, y)
        
        U = dx_func(X, Y)
        V = dy_func(X, Y)
        
        # Normalize arrows
        N = np.sqrt(U**2 + V**2)
        U = U/N
        V = V/N
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.quiver(X, Y, U, V, alpha=0.6)
        
        # Add nullclines
        ax.contour(X, Y, U, levels=[0], colors='red', linestyles='--', alpha=0.5)
        ax.contour(X, Y, V, levels=[0], colors='blue', linestyles='--', alpha=0.5)
        
        ax.set_title(title)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, alpha=0.3)
        
        return fig