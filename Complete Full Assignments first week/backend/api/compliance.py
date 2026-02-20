"""
Compliance API endpoints
"""
from fastapi import APIRouter, Depends
from backend.middleware.auth_middleware import get_current_user
from backend.models.user import User
from backend.schemas.auth import APIResponse

router = APIRouter(prefix="/compliance", tags=["Compliance"])


@router.get("/regulations", response_model=APIResponse)
async def get_regulations():
    """
    Get Indian financial regulations overview
    """
    regulations = {
        "rbi_guidelines": {
            "title": "Reserve Bank of India Guidelines",
            "key_points": [
                "KYC compliance mandatory for all financial transactions",
                "PAN card required for transactions above ₹50,000",
                "AML (Anti-Money Laundering) reporting requirements",
                "Foreign exchange management regulations"
            ]
        },
        "sebi_regulations": {
            "title": "Securities and Exchange Board of India",
            "key_points": [
                "Investor protection guidelines",
                "Disclosure requirements for listed companies",
                "Insider trading prevention",
                "Market manipulation prevention"
            ]
        },
        "digital_banking": {
            "title": "Digital Banking Norms",
            "key_points": [
                "Two-factor authentication required",
                "Transaction limits for digital payments",
                "Data privacy and security standards",
                "Customer grievance redressal mechanism"
            ]
        },
        "kyc_aml": {
            "title": "KYC/AML Compliance",
            "key_points": [
                "Identity verification required",
                "Address proof mandatory",
                "PAN card for financial transactions",
                "Regular customer due diligence",
                "Suspicious transaction reporting"
            ]
        }
    }
    
    return APIResponse(
        status="success",
        message="Regulations retrieved",
        data=regulations
    )


@router.post("/check", response_model=APIResponse)
async def check_compliance(
    transaction_amount: float,
    has_pan: bool = True,
    has_kyc: bool = True,
    current_user: User = Depends(get_current_user)
):
    """
    Check compliance for a transaction
    """
    compliance_status = {
        "compliant": True,
        "checks": [],
        "warnings": [],
        "required_actions": []
    }
    
    # Check PAN requirement
    if transaction_amount > 50000:
        if not has_pan:
            compliance_status["compliant"] = False
            compliance_status["required_actions"].append({
                "action": "Provide PAN card",
                "reason": "Required for transactions above ₹50,000"
            })
        else:
            compliance_status["checks"].append({
                "check": "PAN verification",
                "status": "Pass"
            })
    
    # Check KYC
    if not has_kyc:
        compliance_status["warnings"].append({
            "warning": "KYC not completed",
            "recommendation": "Complete KYC for higher transaction limits"
        })
    else:
        compliance_status["checks"].append({
            "check": "KYC status",
            "status": "Compliant"
        })
    
    # Check transaction limit
    if transaction_amount > 1000000:
        compliance_status["warnings"].append({
            "warning": "High value transaction",
            "recommendation": "May require additional verification"
        })
    
    return APIResponse(
        status="success" if compliance_status["compliant"] else "warning",
        message="Compliance check completed",
        data=compliance_status
    )
