"""
Data API endpoints
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.middleware.auth_middleware import get_current_user
from backend.models.user import User
from backend.schemas.auth import APIResponse
from backend.services.data_service import DataService
import json

router = APIRouter(prefix="/data", tags=["Data Management"])

data_service = DataService()


@router.post("/upload", response_model=APIResponse)
async def upload_data(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload and process CSV/Excel/JSON data file
    """
    try:
        content = await file.read()
        
        # Determine file type and load
        if file.filename.endswith('.csv'):
            df = data_service.load_csv(content)
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = data_service.load_excel(content)
        elif file.filename.endswith('.json'):
            df = data_service.load_json(content)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format. Use CSV, Excel, or JSON"
            )
        
        # Get summary
        summary = data_service.get_data_summary(df)
        
        return APIResponse(
            status="success",
            message=f"File uploaded and processed successfully",
            data={
                "filename": file.filename,
                "summary": summary
            }
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )


@router.post("/clean", response_model=APIResponse)
async def clean_data(
    file: UploadFile = File(...),
    remove_duplicates: bool = False,
    handle_missing: str = "drop",
    normalize: bool = False,
    remove_outliers: bool = False,
    current_user: User = Depends(get_current_user)
):
    """
    Clean and preprocess data
    """
    try:
        content = await file.read()
        
        # Load data
        if file.filename.endswith('.csv'):
            df = data_service.load_csv(content)
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = data_service.load_excel(content)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format"
            )
        
        # Clean data
        operations = {
            'remove_duplicates': remove_duplicates,
            'handle_missing': handle_missing,
            'normalize': normalize,
            'remove_outliers': remove_outliers
        }
        
        df_clean = data_service.clean_data(df, operations)
        
        # Get before/after summary
        before_summary = data_service.get_data_summary(df)
        after_summary = data_service.get_data_summary(df_clean)
        
        return APIResponse(
            status="success",
            message="Data cleaned successfully",
            data={
                "before": before_summary,
                "after": after_summary,
                "rows_removed": df.shape[0] - df_clean.shape[0]
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error cleaning data: {str(e)}"
        )


@router.post("/validate", response_model=APIResponse)
async def validate_data(
    file: UploadFile = File(...),
    rules: str = "{}",
    current_user: User = Depends(get_current_user)
):
    """
    Validate data against rules
    """
    try:
        content = await file.read()
        
        # Load data
        if file.filename.endswith('.csv'):
            df = data_service.load_csv(content)
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = data_service.load_excel(content)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format"
            )
        
        # Parse rules
        validation_rules = json.loads(rules)
        
        # Validate
        result = data_service.validate_data(df, validation_rules)
        
        return APIResponse(
            status="success" if result["valid"] else "validation_failed",
            message="Validation complete",
            data=result
        )
    
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid rules JSON format"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error validating data: {str(e)}"
        )
