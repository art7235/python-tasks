from flask import Flask, request
import utils

app = Flask(__name__)


@app.route('/player', methods=['POST'])
def create_player():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"error": "Invalid request format"}, 400
    
    name = data.get('name')
    level = data.get('level')
    
    level_int = utils.check_create_player(name, level)
    if isinstance(level_int, dict):
        return level_int, 400
    
    player = utils.create_player(name, level_int)
    return {"message": "Player created",
            "player": player.model_dump()}, 200


@app.route('/player/gold', methods=['POST'])
def top_up_balance():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"error": "Invalid request format"}, 400
    
    id = data.get('id')
    gold = data.get('gold')
    
    res = utils.check_top_up_balance(id, gold)
    if isinstance(res, dict):
        return res, 400
    
    id_int, gold_int = res
    
    player = utils.top_up_balance(id_int, gold_int)
    if player:
        return {"message": "balance replenished",
                "player": player.model_dump()}, 200
    return {"error": "User not found"}, 404


@app.route('/players', methods=['GET'])
def return_lst_players():
    players_list = utils.return_lst_players()
    return {"players": players_list}, 200


@app.route('/player', methods=['GET'])
def get_player():
    id = request.args.get("id")
    
    id_int = utils.check_get_player(id)
    if isinstance(id_int, dict):
        return id_int, 400
    
    player = utils.get_player(id_int)
    if player:
        return {"player": player.model_dump()}, 200
    return {"error": "Player not found"}, 404


@app.route('/player', methods=['DELETE'])
def delete_player():
    id = request.args.get("id")
    
    id_int = utils.check_get_player(id)
    if isinstance(id_int, dict):
        return id_int, 400
    
    utils.delete_player(id_int)
    return {"message": "player was deleted"}, 200


@app.route('/leaderboard', methods=['GET'])
def ret_leaderboard():
    players_list = utils.ret_leaderboard()
    return {"players": players_list}, 200


@app.route('/stats', methods=['GET'])
def ret_stats():
    stats = utils.ret_stats()
    return stats, 200


if __name__ == "__main__":
    app.run()