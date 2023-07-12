
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
CORS(app)



app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/mochileando"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100))
    country = db.Column(db.String(5))
    urlImg = db.Column(db.String(200))
    description = db.Column(db.String(400))

    def __init__(self, city, country, urlImg, description):
        self.city = city
        self.country = country
        self.urlImg = urlImg
        self.description = description

with app.app_context():
    db.create_all()  

class CardsSchema(ma.Schema):
    
    class Meta:
        fields = ("id", "city", "country", "urlImg", "description")

card_schema = CardsSchema()  
cards_schema = CardsSchema(many=True)

@app.route("/cards", methods=["GET"])
def get_cards():
    
    all_cards = Cards.query.all() 
    result = cards_schema.dump(all_cards)
    return jsonify(result)

@app.route("/cards/<id>", methods=["GET"])
def get_card(id):
    
    card = Cards.query.get(id)
    return card_schema.jsonify(card)

@app.route("/cards/<id>", methods=["DELETE"])
def delete_card(id):
    
    card = Cards.query.get(id)  
    db.session.delete(card) 
    db.session.commit() 
    return card_schema.jsonify(card)

@app.route("/cards", methods=["POST"])
def create_card():
    
    city = request.json["city"]  
    country = request.json["country"] 
    urlImg = request.json["urlImg"]  
    description = request.json["description"]  
    new_card = Cards(city, country, urlImg, description) 
    db.session.add(new_card)  
    db.session.commit()  
    return card_schema.jsonify(new_card) 

@app.route("/cards/<id>", methods=["PUT"]) 
def update_card(id):
    
    card = Cards.query.get(id) 

    card.country = request.json["country"]
    card.urlimg = request.json["urlImg"]
    card.description = request.json["description"]

    db.session.commit() 
    return card_schema.jsonify(card)

if __name__ == "__main__":
    app.run(debug=True, port=5000)