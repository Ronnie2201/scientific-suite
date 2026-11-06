"""
GUI interface using PyQt5 for the scientific suite.
Run with: python -m interface.gui
"""

import sys
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTextEdit, QTabWidget, QSplitter,
    QGroupBox, QLabel, QComboBox, QSpinBox, QDoubleSpinBox,
    QCheckBox, QGridLayout, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt

from core.equation_parser import EquationParser
from core.solvers.algebraic import AlgebraicSolver
from core.solvers.numerical import NumericalMethods
from visualization.plotter import Plotter
from visualization.graph_types import GraphTypes


class MplCanvas(FigureCanvas):
    """Matplotlib canvas embedded in a Qt widget."""

    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)


class ScientificGUI(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.parser = EquationParser()
        self.algebraic = AlgebraicSolver()
        self.numerical = NumericalMethods()
        self.plotter = Plotter()
        self.graphs = GraphTypes()

        self.setWindowTitle("Scientific Computing Suite")
        self.setGeometry(100, 100, 1300, 850)
        self._build_ui()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._build_input_panel())
        splitter.addWidget(self._build_visualization_panel())
        splitter.setSizes([420, 880])
        main_layout.addWidget(splitter)

    def _build_input_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        tabs = QTabWidget()
        tabs.addTab(self._build_solver_tab(), "Equation Solver")
        tabs.addTab(self._build_calculus_tab(), "Calculus")
        tabs.addTab(self._build_plotting_tab(), "Plotting")
        tabs.addTab(self._build_special_tab(), "Special Functions")
        layout.addWidget(tabs)

        output_group = QGroupBox("Output")
        out_layout = QVBoxLayout()
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        out_layout.addWidget(self.output_text)
        output_group.setLayout(out_layout)
        layout.addWidget(output_group)

        return panel

    def _build_solver_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        layout.addWidget(QLabel("Equation (use '=' for equations):"))
        self.equation_input = QLineEdit()
        self.equation_input.setPlaceholderText("e.g., x**2 - 4 = 0")
        layout.addWidget(self.equation_input)

        layout.addWidget(QLabel("Variable to solve for:"))
        self.variable_input = QLineEdit("x")
        layout.addWidget(self.variable_input)

        group = QGroupBox("Solver Options")
        gl = QVBoxLayout()

        self.solver_type = QComboBox()
        self.solver_type.addItems(["Symbolic", "Numerical", "Both"])
        gl.addWidget(QLabel("Solver Type:"))
        gl.addWidget(self.solver_type)

        self.numerical_method = QComboBox()
        self.numerical_method.addItems(["newton", "bisection"])
        gl.addWidget(QLabel("Numerical Method:"))
        gl.addWidget(self.numerical_method)

        group.setLayout(gl)
        layout.addWidget(group)

        btn = QPushButton("Solve")
        btn.clicked.connect(self.solve_equation)
        layout.addWidget(btn)
        layout.addStretch()
        return tab

    def _build_calculus_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        layout.addWidget(QLabel("Function f(x):"))
        self.calc_function_input = QLineEdit()
        self.calc_function_input.setPlaceholderText("e.g., sin(x) + x**2")
        layout.addWidget(self.calc_function_input)

        self.calc_operation = QComboBox()
        self.calc_operation.addItems(
            ["Integrate", "Differentiate", "Find Roots", "Taylor Series"]
        )
        layout.addWidget(self.calc_operation)

        group = QGroupBox("Parameters")
        grid = QGridLayout()

        grid.addWidget(QLabel("From:"), 0, 0)
        self.integral_from = QDoubleSpinBox()
        self.integral_from.setRange(-1e6, 1e6)
        self.integral_from.setValue(0)
        grid.addWidget(self.integral_from, 0, 1)

        grid.addWidget(QLabel("To:"), 1, 0)
        self.integral_to = QDoubleSpinBox()
        self.integral_to.setRange(-1e6, 1e6)
        self.integral_to.setValue(1)
        grid.addWidget(self.integral_to, 1, 1)

        grid.addWidget(QLabel("Derivative point x:"), 2, 0)
        self.derivative_point = QDoubleSpinBox()
        self.derivative_point.setRange(-1e6, 1e6)
        self.derivative_point.setValue(0)
        grid.addWidget(self.derivative_point, 2, 1)

        group.setLayout(grid)
        layout.addWidget(group)

        btn = QPushButton("Calculate")
        btn.clicked.connect(self.calculate_calculus)
        layout.addWidget(btn)
        layout.addStretch()
        return tab

    def _build_plotting_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        layout.addWidget(QLabel("Function(s) of x (comma-separated):"))
        self.plot_function_input = QLineEdit()
        self.plot_function_input.setPlaceholderText("e.g., sin(x), cos(x), x**2")
        layout.addWidget(self.plot_function_input)

        group = QGroupBox("Plot Range")
        grid = QGridLayout()

        grid.addWidget(QLabel("X min:"), 0, 0)
        self.x_min = QDoubleSpinBox()
        self.x_min.setRange(-1e6, 1e6)
        self.x_min.setValue(-10)
        grid.addWidget(self.x_min, 0, 1)

        grid.addWidget(QLabel("X max:"), 1, 0)
        self.x_max = QDoubleSpinBox()
        self.x_max.setRange(-1e6, 1e6)
        self.x_max.setValue(10)
        grid.addWidget(self.x_max, 1, 1)

        grid.addWidget(QLabel("Points:"), 2, 0)
        self.num_points = QSpinBox()
        self.num_points.setRange(10, 10000)
        self.num_points.setValue(1000)
        grid.addWidget(self.num_points, 2, 1)

        group.setLayout(grid)
        layout.addWidget(group)

        opts = QGroupBox("Plot Options")
        ol = QVBoxLayout()
        self.show_grid = QCheckBox("Show Grid")
        self.show_grid.setChecked(True)
        self.show_legend = QCheckBox("Show Legend")
        self.show_legend.setChecked(True)
        self.show_derivative = QCheckBox("Show Derivative")
        ol.addWidget(self.show_grid)
        ol.addWidget(self.show_legend)
        ol.addWidget(self.show_derivative)
        opts.setLayout(ol)
        layout.addWidget(opts)

        btn = QPushButton("Plot")
        btn.clicked.connect(self.plot_function)
        layout.addWidget(btn)
        layout.addStretch()
        return tab

    def _build_special_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.special_func_type = QComboBox()
        self.special_func_type.addItems(
            ["Quadratic", "Trigonometric", "Exponential", "Logarithmic"]
        )
        layout.addWidget(QLabel("Function Type:"))
        layout.addWidget(self.special_func_type)

        params = QGroupBox("Parameters (a, b, c)")
        grid = QGridLayout()

        for row, name, default in [(0, "a", 1.0), (1, "b", 0.0), (2, "c", 0.0)]:
            grid.addWidget(QLabel(f"{name}:"), row, 0)
            box = QDoubleSpinBox()
            box.setRange(-1e6, 1e6)
            box.setValue(default)
            box.setSingleStep(0.1)
            grid.addWidget(box, row, 1)
            setattr(self, f"special_{name}", box)

        params.setLayout(grid)
        layout.addWidget(params)

        btn = QPushButton("Plot Special Function")
        btn.clicked.connect(self.plot_special)
        layout.addWidget(btn)
        layout.addStretch()
        return tab

    def _build_visualization_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        layout.addWidget(self.canvas)
        layout.addWidget(NavigationToolbar(self.canvas, panel))

        btn_row = QHBoxLayout()
        clear_btn = QPushButton("Clear Plot")
        clear_btn.clicked.connect(self.clear_plot)
        btn_row.addWidget(clear_btn)

        save_btn = QPushButton("Save Plot")
        save_btn.clicked.connect(self.save_plot)
        btn_row.addWidget(save_btn)

        layout.addLayout(btn_row)
        return panel

    # --------------------------------------------------------------- Logic
    def _func_from_expr(self, expr):
        """Convert a sympy expression into a numpy-safe callable."""
        return lambda x_val: float(expr.subs('x', x_val))

    def solve_equation(self):
        equation = self.equation_input.text().strip()
        variable = self.variable_input.text().strip() or 'x'
        if not equation:
            return
        try:
            expr = self.parser.validate_equation(equation)
            mode = self.solver_type.currentText()

            if mode in ("Symbolic", "Both"):
                solutions = self.algebraic.solve_symbolic(expr, variable)
                self.output_text.append(f"[Symbolic] solutions: {solutions}")

            if mode in ("Numerical", "Both"):
                if expr.is_Equality:
                    f_expr = expr.lhs - expr.rhs
                else:
                    f_expr = expr
                # Free symbol may differ from variable name
                symbols = list(f_expr.free_symbols)
                if not symbols:
                    self.output_text.append("No variable found in equation.")
                    return
                free = symbols[0]
                func = lambda v: float(f_expr.subs(free, v))
                try:
                    root = self.numerical.find_roots(
                        func, (-10, 10), self.numerical_method.currentText()
                    )
                    self.output_text.append(f"[Numerical] root: {root}")
                except Exception as e:
                    self.output_text.append(f"[Numerical] failed: {e}")

            # Visualize the function
            if expr.is_Equality:
                f_expr = expr.lhs - expr.rhs
            else:
                f_expr = expr
            symbols = list(f_expr.free_symbols)
            if symbols:
                free = symbols[0]
                func = lambda v: float(f_expr.subs(free, v))
                xs = np.linspace(-10, 10, 800)
                ys = np.array([func(xi) for xi in xs], dtype=float)
                self.canvas.axes.clear()
                self.canvas.axes.plot(xs, ys, 'b-', label=f'f({free})')
                self.canvas.axes.axhline(0, color='k', linewidth=0.5)
                self.canvas.axes.axvline(0, color='k', linewidth=0.5)
                self.canvas.axes.grid(True, alpha=0.3)
                self.canvas.axes.legend()
                self.canvas.draw()
        except Exception as e:
            self.output_text.append(f"Error: {e}")

    def calculate_calculus(self):
        func_str = self.calc_function_input.text().strip()
        op = self.calc_operation.currentText()
        if not func_str:
            return
        try:
            expr = self.parser.parse_expression(func_str)
            func = self._func_from_expr(expr)

            if op == "Integrate":
                result, err = self.numerical.integrate_1d(
                    func, self.integral_from.value(), self.integral_to.value()
                )
                self.output_text.append(f"Integral ≈ {result:.10g}  (error ≈ {err:.2e})")

            elif op == "Differentiate":
                x = self.derivative_point.value()
                d = self.numerical.differentiate(func, x)
                self.output_text.append(f"f'({x}) ≈ {d:.10g}")

            elif op == "Find Roots":
                xs = np.linspace(self.integral_from.value(),
                                 self.integral_to.value(), 2000)
                ys = np.array([func(x) for x in xs])
                sign_changes = np.where(np.diff(np.signbit(ys)))[0]
                roots = []
                for i in sign_changes:
                    try:
                        r = self.numerical.find_roots(
                            func, (xs[i], xs[i+1]), 'bisection'
                        )
                        roots.append(round(r, 10))
                    except Exception:
                        pass
                self.output_text.append(f"Roots found: {roots or 'none'}")

            elif op == "Taylor Series":
                x0 = self.derivative_point.value()
                approx = self.numerical.taylor_series(func, x0, 5, None)
                self.output_text.append(
                    f"Taylor series around x={x0} with 5 terms generated."
                )
                xs = np.linspace(x0 - 2, x0 + 2, 500)
                ys = [approx(x) for x in xs]
                self.canvas.axes.clear()
                self.canvas.axes.plot(xs, ys, 'r-', label='Taylor approx')
                self.canvas.axes.plot(xs, [func(x) for x in xs], 'b--', label='f(x)')
                self.canvas.axes.legend()
                self.canvas.axes.grid(True, alpha=0.3)
                self.canvas.draw()
        except Exception as e:
            self.output_text.append(f"Error: {e}")

    def plot_function(self):
        funcs_str = self.plot_function_input.text().strip()
        if not funcs_str:
            return
        try:
            self.canvas.axes.clear()
            xs = np.linspace(self.x_min.value(),
                             self.x_max.value(),
                             self.num_points.value())

            func_strs = [s.strip() for s in funcs_str.split(',') if s.strip()]
            for s in func_strs:
                expr = self.parser.parse_expression(s)
                func = self._func_from_expr(expr)
                ys = np.array([func(x) for x in xs], dtype=float)
                self.canvas.axes.plot(xs, ys, label=s)

            if self.show_derivative.isChecked() and len(func_strs) == 1:
                expr = self.parser.parse_expression(func_strs[0])
                func = self._func_from_expr(expr)
                ys = np.array([func(x) for x in xs])
                dy = np.gradient(ys, xs)
                self.canvas.axes.plot(xs, dy, '--', label="derivative")

            if self.show_grid.isChecked():
                self.canvas.axes.grid(True, alpha=0.3)
            if self.show_legend.isChecked():
                self.canvas.axes.legend()

            self.canvas.axes.axhline(0, color='k', linewidth=0.5)
            self.canvas.axes.axvline(0, color='k', linewidth=0.5)
            self.canvas.axes.set_xlabel('x')
            self.canvas.axes.set_ylabel('y')
            self.canvas.draw()
        except Exception as e:
            self.output_text.append(f"Error: {e}")

    def plot_special(self):
        kind = self.special_func_type.currentText()
        a = self.special_a.value()
        b = self.special_b.value()
        c = self.special_c.value()
        try:
            self.canvas.axes.clear()
            if kind == "Quadratic":
                xs = np.linspace(-10, 10, 1000)
                ys = a * xs**2 + b * xs + c
                self.canvas.axes.plot(xs, ys, 'b-', label=f'{a}x²+{b}x+{c}')
                if a != 0:
                    vx = -b / (2 * a)
                    vy = a * vx**2 + b * vx + c
                    self.canvas.axes.plot(vx, vy, 'ro', label='vertex')

            elif kind == "Trigonometric":
                xs = np.linspace(0, 4 * np.pi, 1000)
                ys = a * np.sin(b * xs + c)
                self.canvas.axes.plot(xs, ys, 'b-',
                                      label=f'{a}·sin({b}x+{c})')

            elif kind == "Exponential":
                base = a if a not in (0,) else 2
                xs = np.linspace(-3, 3, 1000)
                ys = b * np.power(base, xs)
                self.canvas.axes.plot(xs, ys, 'b-',
                                      label=f'{b}·{base}^x')

            elif kind == "Logarithmic":
                base = a if a > 1 else 10
                coeff = b if b != 0 else 1
                xs = np.linspace(0.01, 10, 1000)
                ys = coeff * np.log(xs) / np.log(base)
                self.canvas.axes.plot(xs, ys, 'b-',
                                      label=f'{coeff}·log_{base}(x)')

            self.canvas.axes.grid(True, alpha=0.3)
            self.canvas.axes.legend()
            self.canvas.axes.axhline(0, color='k', linewidth=0.5)
            self.canvas.axes.axvline(0, color='k', linewidth=0.5)
            self.canvas.draw()
        except Exception as e:
            self.output_text.append(f"Error: {e}")

    def clear_plot(self):
        self.canvas.axes.clear()
        self.canvas.draw()
        self.output_text.clear()

    def save_plot(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Plot", "",
            "PNG (*.png);;PDF (*.pdf);;SVG (*.svg)"
        )
        if filename:
            self.canvas.fig.savefig(filename, dpi=300, bbox_inches='tight')
            self.output_text.append(f"Saved: {filename}")


def main():
    app = QApplication(sys.argv)
    win = ScientificGUI()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()