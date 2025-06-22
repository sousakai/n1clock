from datetime import *
import csv

def calcularSaida(horario_entrada):
    try:
        entrada = datetime.strptime(horario_entrada, "%H:%M") 
        #usamos o datetime strip to time para converter o horário de entrada recebido pela função no formado de tempo %H:%M.
        
    except ValueError:
        return None
    expediente = timedelta(hours=9, minutes = 21) #timedelta é usado para representar períodos de tempo/duração
    saida = entrada + expediente
    return entrada.strftime("%H:%M"), saida.strftime("%H:%M") 
#usamos string format time para formatar as strings em formato de tempo

#horario_usuario = input("Digite o horário de entrada nesse formato: 00:00:\n") 
#resultado = calcularSaida(horario_usuario)

#if resultado is None:
    print("Formato inválido (use 00:00)")
#else: 
    print(f"Você deve sair às {resultado[1]}.")
#resultado[1] é usado pois a função retorna dois valores 
