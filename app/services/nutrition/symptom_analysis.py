def analyze_symptoms(symptoms: list[str]) -> list[dict]:
    scores = []
    
    # Simple logic engine: Maps keywords to body functions
    energy_hits = sum(1 for s in symptoms if s in ["low_energy", "tired", "brain_fog"])
    digestion_hits = sum(1 for s in symptoms if s in ["bloating", "gas", "nausea"])
    
    # Calculate inverted score (More symptoms = Lower score)
    energy_score = max(10, 100 - (energy_hits * 15))
    digestion_score = max(10, 100 - (digestion_hits * 20))
    
    scores.append({
        "category": "Energy",
        "score": energy_score,
        "description": "Supports mood, metabolism & focus"
    })
    
    scores.append({
        "category": "Digestion",
        "score": digestion_score,
        "description": "Supports absorption & gut health"
    })
    
    return scores