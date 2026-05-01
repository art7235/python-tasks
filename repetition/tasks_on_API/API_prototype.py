





data_base = {}

def create_user(name, age):
    id = str(len(data_base) + 1)
    user = {"name": name, "age": age}
    data_base[id] = user
    return data_base[id]

def get_user(name, age):
    for user_id, user in data_base.items():
        if user["name"] == name and user["age"] == age:
            return user_id

label = True
while label:
    print("\n1 - Создать, 2 - Найти, 0 - Выход")
    command = input("Выберите действие: ")

    if command == "1":
        create_user(input(), int(input()))

    elif command == "2":
        print(get_user(input(), int(input())))
        
    elif command == "0":
        label = False