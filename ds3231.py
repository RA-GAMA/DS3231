'''Módulo  de control para RTC DS3231 por protocolo I2C'''

from machine import Pin, SoftI2C

class Ds3231:

    def __init__(self,_i2c:SoftI2C=None,_dir=0x68):
        '''inicia un nuevo objeto de control del sensor
        _i2c = Protocolo I2c
        '''
            # Protocolo I2C
        self.i2c = SoftI2C(sda=Pin(21),scl=Pin(22)) if _i2c==None else _i2c
            # Dirección I2C del dispositivo
        self.direccion = _dir
            # Declara valores de uso
        self.AA,self.MM,self.DD,self.sem,self.hh,self.mm,self.ss = 0,0,0,0,0,0,0
    
    def bcd(self,_numero:int=0)->str:
        '''convierte el valor dado en su representación BCD
        _numero = valor entero (>=0)
        '''
        t=str(_numero)                          # Convierte el número en texto
        n=0                                     # Prepara un número para adición
        for i in range(len(t)):                 # Cicla entre cada número
           n|=int(t[i:i+1])<<(len(t)-1-i)*4     # Agrega su valor binario con Bitwise OR
        return n
    
    def decimal(self,_numero:int)->int:
        '''convierte el valor BCD dado en su representación decimal convencional
        _numero = valor en formato BCD
        '''
        tx=''                                   # Prepara una cadena vacía
        t='{:04b}'.format(_numero)              # Convierte a binario
        while len(t)%4>>0: t='0'+t              # Agrega ceros en MSB, para concordancia.
        for i in range(len(t)//4):              # Cicla entre cada nibble
            tx+=str(int('0b'+t[i*4:(i+1)*4]))   # Agrega el número a una la cadena
        return int(tx)                          # Convierte la cadena en número
    
    def leer(self):
        '''Lee la fecha del RTC'''
            # lee los valores
        l = self.i2c.readfrom_mem(self.direccion,0x00,7)
            # convierte los valores BCD a Decimal
        self.AA=self.decimal(l[6])+2000         # Año
        self.MM=self.decimal(l[5])              # Mes
        self.DD=self.decimal(l[4])              # Día del mes
        self.sem=self.decimal(l[3])             # Día de la semana
        self.hh=self.decimal(l[2])              # Hora
        self.mm=self.decimal(l[1])              # Minuto
        self.ss=self.decimal(l[0])              # Segundo
    
    def guardar(self,_año:int=2000,_mes:int=1,_dia:int=1,
                _diasem:int=1,_hora:int=0,_minuto:int=0,
                _segundo:int=0):
        '''guarda una hora personalizada en el RTC
        _año = valor del año actual deseado (>2000)
        _mes = valor del mes actual deseado (1-12)
        _dia = valor del día del mes deseado (1-31)
        _diasem = valor del día de la semana deseado (1-7)
        _hora = valor de la hora actual deseada (0-23)
        _minuto = valor del minuto actual deseado (0-59)
        _segundo = valor del segundo actual deseado (0-59)
        '''
            # crea la lista de valores para enviar
        l=[]
        l.append(self.bcd(self.ss if _segundo==None else _segundo))
        l.append(self.bcd(self.mm if _minuto==None else _minuto))
        l.append(self.bcd(self.hh if _hora==None else _hora))
        l.append(self.bcd(self.sem if _diasem==None else _diasem))
        l.append(self.bcd(self.DD if _dia==None else _dia))
        l.append(self.bcd(self.MM if _mes==None else _mes))
            # guarda 2 dígitos relevantes del año (formato BCD-> 1 byte)
        l.append(self.bcd((self.AA if _año==None else _año)%100))
            # envía los valores especificados
        self.i2c.writeto_mem(self.direccion,0x00,bytearray(l))
    
    def __getattr__(self,_nombre:str):
        '''devuelve un atributo no delcarado
        _nombre = nombre del atributo buscado
        '''
            # actualiza los valores desde el RTC
        self.leer()
            # devuelve el valor deseado
        if _nombre=='año':return self.AA
        elif _nombre=='mes':return self.MM
        elif _nombre=='dia':return self.DD
        elif _nombre=='semana':return self.sem
        elif _nombre=='hora':return self.hh
        elif _nombre=='minuto':return self.mm
        elif _nombre=='segundo':return self.ss
        elif _nombre=='Hora':return [self.hh,self.mm,self.ss]
        elif _nombre=='fecha':return [self.AA,self.MM,self.DD]
        elif _nombre=='Fecha':return [self.AA,self.MM,self.DD,self.sem,self.hh,self.mm,self.ss]
        elif _nombre== 'date':return [self.AA,self.MM,self.DD,self.sem,self.hh,self.mm,self.ss,0]