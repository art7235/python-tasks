from flask import Flask, request

app = Flask(__name__)

@app.route("/stats")
def push_characteristics():
    strength = request.args.get("strength")
    agility = request.args.get("agility")

    if strength is None or agility is None:
        return {"error": "strength and agility are required"}
    
    if not strength.isdigit() or not agility.isdigit():
        return {"error": "strength and agility must be numbers"}
    
    strength_int = int(strength)
    agility_int = int(agility)
    
    if strength_int < 0 or agility_int < 0:
        return {"error": "strength and agility cannot be negative"}
    
    return set_characteristics(strength_int, agility_int)
    

def set_characteristics(strength, agility):
    power = strength + agility
    attack = strength * 2
    speed = agility * 3
    return {
            "strength": strength,
            "agility": agility,
            "power": power,
            "attack": attack,
            "speed": speed,
            }

if __name__ == "__main__":
    app.run()