from pydantic import BaseModel, ConfigDict
from schemas.expense import ExpenseResponse

class CategoryBreakdown(BaseModel):
    category: str
    amount: float


class DashboardSummaryResponse(BaseModel):
    total_expense: float
    expense_count: int
    highest_expense: float
    top_category: str | None
    current_month_total: float

    recent_expenses: list[ExpenseResponse]
    category_breakdown: list[CategoryBreakdown]
    
    model_config = ConfigDict(
        from_attributes=True
    )