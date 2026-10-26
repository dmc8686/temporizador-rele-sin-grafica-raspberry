#temporizador_rele-solido_raspberry-sinGrafica
titulo ='''
##############################################
Este programa controla un rele solido
sin interfaz grafica
en el pin11 GPIO17 activa por uno

etapa 12 - implementa una Barra de porcentaje

nota:
unifica numero de versiones
agrega validacion de entrada

AUTHOR: diegocarrizo85@gmail.com
##############################################
'''
print(titulo)

import time
import sys
from gpiozero import LED

led = LED(17) # Corresponde al pin11

# Variables globales iniciales
bandera_contando = False
intentos_permitidos = 4
intentos_actuales = 1
MAXIMO_MINUTO_PROGRAMADO = 121 # dos horas mas un minuto

# Inicializo el rele apagado de forma activa (0V, no flotante)
led.off()

try:
    print("programa activo esperando orden")
    minuto_programado = int(input("Ingrese los minutos a contar: "))
    #validacion tipica
    while minuto_programado <= 0 or minuto_programado > MAXIMO_MINUTO_PROGRAMADO: #true es un error
        intentos_actuales += 1 #incremento en 1
        print(f"Error de ingreso. Intente valores comprendidos entre 1 y {MAXIMO_MINUTO_PROGRAMADO} (intento: {intentos_actuales})")
        if intentos_actuales > intentos_permitidos: #esto aca queda desprolijo pero es la funcion que necesito
            raise ValueError("Error en el ingreso de datos.") #deberia usar este texto
        minuto_programado = int(input("Ingrese los minutos a contar: "))
        
    
    hora_actual = time.strftime("%H")
    minuto_actual = time.strftime("%M")
    print(f"programa iniciado a las {hora_actual}hs y {minuto_actual}min\n")
    print(f"..contando {minuto_programado} minutos..\n")

    tiempo_inicial_segundos = time.time()
    segundos_totales_programados = minuto_programado * 60
    
    # Prendo el relé manualmente
    led.on()
    #activo manualmente bandera de cuenta
    bandera_contando = True 

    while bandera_contando:
        tiempo_actual_segundos = time.time() 
        tiempo_transcurrido_segundos = tiempo_actual_segundos - tiempo_inicial_segundos
        minuto_transcurrido = int(tiempo_transcurrido_segundos // 60) #division entera
        
        # Calcula el progreso actual
        porcentaje = min(100, int((tiempo_transcurrido_segundos / segundos_totales_programados) * 100))
        largo_barra = 20 #esto aca se repite en todas las iteraciones y da ocote
        bloques_llenos = int((porcentaje / 100) * largo_barra)
        barra = "█" * bloques_llenos + "-" * (largo_barra - bloques_llenos)
        #hago una unica impresion por iteracion
        # sys.stdout.write y \r permiten reescribir la misma línea en SSH sin llenar la pantalla de basura
        sys.stdout.write(f"\rProgreso: [{barra}] {porcentaje}% | Segundos: {int(tiempo_transcurrido_segundos)}s | Minutos transcurridos: {minuto_transcurrido} de {minuto_programado} min")
        #esta linea no usa salto de linea
        sys.stdout.flush()#vacia el buffer para que se muestre el mensaje en el instante y no espere llenado de buffer

        # Control de Fin de Tiempo
        if tiempo_transcurrido_segundos >= segundos_totales_programados:
            print(f"\n\nRele Apagado por tiempo transcurrido de {minuto_programado} minutos")
            bandera_contando = False
            
        # Alivio para procesar excepciones
        time.sleep(1)
                
except KeyboardInterrupt:
    print("\n\n[!] Programa detenido por el usuario mediante CTRL + C.")
    bandera_contando = False
    
except ValueError as e:
    print(f"\n\n[!] Error: Se esperaba que ingresaras un número entero comprendido entre 1 y {MAXIMO_MINUTO_PROGRAMADO}.")
    print(f"Error capturado: {e}")
    bandera_contando = False
    
finally:
    led.off()  # Forzamos los 0V para que no quede flotante
    bandera_contando = False
    
    print("\n###########################################")
    print("pin11 gpio17 puesto a cero")
    hora_actual = time.strftime("%H")
    minuto_actual = time.strftime("%M")
    print(f"programa finalizado a las {hora_actual}hs y {minuto_actual}min")
    print("###########################################")
