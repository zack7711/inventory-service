
from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware

from database import test_connection
from models import Inventory
import service


# Create FastAPI application
app = FastAPI(
    title="Inventory Service API",
    description="Inventory Microservice for Order Product System",
    version="1.0.0"
)


# Database connection on startup
@app.on_event("startup")
async def startup_event():
    await test_connection()


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home Endpoint
@app.get("/")
def home():
    return {
        "message": "Inventory Service is running"
    }


# Create Inventory
@app.post("/api/inventory", status_code=201)
async def create_inventory(inventory: Inventory):
    created_item = await service.create_inventory(inventory)

    if created_item is None:
        raise HTTPException(
            status_code=400,
            detail="Inventory record already exists for this product."
        )

    return created_item


# Get All Inventory
@app.get("/api/inventory")
async def get_all_inventory():
    return await service.get_all_inventory()


# Get Inventory by Product ID
@app.get("/api/inventory/{product_id}")
async def get_inventory_by_product_id(product_id: str):
    item = await service.get_inventory_by_product_id(
        product_id
    )

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found."
        )

    return item


# Update Inventory
@app.put("/api/inventory/{product_id}")
async def update_inventory(
    product_id: str,
    inventory: Inventory
):
    updated_item = await service.update_inventory(
        product_id,
        inventory
    )

    if updated_item is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found."
        )

    return updated_item


# Check Stock Availability
@app.get("/api/inventory/{product_id}/available/{quantity}")
async def check_availability(
    product_id: str,
    quantity: int = Path(..., gt=0)
):
    available = await service.check_availability(
        product_id,
        quantity
    )

    if available is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found."
        )

    return {
        "product_id": product_id,
        "requested_quantity": quantity,
        "available": available
    }


# Reduce Stock
@app.post("/api/inventory/{product_id}/reduce/{quantity}")
async def reduce_stock(
    product_id: str,
    quantity: int = Path(..., gt=0)
):
    result = await service.reduce_stock(
        product_id,
        quantity
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found."
        )

    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Invalid quantity or insufficient stock."
        )

    return result


# Delete Inventory
@app.delete("/api/inventory/{product_id}")
async def delete_inventory(product_id: str):
    deleted = await service.delete_inventory(product_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found."
        )

    return {
        "message": "Inventory item deleted successfully."
    }
