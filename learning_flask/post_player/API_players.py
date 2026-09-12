from flask import Flask, request
import utils

app = Flask(__name__)


def error_response(message, status_code):
    return {"error": message}, status_code


@app.route('/player', methods=['POST'])
def create_player():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("Invalid request format", 400)

    name = data.get('name')

    level, error = utils.check_player_and_get_level(name)
    if error != "":
        if error == "name already exists":
            return error_response(error, 409)
        return error_response(error, 400)

    player = utils.create_player(name)
    return {"message": "Player created",
            "player": player.model_dump()}, 200


@app.route('/player/gold', methods=['POST'])
def top_up_balance():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("Invalid request format", 400)

    id = data.get('id')
    gold = data.get('gold')

    id_int, error = utils.check_top_up_balance(id, gold)
    if error != "":
        return error_response(error, 400)

    player = utils.top_up_balance(id_int, int(gold))
    if player:
        return {"message": "balance replenished",
                "player": player.model_dump()}, 200
    return error_response("Player not found", 404)


@app.route("/player/experience", methods=['POST'])
def raise_the_level():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("Invalid request format", 400)

    id = data.get('id')
    experience = data.get("experience")

    id_int, error = utils.check_id_and_experience(id, experience)
    if error != "":
        return error_response(error, 400)

    player = utils.top_up_experience(id_int, int(experience))
    if player:
        return {"message": "experience replenished",
                "player": player.model_dump()}, 200
    return error_response("Player not found", 404)


@app.route('/players', methods=['GET'])
def return_lst_players():
    name = request.args.get("name")

    if name is not None:
        name_clean, error = utils.check_search_name(name)
        if error != "":
            return error_response(error, 400)

        players_list = utils.search_players_by_name(name_clean)
        return players_list, 200

    players_list = utils.return_lst_players()
    return {"players": players_list}, 200


@app.route('/player', methods=['GET'])
def get_player():
    id = request.args.get("id")

    id_int, error = utils.check_get_player(id)
    if error != "":
        return error_response(error, 400)

    player = utils.get_player(id_int)
    if player:
        return {"player": player.model_dump()}, 200
    return error_response("Player not found", 404)


@app.route('/player', methods=['DELETE'])
def delete_player():
    id = request.args.get("id")

    id_int, error = utils.check_get_player(id)
    if error != "":
        return error_response(error, 400)

    player = utils.get_player(id_int)
    if player is None:
        return error_response("Player not found", 404)

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