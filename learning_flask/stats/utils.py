def check_stats(strength, agility):
    if strength is None or agility is None:
        return {"error": "strength and agility are required"}
    
    if not strength.isdigit() or not agility.isdigit():
        return {"error": "strength and agility must be numbers"}
    
    strength_int = int(strength)
    agility_int = int(agility)
    
    if strength_int < 0 or agility_int < 0:
        return {"error": "strength and agility cannot be negative"}
    

def get_calc_stats(strength, agility):
    power = strength + agility
    attack = strength * 2
    speed = agility * 3

    return power, attack, speed