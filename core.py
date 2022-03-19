from distutils import core
from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt, os
import datetime

app = Flask(__name__)
api = Api(app)

filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'pengguna.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = "beni123"
 
db = SQLAlchemy(app)

class Users(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(50))
   password = db.Column(db.String(50))
db.create_all()

class RegisterPengguna(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        if dataUsername and dataPassword:
            dataModel = Users(username=dataUsername, password=dataPassword)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"Pesan":"Berhasil"}), 200)
        return jsonify({"Pesan":"Username/Password harus diisi"})

class LoginUser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        queryUsername = [data.username for data in Users.query.all()]
        queryPassword = [data.password for data in Users.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword:

            token = jwt.encode(
                {
                    "username":queryUsername, 
                    "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
                }, app.config['SECRET_KEY'], algorithm="HS256"
            )
            return make_response(jsonify({"Username": dataUsername, "Password": dataPassword, "token":token, "Pesan":"Login Sukses"}), 200)
        return jsonify({"Pesan":"Login Gagal"})

api.add_resource(RegisterPengguna, "/api/v1/register", methods=["POST"])
api.add_resource(LoginUser, "/api/v1/login", methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)