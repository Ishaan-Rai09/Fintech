"""
ML API endpoints
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.middleware.auth_middleware import get_current_user
from backend.models.user import User
from backend.schemas.auth import APIResponse
from backend.services.data_service import DataService
from backend.ml.pipeline import MLPipeline
from backend.ml.models import get_model
from backend.ml.preprocessing import MLPreprocessor
import json

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

data_service = DataService()


@router.post("/train", response_model=APIResponse)
async def train_model(
    file: UploadFile = File(...),
    model_type: str = "linear",
    task: str = "regression",
    target_column: str = "target",
    model_name: str = "custom_model",
    test_size: float = 0.2,
    current_user: User = Depends(get_current_user)
):
    """
    Train a machine learning model
    
    Supported models: linear, random_forest, xgboost, logistic, polynomial
    Tasks: regression, classification
    """
    try:
        # Load data
        content = await file.read()
        df = data_service.load_csv(content)
        
        if target_column not in df.columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Target column '{target_column}' not found in data"
            )
        
        # Create pipeline
        pipeline = MLPipeline(model_name=model_name)
        
        # Prepare data
        X, y = pipeline.prepare_data(df, target_col=target_column)
        
        # Split data
        preprocessor = MLPreprocessor()
        X_train, X_test, y_train, y_test = preprocessor.split_data(X, y, test_size=test_size)
        
        # Get model
        model = get_model(model_type, task=task)
        
        # Train
        pipeline.train(X_train, y_train, model, scale=True)
        
        # Evaluate
        metrics = pipeline.evaluate(X_test, y_test)
        
        # Save model
        saved_path = pipeline.save_model(f"{model_name}_{model_type}.pkl")
        
        return APIResponse(
            status="success",
            message="Model trained successfully",
            data={
                "model_type": model_type,
                "task": task,
                "features": pipeline.feature_names,
                "metrics": metrics,
                "saved_path": saved_path
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error training model: {str(e)}"
        )


@router.post("/predict", response_model=APIResponse)
async def predict(
    file: UploadFile = File(...),
    model_filename: str = "custom_model_linear.pkl",
    current_user: User = Depends(get_current_user)
):
    """
    Make predictions using a trained model
    """
    try:
        # Load data
        content = await file.read()
        df = data_service.load_csv(content)
        
        # Load model
        pipeline = MLPipeline(model_name="loaded_model")
        pipeline.load_model(model_filename)
        
        # Ensure features match
        if pipeline.feature_names:
            missing_features = [f for f in pipeline.feature_names if f not in df.columns]
            if missing_features:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing features: {missing_features}"
                )
            X = df[pipeline.feature_names]
        else:
            X = df.select_dtypes(include=['number'])
        
        # Predict
        predictions = pipeline.predict(X)
        
        return APIResponse(
            status="success",
            message="Predictions generated",
            data={
                "predictions": predictions.tolist()[:100],  # Limit to 100
                "count": len(predictions),
                "model": model_filename
            }
        )
    
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error making predictions: {str(e)}"
        )


@router.get("/models", response_model=APIResponse)
async def list_models(current_user: User = Depends(get_current_user)):
    """
    List available trained models
    """
    import os
    from backend.config import settings
    
    try:
        model_files = [f for f in os.listdir(settings.MODEL_PATH) if f.endswith('.pkl')]
        
        return APIResponse(
            status="success",
            message=f"Found {len(model_files)} models",
            data={"models": model_files}
        )
    except Exception as e:
        return APIResponse(
            status="success",
            message="No models found",
            data={"models": []}
        )


@router.get("/metrics/{model_filename}", response_model=APIResponse)
async def get_model_metrics(
    model_filename: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get metrics for a trained model
    """
    try:
        pipeline = MLPipeline(model_name="loaded_model")
        pipeline.load_model(model_filename)
        
        return APIResponse(
            status="success",
            message="Model info retrieved",
            data={
                "model_name": pipeline.model_name,
                "features": pipeline.feature_names,
                "has_scaler": pipeline.scaler is not None
            }
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model '{model_filename}' not found"
        )
