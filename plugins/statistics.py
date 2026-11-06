"""
Statistical analysis plugin
"""
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

class StatisticsPlugin:
    """Statistical analysis tools"""
    
    def __init__(self):
        self.data = None
        self.results = {}
        
    def load_data(self, data):
        """Load data for analysis"""
        if isinstance(data, pd.DataFrame):
            self.data = data
        else:
            self.data = pd.DataFrame(data)
        return self
    
    def descriptive_stats(self, columns=None):
        """Calculate descriptive statistics"""
        if columns:
            data = self.data[columns]
        else:
            data = self.data
            
        stats_dict = {
            'mean': data.mean(),
            'median': data.median(),
            'mode': data.mode().iloc[0] if not data.mode().empty else None,
            'std': data.std(),
            'var': data.var(),
            'min': data.min(),
            'max': data.max(),
            'range': data.max() - data.min(),
            'q1': data.quantile(0.25),
            'q3': data.quantile(0.75),
            'iqr': data.quantile(0.75) - data.quantile(0.25),
            'skewness': data.skew(),
            'kurtosis': data.kurtosis()
        }
        
        self.results['descriptive'] = stats_dict
        return stats_dict
    
    def correlation_analysis(self, method='pearson'):
        """Calculate correlation matrix"""
        if method == 'pearson':
            corr_matrix = self.data.corr()
        elif method == 'spearman':
            corr_matrix = self.data.corr(method='spearman')
        elif method == 'kendall':
            corr_matrix = self.data.corr(method='kendall')
        
        self.results['correlation'] = corr_matrix
        return corr_matrix
    
    def hypothesis_test(self, column, test_value=0, test_type='ttest_1samp'):
        """Perform hypothesis tests"""
        data = self.data[column].dropna()
        
        if test_type == 'ttest_1samp':
            t_stat, p_value = stats.ttest_1samp(data, test_value)
            result = {
                'test': 'One-sample t-test',
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        
        elif test_type == 'ttest_ind':
            # Assuming column contains two groups marked by 0/1
            group1 = data[data == 0]
            group2 = data[data == 1]
            t_stat, p_value = stats.ttest_ind(group1, group2)
            result = {
                'test': 'Independent t-test',
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        
        elif test_type == 'wilcoxon':
            stat, p_value = stats.wilcoxon(data - test_value)
            result = {
                'test': 'Wilcoxon signed-rank test',
                'statistic': stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        
        self.results['hypothesis_test'] = result
        return result
    
    def anova_oneway(self, groups_column, value_column):
        """One-way ANOVA"""
        groups = self.data[groups_column].unique()
        group_data = [self.data[self.data[groups_column] == g][value_column].dropna() 
                     for g in groups]
        
        f_stat, p_value = stats.f_oneway(*group_data)
        
        result = {
            'test': 'One-way ANOVA',
            'f_statistic': f_stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'groups': groups
        }
        
        self.results['anova'] = result
        return result
    
    def linear_regression(self, x_column, y_column):
        """Simple linear regression"""
        x = self.data[x_column].values
        y = self.data[y_column].values
        
        # Remove NaN
        mask = ~(np.isnan(x) | np.isnan(y))
        x = x[mask]
        y = y[mask]
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        result = {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_value**2,
            'p_value': p_value,
            'std_error': std_err,
            'equation': f'y = {slope:.4f}x + {intercept:.4f}'
        }
        
        # Calculate predictions
        result['predictions'] = slope * x + intercept
        result['residuals'] = y - result['predictions']
        
        self.results['regression'] = result
        return result
    
    def probability_distributions(self, dist_type='normal', params=None, n_points=1000):
        """Generate probability distributions"""
        if params is None:
            params = {}
        
        x = np.linspace(-5, 5, n_points)
        
        if dist_type == 'normal':
            mu = params.get('mean', 0)
            sigma = params.get('std', 1)
            y = stats.norm.pdf(x, mu, sigma)
            dist_name = f'Normal(μ={mu}, σ={sigma})'
            
        elif dist_type == 'uniform':
            low = params.get('low', 0)
            high = params.get('high', 1)
            y = stats.uniform.pdf(x, low, high - low)
            dist_name = f'Uniform({low}, {high})'
            
        elif dist_type == 'exponential':
            scale = params.get('scale', 1)
            x = np.linspace(0, 10, n_points)
            y = stats.expon.pdf(x, scale=scale)
            dist_name = f'Exponential(λ={1/scale:.2f})'
            
        elif dist_type == 'binomial':
            n = params.get('n', 10)
            p = params.get('p', 0.5)
            x = np.arange(0, n+1)
            y = stats.binom.pmf(x, n, p)
            dist_name = f'Binomial(n={n}, p={p})'
        
        return {'x': x, 'y': y, 'name': dist_name}
    
    def plot_distribution(self, dist_type='normal', params=None):
        """Plot probability distribution"""
        dist = self.probability_distributions(dist_type, params)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dist['x'], dist['y'], 'b-', linewidth=2)
        ax.fill_between(dist['x'], 0, dist['y'], alpha=0.3)
        ax.set_title(f'Probability Distribution: {dist["name"]}')
        ax.set_xlabel('x')
        ax.set_ylabel('Probability Density')
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def outlier_detection(self, column, method='iqr'):
        """Detect outliers in data"""
        data = self.data[column].dropna()
        
        if method == 'iqr':
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = data[(data < lower_bound) | (data > upper_bound)]
            
            result = {
                'method': 'IQR',
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'outliers': outliers.tolist(),
                'n_outliers': len(outliers),
                'outlier_indices': outliers.index.tolist()
            }
            
        elif method == 'zscore':
            z_scores = np.abs((data - data.mean()) / data.std())
            outliers = data[z_scores > 3]
            
            result = {
                'method': 'Z-score',
                'threshold': 3,
                'outliers': outliers.tolist(),
                'n_outliers': len(outliers),
                'outlier_indices': outliers.index.tolist(),
                'z_scores': z_scores[z_scores > 3].tolist()
            }
        
        self.results['outliers'] = result
        return result
    
    def summary_report(self):
        """Generate comprehensive statistical report"""
        report = []
        report.append("=" * 50)
        report.append("STATISTICAL ANALYSIS REPORT")
        report.append("=" * 50)
        
        # Descriptive statistics
        if 'descriptive' in self.results:
            report.append("\nDESCRIPTIVE STATISTICS:")
            report.append("-" * 30)
            desc = self.results['descriptive']
            for stat, values in desc.items():
                report.append(f"{stat.upper()}:")
                if isinstance(values, pd.Series):
                    for col, val in values.items():
                        report.append(f"  {col}: {val:.4f}")
                else:
                    report.append(f"  {values}")
        
        # Correlation
        if 'correlation' in self.results:
            report.append("\nCORRELATION MATRIX:")
            report.append("-" * 30)
            corr = self.results['correlation']
            report.append(str(corr))
        
        # Hypothesis test
        if 'hypothesis_test' in self.results:
            report.append("\nHYPOTHESIS TEST:")
            report.append("-" * 30)
            test = self.results['hypothesis_test']
            for key, value in test.items():
                report.append(f"{key}: {value}")
        
        # Regression
        if 'regression' in self.results:
            report.append("\nLINEAR REGRESSION:")
            report.append("-" * 30)
            reg = self.results['regression']
            report.append(f"Equation: {reg['equation']}")
            report.append(f"R²: {reg['r_squared']:.4f}")
            report.append(f"P-value: {reg['p_value']:.4f}")
        
        # Outliers
        if 'outliers' in self.results:
            report.append("\nOUTLIER DETECTION:")
            report.append("-" * 30)
            out = self.results['outliers']
            report.append(f"Method: {out['method']}")
            report.append(f"Number of outliers: {out['n_outliers']}")
            if out['n_outliers'] > 0:
                report.append(f"Outlier values: {out['outliers']}")
        
        return "\n".join(report)