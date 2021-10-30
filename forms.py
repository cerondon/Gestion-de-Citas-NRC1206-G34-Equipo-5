from wtforms import Form, StringField, TextField, PasswordField, validators, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import EmailField

class Formulario_login(Form):
    usuario = StringField ('Usuario:',
    [
        validators.DataRequired(message='Dato Requerido.'),
        validators.Length(min=4, max=25, message='La longitud debe estar entre 8 y 25 caracteres.')
    ])
    password = PasswordField ('Contraseña:',
    [
        validators.DataRequired(message='Dato Requerido.'),
        validators.Length(min=4, max=25, message='La longitud debe estar entre 8 y 25 caracteres.')
    ])
    recordar = BooleanField('recordar')    #check de recordar datos
    enviar=SubmitField('Iniciar')

class Formulario_Contacto(Form):
    nombre = StringField( 'Nombre')
    email = EmailField( 'Correo')
    mensaje = TextAreaField( 'Mensaje' )
    #operador=SelectField("Operador",choices=[("+","Sumar"),("-","Resta"),
	#						("*","Multiplicar"),("/","Dividir")])
    enviar = SubmitField( 'Enviar' )
    
class Formulario_Registro(Form):
    nombre = StringField( 'Nombre')
    email = EmailField( 'Correo')
    apellido = StringField( 'apellido' )
    fecha_nacimiento = StringField( 'fecha_nacimiento')
    
    usuario = StringField( 'usuario')
    identificacion = StringField( 'identificacion')
    password = StringField( 'password')
    sexo = StringField( 'sexo')
    c_password = StringField( 'c_password')
    telefono = StringField( 'telefono')
    direccion = StringField( 'direccion')
    eps = StringField( 'eps')
    nombre = StringField( 'Nombre')
    confirmar = SelectField('confirmar')
    registrar = SubmitField('Registrar')
   # limpiar = 
    