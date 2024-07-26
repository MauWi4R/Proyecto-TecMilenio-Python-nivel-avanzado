import sqlite3

# Función para inicializar la base de datos
def inicializar_db():
    conn = sqlite3.connect('Proyecto_Final.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cliente (
        id INTEGER PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        direccion VARCHAR(200),
        correo_electronico VARCHAR(100),
        telefono VARCHAR(20)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Producto (
        id INTEGER PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        precio FLOAT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pedido (
        id INTEGER PRIMARY KEY,
        cliente_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        precio_total FLOAT NOT NULL,
        FOREIGN KEY(cliente_id) REFERENCES Cliente (id),
        FOREIGN KEY(producto_id) REFERENCES Producto (id)
    )
    ''')

    conn.commit()
    conn.close()

# Función para verificar la conexión a la base de datos
def verificar_conexion_db():
    try:
        conn = sqlite3.connect('Proyecto_Final.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        print("Tablas en la base de datos:", tablas)
        
        cursor.execute("INSERT INTO Cliente (nombre, direccion) VALUES (?, ?)", ("Cliente Prueba", "Dirección Prueba"))
        conn.commit()
        
        cursor.execute("SELECT * FROM Cliente WHERE nombre = ?", ("Cliente Prueba",))
        resultado = cursor.fetchone()
        if resultado:
            print("Inserción de prueba exitosa:", resultado)
        else:
            print("La inserción de prueba falló")
        
        cursor.execute("DELETE FROM Cliente WHERE nombre = ?", ("Cliente Prueba",))
        conn.commit()
        
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
        return False

# Funciones para gestionar clientes
def agregar_cliente():
    nombre = input("Nombre del cliente: ")
    direccion = input("Dirección: ")
    correo = input("Correo electrónico: ")
    telefono = input("Teléfono: ")
    
    try:
        with sqlite3.connect('Proyecto_Final.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Cliente (nombre, direccion, correo_electronico, telefono)
                VALUES (?, ?, ?, ?)
            """, (nombre, direccion, correo, telefono))
            
            print(f"Cliente agregado con éxito. ID: {cursor.lastrowid}")
            
            cursor.execute("SELECT * FROM Cliente WHERE id = ?", (cursor.lastrowid,))
            cliente = cursor.fetchone()
            if cliente:
                print("Cliente insertado:", cliente)
            else:
                print("No se pudo verificar la inserción del cliente")
    except sqlite3.Error as e:
        print(f"Error al agregar el cliente: {e}")

def ver_clientes():
    try:
        with sqlite3.connect('Proyecto_Final.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cliente")
            clientes = cursor.fetchall()
            for cliente in clientes:
                print(f"ID: {cliente[0]}, Nombre: {cliente[1]}, Dirección: {cliente[2]}, Correo: {cliente[3]}, Teléfono: {cliente[4]}")
    except sqlite3.Error as e:
        print(f"Error al ver los clientes: {e}")

def actualizar_cliente():
    cliente_id = input("Ingrese el ID del cliente a actualizar: ")
    nombre = input("Nuevo nombre (deje en blanco para no cambiar): ")
    direccion = input("Nueva dirección (deje en blanco para no cambiar): ")
    correo = input("Nuevo correo (deje en blanco para no cambiar): ")
    telefono = input("Nuevo teléfono (deje en blanco para no cambiar): ")
    
    updates = []
    values = []
    if nombre:
        updates.append("nombre = ?")
        values.append(nombre)
    if direccion:
        updates.append("direccion = ?")
        values.append(direccion)
    if correo:
        updates.append("correo_electronico = ?")
        values.append(correo)
    if telefono:
        updates.append("telefono = ?")
        values.append(telefono)
    
    if updates:
        try:
            with sqlite3.connect('Proyecto_Final.db') as conn:
                cursor = conn.cursor()
                query = f"UPDATE Cliente SET {', '.join(updates)} WHERE id = ?"
                values.append(cliente_id)
                cursor.execute(query, tuple(values))
                print("Cliente actualizado con éxito.")
        except sqlite3.Error as e:
            print(f"Error al actualizar el cliente: {e}")
    else:
        print("No se realizaron cambios.")

def eliminar_cliente():
    cliente_id = input("Ingrese el ID del cliente a eliminar: ")
    try:
        with sqlite3.connect('Proyecto_Final.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Cliente WHERE id = ?", (cliente_id,))
            if cursor.rowcount > 0:
                print("Cliente eliminado con éxito.")
            else:
                print("No se encontró el cliente.")
    except sqlite3.Error as e:
        print(f"Error al eliminar el cliente: {e}")

# Funciones para gestionar productos
def agregar_producto():
    nombre = input("Nombre del producto: ")
    precio = float(input("Precio del producto: "))
    
    try:
        with sqlite3.connect('Proyecto_Final.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Producto (nombre, precio) VALUES (?, ?)", (nombre, precio))
            print(f"Producto agregado con éxito. ID: {cursor.lastrowid}")
    except sqlite3.Error as e:
        print(f"Error al agregar el producto: {e}")

def ver_productos():
    try:
        with sqlite3.connect('Proyecto_Final.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Producto")
            productos = cursor.fetchall()
            for producto in productos:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Precio: ${producto[2]:.2f}")
    except sqlite3.Error as e:
        print(f"Error al ver los productos: {e}")

def actualizar_producto():
    producto_id = input("Ingrese el ID del producto a actualizar: ")
    nombre = input("Nuevo nombre (deje en blanco para no cambiar): ")
    precio = input("Nuevo precio (deje en blanco para no cambiar): ")
    
    updates = []
    values = []
    if nombre:
        updates.append("nombre = ?")
        values.append(nombre)
    if precio:
        updates.append("precio = ?")
        values.append(float(precio))
    
    if updates:
        try:
            with sqlite3.connect('Proyecto_Final.db') as conn:
                cursor = conn.cursor()
                query = f"UPDATE Producto SET {', '.join(updates)} WHERE id = ?"
                values.append(producto_id)
                cursor.execute(query, tuple(values))
                if cursor.rowcount > 0:
                    print("Producto actualizado con éxito.")
                else:
                    print("No se encontró el producto o no se realizaron cambios.")
        except sqlite3.Error as e:
            print(f"Error al actualizar el producto: {e}")
    else:
        print("No se realizaron cambios.")

def eliminar_producto():
    producto_id = input("Ingrese el ID del producto a eliminar: ")
    try:
        with sqlite3.connect('Proyecto_Final.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Producto WHERE id = ?", (producto_id,))
            if cursor.rowcount > 0:
                print("Producto eliminado con éxito.")
            else:
                print("No se encontró el producto.")
    except sqlite3.Error as e:
        print(f"Error al eliminar el producto: {e}")


# Funciones para gestionar pedidos

def agregar_pedido():
    # Conectar a la base de datos
    conn = sqlite3.connect('Proyecto_Final.db')
    cursor = conn.cursor()

    # Solicitar nombre del cliente
    nombre_cliente = input("Ingrese el nombre del cliente: ")

    # Verificar si el cliente existe
    cursor.execute("SELECT id FROM Cliente WHERE nombre = ?", (nombre_cliente,))
    cliente = cursor.fetchone()
    
    if cliente is None:
        print("El cliente no existe en la base de datos.")
        conn.close()
        return
    else:
        cliente_id = cliente[0]

    # Inicializar variables para el pedido
    productos = []
    precio_total = 0

    # Solicitar productos hasta que el usuario termine
    while True:
        nombre_producto = input("Ingrese el nombre del producto (o 'fin' para terminar): ")
        if nombre_producto.lower() == 'fin':
            break

        # Verificar si el producto existe
        cursor.execute("SELECT id, precio FROM Producto WHERE nombre = ?", (nombre_producto,))
        producto = cursor.fetchone()

        if producto is None:
            print("Producto no encontrado.")
        else:
            producto_id, precio = producto
            productos.append((producto_id, precio))
            precio_total += precio

    # Crear el pedido
    if productos:
        cursor.execute("INSERT INTO Pedido (cliente_id, producto_id, precio_total) VALUES (?, ?, ?)",
                       (cliente_id, productos[0][0], precio_total))
        pedido_id = cursor.lastrowid

        # Si hay más de un producto, insertarlos en la tabla Pedido
        for producto_id, _ in productos[1:]:
            cursor.execute("INSERT INTO Pedido (cliente_id, producto_id, precio_total) VALUES (?, ?, ?)",
                           (cliente_id, producto_id, 0))

        print(f"Pedido creado con éxito. ID del pedido: {pedido_id}")
        print(f"Total del pedido: ${precio_total:.2f}")

    # Preguntar si desea imprimir el ticket
        imprimir_ticket = input("¿Desea imprimir el ticket? (s/n): ")
        if imprimir_ticket.lower() == 's':
            # Crear el ticket
            try:
                cursor.execute("SELECT nombre FROM Cliente WHERE id = ?", (cliente_id,))
                cliente_nombre = cursor.fetchone()[0]

                cursor.execute("SELECT nombre FROM Producto WHERE id = ?", (productos[0][0],))
                producto_nombre = cursor.fetchone()[0]

                unidades = len(productos)

                with open(f"ticket_{pedido_id}.txt", "w") as ticket_file:
                    ticket_file.write(
                        f"===== TICKET DE COMPRA =====\n"
                        f"ID del Pedido: {pedido_id}\n"
                        f"Cliente: {cliente_nombre}\n"
                        f"Producto: {producto_nombre}\n"
                        f"Unidades: {unidades}\n"
                        f"Precio Total: ${precio_total:.2f}\n"
                        f"=============================\n"
                    )
                print(f"Ticket guardado como ticket_{pedido_id}.txt")
            except Exception as e:
                print(f"Error al crear el ticket: {e}")
    else:
        print("No se agregaron productos al pedido.")

    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()

def ver_pedidos():
    try:
        with sqlite3.connect('Proyecto_Final.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Pedido.id, Cliente.nombre, Producto.nombre, Pedido.precio_total
                FROM Pedido
                JOIN Cliente ON Pedido.cliente_id = Cliente.id
                JOIN Producto ON Pedido.producto_id = Producto.id
            """)
            pedidos = cursor.fetchall()
            for pedido in pedidos:
                print(f"ID Pedido: {pedido[0]}, Cliente: {pedido[1]}, Producto: {pedido[2]}, Precio Total: ${pedido[3]:.2f}")
    except sqlite3.Error as e:
        print(f"Error al ver los pedidos: {e}")

def eliminar_pedido():
    pedido_id = input("Ingrese el ID del pedido a eliminar: ")
    try:
        with sqlite3.connect('Proyecto_Final.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Pedido WHERE id = ?", (pedido_id,))
            if cursor.rowcount > 0:
                print("Pedido eliminado con éxito.")
            else:
                print("No se encontró el pedido.")
    except sqlite3.Error as e:
        print(f"Error al eliminar el pedido: {e}")

# Menús
def menu_clientes():
    while True:
        print("\n=== Gestión de Clientes ===")
        print("1. Agregar Cliente")
        print("2. Ver Clientes")
        print("3. Actualizar Cliente")
        print("4. Eliminar Cliente")
        print("5. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            agregar_cliente()
        elif opcion == '2':
            ver_clientes()
        elif opcion == '3':
            actualizar_cliente()
        elif opcion == '4':
            eliminar_cliente()
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

def menu_productos():
    while True:
        print("\n=== Gestión de Productos ===")
        print("1. Agregar Producto")
        print("2. Ver Productos")
        print("3. Actualizar Producto")
        print("4. Eliminar Producto")
        print("5. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            agregar_producto()
        elif opcion == '2':
            ver_productos()
        elif opcion == '3':
            actualizar_producto()
        elif opcion == '4':
            eliminar_producto()
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

def menu_pedidos():
    while True:
        print("\n=== Gestión de Pedidos ===")
        print("1. Crear Pedido")
        print("2. Ver Pedidos")
        print("3. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            agregar_pedido()
        elif opcion == '2':
            ver_pedidos()
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

def menu_principal():
    while True:
        print("\n===== Happy Burger - Menú Principal =====")
        print("1. Gestionar Clientes")
        print("2. Gestionar Productos")
        print("3. Gestionar Pedidos")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            menu_clientes()
        elif opcion == '2':
            menu_productos()
        elif opcion == '3':
            menu_pedidos()
        elif opcion == '4':
            print("Gracias por usar Happy Burger. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

# Función principal
def main():
    inicializar_db()
    if not verificar_conexion_db():
        print("La verificación de la base de datos falló. El programa se cerrará.")
        return
    menu_principal()

if __name__ == "__main__":
    main()
