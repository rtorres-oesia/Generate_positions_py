import json


def queryJson(*args):
    if args and len(args[0]) == 6:
        pathfile=str(args[0][0]).strip()
        with open(pathfile) as file:
            data = json.load(file)

            result = [
                x
                for x in data
                if x["ID_PASILLO"] == args[0][1]
                and x["LADO"] == args[0][2]
                and x["POSICION_X"] == args[0][3]
                and x["POSICION_Y"] == args[0][4]
                and x["POSICION_Z"] == args[0][5]
            ]

        file.close

        idPosicion = str(result[0]["ID_POSICION"]) if len(result) > 0 else ""
    else:
        idPosicion = ""

    return idPosicion


# For Examples
datos_positions = """
{
		"ID_POSICION": 20010010422,
		"ID_INSTALACION": 1386,
		"ID_ZONA": 1,
		"ID_TIPO_POSICION": 2,
		"ID_ESTADO_POSICION": 1,
		"ID_MOTIVO_INHABILITACION": 1,
		"ID_PASILLO": 1,
		"HABILITADO": 0,
		"POSICION_X": 1,
		"POSICION_Y": 4,
		"POSICION_Z": 2,
		"LADO": 2,
		"SILO": 1,
		"DESCRIPCION": "PO0010010422",
		"FECHA_MODIFICACION": "2022-07-14 10:16:47",
		"USUARIO_MODIFICACION": "central\\ricardotca",
		"ID_TIPO_POSICION_ALMACENAMIENTO": 1,
		"NIVEL": null,
		"ID_SUBINSTALACION": null,
		"ID_POSICION_ASOCIADA": null,
		"CAPACIDAD": null
}
"""
