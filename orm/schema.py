from typing import Dict
from typing import List, Optional

from pydantic import BaseModel, Field


class UserCreateResponse(BaseModel):
    id: int
    username: str
    url: str


class UserLoginResponse(BaseModel):
    access_token: str = Field(description="JWT access token")
    token_type: str = Field(example="bearer")
    expires_in: int = Field(example=3600)
    user: Dict[str, str] = Field(description="Basic user info (id and username)")


class FNResult(BaseModel):
    n_FN: int
    individual_FN_images: List[str]
    assembled_image: str
    compressed_image: str


class ResultSummary(BaseModel):
    FN_method: str
    data_type: str
    data_format: str
    n_FN: int
    individual_FN_images: List[str]
    assembled_image: str
    compressed_image: str
    rfMRI_REST1_LR_Atlas_MSMAll_hp2000_clean_dtseries_n1: Optional[FNResult] = None


class ResponseModel(BaseModel):
    status: str
    result_summary: ResultSummary
