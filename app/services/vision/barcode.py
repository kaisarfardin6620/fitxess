# app/services/vision/barcode.py
import httpx

async def fetch_product_by_barcode(barcode: str) -> dict:
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, timeout=10.0)
            if resp.status_code != 200:
                return None
            
            data = resp.json()
            if data.get("status") != 1:
                return None
                
            p = data.get("product", {})
            n = p.get("nutriments", {})
            
            return {
                "name": p.get("product_name", "Unknown"),
                "calories": int(n.get("energy-kcal_100g", 0)),
                "protein": float(n.get("proteins_100g", 0)),
                "carbs": float(n.get("carbohydrates_100g", 0)),
                "fats": float(n.get("fat_100g", 0)),
                "serving_size": p.get("serving_size", "100g")
            }
        except Exception as e:
            print(f"Barcode API Error: {e}")
            return None