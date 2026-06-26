import json




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



response = {}
label = True
while label:
    method = input("введите метод: ")
    path = input("введите путь: ")

    if method == "GET":
        if path == "/hello":
            response = {"status": 200,"data": "Hello, world"}
            a = json.dumps(response)
            print(a)
        elif path == "/user":
            response = {"status": 200,"data": data_base}
            print(response)
        else:
            response = {"status": 404, "error": "Not found"}
            print(response)

    elif method == "POST":
        if path == "/user":
            create_user(input("укажите имя: "), input("укажите возраст: "))

    else:
        response = {"status": 404, "error": "Not found"}
        print(response)
