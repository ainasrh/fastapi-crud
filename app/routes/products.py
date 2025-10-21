from fastapi import APIRouter, HTTPException, status,Query,UploadFile,File,Form
from ..models.products import ProductSchema,ProductUpdateSchema
from ..db import get_collection
from typing import List,Optional
from datetime import datetime
from ..config import cloudinary
from uuid import uuid4
import cloudinary.uploader


router = APIRouter()

products_collection = get_collection("products")

@router.post("/create", response_model=ProductSchema, status_code=201)
async def create_product(
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    quantity: int = Form(...),
    image: UploadFile = File(None)
):
    try:
        product = ProductSchema(
            name=name,
            description= description,
            price= price,
            quantity = quantity,
            created_at = datetime.utcnow(),

        )
        product_data = product.dict()

        if image:
            upload_result = cloudinary.uploader.upload(image.file)
            product_data["image_url"] = upload_result.get("secure_url")

        result = await products_collection.insert_one(product_data)
        if not result.inserted_id:
            raise HTTPException(status_code=400, detail="Failed to create product")

        return product_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/products", response_model=List[ProductSchema])
async def get_products(id: Optional[str] = Query(None)):

    if id is not None:
        product_data = await products_collection.find_one({"id": id})
        if not product_data:
            raise HTTPException(status_code=404, detail="Product not found")
        return [ProductSchema(**product_data)]  

    products_cursor = products_collection.find()
    products = []
    async for product in products_cursor:
        products.append(ProductSchema(**product))
    return products



@router.delete("/delete/{id}",response_model=dict)
async def delete_products(id:str):

    res = await products_collection.delete_one({"id":id})

    if res.deleted_count == 0:
        raise HTTPException(status_code=404)
    
    return {"message": f"Product with id {id} deleted successfully"}





@router.patch("/products/{id}", response_model=dict)
async def update_product(id: str, product_update: ProductUpdateSchema):
    try:
        update_data = product_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided for update")
        
        update_data["updated_at"] = datetime.utcnow()
        
        # Try to find the product first to ensure it exists
        existing_product = await products_collection.find_one({"id": id})
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Update the product
        result = await products_collection.update_one({"id": id}, {"$set": update_data})
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes made to the product")
        
        return {"message": f"Product with id {id} updated successfully", "modified_count": result.modified_count}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
