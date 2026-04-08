from sqlalchemy.orm import Session
from app.services import finance_service
from app.ai_engine import financial_score_model, forecasting_model
from app.models.user_finance import Expense


def get_ai_insights(db: Session, user_id: int, skip_finance_call: bool = False, raw_metrics: dict = None):
    if skip_finance_call and raw_metrics:
        metrics = raw_metrics
    else:
        metrics = finance_service.get_dashboard_metrics(db, user_id)

    emergency_fund_ratio = 3.0
    debt_to_income = (metrics['monthlyIncome'] * 0.1) if metrics['monthlyIncome'] > 0 else 0.0

    health_score = financial_score_model.calculate_financial_health(
        metrics['savingsRate'], debt_to_income, emergency_fund_ratio
    )
    recommendations = financial_score_model.generate_recommendations(metrics)

    expenses = db.query(Expense.date, Expense.amount).filter(Expense.user_id == user_id).all()
    forecast = forecasting_model.forecast_expenses(expenses) if expenses else 0.0

    return {
        "score": health_score,
        "recommendations": recommendations,
        "forecastedNextMonth": forecast,
        "metrics": metrics
    }
