# --- File: app/schemas/maintenance/maintenance_cost.py ---
"""
Maintenance cost tracking and budget management schemas.

Provides comprehensive cost tracking, budget allocation, expense reporting,
and vendor invoice management with detailed analytics.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List, Optional

from pydantic import Field, field_validator, model_validator,computed_field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema
from app.schemas.common.filters import DateRangeFilter

__all__ = [
    "CostTracking",
    "BudgetAllocation",
    "CategoryBudget",
    "ExpenseReport",
    "MonthlyExpense",
    "ExpenseItem",
    "VendorInvoice",
    "InvoiceLineItem",
    "CostAnalysis",
]


class CostTracking(BaseSchema):
    """
    Cost tracking for maintenance request.
    
    Tracks estimated vs actual costs with variance analysis.
    """

    maintenance_id: UUID = Field(
        ...,
        description="Maintenance request unique identifier",
    )
    request_number: str = Field(
        ...,
        description="Request number",
    )
    estimated_cost: Decimal = Field(
        ...,
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Original estimated cost",
    )
    approved_cost: Decimal = Field(
        ...,
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Approved budget amount",
    )
    actual_cost: Decimal = Field(
        ...,
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Actual cost incurred",
    )
    variance: Decimal = Field(
        ...,
        max_digits=10,
        decimal_places=2,
        description="Cost variance (actual - approved)",
    )
    variance_percentage: Decimal = Field(
        ...,
        decimal_places=2,
        description="Variance as percentage of approved",
    )
    within_budget: bool = Field(
        ...,
        description="Whether actual cost is within approved budget",
    )
    materials_cost: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Materials cost component",
    )
    labor_cost: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Labor cost component",
    )
    vendor_charges: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="External vendor charges",
    )
    other_costs: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Other miscellaneous costs",
    )
    tax_amount: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Tax component",
    )

    @field_validator(
        "estimated_cost",
        "approved_cost",
        "actual_cost",
        "variance",
        "variance_percentage",
        "materials_cost",
        "labor_cost",
        "vendor_charges",
        "other_costs",
        "tax_amount",
    )
    @classmethod
    def round_amounts(cls, v: Decimal) -> Decimal:
        """Round monetary amounts to 2 decimal places."""
        return round(v, 2)

    @computed_field
    @property
    def cost_breakdown_total(self) -> Decimal:
        """Calculate total from breakdown components."""
        return round(
            self.materials_cost
            + self.labor_cost
            + self.vendor_charges
            + self.other_costs
            + self.tax_amount,
            2,
        )


class CategoryBudget(BaseSchema):
    """
    Budget allocation for specific maintenance category.
    
    Tracks allocation, spending, and utilization per category.
    """

    category: str = Field(
        ...,
        description="Maintenance category name",
    )
    category_code: Optional[str] = Field(
        None,
        max_length=50,
        description="Category code",
    )
    allocated: Decimal = Field(
        ...,
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Allocated budget amount",
    )
    spent: Decimal = Field(
        ...,
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Amount spent",
    )
    committed: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Amount committed (approved but not paid)",
    )
    remaining: Decimal = Field(
        ...,
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Remaining budget",
    )
    utilization_percentage: Decimal = Field(
        ...,
        ge=0,
        le=100,
        decimal_places=2,
        description="Budget utilization percentage",
    )
    request_count: int = Field(
        default=0,
        ge=0,
        description="Number of maintenance requests",
    )
    average_cost: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        decimal_places=2,
        description="Average cost per request",
    )

    @field_validator(
        "allocated",
        "spent",
        "committed",
        "remaining",
        "utilization_percentage",
        "average_cost",
    )
    @classmethod
    def round_amounts(cls, v: Decimal) -> Decimal:
        """Round amounts to 2 decimal places."""
        return round(v, 2)

    @computed_field
    @property
    def is_over_budget(self) -> bool:
        """Check if category is over budget."""
        return self.spent > self.allocated

    @computed_field
    @property
    def available_for_commitment(self) -> Decimal:
        """Calculate amount available for new commitments."""
        return round(
            max(Decimal("0.00"), self.allocated - self.spent - self.committed),
            2,
        )


class BudgetAllocation(BaseSchema):
    """
    Overall budget allocation for hostel maintenance.
    
    Tracks fiscal year budget with category-wise breakdown
    and utilization metrics.
    """

    hostel_id: UUID = Field(
        ...,
        description="Hostel unique identifier",
    )
    hostel_name: str = Field(
        ...,
        description="Hostel name",
    )
    fiscal_year: str = Field(
        ...,
        pattern=r"^\d{4}$",
        description="Fiscal year (YYYY format)",
    )
    fiscal_year_start: date = Field(
        ...,
        description="Fiscal year start date",
    )
    fiscal_year_end: date = Field(
        ...,
        description="Fiscal year end date",
    )
    total_budget: Decimal = Field(
        ...,
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Total allocated budget",
    )
    allocated_budget: Decimal = Field(
        ...,
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Budget allocated to categories",
    )
    spent_amount: Decimal = Field(
        ...,
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Total amount spent",
    )
    committed_amount: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Committed but not yet spent",
    )
    remaining_budget: Decimal = Field(
        ...,
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Remaining unallocated budget",
    )
    utilization_percentage: Decimal = Field(
        ...,
        ge=0,
        le=100,
        decimal_places=2,
        description="Overall budget utilization",
    )
    budget_by_category: Dict[str, CategoryBudget] = Field(
        ...,
        description="Budget breakdown by category",
    )
    reserve_fund: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Emergency reserve fund",
    )
    
    # Forecasting
    projected_annual_spend: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Projected annual spending",
    )
    burn_rate_monthly: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Average monthly spending rate",
    )

    @field_validator("fiscal_year_end")
    @classmethod
    def validate_fiscal_year(cls, v: date, info) -> date:
        """Validate fiscal year dates."""
        if "fiscal_year_start" in info.data:
            if v <= info.data["fiscal_year_start"]:
                raise ValueError("Fiscal year end must be after start")
        return v

    @computed_field
    @property
    def is_over_budget(self) -> bool:
        """Check if overall budget is exceeded."""
        return self.spent_amount > self.total_budget

    @computed_field
    @property
    def months_remaining(self) -> int:
        """Calculate months remaining in fiscal year."""
        today = date.today()
        if today > self.fiscal_year_end:
            return 0
        
        months = (
            (self.fiscal_year_end.year - today.year) * 12
            + (self.fiscal_year_end.month - today.month)
        )
        return max(0, months)


class MonthlyExpense(BaseSchema):
    """
    Monthly expense summary.
    
    Aggregates maintenance expenses for a specific month.
    """

    month: str = Field(
        ...,
        pattern=r"^\d{4}-(0[1-9]|1[0-2])$",
        description="Month in YYYY-MM format",
    )
    month_name: str = Field(
        ...,
        description="Month name (January, February, etc.)",
    )
    year: int = Field(
        ...,
        ge=2000,
        le=2100,
        description="Year",
    )
    total_expenses: Decimal = Field(
        ...,
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Total expenses for the month",
    )
    request_count: int = Field(
        ...,
        ge=0,
        description="Number of maintenance requests",
    )
    completed_count: int = Field(
        default=0,
        ge=0,
        description="Number of completed requests",
    )
    average_cost: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Average cost per request",
    )
    budget_allocated: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Budget allocated for the month",
    )
    variance_from_budget: Optional[Decimal] = Field(
        None,
        description="Variance from monthly budget",
    )

    @computed_field
    @property
    def within_budget(self) -> Optional[bool]:
        """Check if monthly expenses are within budget."""
        if self.budget_allocated is None:
            return None
        return self.total_expenses <= self.budget_allocated


class ExpenseItem(BaseSchema):
    """
    Individual expense item in reports.
    
    Represents single maintenance request in expense listings.
    """

    maintenance_id: UUID = Field(
        ...,
        description="Maintenance request unique identifier",
    )
    request_number: str = Field(
        ...,
        description="Request number",
    )
    title: str = Field(
        ...,
        description="Request title",
    )
    category: str = Field(
        ...,
        description="Maintenance category",
    )
    priority: str = Field(
        ...,
        description="Priority level",
    )
    estimated_cost: Decimal = Field(
        ...,
        ge=0,
        description="Estimated cost",
    )
    actual_cost: Decimal = Field(
        ...,
        ge=0,
        description="Actual cost incurred",
    )
    cost_variance: Decimal = Field(
        ...,
        description="Cost variance amount",
    )
    completion_date: date = Field(
        ...,
        description="Completion date",
    )
    vendor_name: Optional[str] = Field(
        None,
        description="Vendor name (if applicable)",
    )

    @computed_field
    @property
    def over_budget(self) -> bool:
        """Check if expense was over estimated cost."""
        return self.actual_cost > self.estimated_cost


class ExpenseReport(BaseSchema):
    """
    Comprehensive maintenance expense report.
    
    Provides detailed expense analysis with multiple dimensions
    and top expense listings.
    """

    hostel_id: Optional[UUID] = Field(
        None,
        description="Hostel ID (if hostel-specific)",
    )
    hostel_name: Optional[str] = Field(
        None,
        description="Hostel name",
    )
    report_period: DateRangeFilter = Field(
        ...,
        description="Report period",
    )
    generated_at: datetime = Field(
        ...,
        description="Report generation timestamp",
    )
    generated_by: Optional[UUID] = Field(
        None,
        description="User who generated report",
    )
    
    # Summary statistics
    total_expenses: Decimal = Field(
        ...,
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Total expenses in period",
    )
    total_requests: int = Field(
        ...,
        ge=0,
        description="Total maintenance requests",
    )
    completed_requests: int = Field(
        ...,
        ge=0,
        description="Completed requests",
    )
    average_cost_per_request: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Average cost per request",
    )
    
    # Budget comparison
    total_budget: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Total budget for period",
    )
    budget_utilization: Optional[Decimal] = Field(
        None,
        ge=0,
        le=100,
        description="Budget utilization percentage",
    )
    
    # Breakdown by category
    expenses_by_category: Dict[str, Decimal] = Field(
        ...,
        description="Expenses grouped by category",
    )
    requests_by_category: Dict[str, int] = Field(
        default_factory=dict,
        description="Request count by category",
    )
    
    # Monthly breakdown
    monthly_expenses: List[MonthlyExpense] = Field(
        ...,
        description="Month-by-month expenses",
    )
    
    # Priority-based breakdown
    expenses_by_priority: Dict[str, Decimal] = Field(
        default_factory=dict,
        description="Expenses grouped by priority",
    )
    
    # Top expenses
    top_expensive_requests: List[ExpenseItem] = Field(
        default_factory=list,
        max_length=50,
        description="Highest cost maintenance requests",
    )
    
    # Vendor analysis
    top_vendors_by_spending: Optional[List[Dict[str, any]]] = Field(
        None,
        max_length=20,
        description="Top vendors by total spending",
    )

    @computed_field
    @property
    def completion_rate(self) -> Decimal:
        """Calculate completion rate percentage."""
        if self.total_requests == 0:
            return Decimal("0.00")
        return round(
            Decimal(self.completed_requests) / Decimal(self.total_requests) * 100,
            2,
        )


class InvoiceLineItem(BaseSchema):
    """
    Line item in vendor invoice.
    
    Represents individual item/service in invoice.
    """

    line_number: int = Field(
        ...,
        ge=1,
        description="Line item number",
    )
    description: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Item/service description",
    )
    item_code: Optional[str] = Field(
        None,
        max_length=50,
        description="Item code/SKU",
    )
    quantity: Decimal = Field(
        ...,
        gt=0,
        max_digits=10,
        decimal_places=3,
        description="Quantity",
    )
    unit: str = Field(
        ...,
        max_length=20,
        description="Unit of measurement",
    )
    unit_price: Decimal = Field(
        ...,
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Price per unit",
    )
    total_price: Decimal = Field(
        ...,
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Total line price",
    )
    tax_rate: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        le=100,
        decimal_places=2,
        description="Tax rate percentage",
    )
    tax_amount: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Tax amount",
    )

    @model_validator(mode="after")
    def validate_pricing(self) -> "InvoiceLineItem":
        """
        Validate pricing calculations.
        
        Ensures total_price = quantity × unit_price (pre-tax).
        """
        calculated_total = self.quantity * self.unit_price
        
        # Allow small rounding differences
        if abs(calculated_total - self.total_price) > Decimal("0.01"):
            raise ValueError(
                f"Total price ({self.total_price}) doesn't match "
                f"quantity ({self.quantity}) × unit price ({self.unit_price})"
            )
        
        # Validate tax calculation if tax_rate > 0
        if self.tax_rate > 0:
            calculated_tax = self.total_price * self.tax_rate / 100
            if abs(calculated_tax - self.tax_amount) > Decimal("0.01"):
                raise ValueError(
                    f"Tax amount ({self.tax_amount}) doesn't match "
                    f"total price ({self.total_price}) × tax rate ({self.tax_rate}%)"
                )
        
        return self


class VendorInvoice(BaseCreateSchema):
    """
    Vendor invoice for maintenance work.
    
    Comprehensive invoice tracking with line items, taxes,
    and payment terms.
    """

    maintenance_id: UUID = Field(
        ...,
        description="Maintenance request unique identifier",
    )
    vendor_name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Vendor company name",
    )
    vendor_id: Optional[UUID] = Field(
        None,
        description="Vendor ID in system (if registered)",
    )
    vendor_address: Optional[str] = Field(
        None,
        max_length=500,
        description="Vendor billing address",
    )
    vendor_tax_id: Optional[str] = Field(
        None,
        max_length=50,
        description="Vendor tax ID/GST number",
    )
    invoice_number: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Vendor invoice number",
    )
    invoice_date: date = Field(
        ...,
        description="Invoice issue date",
    )
    purchase_order_number: Optional[str] = Field(
        None,
        max_length=100,
        description="Our purchase order number",
    )
    line_items: List[InvoiceLineItem] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Invoice line items",
    )
    subtotal: Decimal = Field(
        ...,
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Subtotal (before tax)",
    )
    tax_amount: Decimal = Field(
        ...,
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Total tax amount",
    )
    discount_amount: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Discount amount",
    )
    total_amount: Decimal = Field(
        ...,
        ge=0,
        max_digits=12,
        decimal_places=2,
        description="Total invoice amount",
    )
    payment_terms: str = Field(
        ...,
        max_length=200,
        description="Payment terms (e.g., Net 30, Due on receipt)",
    )
    due_date: date = Field(
        ...,
        description="Payment due date",
    )
    currency: str = Field(
        default="INR",
        max_length=3,
        description="Currency code (ISO 4217)",
    )
    invoice_document_url: Optional[str] = Field(
        None,
        description="URL to invoice document/PDF",
    )
    notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="Additional notes",
    )

    @field_validator("invoice_date", "due_date")
    @classmethod
    def validate_dates(cls, v: date) -> date:
        """Validate invoice dates are reasonable."""
        # Invoice date shouldn't be too far in past or future
        days_diff = abs((date.today() - v).days)
        if days_diff > 365:
            raise ValueError(
                "Invoice date cannot be more than 1 year from today"
            )
        return v

    @model_validator(mode="after")
    def validate_invoice_totals(self) -> "VendorInvoice":
        """
        Validate invoice calculations.
        
        Ensures subtotal matches line items and total is calculated correctly.
        """
        # Validate subtotal matches line items
        line_items_total = sum(item.total_price for item in self.line_items)
        
        if abs(line_items_total - self.subtotal) > Decimal("0.01"):
            raise ValueError(
                f"Subtotal ({self.subtotal}) doesn't match sum of line items ({line_items_total})"
            )
        
        # Validate total calculation
        calculated_total = self.subtotal + self.tax_amount - self.discount_amount
        
        if abs(calculated_total - self.total_amount) > Decimal("0.01"):
            raise ValueError(
                f"Total amount ({self.total_amount}) doesn't match "
                f"subtotal ({self.subtotal}) + tax ({self.tax_amount}) - discount ({self.discount_amount})"
            )
        
        # Due date should be on or after invoice date
        if self.due_date < self.invoice_date:
            raise ValueError("Due date cannot be before invoice date")
        
        return self


class CostAnalysis(BaseSchema):
    """
    Cost analysis and trends.
    
    Provides insights into cost patterns, trends, and efficiency metrics.
    """

    hostel_id: UUID = Field(
        ...,
        description="Hostel unique identifier",
    )
    hostel_name: str = Field(
        ...,
        description="Hostel name",
    )
    analysis_period: DateRangeFilter = Field(
        ...,
        description="Analysis period",
    )
    previous_period: Optional[DateRangeFilter] = Field(
        None,
        description="Previous period for comparison",
    )
    
    # Cost trends
    cost_trend: str = Field(
        ...,
        pattern=r"^(increasing|decreasing|stable)$",
        description="Overall cost trend direction",
    )
    trend_percentage: Decimal = Field(
        ...,
        decimal_places=2,
        description="Trend change percentage",
    )
    
    # Cost drivers
    highest_cost_category: str = Field(
        ...,
        description="Category with highest total cost",
    )
    highest_cost_category_amount: Decimal = Field(
        ...,
        ge=0,
        description="Amount spent in highest cost category",
    )
    most_frequent_category: str = Field(
        ...,
        description="Most frequently occurring category",
    )
    most_frequent_category_count: int = Field(
        ...,
        ge=0,
        description="Request count for most frequent category",
    )
    
    # Efficiency metrics
    cost_per_student: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Average maintenance cost per student",
    )
    cost_per_room: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Average maintenance cost per room",
    )
    cost_per_sqft: Optional[Decimal] = Field(
        None,
        ge=0,
        decimal_places=2,
        description="Cost per square foot",
    )
    
    # Performance benchmarks
    comparison_to_previous_period: Decimal = Field(
        ...,
        decimal_places=2,
        description="Percentage change from previous period",
    )
    comparison_to_budget: Optional[Decimal] = Field(
        None,
        decimal_places=2,
        description="Percentage variance from budget",
    )
    
    # Predictive insights
    projected_annual_cost: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Projected annual cost based on trends",
    )
    seasonal_variation: Optional[Decimal] = Field(
        None,
        description="Seasonal variation coefficient",
    )
    
    # Recommendations
    cost_saving_opportunities: Optional[List[str]] = Field(
        None,
        max_length=10,
        description="Identified cost-saving opportunities",
    )
    risk_areas: Optional[List[str]] = Field(
        None,
        max_length=10,
        description="Areas of cost risk",
    )