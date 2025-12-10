"""
Financial analytics schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import List, Dict, Optional

from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.filters import DateRangeFilter


class RevenueBreakdown(BaseSchema):
    """Revenue breakdown by type/category"""
    total_revenue: Decimal
    booking_revenue: Decimal
    rent_revenue: Decimal
    mess_revenue: Decimal
    other_revenue: Decimal

    revenue_by_hostel: Dict[UUID, Decimal] = Field(
        default_factory=dict, description="Hostel ID -> revenue"
    )
    revenue_by_payment_type: Dict[str, Decimal] = Field(
        default_factory=dict, description="PaymentType -> revenue"
    )


class ExpenseBreakdown(BaseSchema):
    """Expense breakdown by category"""
    total_expenses: Decimal
    maintenance_expenses: Decimal
    staff_expenses: Decimal
    utility_expenses: Decimal
    other_expenses: Decimal

    expenses_by_hostel: Dict[UUID, Decimal] = Field(
        default_factory=dict, description="Hostel ID -> expenses"
    )
    expenses_by_category: Dict[str, Decimal] = Field(
        default_factory=dict, description="Category -> expenses"
    )


class ProfitAndLossReport(BaseSchema):
    """P&L report for a hostel or platform"""
    scope_type: str = Field(..., pattern="^(hostel|platform)$")
    scope_id: Optional[UUID] = None

    period: DateRangeFilter
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # Revenue & expense
    revenue: RevenueBreakdown
    expenses: ExpenseBreakdown

    # Calculated
    gross_profit: Decimal
    net_profit: Decimal
    profit_margin_percentage: Decimal


class CashflowSummary(BaseSchema):
    """Cashflow summary"""
    scope_type: str = Field(..., pattern="^(hostel|platform)$")
    scope_id: Optional[UUID] = None

    period: DateRangeFilter
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    opening_balance: Decimal
    closing_balance: Decimal

    inflows: Decimal
    outflows: Decimal

    inflow_breakdown: Dict[str, Decimal] = Field(default_factory=dict)
    outflow_breakdown: Dict[str, Decimal] = Field(default_factory=dict)

    cashflow_timeseries: List["CashflowPoint"] = Field(default_factory=list)


class CashflowPoint(BaseSchema):
    """Cashflow timeseries point"""
    date: date
    inflow: Decimal
    outflow: Decimal
    net_flow: Decimal


class FinancialReport(BaseSchema):
    """Top-level financial analytics response"""
    scope_type: str
    scope_id: Optional[UUID] = None

    period: DateRangeFilter
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    pnl_report: ProfitAndLossReport
    cashflow: CashflowSummary

    # Ratios
    collection_rate: Decimal = Field(..., description="% of billed amount collected")
    overdue_ratio: Decimal = Field(..., description="% of amount that is overdue")
    avg_revenue_per_student: Decimal
    avg_revenue_per_bed: Decimal