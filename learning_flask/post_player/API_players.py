from flask import Flask, request
import utils

app = Flask(__name__)


def error_response(message, status_code):
    return {"error": message}, status_code


@app.route('/admin/player', methods=['POST'])
def create_player():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("Invalid request format", 400)

    name = data.get('name')
    level = data.get('level')

    level_0, error = utils.check_player_and_get_level(name)
    if error != "":
        if error == "name already exists":
            return error_response(error, 409)
        return error_response(error, 400)

    player = utils.create_player(name, level)
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


@app.route('/admin/players', methods=['POST'])
def return_lst_players():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("Invalid request format", 400)

    filter = utils.PlayersFilter()

    name = data.get("name")
    id = data.get("id")
    min_level = data.get("min_level")
    max_level = data.get("max_level")

    if name is not None:
        filter.name_pattern = name

    if id is not None:
        if isinstance(id, bool) or not str(id).isdigit():
            return error_response("id must be a number", 400)
        filter.id_pattern = int(id)

    if min_level is not None:
        if isinstance(min_level, bool) or not str(min_level).isdigit():
            return error_response("min_level must be a number", 400)
        filter.min_level = int(min_level)

    if max_level is not None:
        if isinstance(max_level, bool) or not str(max_level).isdigit():
            return error_response("max_level must be a number", 400)
        filter.max_level = int(max_level)

    page = data.get("page")
    limit = data.get("limit")
    sort_by = data.get("sort_by")
    order = data.get("order")

    page_int, limit_int, sort_by, order, error = utils.check_pagination_and_sort(
        page, limit, sort_by, order
    )
    if error != "":
        return error_response(error, 400)

    result = utils.paginate_players(filter, page_int, limit_int, sort_by, order)
    return result, 200


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
    utils.generate_mock_players()
    app.run()