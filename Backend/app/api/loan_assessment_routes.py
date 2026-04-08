"""
Loan Assessment API Routes — FinWise AI Finance
================================================
Exposes two endpoints:
  POST /api/v1/loan-assessment/predict  — Run XGBoost model inference
  GET  /api/v1/loan-assessment/info     — Model metadata / health check
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

from app.api.dependencies import get_current_active_user
from app.models.user_finance import User
from app.ml_models.loan_inference import (
    predict_loan_eligibility,
    get_model_info,
    LoanInputValidationError,
    VALID_EDUCATION,
    VALID_EMPLOYMENT,
    VALID_MARITAL,
    VALID_MORTGAGE,
    VALID_DEPENDENTS,
    VALID_LOAN_PURPOSE,
    VALID_COSIGNER,
)

router = APIRouter()


# ── Request Schema ─────────────────────────────────────────────────────────────

class LoanAssessmentRequest(BaseModel):
    # Borrower profile
    age: int = Field(..., ge=18, le=100, description="Applicant age in years")
    income: float = Field(..., gt=0, description="Annual gross income in USD")
    credit_score: int = Field(..., ge=300, le=850, description="FICO credit score")
    months_employed: int = Field(..., ge=0, le=600, description="Months at current employment")
    num_credit_lines: int = Field(..., ge=1, le=50, description="Number of open credit lines")
    education: str = Field(..., description=f"One of: {VALID_EDUCATION}")
    employment_type: str = Field(..., description=f"One of: {VALID_EMPLOYMENT}")
    marital_status: str = Field(..., description=f"One of: {VALID_MARITAL}")
    has_mortgage: str = Field(..., description="'Yes' or 'No'")
    has_dependents: str = Field(..., description="'Yes' or 'No'")
    has_co_signer: str = Field(..., description="'Yes' or 'No'")

    # Loan details
    loan_amount: float = Field(..., gt=0, description="Requested loan amount in USD")
    loan_term: int = Field(..., ge=6, le=360, description="Loan term in months")
    dti_ratio: float = Field(..., ge=0.0, le=2.0, description="Debt-to-income ratio (0-2)")
    loan_purpose: str = Field(..., description=f"One of: {VALID_LOAN_PURPOSE}")

    @field_validator("education")
    @classmethod
    def validate_education(cls, v: str) -> str:
        if v not in VALID_EDUCATION:
            raise ValueError(f"education must be one of {VALID_EDUCATION}")
        return v

    @field_validator("employment_type")
    @classmethod
    def validate_employment(cls, v: str) -> str:
        if v not in VALID_EMPLOYMENT:
            raise ValueError(f"employment_type must be one of {VALID_EMPLOYMENT}")
        return v

    @field_validator("marital_status")
    @classmethod
    def validate_marital(cls, v: str) -> str:
        if v not in VALID_MARITAL:
            raise ValueError(f"marital_status must be one of {VALID_MARITAL}")
        return v

    @field_validator("has_mortgage")
    @classmethod
    def validate_mortgage(cls, v: str) -> str:
        if v not in VALID_MORTGAGE:
            raise ValueError("has_mortgage must be 'Yes' or 'No'")
        return v

    @field_validator("has_dependents")
    @classmethod
    def validate_dependents(cls, v: str) -> str:
        if v not in VALID_DEPENDENTS:
            raise ValueError("has_dependents must be 'Yes' or 'No'")
        return v

    @field_validator("loan_purpose")
    @classmethod
    def validate_purpose(cls, v: str) -> str:
        if v not in VALID_LOAN_PURPOSE:
            raise ValueError(f"loan_purpose must be one of {VALID_LOAN_PURPOSE}")
        return v

    @field_validator("has_co_signer")
    @classmethod
    def validate_cosigner(cls, v: str) -> str:
        if v not in VALID_COSIGNER:
            raise ValueError("has_co_signer must be 'Yes' or 'No'")
        return v


# ── Response Schema ────────────────────────────────────────────────────────────

class LoanAssessmentResponse(BaseModel):
    eligible: bool
    default_probability: float
    default_probability_pct: float
    threshold_used: float
    risk_level: str
    confidence_pct: float
    explanation: str
    key_factors: List[str]


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.post(
    "/predict",
    response_model=LoanAssessmentResponse,
    summary="Run XGBoost loan eligibility assessment",
    description=(
        "Submits borrower and loan details to the trained XGBoost model. "
        "Returns an eligibility verdict, default probability, risk level, and key factors."
    ),
)
def assess_loan(
    request: LoanAssessmentRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Run the XGBoost pipeline and return a loan eligibility result."""
    try:
        result = predict_loan_eligibility(
            age=request.age,
            income=request.income,
            loan_amount=request.loan_amount,
            credit_score=request.credit_score,
            months_employed=request.months_employed,
            num_credit_lines=request.num_credit_lines,
            loan_term=request.loan_term,
            dti_ratio=request.dti_ratio,
            education=request.education,
            employment_type=request.employment_type,
            marital_status=request.marital_status,
            has_mortgage=request.has_mortgage,
            has_dependents=request.has_dependents,
            loan_purpose=request.loan_purpose,
            has_co_signer=request.has_co_signer,
        )
    except LoanInputValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Input validation failed: {exc}",
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Loan assessment model unavailable: {exc}",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error during loan assessment: {exc}",
        )

    return LoanAssessmentResponse(
        eligible=result.eligible,
        default_probability=result.default_probability,
        default_probability_pct=round(result.default_probability * 100, 2),
        threshold_used=result.threshold_used,
        risk_level=result.risk_level,
        confidence_pct=result.confidence_pct,
        explanation=result.explanation,
        key_factors=result.key_factors,
    )


@router.get(
    "/info",
    summary="Model metadata and health check",
    description="Returns loaded model information including pipeline steps, threshold, and accepted feature values.",
)
def model_info(current_user: User = Depends(get_current_active_user)):
    """Return model metadata for debugging and frontend form population."""
    return get_model_info()
