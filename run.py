from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.app_context().push()

#mysql://usuario:password@host/BasedeDatos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:cr1st14N@localhost/db_todolist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

### creando tabla con el ORM ###

class Tarea(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    descripcion = db.Column(db.String(200),nullable=False)
    estado = db.Column(db.String(100),nullable=False)

    def __init__(self,descripcion,estado):
        self.descripcion = descripcion
        self.estado=estado

#esquemas#
ma = Marshmallow(app)
class TareaSchema(ma.Schema):
    class Meta:
        fields = ('id','descripcion','estado')


db.create_all()
print('se creo la tabla tarea en db')

@app.route('/tarea', methods=['POST'])
def set_tarea():
    descripcion = request.json['descripcion']
    estado = request.json['estado']

    #insert insto...
    nueva_tarea = Tarea(descripcion,estado)
    db.session.add(nueva_tarea)
    db.session.commit()

    data_schema = TareaSchema()

    context ={
        'status':True,
        'message':'registro exitoso',
        'content': data_schema.dump(nueva_tarea)
    }

    return jsonify(context)

@app.route('/tarea')
def get_tarea():
    data = Tarea.query.all()
    print(data)

    data_schema = TareaSchema(many=True)

    context ={
        'status':True,
        'content':data_schema.dump(data)
    }

    return jsonify(context)

@app.route('/tarea/<id>')
def get_tarea_id(id):
    data= Tarea.query.get(id)
    data_schema = TareaSchema()

    context ={
        'status':True,
        'content':data_schema.dump(data)
    }
    return jsonify(context)

@app.route('/tarea/<id>', methods=['PUT'])
def update_tarea(id):
    descripcion = request.json['descripcion']
    estado = request.json['estado']

    tarea_actual = Tarea.query.get(id)
    tarea_actual.descripcion = descripcion
    tarea_actual.estado = estado
    db.session.commit()

    data_schema = TareaSchema()
    context ={
        'status':True,
        'content':data_schema.dump(tarea_actual)
    }

    return jsonify(context)

@app.route('/tarea/<id>', methods=['DELETE'])
def delete_tarea(id):
    tarea = Tarea.query.get(id)
    db.session.delete(tarea)
    db.session.commit()

    data_schema = TareaSchema()

    context ={
        'status':True,
        'message':'tarea eliminada',
        'content':data_schema.dump(tarea)
    }

    return jsonify(context)

app.run(debug=True)