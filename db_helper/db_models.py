from sqlalchemy.ext.hybrid import hybrid_property

from app import db, UserMixin

class users(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(), unique=True)
    nombre_completo = db.Column(db.String(100))
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, cedula, nombre_completo,username,email,password):
        self.cedula = cedula
        self.nombre_completo = nombre_completo
        self.username = username
        self.email = email
        self.password = password

class pediddos_por_producto(db.Model):
    __tablename__ = 'pediddos_por_producto'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer,db.ForeignKey('pedido.id'))
    producto_id = db.Column(db.Integer,db.ForeignKey('producto.id'))
    producto = db.relationship("producto", back_populates="pedidos")
    pedido = db.relationship("pedido", back_populates="productos")




class pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    fecha_pedido = db.Column(db.Date)
    nombre_completo_cliente = db.Column(db.String(100))
    cedula_cliente = db.Column(db.String(30), unique=True)
    direccion_cliente = db.Column(db.String(50), unique=True)
    correo_cliente = db.Column(db.String(100))
    moneda = db.Column(db.String(100))
    productos =  db.relationship('pediddos_por_producto', back_populates="pedido")

    def __init__(self, fecha_pedido, nombre_completo_cliente,cedula_cliente,direccion_cliente,correo_cliente,moneda):
        self.fecha_pedido = fecha_pedido
        self.nombre_completo_cliente = nombre_completo_cliente
        self.cedula_cliente = cedula_cliente
        self.direccion_cliente = direccion_cliente
        self.correo_cliente = correo_cliente
        self.moneda = moneda

class producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    codigo_producto = db.Column(db.String())
    nombre_producto = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)
    unidad_de_medida_de_la_cantidad = db.Column(db.Float)
    total = db.column_property(unidad_de_medida_de_la_cantidad * cantidad)
    pedidos =  db.relationship('pediddos_por_producto', back_populates="producto")



    def __init__(self, codigo_producto, nombre_producto,cantidad,unidad_de_medida_de_la_cantidad):
        self.codigo_producto = codigo_producto
        self.nombre_producto = nombre_producto
        self.cantidad = cantidad
        self.unidad_de_medida_de_la_cantidad = unidad_de_medida_de_la_cantidad


