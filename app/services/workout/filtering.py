from typing import List, Dict

def filter_exercises(
    all_exercises: List[Dict], 
    injuries: List[str], 
    available_equipment: List[str]
) -> List[Dict]:
    valid_exercises = []
    user_equip = set(e.lower() for e in available_equipment)
    user_injuries = set(i.lower() for i in injuries)

    for ex in all_exercises:
        ex_equip = ex.get("equipment", "").lower()
        
        if ex_equip != "bodyweight" and ex_equip not in user_equip:
            continue
            
        bad_for = set(ex.get("bad_for_injuries", []))
        if not bad_for.isdisjoint(user_injuries):
            continue
            
        valid_exercises.append(ex)
        
    return valid_exercises