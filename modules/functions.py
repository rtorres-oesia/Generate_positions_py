import json, os, glob

# region Constants

_consQuery = "INSERT INTO SGA_SILO_SHUTTLE.POSICION_REFERENCIA_PLC (ID_POSICION,ID_INSTALACION,REFERENCIA_PLC) VALUES "
_consFileExtension = ".sql"

# endregion

lstParameters = []


def queryParameterJson(pathFile):
    with open(pathFile) as file:
        parameters = json.load(file)

        pathFile = parameters["pathJSON"]
        lstParameters.append(pathFile)

        pathExcel = parameters["pathExcelLocation"]
        lstParameters.append(pathExcel)

        pathExitFolder = parameters["pathOutputFolder"]
        lstParameters.append(pathExitFolder)

        sheet_name = parameters["sheet_name_param"]
        lstParameters.append(sheet_name)

        columns_query = parameters["columns_for_query"]
        lstParameters.append(columns_query)

        file.close

    return lstParameters


def createFolder(pathFolder):
    if not os.path.exists(pathFolder):
        os.mkdir(pathFolder)
    else:
        files = glob.glob(pathFolder + "*")
        for f in files:
            os.remove(f)

    return True if os.path.exists(pathFolder) else False


def generateFile(asileInt, pathOutputFolder, lstLines):
    pathfile = pathOutputFolder + "aisle_" + str(int(asileInt)) + _consFileExtension
    with open(pathfile, "w") as f:
        f.write(_consQuery + (",".join(lstLines)))
    f.close()


def queryPositionJson(*args):
    if args and len(args[0]) == 6:
        pathfile = str(args[0][0]).strip()
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
