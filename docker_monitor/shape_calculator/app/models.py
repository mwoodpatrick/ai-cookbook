from typing import Literal, Union
from pydantic import BaseModel, Field

class Circle(BaseModel):
    """Represents a circle with a given radius."""
    shape_type: Literal["circle"] = "circle"
    radius: float = Field(..., gt=0, description="The radius of the circle, must be positive.")

class Rectangle(BaseModel):
    """Represents a rectangle with given width and height."""
    shape_type: Literal["rectangle"] = "rectangle"
    width: float = Field(..., gt=0, description="The width of the rectangle, must be positive.")
    height: float = Field(..., gt=0, description="The height of the rectangle, must be positive.")

class Triangle(BaseModel):
    """Represents a triangle with a given base and height."""
    shape_type: Literal["triangle"] = "triangle"
    base: float = Field(..., gt=0, description="The base of the triangle, must be positive.")
    height: float = Field(..., gt=0, description="The height of the triangle, must be positive.")

# A union type to represent any supported shape
Shape = Union[Circle, Rectangle, Triangle]
