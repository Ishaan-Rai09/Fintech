"""
ML Models implementation
"""
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier
import numpy as np
from typing import Dict, Any


class LinearRegressionModel:
    """Linear Regression model wrapper"""
    
    @staticmethod
    def create(fit_intercept: bool = True):
        """Create Linear Regression model"""
        return LinearRegression(fit_intercept=fit_intercept)
    
    @staticmethod
    def create_polynomial(degree: int = 2):
        """Create Polynomial Regression model"""
        from sklearn.preprocessing import PolynomialFeatures
        from sklearn.pipeline import Pipeline
        
        model = Pipeline([
            ('poly', PolynomialFeatures(degree=degree)),
            ('linear', LinearRegression())
        ])
        return model


class RandomForestModel:
    """Random Forest model wrapper"""
    
    @staticmethod
    def create_regressor(n_estimators: int = 100, max_depth: int = None, 
                        random_state: int = 42):
        """Create Random Forest Regressor"""
        return RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )
    
    @staticmethod
    def create_classifier(n_estimators: int = 100, max_depth: int = None,
                         random_state: int = 42):
        """Create Random Forest Classifier"""
        return RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )


class XGBoostModel:
    """XGBoost model wrapper"""
    
    @staticmethod
    def create_regressor(n_estimators: int = 100, learning_rate: float = 0.1,
                        max_depth: int = 6, random_state: int = 42):
        """Create XGBoost Regressor"""
        return XGBRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )
    
    @staticmethod
    def create_classifier(n_estimators: int = 100, learning_rate: float = 0.1,
                         max_depth: int = 6, random_state: int = 42):
        """Create XGBoost Classifier"""
        return XGBClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )


class LogisticRegressionModel:
    """Logistic Regression model wrapper"""
    
    @staticmethod
    def create(max_iter: int = 1000, random_state: int = 42):
        """Create Logistic Regression model"""
        return LogisticRegression(
            max_iter=max_iter,
            random_state=random_state
        )


def get_model(model_type: str, task: str = 'regression', **kwargs):
    """
    Factory function to get model by type
    
    Args:
        model_type: 'linear', 'random_forest', 'xgboost', 'logistic'
        task: 'regression' or 'classification'
        **kwargs: Additional model parameters
    """
    if model_type == 'linear':
        if task == 'regression':
            return LinearRegressionModel.create(**kwargs)
        else:
            return LogisticRegressionModel.create(**kwargs)
    
    elif model_type == 'random_forest':
        if task == 'regression':
            return RandomForestModel.create_regressor(**kwargs)
        else:
            return RandomForestModel.create_classifier(**kwargs)
    
    elif model_type == 'xgboost':
        if task == 'regression':
            return XGBoostModel.create_regressor(**kwargs)
        else:
            return XGBoostModel.create_classifier(**kwargs)
    
    elif model_type == 'logistic':
        return LogisticRegressionModel.create(**kwargs)
    
    elif model_type == 'polynomial':
        degree = kwargs.get('degree', 2)
        return LinearRegressionModel.create_polynomial(degree=degree)
    
    else:
        raise ValueError(f"Unknown model type: {model_type}")
