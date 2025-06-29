This detailed example demonstrates a Python Docker application that effectively utilizes type hints for improved code readability, maintainability, and early error detection.

We'll create a simple FastAPI application that calculates the area of different shapes, leveraging Python's `typing` module extensively.

### Project Structure

```
.
├── app/
│   ├── main.py
│   └── models.py
├── Dockerfile
├── requirements.txt
└── README.md
```

### 1\. `app/models.py` (Defining Typed Data Structures)

This file will define our data models using `pydantic` (which integrates well with FastAPI and provides excellent type validation).

```python
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
```

**Explanation of Typing in `models.py`:**

  * **`from typing import Literal, Union`**: Imports essential typing constructs.
  * **`Literal["circle"]`**: This is a powerful type hint introduced in Python 3.8. It specifies that the `shape_type` field must literally be the string "circle" (or "rectangle", "triangle" for the other models). This helps with type checking and provides strong guarantees about the expected value.
  * **`Union[Circle, Rectangle, Triangle]`**: This defines a `Shape` type that can be *any one* of the `Circle`, `Rectangle`, or `Triangle` models. This is crucial for handling polymorphic input.
  * **`BaseModel`**: From `pydantic`, this base class automatically provides type validation based on the type hints you provide for class attributes.
  * **`Field(..., gt=0, description=...)`**: `pydantic`'s `Field` allows you to add more validation rules (e.g., `gt=0` for "greater than 0") and descriptions to your fields, which are also used to generate OpenAPI documentation.

### 2\. `app/main.py` (The FastAPI Application with Type Hints)

This is the core FastAPI application logic.

```python
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
```

**Explanation of Typing in `main.py`:**

  * **`from typing import Union`**: Again, importing `Union` for polymorphic handling.
  * **`from .models import Circle, Rectangle, Triangle, Shape`**: Importing our defined data models.
  * **Function Signatures (`calculate_circle_area(circle: Circle) -> float`)**:
      * `circle: Circle`: This specifies that the `circle` argument must be an instance of the `Circle` class.
      * `-> float`: This is a *return type hint*, indicating that the function is expected to return a `float`.
  * **`async def calculate_area(shape: Shape) -> float:`**:
      * `shape: Shape`: This is the most crucial type hint here. It tells FastAPI (and any type checker) that the `shape` argument can be *any* of the types defined in our `Shape` `Union`. FastAPI intelligently uses this to automatically parse the incoming JSON payload into the correct `pydantic` model based on the `shape_type` field.
      * `-> float`: The function returns a `float`.
  * **`isinstance(shape, Circle)`**: While `pydantic` handles the initial parsing, `isinstance` is still necessary within the function to determine the *specific* type of `Shape` instance we received so we can call the correct area calculation function.
  * **`response_model=float`**: In the `@app.post` decorator, `response_model=float` tells FastAPI that the endpoint will return a floating-point number. This helps with OpenAPI documentation generation.

### 3\. `requirements.txt`

This file lists the Python packages required for our application.

```
fastapi
uvicorn
pydantic
```

### 4\. `Dockerfile`

This file defines how to build our Docker image.

```dockerfile
# Use a lightweight official Python base image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app/ ./app/

# Expose the port the FastAPI application will run on
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Explanation of `Dockerfile`:**

  * **`FROM python:3.10-slim-buster`**: Uses an official Python image based on Debian Buster, which is lightweight.
  * **`WORKDIR /app`**: Sets the current working directory inside the container to `/app`.
  * **`COPY requirements.txt .`**: Copies the `requirements.txt` file to the working directory.
  * **`RUN pip install --no-cache-dir -r requirements.txt`**: Installs the Python dependencies. `--no-cache-dir` helps keep the image size smaller.
  * **`COPY app/ ./app/`**: Copies your application code from the host's `app/` directory to the container's `/app/app/` directory.
  * **`EXPOSE 8000`**: Informs Docker that the container listens on port 8000 at runtime.
  * **`CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`**: This is the command that gets executed when the container starts. It runs the `main.py` application using Uvicorn.

### 5\. `README.md` (Instructions)

```markdown
# Python Docker Application with Typing (Shape Area Calculator)

This project demonstrates a simple FastAPI application that calculates the area of different shapes, making extensive use of Python's type hints. The application is containerized using Docker.

## Project Structure

```

.
├── app/
│   ├── main.py        \# FastAPI application logic
│   └── models.py      \# Pydantic models with type hints
├── Dockerfile         \# Docker build instructions
├── requirements.txt   \# Python dependencies
└── README.md          \# This file

````

## Setup and Running

1.  **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Build the Docker image:**

    ```bash
    docker build -t shape-calculator-app .
    ```

3.  **Run the Docker container:**

    ```bash
    docker run -p 8000:8000 shape-calculator-app
    ```

    The application will now be running at `http://localhost:8000`.

## API Endpoints

Once the application is running, you can access the interactive API documentation (Swagger UI) at:

[http://localhost:8000/docs](http://localhost:8000/docs)

You can also test the endpoint using `curl`:

**Calculate Circle Area:**

```bash
curl -X POST "http://localhost:8000/calculate_area/" \
     -H "Content-Type: application/json" \
     -d '{
           "shape_type": "circle",
           "radius": 5
         }'
# Expected output: 78.53975
````

**Calculate Rectangle Area:**

```bash
curl -X POST "http://localhost:8000/calculate_area/" \
     -H "Content-Type: application/json" \
     -d '{
           "shape_type": "rectangle",
           "width": 10,
           "height": 4
         }'
# Expected output: 40.0
```

**Calculate Triangle Area:**

```bash
curl -X POST "http://localhost:8000/calculate_area/" \
     -H "Content-Type: application/json" \
     -d '{
           "shape_type": "triangle",
           "base": 6,
           "height": 8
         }'
# Expected output: 24.0
```

## Benefits of Typing in this Application

  * **Improved Readability:** Function signatures clearly indicate expected input types and return types, making the code easier to understand at a glance.
  * **Early Error Detection:** Type checkers (like MyPy) can identify potential type mismatches or incorrect attribute access *before* runtime, catching bugs during development rather than in production.
      * For example, if you accidentally tried to access `shape.diameter` on a `Rectangle` object, a type checker would immediately flag it.
  * **Better Code Completion and IDE Support:** IDEs like VS Code can provide more accurate and helpful code completion suggestions because they understand the types of your variables and function parameters.
  * **Enhanced Maintainability:** When refactoring or adding new features, type hints act as living documentation, guiding developers on how different parts of the codebase are intended to interact.
  * **Robust API Validation (via Pydantic):** Pydantic automatically validates incoming request bodies against the defined type hints (`BaseModel` classes). If the incoming data doesn't conform to the expected types or rules (e.g., `radius` not being a positive float), FastAPI will return a clear validation error without you having to write explicit validation logic.
  * **Automatic API Documentation (via FastAPI):** FastAPI uses the type hints and Pydantic models to automatically generate interactive OpenAPI (Swagger UI) documentation for your API, making it easy for others to understand and consume your services.

This example showcases how integrating Python's `typing` with a framework like FastAPI and tools like Docker leads to a robust, maintainable, and well-documented application.
