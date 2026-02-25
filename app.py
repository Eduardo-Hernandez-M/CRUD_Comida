import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

#crear instancia
app =  Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Modelo de la base de datos
class Comidas(db.Model):
    __tablename__ = 'comidas'
    id_comida = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    precio = db.Column(db.String)

    def to_dict(self):
        return{
            'id_comida': self.id_comida,
            'nombre': self.nombre,
            'precio': self.precio,
        }


#Ruta raiz
@app.route('/comidas')
def index():
    #Trae todos las comidas
    comidas = Comidas.query.all()
    #return estudiantes
    return render_template('index.html', comidas=comidas)

if __name__ == '__main__':
    app.run(debug=True)