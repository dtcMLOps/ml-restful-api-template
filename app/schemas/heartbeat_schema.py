from typing import List

from pydantic import BaseModel, Field

class ResponseCommon(BaseModel):
    status: str
    message: str
