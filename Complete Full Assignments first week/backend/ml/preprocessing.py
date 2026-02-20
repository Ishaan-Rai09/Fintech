"""
ML preprocessing utilities
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from typing import Tuple, List, Optional


class MLPreprocessor:
    """Preprocessing utilities for ML pipelines"""
    
    @staticmethod
    def split_data(X, y, test_size: float = 0.2, random_state: int = 42) -> Tuple:
        """Split data into train and test sets"""
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    @staticmethod
    def standardize(X_train, X_test):
        """Standardize features (mean=0, std=1)"""
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled, scaler
    
    @staticmethod
    def normalize(X_train, X_test, feature_range=(0, 1)):
        """Normalize features to a range"""
        scaler = MinMaxScaler(feature_range=feature_range)
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled, scaler
    
    @staticmethod
    def encode_labels(y_train, y_test):
        """Encode categorical labels to integers"""
        encoder = LabelEncoder()
        y_train_encoded = encoder.fit_transform(y_train)
        y_test_encoded = encoder.transform(y_test)
        return y_train_encoded, y_test_encoded, encoder
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, strategy: str = 'mean'):
        """Handle missing values in DataFrame"""
        df_clean = df.copy()
        
        if strategy == 'mean':
            df_clean = df_clean.fillna(df_clean.mean(numeric_only=True))
        elif strategy == 'median':
            df_clean = df_clean.fillna(df_clean.median(numeric_only=True))
        elif strategy == 'mode':
            for col in df_clean.columns:
                if df_clean[col].isnull().any():
                    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0] if not df_clean[col].mode().empty else 0)
        elif strategy == 'drop':
            df_clean = df_clean.dropna()
        
        return df_clean
    
    @staticmethod
    def select_features(df: pd.DataFrame, target_col: str, 
                       exclude_cols: Optional[List[str]] = None) -> Tuple[pd.DataFrame, pd.Series]:
        """Select features and target from DataFrame"""
        if exclude_cols is None:
            exclude_cols = []
        
        # Get feature columns (exclude target and specified columns)
        feature_cols = [col for col in df.columns 
                       if col != target_col and col not in exclude_cols]
        
        # Select only numeric features
        X = df[feature_cols].select_dtypes(include=[np.number])
        y = df[target_col]
        
        return X, y
