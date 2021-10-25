from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

#*********** Rutas ************
@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
@app.route("/index", methods=['GET'])
def home():
    return render_template("home.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

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