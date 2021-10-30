import re
from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect, url_for
from flask import jsonify
from flask import session
from flask import current_app, g
from flask import make_response
from werkzeug import Response, exceptions
from utils import isEmailValid, isUsernameValid, isPasswordValid
from forms import Formulario_login, Formulario_Contacto

from db import get_db, close_db

import os
import yagmail as yagmail
from mensaje import mensajes # "BD": estará cargado sólo en memoria RAM.
from werkzeug.security import generate_password_hash, check_password_hash   # Permite realizar el hash a la contraseña


app = Flask(__name__)
app.secret_key = os.urandom(24)

#*********** Rutas ************

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def home():
    form=Formulario_Contacto(request.form)
    email=None
    if request.method == "POST":
        nombre = form.nombre.data
        email = form.email.data
        mensaje = form.mensaje.data
        error=None
        db = get_db()
        if email != None:
            db.execute(              # Se usa execute por seguridad informática
                'INSERT INTO Mensajes (nombre, correo, mensaje) VALUES (?,?,?)'
                ,
                (nombre, email, mensaje)
            )
            db.commit()  
            error = "Mensaje Enviado, gracias por escribirnos."
            flash(error)     
            return redirect('home')  #render_template("login.html")  
        else:
            return render_template("home.html")   
    #entra por GET   
    return render_template("home.html", form=form)


@app.route("/registro", methods=["GET", "POST"])
def registro():
    try:
        if request.method == 'POST':
            nombre=request.form['nombre']
            apellido=request.form['apellido']
            fecha_nacimiento=request.form['f_nacimiento']
            identificacion=request.form['identificacion']
            sexo=request.form['sexo']
            ciudad=request.form['ciudad']
            telefono=request.form['telefono']
            direccion=request.form['direccion']   
            eps=request.form['eps']        
            email=request.form['email']
            usuario=request.form['usuario']
            password=request.form['password']
            
            error=None
            db = get_db()
            
            if not nombre:
                error = "Debe registrar al menos un Nombre."
                flash(error)
            if not apellido:
                error = "Debe registrar al menos un Apellido."
                flash(error)
            if not identificacion:
                error = "Debe registrar su No. de Identificación."
                flash(error)
            if not email:
                error = "Debe registrar un Correo Electrónico."
                flash(error)
            if not usuario:
                error = "Usuario Requerido."
                flash(error)
            if not password:
                error = "Constraseña Requerida."
                flash(error)
            #VALIDACIÓN
            
            if not isUsernameValid(usuario):
                error="El usuario debe ser alfanumerico o incluir sólo '.','_'-'"
                flash(error)
                return render_template("registro.html")
            elif not isEmailValid(email):
                error="Correo inválido"
                flash(error)
                return render_template("registro.html")
            elif not isPasswordValid(password):
                error="La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres"   
                flash(error)
                return render_template("registro.html") #, form=form)
            
            user_correo=db.execute(              # Se usa execute por seguridad informática
                    'SELECT * FROM Usuarios WHERE correo = ?'
                    ,
                    (email,)
                ).fetchone()
            user_identificacion=db.execute(              # Se usa execute por seguridad informática
                    'SELECT * FROM Usuarios WHERE identificacion = ?'
                    ,
                    (identificacion,)
                ).fetchone()
            
            if user_identificacion is not None:
                error="Cédula ya registrada" 
                flash(error)
                return render_template("registro.html") #, form=form)
            if user_correo is not None:
                error="Correo electrónico ya existe" 
                flash(error) 
                return render_template("registro.html") #, form=form)
            else:
                password_cifrado = generate_password_hash(password)   #Encripta la constraseña
                db.execute(              # Se usa execute por seguridad informática
                    'INSERT INTO Usuarios (nombre, apellido, fecha_nacimiento, identificacion, sexo, ciudad, telefono, direccion, eps, correo, usuario, contrasena) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
                    ,
                    (nombre, apellido, fecha_nacimiento, identificacion, sexo, ciudad, telefono, direccion, eps, email, usuario, password_cifrado)
                )
                db.commit()       
                return redirect('login')  #render_template("login.html")
            
            #entró por GET    
        return render_template("registro.html")
    except:
        flash("Ocurrió un error no identificado")
        return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form=Formulario_login(request.form)      #carga los datos del formulario
    if request.method == "POST" and form.validate():
        
        usuario = form.usuario.data
        password = form.password.data
        error=None
        db = get_db()
                
        if not usuario:
            error="Usuario requerido."
            flash(error)
        if not password:
            error="Contraseña requerida."
            flash(error)
        if error!=None:
            return render_template("login.html")
        else: 
            user=db.execute(              # Se usa execute por seguridad informática
                'SELECT id, nombre, apellido, fecha_nacimiento, identificacion, sexo, ciudad, telefono, direccion, eps, correo, usuario, contrasena FROM Usuarios WHERE usuario = ?'   #                    'SELECT * FROM Usuarios WHERE usuario = ? and contrasena = ?
                ,
                (usuario,)
            ).fetchone()  
            if user is None: 
                error="El usuario no Existe"
                flash(error)
            else:
                usuario_valido = check_password_hash(user[12], password)     #Compara las constraseñas    
                if usuario_valido:
                    flash('inicio sesión, Bienvenido {}'.format(form.usuario.data))
                #    flash(format(form.password.data)) 
                    session.clear()
                    session['id_usuario']=user[0]
                    response = make_response( redirect(url_for('menuPaciente')))   # Cookie
                    response.set_cookie('username', usuario)
                    
                    return response  #render_template("menuPaciente.html")
                flash("Usuario o Contraseña No Válidos")
                return render_template("login.html", form=form)
        
    #Entró por GET    
    return render_template("login.html", form=form)

