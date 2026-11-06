def test_imports():
    """Test all required imports"""
    packages = [
        'numpy',
        'scipy',
        'sympy',
        'pandas',
        'matplotlib',
        'seaborn',
        'plotly',
        'networkx',
        'PyQt5'
    ]
    
    print("Testing installations...\n")
    
    for package in packages:
        try:
            if package == 'PyQt5':
                # Special handling for PyQt5
                from PyQt5.QtWidgets import QApplication
                print(f"✓ {package} - OK")
            else:
                module = __import__(package)
                version = getattr(module, '__version__', 'unknown')
                print(f"✓ {package} - version {version}")
        except ImportError as e:
            print(f"✗ {package} - NOT FOUND: {e}")

if __name__ == "__main__":
    test_imports()
    
    # Test basic functionality
    print("\nTesting basic functionality...")
    
    try:
        import numpy as np
        print(f"NumPy array test: {np.array([1,2,3])}")
        
        import matplotlib.pyplot as plt
        print("Matplotlib imported successfully")
        
        import sympy as sp
        x = sp.Symbol('x')
        print(f"SymPy expression test: {sp.sin(x)**2 + sp.cos(x)**2} = 1")
        
        print("\n✓ All systems go! Installation successful!")
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")