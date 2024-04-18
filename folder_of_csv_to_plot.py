#pip install matplotlib
import csv
import matplotlib.pyplot as plt
import os


directorio = '/workspace/CSVplot/files/'
archivos = os.listdir(directorio)

archivos_csv = [archivo for archivo in archivos if archivo.endswith('.csv')]
for fileName in archivos_csv:
    print(fileName)



    #fileName='initCALAmbient25_100.csv'
    startRow = 0

    Current = []
    Temperature = []


    with open(directorio+fileName, mode='r') as file:
        csv_reader = csv.reader(file)
        for i, row in enumerate(csv_reader):
            if i >= startRow:
                if row[42] and row[150]:  # Verificar que hay valores en ambas columnas
                    try:
                        value_1 = float(row[42])*2000  # Convertir el valor de la columna 1 a flotante
                        value_2 = float(row[150])  # Convertir el valor de la columna 2 a flotante
                        Current.append(value_1)
                        Temperature.append(value_2)
                    except ValueError:
                        pass  # Saltar valores no numéricos

    # Crear una figura y ejes
    fig, ax1 = plt.subplots()

    # Graficar la primera columna en el primer eje y
    color = 'tab:blue'
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Current [A]', color=color)
    ax1.plot(Current, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Crear un segundo eje y compartiendo el mismo eje x
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Temperature [ºC]', color=color)
    ax2.plot(Temperature, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Añadir título al gráfico
    plt.title(fileName)

    # Mostrar el gráfico
    plt.show()
