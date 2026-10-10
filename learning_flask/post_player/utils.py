from pydantic import BaseModel
from datetime import datetime
import random


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

    def has_id(self):
        if self.id_pattern is None:
            return False
        return True

    def has_min_level(self):
        if self.min_level is None:
            return False
        return True

    def has_max_level(self):
        if self.max_level is None:
            return False
        return True

    def matches(self, player: Player) -> bool:
        if self.has_name():
            name_lower = self.name_pattern.casefold()
            if name_lower not in player.name.casefold():
                return False

        if self.has_id():
            if player.id != self.id_pattern:
                return False

        if self.has_min_level():
            if player.level < self.min_level:
                return False

        if self.has_max_level():
            if player.level > self.max_level:
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


def check_pagination_and_sort(page, limit, sort_by, order) -> tuple[int, int, str, str, str]:
    if page is None:
        page = "1"

    if limit is None:
        limit = "10"

    if not str(page).isdigit():
        return 0, 0, "", "", "page must be a number"

    if not str(limit).isdigit():
        return 0, 0, "", "", "limit must be a number"

    page_int = int(page)
    limit_int = int(limit)

    if page_int < 1:
        return 0, 0, "", "", "page must be >= 1"

    if limit_int < 1:
        return 0, 0, "", "", "limit must be >= 1"

    if limit_int > 100:
        return 0, 0, "", "", "limit must be <= 100"

    if sort_by is None or sort_by == "":
        sort_by = "created_at"

    if sort_by not in ("level", "gold", "created_at"):
        return 0, 0, "", "", "sort_by must be one of: level, gold, created_at"

    if order is None or order == "":
        order = "asc"

    if order not in ("asc", "desc"):
        return 0, 0, "", "", "order must be one of: asc, desc"

    return page_int, limit_int, sort_by, order, ""


def is_name_taken(name: str) -> bool:
    name_lower = name.strip().casefold()
    for player in players.values():
        if player.name.casefold() == name_lower:
            return True
    return False


def create_player(name: str, level: int) -> Player:
    global player_id
    player_id += 1
    player = Player(name=name, level=level, gold=0, experience=0,
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


def players_list(filter: PlayersFilter) -> list:
    players_list = list(players.items())
    players_list.sort(key=lambda item: item[1].created_at)

    res = []
    for _, player in players_list:
        if not filter.matches(player):
            continue

        player_data = player.model_dump()
        player_data["id"] = player.id
        res.append(player_data)

    return res


def paginate_players(filter: PlayersFilter, page: int, limit: int,
                     sort_by: str, order: str) -> dict:
    filtered = []
    for player in players.values():
        if filter.matches(player):
            filtered.append(player)

    if order == "desc":
        reverse = True
    else:
        reverse = False

    filtered.sort(key=lambda player: getattr(player, sort_by), reverse=reverse)

    total = len(filtered)
    total_pages = (total + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit
    page_players = filtered[start:end]

    items = []
    for player in page_players:
        items.append({
            "id": player.id,
            "name": player.name,
            "level": player.level
        })

    return {
        "players": items,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
        "sort_by": sort_by,
        "order": order
    }


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


mock_names = ["art7235", "qwerty", "12345", "awsd", "Артём", "Ольга", "Максим", "Елена", "Иван"]


def generate_mock_players():
    used_names = set()
    attempts = 0
    max_attempts = 300

    while len(used_names) < 100 and attempts < max_attempts:
        attempts += 1
        name = mock_names[random.randint(0, len(mock_names) - 1)]

        unique_name = name
        suffix = 1
        while unique_name in used_names:
            unique_name = f"{name}_{suffix}"
            suffix += 1

        used_names.add(unique_name)
        level = random.randint(1, 100)
        create_player(unique_name, level)