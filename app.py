from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

from productos import productos # "BD": estará cargado sólo en memoria RAM.

@app.route('/')
def index():
    return "Entro en la raiz."

@app.route('/productos')
def get_productos():
    return jsonify( { "productos": productos } )
   

@app.route('/productos/<string:nom_producto>')  # METODO GET
def get_producto(nom_producto):
    lista_productos = [ producto for producto in productos if producto['nombre'] == nom_producto ]
    if len(lista_productos) > 0:
        return jsonify( {"producto": lista_productos[0] } )
    return jsonify( { "message": "Producto {} no encontrado.".format(nom_producto) } )

@app.route('/productos', methods=['POST'])     # METODO POST
def add_producto():
    producto = request.json
    productos.append( producto )  
    return jsonify( {"message": "Producto {} agregado.".format(producto['nombre']), "productos": productos } )

@app.route('/productos/<string:nom_producto>', methods=['PUT'])   # METODO PUT
def update_producto(nom_producto):
    #1. Buscar el producto.
    lista_productos = [ producto for producto in productos if producto['nombre'] == nom_producto ]
    if len( lista_productos ) > 0:
        producto = lista_productos[0]
        
        #2. Actualizar.
        producto['nombre'] = request.json['nombre']
        producto['precio'] = request.json['precio']
        producto['cantidad'] = request.json['cantidad']
      
        #3. Dar respuesta al usuario.
        return jsonify( {"message": "Producto {} actualizado.".format(nom_producto), "productos": productos } )
    #4. Producto no encontrado.
    return jsonify( {"message": "Producto {} no encontrado.".format(nom_producto), "productos": productos } )

@app.route('/productos/<string:nom_producto>', methods=['DELETE'])     # METODO DELETE
def delete_producto(nom_producto):
    lista_productos = [ producto for producto in productos if producto['nombre'] == nom_producto ]
    if len( lista_productos ) > 0:
        producto = lista_productos[0]
        productos.remove( producto )
        return jsonify( { "message": "Producto {} eliminado.".format(nom_producto), "productos": productos } )
    # No encontrado:
    return jsonify( { "message": "Producto {} no encontrado.".format(nom_producto), "productos": productos } )

#******************************
if __name__ == '__main__':
    app.run(debug=True, port=5000)