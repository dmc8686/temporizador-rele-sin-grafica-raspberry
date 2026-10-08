#temporizador_rele-solido_raspberry-sinGrafica
titulo ='''
###########################################
Este programa controla un rele solido sin grafica en el
pin11 GPIO17
es sin grafica para que sea liviano y tenga menos problemas
para usarlo por ssh en un raspberry chiquita tipo zero2w

etapa10

muevo el try arriba de casi todo
agrego un timer sleep porque se sugiere y parece que va

borro las funciones porque todavia no las uso
y por ahi joden

agrego try except finally
nota:
no siempre funciona la excepcion
a veces aparece letra roja
tambien pasa que si ejecuto desde terminal
el puerto queda liberado y flotante:::::ojo con eso
medir con osciloscopio en el dispositivo remoto
en mi caso la raspberry pi2w que seguramente quede flotante

aca interrumpo el loop por teclado
(predeterminado un bucle se detiene con ctrl + c)

el pin se pone a cero
no libero el puerto porque eso lo pone flotante

notas e ideas:

agregar una barra de porcentaje

podria tener botones fisicos de control
podria tener comandos de control

AUTHOR: diegocarrizo85@gmail.com
###########################################
'''
print(titulo)

import time
from gpiozero import LED

led = LED(17) # corresponde al pin11

#variables globales
minuto_programado = 50 #este valor en esta etapa se sobreescribe
bandera_contando = True
bandera_minuto_mostrado = False
minuto_mostrado = 0
mensaje_mostrado = False

#inicializo el rele apagado
led.off()
try:
    
    #tiempo inicial
    #tiempo_inicial_segundos = time.time()
    #hora_actual = time.strftime("%H")
    #minuto_actual = time.strftime("%M")

    print("programa activo esperando orden")
    minuto_programado = int(input("Ingrese los minutos a contar: "))
        
    hora_actual = time.strftime("%H")
    minuto_actual = time.strftime("%M")
    print(f"programa iniciado a las {hora_actual}hs y {minuto_actual}min")
    print(f"..contando {minuto_programado} minutos..")

    #tiempo inicial
    tiempo_inicial_segundos = time.time()
    #prendo yo aca el rele a mano
    led.on()

    #hacer un loop

    while bandera_contando == True :
        tiempo_actual_segundos = time.time() 
        tiempo_transcurrido_segundos = tiempo_actual_segundos-tiempo_inicial_segundos
        minuto_transcurrido = int(tiempo_transcurrido_segundos // 60)
        
        if minuto_transcurrido != minuto_mostrado:
            print(f"minuto_transcurrido: {minuto_transcurrido} de {minuto_programado} minutos")
            bandera_minuto_mostrado = True
            minuto_mostrado = minuto_transcurrido
        else:
            bandera_minuto_mostrado = False
            
        if (bandera_contando == True) and (minuto_transcurrido >= minuto_programado):
            led.off()
            bandera_contando = False
            if not mensaje_mostrado:#false
                print(f"Rele Apagado por tiempo transcurrido de {minuto_programado} minutos")
                mensaje_mostrado = True
                
        time.sleep(1)#supuestamente este sleep relaja el sistema y da tiempo a procesar una excepcion
                
except KeyboardInterrupt:
    print("programa detenido por ctrl c")
    bandera_contando = False
    led.off()
    
finally:
    led.off()
    bandera_contando = False
    #led.close()  #esta linea hace que el pin quede flotante
    print("pin11 gpio17 puesto a cero")
    hora_actual = time.strftime("%H")
    minuto_actual = time.strftime("%M")
    print(f"programa finalizado a las {hora_actual}hs y {minuto_actual}min")
    
