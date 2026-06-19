from flask import Flask, request

app = Flask(__name__)

@app.route("/character")
def create_character():
    name = request.args.get("name")
    level = request.args.get("level")

    if name is None or level is None:
        return {"error": "name and level are required"}

    if not level.isdigit():
        return {"error": "level must be a number"}

    level_int = int(level)

    if level_int < 1:
        return {"error": "level must be at least 1"}

    if name == "":
        return {"error": "name cannot be empty"}

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