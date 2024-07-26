from flask import Flask, app, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pedidos/<int:pedido_id>', methods=['GET'])
def get_pedido(pedido_id):
    conn = sqlite3.connect('Proyecto_Final.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Pedido.id, Cliente.nombre, Producto.nombre, Pedido.unidades, Pedido.precio_total
        FROM Pedido
        JOIN Cliente ON Pedido.cliente_id = Cliente.id
        JOIN Producto ON Pedido.producto_id = Producto.id
        WHERE Pedido.id = ?
    """, (pedido_id,))
    pedido = cursor.fetchone()
    conn.close()

    if pedido:
        data = {
            "success": True,
            "pedido": {
                "id": pedido[0],
                "cliente": pedido[1],
                "producto": pedido[2],
                "unidades": pedido[3],
                "precio_total": pedido[4]
            }
        }
    else:
        data = {
            "success": False
        }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
