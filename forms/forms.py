
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

class login_form(FlaskForm):
    user_name = StringField('nombre de usuario', validators=[InputRequired(), Length(min= 4, max=15)])
    password = PasswordField('contraseña', validators=[InputRequired(), Length(min = 4, max = 100)])

class generar_factura_form(FlaskForm):
    codigo_pedido = StringField('codigo pedido', validators=[InputRequired(), Length(min= 1, max=30)])