@app.before_request
def cargar_usuario_registrado():
    id_usuario = session.get('id_usuario')
    if id_usuario is None:
        g.user=None
    else:
        g.user = get_db().execute(
            'SELECT id, nombre, apellido, fecha_nacimiento, identificacion, sexo, ciudad, telefono, direccion, eps, correo, usuario, contrasena FROM Usuarios WHERE id = ?'   #                    'SELECT * FROM Usuarios WHERE usuario = ? and contrasena = ?
            ,
            (id_usuario,)    
        ).fetchone() 

@app.route("/menuAdmon", methods=["GET", "POST"])
def menuAdmon():
    return render_template("menuAdmon.html")

@app.route("/menuMedico", methods=["GET", "POST"])
def menuMedico():
    return render_template("menuMedico.html")

@app.route("/menuPaciente", methods=["GET", "POST"])
def menuPaciente():
    return render_template("menuPaciente.html")

@app.route("/asignacionCitas", methods=["GET", "POST"])
def asignacionCitas():
    return render_template("asignacionCitas.html")

@app.route('/mensaje')
def message():
     return jsonify({"Mensajes": mensajes})
 

@app.route('/logout')
def logout():
    session.clear()
    return redirect('login')


"""
@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    return "Página de perfil de usuario Administrador"

@app.route("/agenda", methods=["GET", "POST"])

def agenda():
    return "Página de Agenda de Citas"

@app.route("/reportes", methods=["GET", "POST"])
def reportes():
    return "Página de Reportes Médicos"

@app.route("/perfil_Medico", methods=["GET"])
def perfil():
    return "Página de perfil de usuario Médico"

@app.route("/programacion", methods=["GET", "POST"])
def programación():
    return "Página de Programación de Citas"

@app.route("/programacion/<id_reporte>", methods=["GET", "POST"])
def reporte(id_reporte):
    return "Página de Generación de Reportes Médicos para:    """ # {id_reporte}"
"""

@app.route("/perfil_Paciente", methods=["GET", "POST"])
def perfil_Paciente():
    return "Página de perfil de Paciente"

@app.route("/asignacionCitas", methods=["GET", "POST"])
def asignacionCitas():
    return "Página de Asignacion de Citas"

@app.route("/calificacion", methods=["GET", "POST"])
def calificacion():
    return "Página de Calificacion de atención Médica"


if __name__=="__main__":
	app.run(debug=True)
 """
 
#if __name__ == '__main__':                        # Certificado SSL
#    app.run( host='127.0.0.1', port =443, ssl_context=('micertificado.pem', 'llaveprivada.pem') )
 