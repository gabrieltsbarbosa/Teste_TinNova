from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

basedir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cars.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

api = Api(app,
          doc='/', 
          title='An API for cars sellers', 
          description='A simple REST API for cars sellers')

db = SQLAlchemy(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    veiculo = db.Column(db.String(40), nullable=False)
    marca = db.Column(db.String(40), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    cor = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.String(255))
    vendido = db.Column(db.Boolean, default=False, nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    updated = db.Column(db.DateTime(), nullable=False)
    
    def __repr__(self):
        return self.veiculo
    

car_model = api.model(
    'Car',
    {
        'id': fields.Integer,
        'veiculo': fields.String,
        'marca': fields.String,
        'ano': fields.Integer,
        'cor': fields.String,
        'descricao': fields.String,
        'vendido': fields.Boolean
    }
)

car_model_for_update_or_post = api.model(
    'Car',
    {
        'veiculo': fields.String,
        'marca': fields.String,
        'ano': fields.Integer,
        'cor': fields.String,
        'descricao': fields.String,
        'vendido': fields.Boolean
    }
)

car_model_detailed = api.model(
    'Car',
    {
        'id': fields.Integer,
        'veiculo': fields.String,
        'marca': fields.String,
        'ano': fields.Integer,
        'cor': fields.String,
        'descricao': fields.String,
        'vendido': fields.Boolean,
        'created': fields.DateTime,
        'updated': fields.DateTime
    }
)
                           
@api.route('/veiculos')
class Cars(Resource):    
    
    @api.marshal_list_with(car_model, code = 200, envelope = "Veiculos")
    def get(self):
        """
        Caso sem filtro retorna todos os veículos, com filtro retorna de acordo com os parametros
        """
        marca = request.args.get('marca')
        ano = request.args.get('ano')
        cor = request.args.get('cor')
        
        if marca == None and ano == None and cor == None:
            cars = db.session.execute(
                db.select(db.text('*'))
                .where(Car.marca == marca, Car.ano == ano, Car.cor == cor)).all()
            
        else:
            cars = Car.query.all()
            
        
        return cars, 200
    
    @api.marshal_with(car_model, code = 201, envelope = "Veiculo")
    @api.doc(body = car_model_for_update_or_post)
    def post(self):
        """
        Adiciona um novo veículo
        """
        data = request.get_json()
        
        veiculo = data.get('veiculo')
        marca = data.get('marca')
        ano = data.get('ano')
        cor = data.get('cor')
        descricao = data.get('descricao')
        vendido = data.get('vendido')
        created = datetime.now()
        
        new_car = Car(veiculo = veiculo,
                       marca = marca,
                       ano = ano,
                       cor = cor,
                       descricao = descricao,
                       vendido = vendido,
                       created = created,
                       updated = created)
        
        db.session.add(new_car)
        db.session.commit()
        
        return new_car, 201
    

@api.route('/veiculos/<int:id>')
class CarsResource(Resource):
    
    @api.marshal_with(car_model_detailed, code = 200, envelope = "veiculo")
    def get(self, id):
        """
        Retorna os detalhes do veículo
        """
        veiculo = Car.query.get_or_404(id)
        
        return veiculo
    
    @api.marshal_with(car_model, code = 200, envelope = "veiculo")
    @api.expect(car_model_for_update_or_post)
    def put(self, id):
        """
        Atualiza os dados de um veículo
        """
        car_to_update = Car.query.get_or_404(id)
        
        data = request.get_json()
        
        car_to_update.veiculo = data.get('veiculo')
        car_to_update.marca = data.get('marca')
        car_to_update.ano = data.get('ano')
        car_to_update.cor = data.get('cor')
        car_to_update.descricao = data.get('descricao')
        car_to_update.vendido = data.get('vendido')
        car_to_update.updated = datetime.now()
        
        db.session.commit()
        
        return car_to_update, 200
    
    @api.marshal_with(car_model, code = 200, envelope = "veiculo")
    @api.expect(car_model_for_update_or_post)
    def patch(self, id):
        """
        Atualiza apenas alguns dados do veículo
        """
        car_to_update = Car.query.get_or_404(id)
        
        data = request.get_json()
        
        car_to_update.veiculo = data.get('veiculo') if data.get('veiculo') != None else car_to_update.veiculo
        car_to_update.marca = data.get('marca') if data.get('marca') != None else car_to_update.marca
        car_to_update.ano = data.get('ano') if data.get('ano') != None else car_to_update.ano
        car_to_update.cor = data.get('cor') if data.get('cor') != None else car_to_update.cor
        car_to_update.descricao = data.get('descricao') if data.get('descricao') != None else car_to_update.descricao
        car_to_update.vendido = data.get('vendido') if data.get('vendido') != None else car_to_update.vendido
        car_to_update.updated = datetime.now()
        
        db.session.commit()
        
        return car_to_update, 200
    
    @api.marshal_with(car_model, code = 200, envelope = "carro deletado")
    def delete(self, id):
        """
        Apaga o veículo.
        """
        car_to_delete = Car.query.get_or_404(id)
        
        db.session.delete(car_to_delete)
        
        db.session.commit()
        
        return car_to_delete, 200
    
    
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Car': Car
    }
    
if __name__ == '__main__':
    assert os.path.exists('.env')
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug = True)