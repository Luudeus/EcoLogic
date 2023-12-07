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


INSERT INTO Book (titulo, autor, anio, genero, stock) VALUES 
('Cien Años de Soledad', 'Gabriel García Márquez', 1967, 'Novela', 10),
('1984', 'George Orwell', 1949, 'Distopía', 15),
('El Principito', 'Antoine de Saint-Exupéry', 1943, 'Fábula', 20),
('Don Quijote de la Mancha', 'Miguel de Cervantes', 1605, 'Novela', 5),
('Hamlet', 'William Shakespeare', 1609, 'Tragedia', 10),
('El Hobbit', 'J.R.R. Tolkien', 1937, 'Fantasía', 12),
('Orgullo y Prejuicio', 'Jane Austen', 1813, 'Novela', 8),
('To Kill a Mockingbird', 'Harper Lee', 1960, 'Novela', 10),
('La Divina Comedia', 'Dante Alighieri', 1320, 'Poesía Épica', 7),
('Moby Dick', 'Herman Melville', 1851, 'Novela', 9),
('El Gran Gatsby', 'F. Scott Fitzgerald', 1925, 'Novela', 14),
('Guerra y Paz', 'León Tolstói', 1869, 'Novela', 6),
('Lolita', 'Vladimir Nabokov', 1955, 'Novela', 8),
('El Señor de los Anillos', 'J.R.R. Tolkien', 1954, 'Fantasía', 10),
('El Código Da Vinci', 'Dan Brown', 2003, 'Novela Misterio', 20),
('Harry Potter y la Piedra Filosofal', 'J.K. Rowling', 1997, 'Fantasía', 30),
('El Alquimista', 'Paulo Coelho', 1988, 'Novela', 12),
('Crimen y Castigo', 'Fiódor Dostoievski', 1866, 'Novela', 7),
('Anna Karenina', 'León Tolstói', 1877, 'Novela', 5),
('El guardián entre el centeno', 'J.D. Salinger', 1951, 'Novela', 11);



INSERT INTO User (RUT, nombre, correo, permisos, contrasenia) VALUES 
('12345678-9', 'Juan Pérez', 'juanperez@mail.com', 'usuario', 'contraseña123'),
('23456789-0', 'Ana Gómez', 'anagomez@mail.com', 'usuario', 'contraseña456'),
('34567890-1', 'Carlos Ruiz', 'carlosruiz@mail.com', 'usuario', 'contraseña789'),
('45678901-2', 'María López', 'marialopez@mail.com', 'usuario', 'pass1234'),
('56789012-3', 'Lucía Hernández', 'luciahernandez@mail.com', 'usuario', 'pass5678'),
('67890123-4', 'Miguel Ángel', 'miguelangel@mail.com', 'usuario', 'mypass123'),
('78901234-5', 'Sofía Martínez', 'sofiamartinez@mail.com', 'usuario', 'sofia123'),
('89012345-6', 'Diego Torres', 'diegotorres@mail.com', 'usuario', 'diego123'),
('90123456-7', 'Andrea Jiménez', 'andreajimenez@mail.com', 'usuario', 'andrea123'),
('01234567-8', 'Roberto García', 'robertogarcia@mail.com', 'usuario', 'roberto123'),
('11223344-5', 'Sara Molina', 'saramolina@mail.com', 'usuario', 'sara1234'),
('22334455-6', 'Luis Navarro', 'luisnavarro@mail.com', 'usuario', 'luis1234'),
('33445566-7', 'Marta Sánchez', 'martasanchez@mail.com', 'usuario', 'marta1234'),
('44556677-8', 'Fernando Castro', 'fernandocastro@mail.com', 'usuario', 'fernando123'),
('55667788-9', 'Laura Ortiz', 'lauraortiz@mail.com', 'usuario', 'laura123'),
('66778899-0', 'Daniel Romero', 'danielromero@mail.com', 'usuario', 'daniel123'),
('77889900-1', 'Patricia Navarrete', 'patricianavarrete@mail.com', 'usuario', 'patricia123'),
('88990011-2', 'Iván Morales', 'ivanmorales@mail.com', 'usuario', 'ivan123'),
('99001122-3', 'Carmen Díaz', 'carmendiaz@mail.com', 'usuario', 'carmen123'),
('10012233-4', 'Alejandro Vega', 'alejandrovega@mail.com', 'usuario', 'alejandro123');


INSERT INTO Lending (RUT_User, id_book, fecha_entrega, fecha_devolucion, estado) VALUES 
('12345678-9', 1, '2023-01-01', '2023-01-15', 'Devuelto'),
('23456789-0', 2, '2023-01-10', '2023-01-24', 'Prestado'),
('34567890-1', 3, '2023-02-01', '2023-02-15', 'Devuelto'),
('45678901-2', 4, '2023-02-10', '2023-02-24', 'Prestado'),
('56789012-3', 5, '2023-03-01', '2023-03-15', 'Devuelto'),
('67890123-4', 6, '2023-03-10', '2023-03-24', 'Prestado'),
('78901234-5', 7, '2023-04-01', '2023-04-15', 'Devuelto'),
('89012345-6', 8, '2023-04-10', '2023-04-24', 'Prestado'),
('90123456-7', 9, '2023-05-01', '2023-05-15', 'Devuelto'),
('01234567-8', 10, '2023-05-10', '2023-05-24', 'Prestado'),
('11223344-5', 11, '2023-06-01', '2023-06-15', 'Devuelto'),
('22334455-6', 12, '2023-06-10', '2023-06-24', 'Prestado'),
('33445566-7', 13, '2023-07-01', '2023-07-15', 'Devuelto'),
('44556677-8', 14, '2023-07-10', '2023-07-24', 'Prestado'),
('55667788-9', 15, '2023-08-01', '2023-08-15', 'Devuelto'),
('66778899-0', 16, '2023-08-10', '2023-08-24', 'Prestado'),
('77889900-1', 17, '2023-09-01', '2023-09-15', 'Devuelto'),
('88990011-2', 18, '2023-09-10', '2023-09-24', 'Prestado'),
('99001122-3', 19, '2023-10-01', '2023-10-15', 'Devuelto'),
('10012233-4', 20, '2023-10-10', '2023-10-24', 'Prestado');
