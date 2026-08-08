from flask import Flask, request
from pydantic import BaseModel
from datetime import datetime
import json

app = Flask(__name__)

class Player(BaseModel):
    name: str
    level: int
    gold: int
    created_at: datetime
  

players = {}
player_id = 0

@app.route('/player', methods=['POST'])
def create_player():
    global player_id
    data = request.get_json(silent=True)
    if isinstance(data, dict):
        name = data.get('name')
        level = data.get('level')

        if name is not None and level is not None:
            player_id += 1
            player = Player(name=name, level=level, gold=0, created_at=datetime.now())
            players[str(player_id)] = player
            return {"message": "Player created",
                    "player": player.model_dump_json()}, 200


@app.route('/player/gold', methods=['POST'])
def top_up_balance():
    data = request.get_json(silent=True)
    if isinstance(data, dict):
        name = data.get('name')
        gold = data.get('gold')

        if name is not None and gold is not None:
            for key, i in players.items():
                if name == i.name:
                    i.gold += gold
                    return {"message": "balance replenished",
                            "player": i.model_dump()}, 200
            return {"error": "User not found"}, 404
    
    return {"error": "Invalid request"}, 400



@app.route('/players', methods=['GET'])
def return_lst_players():
    players_list = list(players.items())
    players_list.sort(key=lambda item: item[1].created_at)
    res = []
    for player_id, player in players_list:
        player_data = player.model_dump()
        player_data["id"] = player_id
        res.append(player_data)
    return {"players": res}, 200


@app.route('/player', methods=['GET'])
def get_player():
    name = request.args.get("name")

    if name is None or name == "":
        return{"error": "name is required"}, 400
       
    for i in players:
        if players[i].name == name:
            return {"player" :players[i].model_dump_json()}, 200
    return {
            "error": "Player not found"
            }, 404

@app.route('/player', methods=['DELETE'])
def delete_player():
    name = request.args.get("name")

    if name is None or name == "":
        return{"error": "name is required"}, 400
       
    for i in players:
        if players[i].name == name:
            players.pop(i)
            break
        
    return {"message" : "player was deleted"}, 200


@app.route('/leaderboard', methods=['GET'])
def ret_leaderboard():
    players_list = list(players.items())
    players_list.sort(key=lambda item: item[1].level, reverse=True)
    res = []
    for player_id, player in players_list:
        res.append({
            "name": player.name,
            "level": player.level
        })
    return {"players": res}, 200


@app.route('/stats', methods=['GET'])
def ret_stats():
    max_level = 0
    averge_level = 0
    for key, i in players.items():
        averge_level+=i.level
        if i.level > max_level:
            max_level = i.level
    return {"players_count": len(players),
    "max_level": max_level,
    "average_level": averge_level/len(players)}, 200


if __name__ == "__main__":
    app.run()