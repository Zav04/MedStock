from pydantic import BaseModel
from typing import List


class C_UpdateStockConsumiveis(BaseModel):
    consumiveis: List[dict]