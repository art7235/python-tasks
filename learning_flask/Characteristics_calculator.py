from flask import Flask, request

app = Flask(__name__)

@app.route("/stats")
def push_characteristics():
    strength = request.args.get("strength")
    agility = request.args.get("agility")

    if strength is None or agility is None:
        return {"error": "strength and agility are required"}
    
    return set_characteristics(int(strength), int(agility))
    

app.run()


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