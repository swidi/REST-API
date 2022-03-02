from flask import Flask
from flask_restful import Resource, Api, reqparse
import sqlite3 as sl

app = Flask(__name__)
api = Api(app)
con = sl.connect('customer.db', check_same_thread=False)
cur = con.cursor()
parser = reqparse.RequestParser()
parser.add_argument("first_name")
parser.add_argument("last_name")
parser.add_argument("email")

cur.execute("""CREATE TABLE IF NOT EXISTS Customer(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, email TEXT);""")

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Customer(Resource):
    def post(self):
        args = parser.parse_args()
        first_name = args["first_name"]
        last_name = args["last_name"]
        email = args["email"]
        print("adding", first_name, last_name, email)
        cur.execute("INSERT INTO Customer(first_name, last_name, email) values(\"{first_name}\", \"{last_name}\", \"{email}\");".format(first_name=first_name, last_name=last_name, email=email))
        con.commit()

    def get(self, customer_id):
        cur.execute("SELECT * FROM Customer where id={}".format(customer_id))
        row = cur.fetchone()
        return row

    def delete(self, customer_id):
        cur.execute("DELETE FROM Customer where id={}".format(customer_id))
        return "Deleted!"

api.add_resource(Customer, '/customer', '/customer/<customer_id>')

if __name__ == '__main__':
    app.run(debug=True)
