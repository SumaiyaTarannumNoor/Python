from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hi'

@app.route('/get_user/<user_id>')
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "Sumaiya",
        "email": "sumaiya@gmail.com"

    }

    extra = request.args.get("extra")

    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200

# Use Postman to check this API
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()

    return jsonify(data), 201


if __name__ == '__main__':
    app.run()
