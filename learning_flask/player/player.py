from flask import Flask, request
import utils

app = Flask(__name__)

@app.route("/player")
def push_player():
    nickname = request.args.get("nickname")
    level = request.args.get("level")
    gold = request.args.get("gold")

    check_err = utils.check_player(nickname, level, gold)
    if check_err is not None:
        return check_err
    
    level_int = int(level)
    gold_int = int(gold)

    status, rich = utils.get_player_stats(level_int, gold_int)

    return {
            "nickname": nickname,
            "level": level_int,
            "gold": gold_int,
            "status": status,
            "rich": rich
            }

if __name__ == "__main__":
    app.run()