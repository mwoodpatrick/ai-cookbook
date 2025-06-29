from fastapi import FastAPI, HTTPException
from typing import Union

from .models import Circle, Rectangle, Triangle, Shape

app = FastAPI(title="Shape Area Calculator",
              description="A simple API to calculate the area of various shapes.")

def calculate_circle_area(circle: Circle) -> float:
    """Calculates the area of a circle."""
    return 3.14159 * (circle.radius ** 2)

def calculate_rectangle_area(rectangle: Rectangle) -> float:
    """Calculates the area of a rectangle."""
    return rectangle.width * rectangle.height

def calculate_triangle_area(triangle: Triangle) -> float:
    """Calculates the area of a triangle."""
    return 0.5 * triangle.base * triangle.height

@app.post("/calculate_area/", response_model=float, summary="Calculate area of a shape")
async def calculate_area(shape: Shape) -> float:
    """
    Calculates the area of a given shape (circle, rectangle, or triangle).

    Args:
        shape: The shape object, which can be a Circle, Rectangle, or Triangle.

    Returns:
        The calculated area as a float.

    Raises:
        HTTPException: If an unknown shape type is provided (should not happen with pydantic validation).
    """
    if isinstance(shape, Circle):
        return calculate_circle_area(shape)
    elif isinstance(shape, Rectangle):
        return calculate_rectangle_area(shape)
    elif isinstance(shape, Triangle):
        return calculate_triangle_area(shape)
    else:
        # This case should theoretically not be reachable due to pydantic validation
        # and the `Shape` Union type, but good for defensive programming.
        raise HTTPException(status_code=400, detail="Unknown shape type provided.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
