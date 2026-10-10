import utils
import random

names = ["art7235","qwerty","12345","awsd", "Артём", "Ольга", "Максим", "Елена", "Иван"]

def generate_mock_players():
    for _ in range(100):
        name = names[random.randint(0, len(names))]
        level = random.randint(1, 100)

        player = utils.create_player(name, level)