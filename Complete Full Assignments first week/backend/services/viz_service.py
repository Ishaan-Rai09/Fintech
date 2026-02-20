"""
Visualization service
"""
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import io
import base64
from typing import Optional, List


class VisualizationService:
    """Service for data visualization"""
    
    def __init__(self):
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['figure.dpi'] = 100
    
    @staticmethod
    def _fig_to_base64(fig) -> str:
        """Convert matplotlib figure to base64 string"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return img_base64
    
    def line_chart(self, df: pd.DataFrame, x_col: str, y_cols: List[str], title: str = "Line Chart") -> str:
        """Create line chart"""
        fig, ax = plt.subplots()
        
        for y_col in y_cols:
            ax.plot(df[x_col], df[y_col], marker='o', label=y_col)
        
        ax.set_xlabel(x_col)
        ax.set_ylabel('Value')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return self._fig_to_base64(fig)
    
    def bar_chart(self, df: pd.DataFrame, x_col: str, y_col: str, title: str = "Bar Chart") -> str:
        """Create bar chart"""
        fig, ax = plt.subplots()
        
        ax.bar(df[x_col], df[y_col], color='steelblue')
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(title)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Rotate x labels if many categories
        if len(df) > 10:
            plt.xticks(rotation=45, ha='right')
        
        return self._fig_to_base64(fig)
    
    def histogram(self, df: pd.DataFrame, col: str, bins: int = 30, title: str = "Histogram") -> str:
        """Create histogram"""
        fig, ax = plt.subplots()
        
        ax.hist(df[col].dropna(), bins=bins, color='steelblue', edgecolor='black', alpha=0.7)
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
        ax.set_title(title)
        ax.grid(True, alpha=0.3, axis='y')
        
        return self._fig_to_base64(fig)
    
    def correlation_matrix(self, df: pd.DataFrame, title: str = "Correlation Matrix") -> str:
        """Create correlation heatmap"""
        # Select numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            raise ValueError("No numeric columns found for correlation")
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        corr = numeric_df.corr()
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
        
        ax.set_title(title)
        
        return self._fig_to_base64(fig)
    
    def scatter_plot(self, df: pd.DataFrame, x_col: str, y_col: str, 
                     hue_col: Optional[str] = None, title: str = "Scatter Plot") -> str:
        """Create scatter plot"""
        fig, ax = plt.subplots()
        
        if hue_col and hue_col in df.columns:
            for category in df[hue_col].unique():
                mask = df[hue_col] == category
                ax.scatter(df.loc[mask, x_col], df.loc[mask, y_col], label=category, alpha=0.6)
            ax.legend()
        else:
            ax.scatter(df[x_col], df[y_col], alpha=0.6, color='steelblue')
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        return self._fig_to_base64(fig)
    
    def time_series_plot(self, df: pd.DataFrame, date_col: str, value_cols: List[str],
                         title: str = "Time Series") -> str:
        """Create time series plot"""
        fig, ax = plt.subplots()
        
        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
            df[date_col] = pd.to_datetime(df[date_col])
        
        df_sorted = df.sort_values(date_col)
        
        for col in value_cols:
            ax.plot(df_sorted[date_col], df_sorted[col], marker='o', label=col)
        
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        
        return self._fig_to_base64(fig)
    
    def box_plot(self, df: pd.DataFrame, columns: List[str], title: str = "Box Plot") -> str:
        """Create box plot"""
        fig, ax = plt.subplots()
        
        data = [df[col].dropna() for col in columns]
        ax.boxplot(data, labels=columns)
        
        ax.set_ylabel('Value')
        ax.set_title(title)
        ax.grid(True, alpha=0.3, axis='y')
        
        if len(columns) > 5:
            plt.xticks(rotation=45, ha='right')
        
        return self._fig_to_base64(fig)
