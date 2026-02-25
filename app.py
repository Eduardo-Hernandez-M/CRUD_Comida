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
    #return comidas
    return render_template('index.html', comidas=comidas)

@app.route('/comidas/new', methods=['GET','POST'])
def create_comida():
    if request.method == 'POST':
        #Agregar Comida
        id_comida = request.form['id_comida']
        nombre = request.form['nombre']
        precio = request.form['precio']

        nvo_comida = Comidas(id_comida=id_comida, nombre=nombre, precio=precio)

        db.session.add(nvo_comida)
        db.session.commit()

        return redirect(url_for('index'))
    
    #Aqui sigue si es GET
    return render_template('create_comida.html')

#Eliminar Comida
@app.route('/comidas/delete/<string:id_comida>')
def delete_comida(id_comida):
    comidas = Comidas.query.get(id_comida)
    if comidas:
        db.session.delete(comidas)
        db.session.commit()
    return redirect(url_for('index'))

#Actualizar Comida
@app.route('/comidas/update/<string:id_comida>', methods=['GET','POST'])
def update_comida(id_comida):
    comida = Comidas.query.get(id_comida)
    if request.method == 'POST':
        comida.nombre = request.form['nombre']
        comida.precio = request.form['precio']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_comida.html', comida=comida)

if __name__ == '__main__':
    app.run(debug=True)