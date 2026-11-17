from datetime import datetime
from pydantic import BaseModel
class InventoryResponse(BaseModel):
 id: str
 product_id: str
 product_name: str
 stock_quantity: int
 reorder_level: int
 updated_at: datetime