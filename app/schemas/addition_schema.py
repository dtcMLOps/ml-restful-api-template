from typing import List

from pydantic import BaseModel, Field


class AdditionInput(BaseModel):
    input_list: List[float] = Field(
        default=None, description="List of float numbers to be added.", example=[1.4, 2.3, 3.2]
    )


class AdditionResults(BaseModel):
    results: float = Field(description="result after addition.", example=6.9)
