from flask import Flask, request
import utils

app = Flask(__name__)

@app.route("/character")
def create_character():
    name = request.args.get("name")
    level = request.args.get("level")

    check_res = utils.chek_character_data(name, level)
    if check_res is not None:
        return check_res
    
    rank = utils.get_charcter_rank(int(level), name)

    return {"name": name,
            "level": level,
            "rank": rank
                }

if __name__ == "__main__":
    app.run()