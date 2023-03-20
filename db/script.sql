DELETE
FROM clientes
WHERE TRUE;

INSERT INTO clientes (dni, nombre, alta, direccion, provincia, municipio, pago, activo)
VALUES ('71230465V', 'Juan Perez', '01/01/2022', 'Calle Mayor 1', 'Madrid', 'Madrid', 'tarjeta;transferencia', 1),
       ('09829481V', 'Ana Sanchez', '15/02/2022', 'Avenida del Mar 2', 'Málaga', 'Málaga', 'efectivo', 1),
       ('16072102R', 'Pedro Gomez', '20/03/2022', 'Plaza Mayor 3', 'Salamanca', 'Salamanca', 'transferencia', 1),
       ('27451981D', 'Laura Rodriguez', '05/04/2022', 'Calle del Sol 4', 'Valencia', 'Valencia', 'efectivo;tarjeta', 1),
       ('17549732L', 'Carlos Garcia', '10/05/2022', 'Avenida de la Libertad 5', 'Sevilla', 'Sevilla', 'transferencia',
        1),
       ('18145899A', 'Lucia Perez', '15/06/2022', 'Calle del Carmen 6', 'Barcelona', 'Barcelona',
        'efectivo;tarjeta;transferencia', 1),
       ('19405345S', 'Miguel Fernandez', '20/07/2022', 'Plaza de España 7', 'Zaragoza', 'Zaragoza', 'tarjeta', 1),
       ('45100615F', 'Sara Lopez', '25/08/2022', 'Calle Real 8', 'Toledo', 'Toledo', 'efectivo;transferencia', 1),
       ('76037857H', 'Pablo Ramirez', '30/09/2022', 'Calle San Juan 9', 'Granada', 'Granada', 'tarjeta', 1),
       ('35650168F', 'Isabel Martinez', '05/10/2022', 'Calle Mayor 10', 'Madrid', 'Madrid',
        'efectivo;tarjeta;transferencia', 1);


DELETE
FROM coches
WHERE TRUE;

INSERT INTO coches (dnicli, matricula, marca, modelo, motor, activo, fecha_baja)
VALUES ('71230465V', '5266 UOQ', 'Volkswagen', 'Golf', 'Gasolina', 1, ''),
       ('71230465V', '1640 VQU', 'Ford', 'Focus', 'Híbrido', 1, ''),
       ('19405345S', '9371 QHF', 'Ford', 'Focus', 'Híbrido', 1, ''),
       ('09829481V', '4156 AWO', 'Toyota', 'Corolla', 'Eléctrico', 1, ''),
       ('16072102R', '8877 AZM', 'Audi', 'A4', 'Diésel', 1, ''),
       ('35650168F', '5255 CRO', 'Audi', 'A4', 'Diésel', 1, ''),
       ('27451981D', '6502 ZGD', 'Renault', 'Clio', 'Gasolina', 1, ''),
       ('76037857H', '0611 TCX', 'Renault', 'Clio', 'Gasolina', 1, ''),
       ('45100615F', '6735 BVR', 'Renault', 'Clio', 'Gasolina', 1, ''),
       ('35650168F', '9505 PSK', 'Renault', 'Clio', 'Gasolina', 1, ''),
       ('19405345S', '0990 JED', 'Renault', 'Clio', 'Gasolina', 1, ''),
       ('17549732L', '1300 HFB', 'BMW', 'Serie 3', 'Diésel', 1, ''),
       ('45100615F', '7697 EDE', 'BMW', 'Serie 3', 'Diésel', 1, ''),
       ('18145899A', '7900 ANX', 'Mercedes-Benz', 'Clase A', 'Híbrido', 1, ''),
       ('76037857H', '4054 OMD', 'Mercedes-Benz', 'Clase A', 'Híbrido', 1, '');

DELETE
FROM servicios
WHERE TRUE;

INSERT INTO servicios(concepto, "precio-unidad")
VALUES ('Ruedas', '50.00'),
       ('Aceite', '30.00'),
       ('Frenos', '80.00'),
       ('Lavado de coche', '20.00'),
       ('Alineación', '40.00'),
       ('Cambio de filtro', '25.00'),
       ('Cambio de bujías', '35.00'),
       ('Revisión de motor', '100.00'),
       ('Cambio de batería', '60.00'),
       ('Cambio de escobillas', '15.00'),
       ('Cambio de neumático', '70.00'),
       ('Cambio de amortiguadores', '200.00'),
       ('Cambio de líquido de frenos', '50.00'),
       ('Cambio de correa de distribución', '150.00'),
       ('Cambio de kit de embrague', '250.00'),
       ('Reparación de la caja de cambios', '350.00'),
       ('Cambio de radiador', '120.00'),
       ('Cambio de termostato', '80.00'),
       ('Cambio de bomba de agua', '90.00'),
       ('Revisión del sistema de escape', '60.00');


DELETE FROM facturas WHERE TRUE;