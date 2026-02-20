"""
ML Pipeline for training and prediction
"""
import pandas as pd
import numpy as np
import joblib
import os
from typing import Any, Dict, Optional
from backend.ml.preprocessing import MLPreprocessor
from backend.config import settings


class MLPipeline:
    """Generic ML pipeline for training and prediction"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.preprocessor = MLPreprocessor()
    
    def prepare_data(self, df: pd.DataFrame, target_col: str, 
                     exclude_cols: Optional[list] = None) -> tuple:
        """Prepare data for training"""
        # Handle missing values
        df_clean = self.preprocessor.handle_missing_values(df, strategy='mean')
        
        # Select features and target
        X, y = self.preprocessor.select_features(df_clean, target_col, exclude_cols)
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        return X, y
    
    def train(self, X_train, y_train, model, scale: bool = True) -> Dict[str, Any]:
        """Train model"""
        # Scale features if requested
        if scale:
            scaler = self.preprocessor.standardize.__func__(X_train, X_train)[2]
            X_train_scaled = scaler.transform(X_train)
            self.scaler = scaler
        else:
            X_train_scaled = X_train
        
        # Train model
        model.fit(X_train_scaled, y_train)
        self.model = model
        
        return {"status": "success", "message": "Model trained successfully"}
    
    def predict(self, X) -> np.ndarray:
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        # Scale if scaler exists
        if self.scaler is not None:
            X_scaled = self.scaler.transform(X)
        else:
            X_scaled = X
        
        predictions = self.model.predict(X_scaled)
        return predictions
    
    def evaluate(self, X_test, y_test) -> Dict[str, float]:
        """Evaluate model performance"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        # Scale if needed
        if self.scaler is not None:
            X_test_scaled = self.scaler.transform(X_test)
        else:
            X_test_scaled = X_test
        
        # Get score
        score = self.model.score(X_test_scaled, y_test)
        
        # Get predictions for additional metrics
        y_pred = self.model.predict(X_test_scaled)
        
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        
        metrics = {
            "score": float(score),
            "r2_score": float(r2_score(y_test, y_pred))
        }
        
        # For regression tasks
        try:
            metrics["mse"] = float(mean_squared_error(y_test, y_pred))
            metrics["rmse"] = float(np.sqrt(metrics["mse"]))
            metrics["mae"] = float(mean_absolute_error(y_test, y_pred))
        except:
            pass
        
        return metrics
    
    def save_model(self, filename: Optional[str] = None) -> str:
        """Save model to disk"""
        if self.model is None:
            raise ValueError("No model to save")
        
        if filename is None:
            filename = f"{self.model_name}.pkl"
        
        filepath = os.path.join(settings.MODEL_PATH, filename)
        
        # Save model and scaler
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'model_name': self.model_name
        }
        
        joblib.dump(model_data, filepath)
        
        return filepath
    
    def load_model(self, filename: str):
        """Load model from disk"""
        filepath = os.path.join(settings.MODEL_PATH, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.scaler = model_data.get('scaler')
        self.feature_names = model_data.get('feature_names')
        self.model_name = model_data.get('model_name', self.model_name)
        
        return self
