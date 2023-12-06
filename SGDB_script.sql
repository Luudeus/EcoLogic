CREATE DATABASE SGDB;
USE SGDB;
CREATE TABLE Book (
    id_book INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    anio YEAR,
    genero VARCHAR(100),
    stock INT NOT NULL
);

CREATE TABLE User (
    RUT VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    correo VARCHAR(255),
    permisos VARCHAR(255),
    contrasenia VARCHAR(255)
);

CREATE TABLE Lending (
    order_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    RUT_User VARCHAR(10) NOT NULL,
    id_book INT NOT NULL,
    fecha_entrega DATE,
    fecha_devolucion DATE,
    estado VARCHAR(50),
    FOREIGN KEY (RUT_User) REFERENCES User(RUT),
    FOREIGN KEY (id_book) REFERENCES Book(id_book)
);


INSERT INTO Book(titulo, autor, anio , genero, stock)
VALUES('R para ciencia de datos', 'Pachá Mauricio', '2021', 'informatica', '10');

INSERT INTO Book(titulo, autor, anio, genero, stock)
VALUES('Introducción a la ciencia animal', 'Pond Wilson G', '2006', 'Zootecnia', '6');

INSERT INTO Book(titulo, autor, anio, genero, stock)
VALUES('Ciencia y tecnología','Monckerberg Fernando', '1989', 'Ciencia y tecnología', '13');

INSERT INTO Book(titulo, autor, anio, genero, stock)
VALUES('Ciencia recreativa:instrumentos de medicion', 'Planeta De Agostoni', '1992', 'Ciencia Experimentos', '6');

INSERT INTO Book(titulo, autor, anio, genero, stock)
VALUES('Ciencia recreativa : escalas de sonido', 'Planeta De Agostoni', '1992', 'Ciencia recreativa', '9');

INSERT INTO Book(titulo, autor, anio, genero, stock)
VALUES('Instrumento musicales : artesania y ciencia', 'Massmann Herbert', '1993', 'Instrumentos musicales', '5');

INSERT INTO Book(titulo, autor, anio, genero, stock)
VALUES('Filosofía ciencia y técnica', 'Heidegger Martin', '2007', 'Tecnología Filosofía', '7');

INSERT INTO Book(titulo, autor, anio, genero, stock)
VALUES('Química : la ciencia central', 'Brown Theodore L', '2009', 'Química', '9');

INSERT INTO Book(titulo, autor, anio, genero, stock)
VALUES('Comunicación humana : ciencia social', 'Fernández Collado Carlos', '1986', 'Comunicación en ciencias sociales', '3');


