"""
Maintenance cost tracking schemas
"""
from datetime import date
from decimal import Decimal
from typing import List, Optional, Dict
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.filters import DateRangeFilter


class CostTracking(BaseSchema):
    """Cost tracking for maintenance request"""
    maintenance_id: UUID
    request_number: str
    
    estimated_cost: Decimal
    approved_cost: Decimal
    actual_cost: Decimal
    
    variance: Decimal
    variance_percentage: Decimal
    
    within_budget: bool
    
    # Breakdown
    materials_cost: Decimal
    labor_cost: Decimal
    vendor_charges: Decimal
    other_costs: Decimal


class BudgetAllocation(BaseSchema):
    """Budget allocation for hostel maintenance"""
    hostel_id: UUID
    hostel_name: str
    
    fiscal_year: str  # YYYY format
    
    # Budget
    total_budget: Decimal
    allocated_budget: Decimal
    spent_amount: Decimal
    remaining_budget: Decimal
    
    utilization_percentage: Decimal
    
    # By category
    budget_by_category: Dict[str, "CategoryBudget"]


class CategoryBudget(BaseSchema):
    """Budget for maintenance category"""
    category: str
    allocated: Decimal
    spent: Decimal
    remaining: Decimal
    utilization_percentage: Decimal


class ExpenseReport(BaseSchema):
    """Maintenance expense report"""
    hostel_id: Optional[UUID] = None
    report_period: DateRangeFilter
    generated_at: datetime
    
    # Summary
    total_expenses: Decimal
    total_requests: int
    average_cost_per_request: Decimal
    
    # By category
    expenses_by_category: Dict[str, Decimal]
    
    # By month
    monthly_expenses: List["MonthlyExpense"]
    
    # By priority
    expenses_by_priority: Dict[str, Decimal]
    
    # Top expenses
    top_expensive_requests: List["ExpenseItem"]


class MonthlyExpense(BaseSchema):
    """Monthly expense summary"""
    month: str  # YYYY-MM
    total_expenses: Decimal
    request_count: int
    average_cost: Decimal


class ExpenseItem(BaseSchema):
    """Individual expense item"""
    maintenance_id: UUID
    request_number: str
    title: str
    category: str
    actual_cost: Decimal
    completion_date: date


class VendorInvoice(BaseCreateSchema):
    """Vendor invoice for maintenance"""
    maintenance_id: UUID
    
    vendor_name: str
    invoice_number: str
    invoice_date: date
    
    # Items
    line_items: List["InvoiceLineItem"]
    
    # Amounts
    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    
    # Payment
    payment_terms: str
    due_date: date
    
    # Attachments
    invoice_document_url: Optional[str] = None


class InvoiceLineItem(BaseSchema):
    """Invoice line item"""
    description: str
    quantity: Decimal
    unit_price: Decimal
    total_price: Decimal


class CostAnalysis(BaseSchema):
    """Cost analysis and trends"""
    hostel_id: UUID
    analysis_period: DateRangeFilter
    
    # Trends
    cost_trend: str = Field(..., pattern="^(increasing|decreasing|stable)$")
    trend_percentage: Decimal
    
    # Cost drivers
    highest_cost_category: str
    most_frequent_category: str
    
    # Efficiency
    cost_per_student: Decimal
    cost_per_room: Decimal
    
    # Benchmarks
    comparison_to_previous_period: Decimal