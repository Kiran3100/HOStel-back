"""
Meal items and dietary schemas
"""
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class MealItems(BaseSchema):
    """Meal items definition"""
    meal_type: str = Field(..., pattern="^(breakfast|lunch|snacks|dinner)$")
    items: List["MenuItem"]


class MenuItem(BaseSchema):
    """Individual menu item"""
    item_name: str = Field(..., min_length=2, max_length=100)
    item_description: Optional[str] = Field(None, max_length=255)
    
    # Dietary classification
    is_vegetarian: bool = Field(True)
    is_vegan: bool = Field(False)
    is_jain: bool = Field(False)
    is_gluten_free: bool = Field(False)
    
    # Allergens
    contains_dairy: bool = Field(False)
    contains_nuts: bool = Field(False)
    contains_soy: bool = Field(False)
    
    # Category
    category: str = Field(..., description="main_course, side_dish, dessert, beverage")


class DietaryOptions(BaseSchema):
    """Dietary options configuration"""
    hostel_id: UUID
    
    # Available options
    vegetarian_menu: bool = Field(True)
    non_vegetarian_menu: bool = Field(False)
    vegan_menu: bool = Field(False)
    jain_menu: bool = Field(False)
    gluten_free_options: bool = Field(False)
    
    # Customization allowed
    allow_meal_customization: bool = Field(False)
    
    # Allergen warnings
    display_allergen_warnings: bool = Field(True)


class NutritionalInfo(BaseSchema):
    """Nutritional information for menu item"""
    item_name: str
    
    # Per serving
    serving_size: str
    calories: Optional[int] = Field(None, ge=0)
    
    # Macros (grams)
    protein: Optional[Decimal] = Field(None, ge=0)
    carbohydrates: Optional[Decimal] = Field(None, ge=0)
    fat: Optional[Decimal] = Field(None, ge=0)
    fiber: Optional[Decimal] = Field(None, ge=0)
    
    # Micros
    sodium_mg: Optional[Decimal] = Field(None, ge=0)
    sugar_g: Optional[Decimal] = Field(None, ge=0)


class ItemMasterList(BaseSchema):
    """Master list of menu items"""
    hostel_id: UUID
    
    categories: List["ItemCategory"]


class ItemCategory(BaseSchema):
    """Category of menu items"""
    category_name: str
    items: List[str]