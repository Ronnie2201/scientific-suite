"""
Main plotting interface with various graph types
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import plotly.graph_objects as go
import plotly.express as px

class Plotter:
    def __init__(self, style='default', figure_size=(10, 6)):
        self.style = style
        self.figure_size = figure_size
        self.fig = None
        self.ax = None
        self.set_style(style)
        
    def set_style(self, style):
        """Set plotting style"""
        plt.style.use(style)
        sns.set_style("whitegrid")
        
    def line_plot(self, x_data, y_data, title="Line Plot", xlabel="X", ylabel="Y", 
                  labels=None, colors=None, linestyles=None, markers=None):
        """Create line plot with multiple lines"""
        self.fig, self.ax = plt.subplots(figsize=self.figure_size)
        
        # Handle single line vs multiple lines
        if not isinstance(y_data[0], (list, np.ndarray)):
            y_data = [y_data]
        
        for i, y in enumerate(y_data):
            label = labels[i] if labels and i < len(labels) else f'Line {i+1}'
            color = colors[i] if colors and i < len(colors) else None
            linestyle = linestyles[i] if linestyles and i < len(linestyles) else '-'
            marker = markers[i] if markers and i < len(markers) else None
            
            self.ax.plot(x_data, y, label=label, color=color, 
                        linestyle=linestyle, marker=marker)
        
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)
        
        return self.fig
    
    def scatter_plot(self, x_data, y_data, title="Scatter Plot", xlabel="X", ylabel="Y",
                     colors=None, sizes=None, labels=None):
        """Create scatter plot"""
        self.fig, self.ax = plt.subplots(figsize=self.figure_size)
        
        scatter = self.ax.scatter(x_data, y_data, c=colors, s=sizes, alpha=0.6)
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        
        if colors is not None:
            plt.colorbar(scatter)
        
        return self.fig
    
    def bar_chart(self, categories, values, title="Bar Chart", xlabel="Categories", 
                  ylabel="Values", horizontal=False, stacked=False):
        """Create bar chart"""
        self.fig, self.ax = plt.subplots(figsize=self.figure_size)
        
        if horizontal:
            self.ax.barh(categories, values)
        else:
            self.ax.bar(categories, values)
        
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.grid(True, alpha=0.3, axis='y')
        
        return self.fig
    
    def histogram(self, data, bins=30, title="Histogram", xlabel="Value", 
                  ylabel="Frequency", density=False):
        """Create histogram"""
        self.fig, self.ax = plt.subplots(figsize=self.figure_size)
        
        self.ax.hist(data, bins=bins, density=density, alpha=0.7, edgecolor='black')
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.grid(True, alpha=0.3)
        
        return self.fig
    
    def box_plot(self, data, labels=None, title="Box Plot", ylabel="Values"):
        """Create box plot"""
        self.fig, self.ax = plt.subplots(figsize=self.figure_size)
        
        self.ax.boxplot(data, labels=labels)
        self.ax.set_title(title)
        self.ax.set_ylabel(ylabel)
        self.ax.grid(True, alpha=0.3)
        
        return self.fig
    
    def contour_plot(self, X, Y, Z, title="Contour Plot", xlabel="X", ylabel="Y"):
        """Create contour plot"""
        self.fig, self.ax = plt.subplots(figsize=self.figure_size)
        
        contour = self.ax.contour(X, Y, Z, levels=20, cmap='viridis')
        self.ax.clabel(contour, inline=True, fontsize=8)
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        plt.colorbar(contour, ax=self.ax)
        
        return self.fig
    
    def surface_plot(self, X, Y, Z, title="3D Surface Plot", xlabel="X", ylabel="Y", zlabel="Z"):
        """Create 3D surface plot"""
        self.fig = plt.figure(figsize=self.figure_size)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        surf = self.ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_zlabel(zlabel)
        plt.colorbar(surf, ax=self.ax, shrink=0.5)
        
        return self.fig
    
    def function_plot(self, func, x_range, num_points=1000, title="Function Plot", 
                      xlabel="X", ylabel="Y", show_derivative=False):
        """Plot mathematical function"""
        x = np.linspace(x_range[0], x_range[1], num_points)
        y = func(x)
        
        self.fig, self.ax = plt.subplots(figsize=self.figure_size)
        
        self.ax.plot(x, y, 'b-', label='f(x)')
        
        if show_derivative:
            # Approximate derivative
            dy = np.gradient(y, x)
            self.ax.plot(x, dy, 'r--', label="f'(x)")
        
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)
        
        # Add zero line
        self.ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
        
        return self.fig
    
    def error_bar_plot(self, x_data, y_data, y_err=None, x_err=None, title="Error Bar Plot"):
        """Create plot with error bars"""
        self.fig, self.ax = plt.subplots(figsize=self.figure_size)
        
        self.ax.errorbar(x_data, y_data, yerr=y_err, xerr=x_err, 
                        fmt='o', capsize=5, capthick=2)
        self.ax.set_title(title)
        self.ax.grid(True, alpha=0.3)
        
        return self.fig
    
    def heatmap(self, data, title="Heatmap", xlabel="X", ylabel="Y"):
        """Create heatmap"""
        self.fig, self.ax = plt.subplots(figsize=self.figure_size)
        
        im = self.ax.imshow(data, cmap='hot', aspect='auto')
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        plt.colorbar(im, ax=self.ax)
        
        return self.fig
    
    def polar_plot(self, theta, r, title="Polar Plot"):
        """Create polar plot"""
        self.fig = plt.figure(figsize=self.figure_size)
        self.ax = self.fig.add_subplot(111, projection='polar')
        
        self.ax.plot(theta, r)
        self.ax.set_title(title)
        
        return self.fig
    
    def subplot_grid(self, plot_functions, grid_size=(2, 2)):
        """Create grid of subplots"""
        rows, cols = grid_size
        self.fig, axes = plt.subplots(rows, cols, figsize=(15, 10))
        axes = axes.flatten()
        
        for i, plot_func in enumerate(plot_functions):
            if i < len(axes):
                plot_func(axes[i])
        
        plt.tight_layout()
        return self.fig
    
    def save_plot(self, filename, dpi=300, bbox_inches='tight'):
        """Save plot to file"""
        if self.fig:
            self.fig.savefig(filename, dpi=dpi, bbox_inches=bbox_inches)
            print(f"Plot saved to {filename}")
    
    def show_plot(self):
        """Display plot"""
        plt.show()
    
    def clear_plot(self):
        """Clear current figure"""
        plt.close()
        self.fig = None
        self.ax = None