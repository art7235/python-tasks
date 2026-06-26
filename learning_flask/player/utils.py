def check_player(nickname, level, gold):
    if nickname is None or level is None or gold is None:
        return {"error": "all parameters are required"}
    
    if nickname == "":
        return {"error": "nickname cannot be empty"}
    
    if not level.isdigit() or not gold.isdigit():
        return {"error": "level and gold must be numbers"}
    
    level_int = int(level)
    gold_int = int(gold)
    
    if level_int < 1:
        return {"error": "level must be at least 1"}
    
    if gold_int < 0:
        return {"error": "gold cannot be negative"}


def get_player_stats(level, gold):
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
    
    return status, rich