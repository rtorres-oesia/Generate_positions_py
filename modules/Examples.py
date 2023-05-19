import json
from functions import datos_positions

title = 'Id_posicion: '

dictionary_positions = json.loads(datos_positions)

print(title+str(dictionary_positions['ID_POSICION']))


#Ejemplo para ver campo de la lectura del Excel
#print ("Location: " + str(loc_value) + " Lane number: " + str(lane_value))

# Get excel value in df with file loaded
# loc_value = df.iloc[1]["LocationCode"]
# lane_value = df.iloc[1]["Lane number"]

#print ("Location: " + str(loc_value) + " Lane number: " + str(lane_value))