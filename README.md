# DS3231
Módulo de control del RTC DS3231 por medio del protocolo I2C

El módulo de reloj en tiempo real (RTC) modelo DS3231 cuenta con un protocolo de comunicación I2C y es muy popular para proyectos personales que requieran precisión de tiempo.

======= CONSUMO ENERGÉTICO ==========
El módulo puede ser alimentado con energía directa con un voltaje de entre 2.3V a 5.5V, lo que lo hace conveniente en uso con baterías de alta duración.
  Para conservar la hora, el módulo consume 100nA aproximadamente, siempre que el puerto i2c no esté activo.
  Pra conservar la hora, el módulo consume aproximadamente 3uA de la batería, en caso que el controlador pierda energía.

======= ALMACENAMIENTO ==============
El módulo emplea 7 registros específicos para registro de la fecha, tal como:
  0x00 = Segundos
  0x01 = Minutos
  0x02 = Horas
  0x03 = Día de la semana
  0x04 = Día del mes
  0x05 = Mes
  0x06 = Año
Cada uno de estos valores tiene una longitud de 1 byte, y es capaz de almacenar 2 dígitos, desde 00 hasta 99.
Para lograrlo usa un valor de tipo decimal codificado en binario (BCD).

-- Nota que el año también almacena 2 dígitos unicamente --

============ LECTURA ==================
> Se leen los 7 bits consecutivos con la función readfrom_mem, indicando el registro de inicio de lectura y la longitud total deseada, en este caso 7.
> Se convierten los valores a su representación decimal

============= Código BCD ================
la codificación decimal binaria parte del principio de que cada número entreo requiere de un máximo de 4 bits (1 nibble) para su interpretación binaria, por ello se aprovecha 1 byte para poder representar cualquier valor entre 00 hasta 99, mientras que el valor convencional sería hasta 255.

EJEMPLO:
  Para convertir el número 45:
    4 = 0100
    5 = 0101
    45 = 0100+0101 = 01000101 = 69

Del mismo modo, para decodificar un valor BCD a binario, se separan los dos nibbles del valor y se expresan en su valor entero:
  Para convertir el número 69:
    69 = 0100+0101
    0100 = 4
    0101 = 5
    69 = 01000101 = 0100+0101 = '4'+'5' = 45
