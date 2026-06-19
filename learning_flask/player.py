from flask import Flask, request

app = Flask(__name__)

@app.route("/player")
def push_player():
    nickname = request.args.get("nickname")
    level = request.args.get("level")
    gold = request.args.get("gold")

    if nickname is None or level is None or gold is None:
        return {"error": "all parameters are required"}
    else:
        return post_player(nickname, int(level), int(gold))

    
def post_player(nickname, level, gold):

    if level < 5:
        status = "Beginner"
    if 5 <= level <= 10:
        status = "Player"
    if level > 10:
        status = "Veteran"

    if gold >= 1000:
        rich = True
    else:
        rich = False

    return {
            "nickname": nickname,
            "level": level,
            "gold": gold,
            "status": status,
            "rich": rich
                }


if __name__ == "__main__":
    app.run()
    


