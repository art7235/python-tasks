from pydantic import BaseModel
from datetime import datetime


class Player(BaseModel):
    name: str
    level: int
    gold: int
    experience: int
    id: int
    created_at: datetime


class PlayersFilter:
    name_pattern: str = ""
    id_pattern: int | None = None
    min_level: int | None = None
    max_level: int | None = None

    def has_name(self):
        if self.name_pattern is None or self.name_pattern == "":
            return False
        return True


players = {}
player_id = 0


def check_player_and_get_level(name: str) -> tuple[int, str]:
    if name is None:
        return 0, "name are required"

    if not isinstance(name, str):
        return 0, "name must be a string"

    if name.strip() == "":
        return 0, "name cannot be empty"

    if is_name_taken(name):
        return 0, "name already exists"

    return 1, ""


def check_top_up_balance(id: str, gold: str) -> tuple[int, str]:
    if id is None or gold is None:
        return 0, "id and gold are required"

    if isinstance(id, bool) or not str(id).isdigit():
        return 0, "id must be a number"

    if isinstance(gold, bool) or not str(gold).isdigit():
        return 0, "gold must be a number"

    id_int = int(id)
    gold_int = int(gold)

    if gold_int < 0:
        return 0, "gold cannot be negative"

    return id_int, ""


def check_id_and_experience(id: str, experience: str) -> tuple[int, str]:
    if id is None or experience is None:
        return 0, "id and experience are required"

    if isinstance(id, bool) or not str(id).isdigit():
        return 0, "id must be a number"

    if isinstance(experience, bool) or not str(experience).isdigit():
        return 0, "experience must be a number"

    id_int = int(id)
    experience_int = int(experience)

    if experience_int < 0:
        return 0, "experience cannot be negative"

    return id_int, ""


def check_get_player(id: str) -> tuple[int, str]:
    if id is None or id == "":
        return 0, "id is required"

    if isinstance(id, bool) or not str(id).isdigit():
        return 0, "id must be a number"

    return int(id), ""


def is_name_taken(name: str) -> bool:
    name_lower = name.strip().casefold()
    for player in players.values():
        if player.name.casefold() == name_lower:
            return True
    return False


def create_player(name: str) -> Player:
    global player_id
    player_id += 1
    player = Player(name=name, level=0, gold=0, experience=0,
                    id=player_id, created_at=datetime.now())
    players[player_id] = player
    return player


def top_up_balance(id: int, gold: int) -> Player | None:
    if id in players:
        players[id].gold += gold
        return players[id]
    return None


def top_up_experience(id: int, experience: int) -> Player | None:
    if id not in players:
        return None

    if experience < 0:
        return None

    players[id].experience += experience
    players[id].level = calculate_level(players[id].experience)

    return players[id]


def calculate_level(experiece: int) -> int:
    return (experiece // 100) + 1


def player_matches_filter(player: Player, filter: PlayersFilter) -> bool:
    if filter.has_name():
        name_lower = filter.name_pattern.casefold()
        if name_lower not in player.name.casefold():
            return False

    if filter.id_pattern is not None:
        if player.id != filter.id_pattern:
            return False

    if filter.min_level is not None:
        if player.level < filter.min_level:
            return False

    if filter.max_level is not None:
        if player.level > filter.max_level:
            return False

    return True


def players_list(filter: PlayersFilter) -> list:
    short_format = filter.has_name()

    players_list = list(players.items())
    players_list.sort(key=lambda item: item[1].created_at)

    res = []
    for _, player in players_list:
        if not player_matches_filter(player, filter):
            continue

        if short_format:
            res.append({
                "id": player.id,
                "name": player.name,
                "level": player.level
            })
        else:
            player_data = player.model_dump()
            player_data["id"] = player.id
            res.append(player_data)

    return res


def get_player(id: int) -> Player | None:
    if id in players:
        return players[id]
    return None


def delete_player(id: int) -> bool:
    if id in players:
        del players[id]
        return True
    return False


def ret_leaderboard() -> list:
    players_list = list(players.items())
    players_list.sort(key=lambda item: item[1].experience, reverse=True)

    res = []
    for _, player in players_list:
        res.append({
            "id": player.id,
            "name": player.name,
            "level": player.level
        })

    if len(res) > 4:
        return res[0:4]
    return res


def ret_stats() -> dict:
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