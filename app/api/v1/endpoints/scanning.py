from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.vision import recognition, barcode
from app.schemas.scanning import FoodScanResult

router = APIRouter()

@router.post("/scan-barcode", response_model=FoodScanResult)
async def scan_barcode_endpoint(code: str):
    data = await barcode.fetch_product_by_barcode(code)
    if not data:
        raise HTTPException(status_code=404, detail="Product not found")
        
    score = 10
    if data["fats"] > 20: score -= 2
    
    return {
        "name": data["name"],
        "calories": int(data["calories"]),
        "protein": data["protein"],
        "carbs": data["carbs"],
        "fats": data["fats"],
        "health_score": score,
        "warnings": data["warnings"]
    }

@router.post("/scan-photo")
async def scan_photo_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    ai_result = recognition.analyze_food_image(contents)
    
    return {
        "name": "AI Identified Food",
        "calories": 300,
        "protein": 20,
        "carbs": 30,
        "fats": 10,
        "health_score": 8,
        "warnings": []
    }