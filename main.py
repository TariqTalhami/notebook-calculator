from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from calculators.spiral import calculate_spiral
from calculators.school import calculate_school

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    # allow_origins=[        "http://localhost:5500",        "http://127.0.0.1:5500",    ],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CalculatePayload(BaseModel):
    category: str
    data: dict


@app.post("/calculate")
def calculate(payload: CalculatePayload):

    if payload.category == "spiral":
        return calculate_spiral(payload.data)

    elif payload.category == "school":
        return calculate_school(payload.data)

    else:
        raise HTTPException(
            status_code=400,
            detail="Unknown product category"
        )
    
    ##########