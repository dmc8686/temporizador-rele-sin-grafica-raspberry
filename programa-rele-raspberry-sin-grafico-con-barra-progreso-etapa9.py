#temporizador_rele-solido_raspberry-sinGrafica
titulo ='''
###########################################
Este programa controla un rele solido
sin interfaz grafica
en el pin11 GPIO17 activa por uno

etapa 9 - implementa una Barra de porcentaje

notas:
aca intento un salto de linea, pero no lo logro

AUTHOR: diegocarrizo85@gmail.com
###########################################
'''
print(titulo)

import time
import sys
from gpiozero import LED

led = LED(17) # Corresponde al pin11

# Variables globales iniciales
bandera_contando = False 
#minuto_mostrado = -2  #aca vario el valor y no afecta nada 

# Inicializo el rele apagado de forma activa (0V, no flotante)
led.off()

try:
    print("programa activo esperando orden")
    # Al estar DENTRO del try, si apretás Ctrl+C acá, saltará limpiamente al except
    minuto_programado = int(input("Ingrese los minutos a contar: "))
    
    hora_actual = time.strftime("%H")
    minuto_actual = time.strftime("%M")
    print(f"programa iniciado a las {hora_actual}hs y {minuto_actual}min\n")
    print(f"..contando {minuto_programado} minutos..\n")

    tiempo_inicial_segundos = time.time()
    segundos_totales_programados = minuto_programado * 60
    
    # Prendo el relé
    led.on()
    #activo manualmente bandera de cuenta
    bandera_contando = True 

    while bandera_contando:
        tiempo_actual_segundos = time.time() 
        tiempo_transcurrido_segundos = tiempo_actual_segundos - tiempo_inicial_segundos
        minuto_transcurrido = int(tiempo_transcurrido_segundos // 60) #division entera
        
        # 1. CONTROL DE IMPRESIÓN DE MINUTOS
        #if minuto_transcurrido != minuto_mostrado:
        #    minuto_mostrado = minuto_transcurrido #ahora creo que esta linea esta de mas
        
        # 2. BARRA DE PORCENTAJE DINÁMICA (Idea de tus notas)
        # Calcula el progreso actual
        porcentaje = min(100, int((tiempo_transcurrido_segundos / segundos_totales_programados) * 100))
        largo_barra = 20 #esto aca se repite en todas las iteraciones y da ocote
        bloques_llenos = int((porcentaje / 100) * largo_barra)
        barra = "█" * bloques_llenos + "-" * (largo_barra - bloques_llenos)
        
        # sys.stdout.write y \r permiten reescribir la misma línea en SSH sin llenar la pantalla de basura
        sys.stdout.write(f"\rProgreso: [{barra}] {porcentaje}% | Segundos: {int(tiempo_transcurrido_segundos)}s | Minutos transcurridos: {minuto_transcurrido} de {minuto_programado} min")
        #esta linea no usa salto de linea
        sys.stdout.flush()#vacia el buffer para que se muestre el mensaje en el instante y no espere llenado de buffer

        # 3. CONTROL DE FIN DE TIEMPO
        if tiempo_transcurrido_segundos >= segundos_totales_programados:
            print(f"\n\nRele Apagado por tiempo transcurrido de {minuto_programado} minutos")
            bandera_contando = False
            
        # 4. ALIVIO DE CPU (CRÍTICO PARA SSH Y RASPBERRY ZERO)
        # Esto hace que el bucle espere 1 segundo en lugar de dar millones de vueltas vacías.
        # Reduce el uso de CPU de 100% a menos del 1%, permitiendo que el Ctrl+C entre al instante.
        time.sleep(1)
                
except KeyboardInterrupt:
    print("\n\n[!] Programa detenido por el usuario mediante CTRL + C.")
    bandera_contando = False
    
except ValueError:
    print("\n\n[!] Error: Se esperaba que ingresaras un número entero.")
    bandera_contando = False
    
finally:
    # EL FINALLY ES INFALIBLE: Siempre se ejecuta, pase lo que pase arriba
    led.off()  # Forzamos los 0V para que no quede flotante
    bandera_contando = False
    
    print("\n###########################################")
    print("pin11 gpio17 puesto a cero (Salida Segura)")
    hora_actual = time.strftime("%H")
    minuto_actual = time.strftime("%M")
    print(f"programa finalizado a las {hora_actual}hs y {minuto_actual}min")
    print("###########################################")
