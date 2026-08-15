from flask import Flask, request

app = Flask(__name__)

@app.route('/hello', methods=['POST'])
def hello():
    data = request.get_json()        # 1. Забрали JSON
    name = data.get('name')          # 2. Достали имя
    return {"message": f"Hello, {name}!"}  # 3. Ответили

app.run()