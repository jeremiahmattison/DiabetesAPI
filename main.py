from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import sqlite3

app = Flask(__name__)
app.config['AISusername'] = 'AISpassword'
jwt = JWTManager(app)

# SQLite db setup
conn = sqlite3.connect('health_data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS health_info (
                    id INTEGER PRIMARY KEY,
                    pregnancies INTEGER,
                    glucose INTEGER,
                    blood_pressure INTEGER,
                    skin_thickness INTEGER,
                    insulin INTEGER,
                    bmi REAL,
                    diabetes_pedigree_function REAL,
                    age INTEGER
                )''')
conn.commit()
conn.close()

# Authentication through JWT tokens
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "AISusername" or password != "AISpassword":
        return jsonify({"msg": "Incorrect username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token ) 

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run()