CREATE TABLE Cliente (
    id INTEGER NOT NULL, 
    nombre VARCHAR(100) NOT NULL, 
    direccion VARCHAR(200), 
    correo_electronico VARCHAR(100), 
    telefono VARCHAR(20), 
    PRIMARY KEY (id)
);

CREATE TABLE Producto (
    id INTEGER NOT NULL, 
    nombre VARCHAR(100) NOT NULL, 
    precio FLOAT NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE Pedido (
    id INTEGER NOT NULL, 
    cliente_id INTEGER NOT NULL, 
    producto_id INTEGER NOT NULL, 
    precio_total FLOAT NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(cliente_id) REFERENCES Cliente (id), 
    FOREIGN KEY(producto_id) REFERENCES Producto (id)
);
