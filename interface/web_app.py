"""
Flask web interface for the Scientific Computing Suite.

Run with:
    python -m interface.web_app

Then open http://localhost:5000 in your browser.

Endpoints (JSON API):
    POST /api/solve       -> { equation, variable, mode }
    POST /api/integrate   -> { expression, a, b }
    POST /api/differentiate -> { expression, x }
    POST /api/plot        -> { expression, xmin, xmax, points }
    POST /api/quadratic   -> { a, b, c }
"""

import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')          # <-- critical for headless/server
import matplotlib.pyplot as plt

from flask import Flask, request, jsonify, render_template_string

from core.equation_parser import EquationParser
from core.solvers.algebraic import AlgebraicSolver
from core.solvers.numerical import NumericalMethods


app = Flask(__name__)
parser = EquationParser()
algebraic = AlgebraicSolver()
numerical = NumericalMethods()


# ------------------------------------------------------------------ helpers
def _fig_to_base64(fig):
    """Serialize a matplotlib figure to a base64 PNG string."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=110, bbox_inches='tight')
    buf.seek(0)
    encoded = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return encoded


def _safe_eval_expression(expr_str):
    """Parse expression string into a callable of x."""
    expr = parser.parse_expression(expr_str)
    if expr.free_symbols and 'x' not in [str(s) for s in expr.free_symbols]:
        raise ValueError("Expression must contain 'x' as variable.")
    return expr, (lambda x_val: float(expr.subs('x', x_val)))


# ------------------------------------------------------------------ landing
INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Scientific Computing Suite</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 900px;
         margin: 40px auto; padding: 0 20px; background: #f7f8fa; }
  h1 { color: #2c3e50; }
  section { background: white; padding: 18px 22px; margin-bottom: 18px;
            border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,.08); }
  input, select, button { font-size: 14px; padding: 6px 10px; margin: 4px 0; }
  input[type=text] { width: 340px; }
  button { cursor: pointer; background: #2563eb; color: white;
           border: none; border-radius: 4px; }
  button:hover { background: #1d4ed8; }
  pre { background: #f1f5f9; padding: 10px; border-radius: 4px;
        overflow-x: auto; }
  img { max-width: 100%; margin-top: 12px; border-radius: 6px; }
  label { display: inline-block; min-width: 130px; }
</style>
</head>
<body>
<h1>🧮 Scientific Computing Suite</h1>

<section>
  <h2>Solve Equation</h2>
  <label>Equation:</label>
  <input type="text" id="eq" value="x**2 - 4 = 0"><br>
  <label>Variable:</label>
  <input type="text" id="var" value="x" size="4"><br>
  <label>Mode:</label>
  <select id="mode">
    <option value="symbolic">Symbolic</option>
    <option value="numerical">Numerical</option>
    <option value="both">Both</option>
  </select><br>
  <button onclick="solveEq()">Solve</button>
  <pre id="solveResult"></pre>
</section>

<section>
  <h2>Integrate f(x)</h2>
  <label>f(x) =</label>
  <input type="text" id="integrand" value="sin(x)"><br>
  <label>From a =</label>
  <input type="text" id="ia" value="0" size="8">
  <label>To b =</label>
  <input type="text" id="ib" value="3.14159" size="8"><br>
  <button onclick="integrate()">Integrate</button>
  <pre id="intResult"></pre>
</section>

<section>
  <h2>Plot f(x)</h2>
  <label>f(x) =</label>
  <input type="text" id="plotExpr" value="sin(x)"><br>
  <label>xmin:</label>
  <input type="text" id="xmin" value="-6.28" size="8">
  <label>xmax:</label>
  <input type="text" id="xmax" value="6.28" size="8"><br>
  <button onclick="plotFn()">Plot</button>
  <div id="plotResult"></div>
</section>

<section>
  <h2>Quadratic ax² + bx + c</h2>
  <label>a:</label><input type="text" id="qa" value="1" size="6">
  <label>b:</label><input type="text" id="qb" value="0" size="6">
  <label>c:</label><input type="text" id="qc" value="-4" size="6"><br>
  <button onclick="plotQuad()">Plot Quadratic</button>
  <div id="quadResult"></div>
</section>

<script>
async function postJSON(url, body) {
  const r = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body)
  });
  return r.json();
}

async function solveEq() {
  const body = {
    equation: document.getElementById('eq').value,
    variable: document.getElementById('var').value,
    mode: document.getElementById('mode').value
  };
  const res = await postJSON('/api/solve', body);
  document.getElementById('solveResult').textContent =
    JSON.stringify(res, null, 2);
}

async function integrate() {
  const body = {
    expression: document.getElementById('integrand').value,
    a: parseFloat(document.getElementById('ia').value),
    b: parseFloat(document.getElementById('ib').value)
  };
  const res = await postJSON('/api/integrate', body);
  document.getElementById('intResult').textContent =
    JSON.stringify(res, null, 2);
}

async function plotFn() {
  const body = {
    expression: document.getElementById('plotExpr').value,
    xmin: parseFloat(document.getElementById('xmin').value),
    xmax: parseFloat(document.getElementById('xmax').value),
    points: 800
  };
  const res = await postJSON('/api/plot', body);
  if (res.image) {
    document.getElementById('plotResult').innerHTML =
      `<img src="data:image/png;base64,${res.image}">`;
  } else {
    document.getElementById('plotResult').textContent =
      JSON.stringify(res);
  }
}

async function plotQuad() {
  const body = {
    a: parseFloat(document.getElementById('qa').value),
    b: parseFloat(document.getElementById('qb').value),
    c: parseFloat(document.getElementById('qc').value)
  };
  const res = await postJSON('/api/quadratic', body);
  if (res.image) {
    document.getElementById('quadResult').innerHTML =
      `<img src="data:image/png;base64,${res.image}">`;
  } else {
    document.getElementById('quadResult').textContent =
      JSON.stringify(res);
  }
}
</script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(INDEX_HTML)


# ------------------------------------------------------------------ API
@app.route('/api/solve', methods=['POST'])
def api_solve():
    data = request.get_json(force=True)
    equation = data.get('equation', '').strip()
    variable = data.get('variable', 'x').strip() or 'x'
    mode = data.get('mode', 'symbolic')

    if not equation:
        return jsonify({'error': 'No equation provided'}), 400

    try:
        expr = parser.validate_equation(equation)
        result = {}

        if mode in ('symbolic', 'both'):
            sols = algebraic.solve_symbolic(expr, variable)
            result['symbolic'] = [str(s) for s in sols] if sols else []

        if mode in ('numerical', 'both'):
            f_expr = expr.lhs - expr.rhs if expr.is_Equality else expr
            syms = list(f_expr.free_symbols)
            if syms:
                free = syms[0]
                func = lambda v: float(f_expr.subs(free, v))
                try:
                    root = numerical.find_roots(func, (-50, 50), 'newton')
                    result['numerical'] = float(root)
                except Exception as e:
                    result['numerical_error'] = str(e)

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/integrate', methods=['POST'])
def api_integrate():
    data = request.get_json(force=True)
    expr_str = data.get('expression', '').strip()
    a = float(data.get('a', 0))
    b = float(data.get('b', 1))

    try:
        expr, func = _safe_eval_expression(expr_str)
        integration_result = numerical.integrate_1d(func, a, b)
        if integration_result is None:
          raise ValueError('Integration did not return a result.')
        try:
          value, err = integration_result
        except (TypeError, ValueError) as e:
          raise ValueError('Integration must return a (value, error) pair.') from e
        return jsonify({
            'expression': expr_str,
            'from': a, 'to': b,
            'value': value,
            'estimated_error': err
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/differentiate', methods=['POST'])
def api_differentiate():
    data = request.get_json(force=True)
    expr_str = data.get('expression', '').strip()
    x = float(data.get('x', 0))
    try:
        _, func = _safe_eval_expression(expr_str)
        d = numerical.differentiate(func, x)
        return jsonify({'expression': expr_str, 'x': x, 'derivative': d})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/plot', methods=['POST'])
def api_plot():
    data = request.get_json(force=True)
    expr_str = data.get('expression', '').strip()
    xmin = float(data.get('xmin', -10))
    xmax = float(data.get('xmax', 10))
    points = int(data.get('points', 800))

    try:
        expr, func = _safe_eval_expression(expr_str)
        xs = np.linspace(xmin, xmax, points)
        ys = np.array([func(x) for x in xs], dtype=float)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.plot(xs, ys, 'b-', label=f'f(x) = {expr_str}')
        ax.axhline(0, color='k', linewidth=0.5)
        ax.axvline(0, color='k', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend()

        return jsonify({'image': _fig_to_base64(fig)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/quadratic', methods=['POST'])
def api_quadratic():
    data = request.get_json(force=True)
    a = float(data.get('a', 1))
    b = float(data.get('b', 0))
    c = float(data.get('c', 0))

    try:
        xs = np.linspace(-10, 10, 800)
        ys = a * xs**2 + b * xs + c

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.plot(xs, ys, 'b-', label=f'{a}x² + {b}x + {c}')
        if a != 0:
            vx = -b / (2 * a)
            vy = a * vx**2 + b * vx + c
            ax.plot(vx, vy, 'ro', label=f'vertex ({vx:.2f}, {vy:.2f})')
        ax.axhline(0, color='k', linewidth=0.5)
        ax.axvline(0, color='k', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend()

        return jsonify({'image': _fig_to_base64(fig)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


def main():
    # host='0.0.0.0' is essential inside a container
    app.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == '__main__':
    main()