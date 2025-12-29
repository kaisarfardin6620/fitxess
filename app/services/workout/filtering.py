# app/services/workout/filtering.py
from typing import List, Dict

def filter_exercises(
    all_exercises: List[Dict], 
    injuries: List[str], 
    available_equipment: List[str]
) -> List[Dict]:
    """
    Filters exercises logic:
    1. Must match available equipment (or be bodyweight).
    2. Must NOT aggravate injuries.
    """
    valid_exercises = []
    
    # Normalize inputs for comparison
    user_equip = set(e.lower() for e in available_equipment)
    user_injuries = set(i.lower() for i in injuries)

    for ex in all_exercises:
        ex_equip = ex.get("equipment", "").lower()
        
        # Equipment Check
        # If exercise requires equipment NOT in user list (and isn't bodyweight), skip
        if ex_equip != "bodyweight" and ex_equip not in user_equip:
            # Simple check. In reality, you might map "barbell" -> "smith machine" etc.
            continue
            
        # Injury Check
        # Assuming exercise has a list of body parts it stresses
        bad_for = set(ex.get("bad_for_injuries", []))
        if not bad_for.isdisjoint(user_injuries):
            # If they share any common element, skip
            continue
            
        valid_exercises.append(ex)
        
    return valid_exercises