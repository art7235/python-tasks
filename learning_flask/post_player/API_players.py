from flask import Flask, request

app = Flask(__name__)

players = []

@app.route('/players', methods=['POST'])
def create_players():
    data = request.get_json(silent=True)
    if isinstance(data, dict):
        name = data.get('name')
        level = data.get('level')

        if name is not None and level is not None:
            players.append({"name": name, "level": level})
        
            return {
                    "message": "Player created"
                    , "status": 200
                    }


@app.route('/players', methods=['GET'])
def return_lst_players():
    return {"players": players, "status": 200}


@app.route('/search_players', methods=['GET'])
def search_players():
    name = request.args.get("name")
    if name is None or name == "":
        return{"error": "name not found",
               "status": 400}   
    for i in range(len(players)):
        if players[i]["name"] == name:
            return {"player" :players[i], "status": 200}
    return {
            "error": "Player not found",
            "status": 404
            }

if __name__ == "__main__":
    app.run()