def chek_character_data(name, level):
    if name is None or level is None:
            return {"error": "name and level are required"}

    if not level.isdigit():
        return {"error": "level must be a number"}

    level_int = int(level)

    if level_int < 1:
        return {"error": "level must be at least 1"}

    if name == "":
        return {"error": "name cannot be empty"}
    

def get_charcter_rank(level_int, name):
    if level_int < 5:
        rank = "Новичок"
    elif 5 <= level_int <= 10:
        rank = "Опытный"
    else:
        rank = "Мастер"
    
    return rank