"""
Data management and I/O operations
"""
import json
import csv
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
import datetime

class DataManager:
    def __init__(self, working_dir="."):
        self.working_dir = Path(working_dir)
        self.current_data = {}
        self.history = []
        
    def load_data(self, filename, format='auto'):
        """Load data from various formats"""
        filepath = self.working_dir / filename
        
        if format == 'auto':
            ext = filepath.suffix.lower()
            if ext == '.csv':
                return self.load_csv(filepath)
            elif ext == '.json':
                return self.load_json(filepath)
            elif ext == '.npy':
                return self.load_numpy(filepath)
            elif ext == '.pkl':
                return self.load_pickle(filepath)
            elif ext == '.xlsx':
                return self.load_excel(filepath)
            else:
                return self.load_text(filepath)
    
    def load_csv(self, filepath, **kwargs):
        """Load CSV file"""
        return pd.read_csv(filepath, **kwargs)
    
    def load_json(self, filepath):
        """Load JSON file"""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def load_numpy(self, filepath):
        """Load NumPy array"""
        return np.load(filepath)
    
    def load_pickle(self, filepath):
        """Load pickle file"""
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    
    def load_excel(self, filepath, sheet_name=0):
        """Load Excel file"""
        return pd.read_excel(filepath, sheet_name=sheet_name)
    
    def load_text(self, filepath):
        """Load text file"""
        with open(filepath, 'r') as f:
            return f.read()
    
    def save_data(self, data, filename, format='auto'):
        """Save data to file"""
        filepath = self.working_dir / filename
        
        if format == 'auto':
            ext = filepath.suffix.lower()
            if ext == '.csv':
                self.save_csv(data, filepath)
            elif ext == '.json':
                self.save_json(data, filepath)
            elif ext == '.npy':
                self.save_numpy(data, filepath)
            elif ext == '.pkl':
                self.save_pickle(data, filepath)
    
    def save_csv(self, data, filepath):
        """Save to CSV"""
        if isinstance(data, pd.DataFrame):
            data.to_csv(filepath, index=False)
        elif isinstance(data, np.ndarray):
            pd.DataFrame(data).to_csv(filepath, index=False)
    
    def save_json(self, data, filepath):
        """Save to JSON"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    
    def save_numpy(self, data, filepath):
        """Save NumPy array"""
        np.save(filepath, data)
    
    def save_pickle(self, data, filepath):
        """Save to pickle"""
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    
    def create_dataset(self, func, x_range, num_points=100):
        """Create dataset from function"""
        x = np.linspace(x_range[0], x_range[1], num_points)
        y = func(x)
        return pd.DataFrame({'x': x, 'y': y})
    
    def add_to_history(self, operation, data_reference):
        """Record operation in history"""
        self.history.append({
            'timestamp': datetime.datetime.now(),
            'operation': operation,
            'data_ref': data_reference
        })
    
    def export_session(self, filename):
        """Export entire session"""
        session = {
            'current_data': self.current_data,
            'history': self.history
        }
        self.save_pickle(session, filename)
    
    def import_session(self, filename):
        """Import previous session"""
        session = self.load_pickle(filename)
        self.current_data = session['current_data']
        self.history = session['history']