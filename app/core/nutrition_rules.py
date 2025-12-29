# app/core/nutrition_rules.py

# Data derived from "Hydration/Micronutrient" PDF
# Values represent the Daily RDA or AI (Minimum Target)

MICRONUTRIENT_GUIDELINES = {
    "child_9_13": {
        "B1": 0.9, "B2": 0.9, "B3": 12, "B5": 4, "B6": 1.0, 
        "B9": 300, "B12": 1.8, "Vitamin D": 15, "Iron": 8, 
        "Magnesium": 240, "Zinc": 8
    },
    "male_14_18": {
        "B1": 1.2, "B2": 1.3, "B3": 16, "B5": 5, "B6": 1.3, 
        "B9": 400, "B12": 2.4, "Vitamin D": 15, "Iron": 11, 
        "Magnesium": 410, "Zinc": 11
    },
    "female_14_18": {
        "B1": 1.0, "B2": 1.0, "B3": 14, "B5": 5, "B6": 1.2, 
        "B9": 400, "B12": 2.4, "Vitamin D": 15, "Iron": 15, 
        "Magnesium": 360, "Zinc": 9
    },
    "male_19_50": {
        "B1": 1.2, "B2": 1.3, "B3": 16, "B5": 5, "B6": 1.3, 
        "B9": 400, "B12": 2.4, "Vitamin D": 15, "Iron": 8, 
        "Magnesium": 400, "Zinc": 11
    },
    "female_19_50": {
        "B1": 1.1, "B2": 1.1, "B3": 14, "B5": 5, "B6": 1.3, 
        "B9": 400, "B12": 2.4, "Vitamin D": 15, "Iron": 18, 
        "Magnesium": 310, "Zinc": 8
    },
    "male_51_plus": {
        "B1": 1.2, "B2": 1.3, "B3": 16, "B5": 5, "B6": 1.7, 
        "B9": 400, "B12": 2.4, "Vitamin D": 15, "Iron": 8, 
        "Magnesium": 420, "Zinc": 11
    },
    "female_51_plus": {
        "B1": 1.1, "B2": 1.1, "B3": 14, "B5": 5, "B6": 1.5, 
        "B9": 400, "B12": 2.4, "Vitamin D": 15, "Iron": 8, 
        "Magnesium": 320, "Zinc": 8
    },
    # Special Conditions
    "pregnancy": {
        "B1": 1.4, "B2": 1.4, "B3": 18, "B5": 6, "B6": 1.9, 
        "B9": 600, "B12": 2.6, "Vitamin D": 15, "Iron": 27, 
        "Magnesium": 350, "Zinc": 11
    },
    "breastfeeding": {
        "B1": 1.4, "B2": 1.6, "B3": 17, "B5": 7, "B6": 2.0, 
        "B9": 500, "B12": 2.8, "Vitamin D": 15, "Iron": 9, 
        "Magnesium": 310, "Zinc": 12
    }
}