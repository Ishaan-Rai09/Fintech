"""
Data management service
"""
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
import io
import json


class DataService:
    """Service for data ingestion, cleaning, and transformation"""
    
    @staticmethod
    def load_csv(file_content: bytes, **kwargs) -> pd.DataFrame:
        """Load CSV file into DataFrame"""
        try:
            df = pd.read_csv(io.BytesIO(file_content), **kwargs)
            return df
        except Exception as e:
            raise ValueError(f"Error loading CSV: {str(e)}")
    
    @staticmethod
    def load_excel(file_content: bytes, **kwargs) -> pd.DataFrame:
        """Load Excel file into DataFrame"""
        try:
            df = pd.read_excel(io.BytesIO(file_content), **kwargs)
            return df
        except Exception as e:
            raise ValueError(f"Error loading Excel: {str(e)}")
    
    @staticmethod
    def load_json(file_content: bytes) -> pd.DataFrame:
        """Load JSON file into DataFrame"""
        try:
            data = json.loads(file_content.decode('utf-8'))
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            raise ValueError(f"Error loading JSON: {str(e)}")
    
    @staticmethod
    def clean_data(df: pd.DataFrame, operations: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Clean and preprocess data
        
        Operations:
        - remove_duplicates: bool
        - handle_missing: 'drop', 'fill_mean', 'fill_median', 'fill_zero'
        - normalize: bool
        - remove_outliers: bool (uses IQR method)
        """
        df_clean = df.copy()
        
        if operations is None:
            operations = {}
        
        # Remove duplicates
        if operations.get('remove_duplicates', False):
            df_clean = df_clean.drop_duplicates()
        
        # Handle missing values
        missing_strategy = operations.get('handle_missing', None)
        if missing_strategy == 'drop':
            df_clean = df_clean.dropna()
        elif missing_strategy == 'fill_mean':
            df_clean = df_clean.fillna(df_clean.mean(numeric_only=True))
        elif missing_strategy == 'fill_median':
            df_clean = df_clean.fillna(df_clean.median(numeric_only=True))
        elif missing_strategy == 'fill_zero':
            df_clean = df_clean.fillna(0)
        
        # Remove outliers using IQR method
        if operations.get('remove_outliers', False):
            numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
        
        # Normalize numeric columns
        if operations.get('normalize', False):
            numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                min_val = df_clean[col].min()
                max_val = df_clean[col].max()
                if max_val > min_val:
                    df_clean[col] = (df_clean[col] - min_val) / (max_val - min_val)
        
        return df_clean
    
    @staticmethod
    def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary statistics of DataFrame"""
        summary = {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "numeric_summary": df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {},
            "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
        }
        return summary
    
    @staticmethod
    def validate_data(df: pd.DataFrame, rules: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data against rules
        
        Rules format:
        {
            "column_name": {
                "type": "numeric" | "string" | "date",
                "required": bool,
                "min": value,
                "max": value,
                "allowed_values": [...]
            }
        }
        """
        validation_results = {
            "valid": True,
            "errors": []
        }
        
        for col, rule in rules.items():
            if col not in df.columns:
                if rule.get('required', False):
                    validation_results["valid"] = False
                    validation_results["errors"].append(f"Required column '{col}' missing")
                continue
            
            # Type validation
            if rule.get('type') == 'numeric':
                if not pd.api.types.is_numeric_dtype(df[col]):
                    validation_results["valid"] = False
                    validation_results["errors"].append(f"Column '{col}' should be numeric")
            
            # Min/Max validation
            if 'min' in rule and pd.api.types.is_numeric_dtype(df[col]):
                if (df[col] < rule['min']).any():
                    validation_results["valid"] = False
                    validation_results["errors"].append(f"Column '{col}' has values below minimum {rule['min']}")
            
            if 'max' in rule and pd.api.types.is_numeric_dtype(df[col]):
                if (df[col] > rule['max']).any():
                    validation_results["valid"] = False
                    validation_results["errors"].append(f"Column '{col}' has values above maximum {rule['max']}")
            
            # Allowed values validation
            if 'allowed_values' in rule:
                invalid_values = ~df[col].isin(rule['allowed_values'])
                if invalid_values.any():
                    validation_results["valid"] = False
                    validation_results["errors"].append(f"Column '{col}' has invalid values")
        
        return validation_results
