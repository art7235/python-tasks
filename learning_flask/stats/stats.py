from flask import Flask, request
import utils

app = Flask(__name__)

@app.route("/stats")
def get_stat():
    strength = request.args.get("strength")
    agility = request.args.get("agility")

    check_err = utils.check_stats(strength, agility)
    if check_err is not None:
        return check_err
    
    power, attack, speed = utils.get_calc_stats(int(strength), int(agility))

    return {
            "strength": strength,
            "agility": agility,
            "power": power,
            "attack": attack,
            "speed": speed,
            }
    

if __name__ == "__main__":
    app.run()