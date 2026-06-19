from flask import Flask, request

app = Flask(__name__)

@app.route("/character")
def create_character():
    name = request.args.get("name")
    level = request.args.get("level")

    if name is None or level is None:
        return {"error": "name and level are required"}

    try:
        level_int = int(level)
    except ValueError:
        return {"error": "level must be a number"}

    if level_int < 5:
        rank = "Новичок"
    elif 5 <= level_int <= 10:
        rank = "Опытный"
    else:
        rank = "Мастер"
    
    return {
        "name": name,
        "level": level_int,
        "rank": rank
    }

if __name__ == "__main__":
    app.run()