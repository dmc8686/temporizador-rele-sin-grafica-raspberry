#temporizador_rele-solido_raspberry-sinGrafica
titulo ='''
###########################################
Este programa controla un rele solido sin grafica en el
pin11 GPIO17
es sin grafica para que sea liviano y tenga menos problemas
para usarlo por ssh en un raspberry chiquita tipo zero2w

etapa11
agrega una validacion de ingreso,
en realidad prefiero disparar una excepcion

posibles mejoras:
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
except ValueError:
    print("\n\n[!] Error: Se esperaba que ingresaras un número entero.")
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
    
