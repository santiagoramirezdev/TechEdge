from flask import Flask, render_template, redirect, url_for, Blueprint

from flask_bootstrap import Bootstrap
from app import app, login_manager
from db_helper.db_models import *
from forms import forms
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

Bootstrap(app)
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask import session, abort

from fpdf import FPDF


class HomeView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('home.html')


admin = Admin(app, index_view=HomeView(name='Home'), template_mode='bootstrap4')


class secure_model_view(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)
            return redirect('/')

class productos_por_pedidoModelView(ModelView):
    """
    """
    column_display_pk = True
    can_delete = True
    can_edit = True
    column_default_sort = 'id'
    column_searchable_list = ['id']

    def is_accessible(self):
        if "logged_in" in session:
            print("estoy logeado voy a retornar true")
            return True
        else:
            abort(403)
            return redirect('/')


class productosModelView(ModelView):
    """
    """
    column_display_pk = True
    can_delete = True
    can_edit = True
    column_default_sort = 'id'
    column_searchable_list = ['id']

    def is_accessible(self):
        if "logged_in" in session:
            print("estoy logeado voy a retornar true")
            return True
        else:
            abort(403)
            return redirect('/')


class pedidosModelView(ModelView):
    """
    """
    column_display_pk = True
    can_delete = True
    can_edit = True
    column_default_sort = 'id'
    column_searchable_list = ['id']
    column_hide_backrefs = True

    def is_accessible(self):
        if "logged_in" in session:
            print("estoy logeado voy a retornar true")
            return True
        else:
            abort(403)
            return redirect('/')


class usuariosModelView(ModelView):
    """
    """
    column_display_pk = True
    can_delete = False
    can_edit = True
    column_default_sort = 'id'
    column_searchable_list = ['id', 'username']

    def is_accessible(self):
        if "logged_in" in session:
            print("estoy logeado voy a retornar true")
            return True
        else:
            abort(403)
            return redirect('/')


techedge = Blueprint('techedge', __name__, url_prefix='/')


@app.route('/')
def index():
    session.clear()
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.login_form()
    # valida si el formulario ha sido completado
    if form.validate_on_submit():
        user = users.query.filter_by(username=form.user_name.data).first()
        if user:
            if user.password == form.password.data:
                session['logged_in'] = True
                return redirect("/admin")

    return render_template('login.html', form=form)


def generate_pdf(productos_list):
    """este metodo genera el pdf de reporte"""
    if productos_list != None:
        cabecera = ""
        pedido = productos_list[0].pedido
        cabecera = cabecera +"id del pedido:  " + str(pedido.id) + "\n" + \
                   "nombre_completo_cliente: " + str(pedido.nombre_completo_cliente) + "\n" + \
                   "cedula_cliente: " + str(pedido.cedula_cliente) + "\n" + \
                   "fecha_pedido: " + str(pedido.fecha_pedido) + "\n" + \
                   "correo_cliente: " + str(pedido.correo_cliente) + "\n" + \
                   "direccion:cliente: " + str(pedido.direccion_cliente) + "\n" + \
                   "moneda_pedido: " + str(pedido.moneda) + "\n" + "\n" + "\n"

        total_factura = 0
        cuerpo = ""
        for i in productos_list:
            cuerpo = cuerpo + \
                     "codigo_producto: " + str(i.producto.codigo_producto) + "\n" + \
                     "id_producto: " + str(i.producto.id) + "\n" + \
                     "nombre_producto: " + str(i.producto.nombre_producto) + "\n" + \
                     "unidad_de_medidad_de_la_cantidad_producto: " + str(i.producto.unidad_de_medida_de_la_cantidad) + "\n" + \
                     "total_producto: " + str(i.producto.total) + "\n" + \
                     "cantidad_producto: " + str(i.producto.cantidad) + "\n" + "\n" + "\n"
            total_factura = total_factura + i.producto.total

        titulo = "pdf reporte " + "\n" + "\n" + "\n"

        mensaje = titulo + cabecera + cuerpo+"el total de la factura es: "+str(total_factura)
        file = open("archivo.txt", "w")
        file.write(mensaje)
        file.close()

        pdf = FPDF()

        pdf.add_page()

        pdf.set_font("Arial", size=15)

        archivo = open("archivo.txt", "r")

        for x in archivo:
            pdf.cell(200, 10, txt=x, ln=1, align='C')

        pdf.output("GFG.pdf")


@app.route('/generar_factura', methods=['GET', 'POST'])
def generar_factura():
    form = forms.generar_factura_form()
    # valida si el formulario ha sido completado
    if form.validate_on_submit():
        print("se va a generar el pdf con el codigo" + form.codigo_pedido.data)
        productos_list = pediddos_por_producto.query.filter_by(pedido_id=form.codigo_pedido.data).all()
        generate_pdf(productos_list)

        # se genera el pdf
        return redirect("/admin")

    return render_template("/generar_pdf.html", form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))


# --------------------model views-------------------

admin.add_view(usuariosModelView(users, db.session))
admin.add_view(productos_por_pedidoModelView(pediddos_por_producto, db.session))
admin.add_view(pedidosModelView(pedido, db.session))
admin.add_view(productosModelView(producto, db.session))
