import math
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Notebook Paper Calculator")

# CORS (OK for internal tools; restrict later if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow browser access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------- MODELS ---------

class PaperCalcInput(BaseModel):
    number_of_notebooks: int = Field(gt=0)
    sheets_per_notebook: int = Field(gt=0)
    paper_weight: float = Field(gt=0)  # g/m²
    small_sheets_per_large: int = Field(gt=0)
    large_length: float = Field(gt=0)  # meters
    large_width: float = Field(gt=0)   # meters


# --------- LOGIC ---------

def calculate_paper_weight(data: PaperCalcInput) -> float:
    number_of_large_sheets = math.ceil(
        data.number_of_notebooks
        * data.sheets_per_notebook
        / data.small_sheets_per_large
    )

    total_area = (
        number_of_large_sheets
        * data.large_length
        * data.large_width
    )

    total_weight = data.paper_weight * total_area / 1000
    return round(total_weight, 2)


# --------- ROUTES ---------

@app.get("/")
def root():
    return {
        "message": "Notebook Paper Calculator API is running",
        "docs": "/docs"
    }


@app.post("/calculate")
def calculate(data: PaperCalcInput):
    total_weight = calculate_paper_weight(data)
    return {
        "total_paper_weight_kg": total_weight
    }
