from pydantic import BaseModel
from datetime import datetime

class Player(BaseModel):
    name: str
    level: int
    gold: int
    id: int
    created_at: datetime

players = {}
player_id = 0


def check_player_and_get_level(name: str, level: int) -> tuple[int , str]:
    if name is None or level is None:
        return 0, "name and level are required"
    
    if name == "":
        return 0, "name cannot be empty"
    
    if not str(level).isdigit():
        return 0, "level must be a number"
    
    level_int = int(level)
    
    if level_int < 1:
        return 0, "level must be at least 1"
    
    return level_int, ""


def check_top_up_balance(id: str, gold: str) -> tuple[int , str]:
    if id is None or gold is None:
        return 0, "id and gold are required"
    
    if not id.isdigit():
        return 0, "id must be a number"
    
    if not gold.isdigit():
        return 0, "gold must be a number"
    
    id_int = int(id)
    gold_int = int(gold)
    
    if gold_int < 0:
        return 0, "gold cannot be negative"
    
    return id_int, ""


def check_get_player(id: str) -> tuple[int , str]:
    if id is None or id == "":
        return 0, "id is required"
    
    if not id.isdigit():
        return 0, "id must be a number"
    
    return int(id), ""


def create_player(name: str, level: int) -> Player:
    global player_id
    player_id += 1
    player = Player(name=name, level=level, gold=0, id=player_id, created_at=datetime.now())
    players[player_id] = player
    return player


def top_up_balance(id, gold):
    if id in players:
        players[id].gold += gold
        return players[id]
    return None


def return_lst_players():
    players_list = list(players.items())
    players_list.sort(key=lambda item: item[1].created_at)

    res = []
    for _, player in players_list:
        player_data = player.model_dump()
        player_data["id"] = player.id
        res.append(player_data)
    
    return res


def get_player(id):
    if id in players:
        return players[id]
    return None


def delete_player(id):
    if id in players:
        del players[id]
        return True
    return False


def ret_leaderboard():
    players_list = list(players.items())
    players_list.sort(key=lambda item: item[1].level, reverse=True)
    
    res = []
    for _, player in players_list:
        res.append({
            "id": player.id,
            "name": player.name,
            "level": player.level
        })
    return res


def ret_stats():
    max_level = 0
    averge_level = 0
    
    for key, player in players.items():
        averge_level += player.level
        if player.level > max_level:
            max_level = player.level
    
    if len(players) == 0:
        return {
            "players_count": 0,
            "max_level": 0,
            "average_level": 0
        }
    
    return {
        "players_count": len(players),
        "max_level": max_level,
        "average_level": averge_level / len(players)
    }