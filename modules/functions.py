import json, os, glob
from os.path import exists

# region Constants

# Public constants
ConsYNotFound = "POS_Y no database"

# Private constants
_consCountForFinde = 4
_consQuery = "INSERT INTO SGA_SILO_SHUTTLE_OYSHO.POSICION_REFERENCIA_PLC (ID_POSICION,ID_INSTALACION,REFERENCIA_PLC) VALUES\n"
_consFileExtension = ".sql"

# endregion

lstParameters = []
dictionaryLanes = {100: 23, 200: 23, 300: 28}


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
        # Concat query const with new values for aisle
        f.write(_consQuery + (",".join(lstLines)))
    f.close()

    if exists(pathfile):
        # Read in the file for replace carry return forach values
        with open(pathfile, "r") as file:
            # Load file in memory
            fileReplace = file.read()
        file.close

        #Replace file with new values for add return carry
        newfile=fileReplace.replace("),", "),\n")
        
        # Write the file out again
        with open(pathfile, "w") as file:
            file.write(newfile)
        file.close
    else:
        print("The file: " + pathfile + " has been deleted!")


# lstX_compare = It is a complex structure because only this type of structure
# can be passed by reference.
def queryPositionJson(*args, lstX_compare):
    idPosicion = str()
    totalIterations = 0

    if args and len(args[0]) == 7:
        # path JSON file
        # pathfile = str(args[0][0]).strip()
        pathFinalFile = str(args[0][6]).strip()
        data = args[0][0]
        # Only the pos_X is changed to compare if the height is equal to 1
        isY1Compare = True if (args[0][4]) == 1 else False

        # Until it find a position
        while not idPosicion and totalIterations < _consCountForFinde:
            result = queryJson(
                data,
                args[0][1],
                args[0][2],
                args[0][3] + lstX_compare[0],
                args[0][4],
                args[0][5],
            )

            idPosicion = str(result[0]["ID_POSICION"]) if len(result) > 0 else str()

            # If no position is found and the query is about the first height (Y=1), the next pos_X will be searched for.
            if not idPosicion:
                if isY1Compare:
                    increaseListValue = lstX_compare[0] + 1
                    lstX_compare.clear()
                    lstX_compare.append(increaseListValue)

                    totalIterations += 1
                else:
                    # Value is assigned to exit the loop
                    idPosicion = ConsYNotFound

            # ISRECORDED change in JSON file
            # if idPosicion:
            #    for x in data:
            #        if x["ID_POSICION"] == int(idPosicion):
            #            x["ISRECORDED"] = 1
            #            break

            #    newData =  json.dumps(data, indent=4)

            #    with open(pathFinalFile, 'w') as fileUpdate:
            #     fileUpdate.write(newData)

            #     fileUpdate.close

            # file.close
    else:
        idPosicion = str()

    return idPosicion


def queryJson(jsonfile, idPasillo, lado, posX, posY, posZ):
    result = [
        x
        for x in jsonfile
        if x["ID_PASILLO"] == idPasillo
        and x["LADO"] == lado
        and x["POSICION_X"] == posX
        and x["POSICION_Y"] == posY
        and x["POSICION_Z"] == posZ
    ]

    return result


def isChangeLane(laneCount, posXDatabase):
    changeLaneValue = dictionaryLanes.get(laneCount)
    if posXDatabase == changeLaneValue:
        return True
    else:
        return False


def rebootDisableXList():
    posXDisabledCount = []
    posXDisabledCount.clear()
    posXDisabledCount.append(0)

    return posXDisabledCount