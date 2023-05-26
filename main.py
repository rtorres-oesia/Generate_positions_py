import pandas as pd
import modules.functions as fn
from os.path import exists

# region Parameter

# input parameters
pathJSON = "C:/WorkPlace/Phyton/bck_grupo_posicion_JSON.json"
# pathExcelLocation = 'C:/WorkPlace/Phyton/OyshoLocation_complete.xlsx'
pathExcelLocation = "C:/WorkPlace/Phyton/OyshoLocation.xlsx"
pathOutputFolder = "C:/WorkPlace/Phyton/Output/"
sheet_name_param = "location"
columns_for_query = "B,C"

# Constants
_consHeaderLoc = "LocationCode"
_consHeaderLane = "Lane number"

_consIdInstalacion = "38"

# Parameter class
isContinue = True
lane = "0"
rowExcelCount = 0
isChangeAisle = False
isChangeOutputFile = False

lstPositions = []

# endregion

# Check files exists
if not exists(pathJSON) or not exists(pathExcelLocation):
    isContinue: False

# Output folder management
isContinue = fn.createFolder(pathOutputFolder)

# Algorithm locations
if isContinue:
    # region Excel management

    # Excel in memory
    # Get two columns in sheet
    df = pd.read_excel(
        pathExcelLocation,
        sheet_name=sheet_name_param,
        index_col=None,
        usecols=columns_for_query,
    )

    # Get total rows in Excel; Does not take header into account
    row_cont = len(df.index)
    print("Total rows: " + str(row_cont))

    # Get first aisle&lane before Excel loop
    aisle = int(str(df.iloc[1][_consHeaderLoc]).split("-")[1])
    lane = str(df.iloc[1][_consHeaderLane])

    # Initialize aisle & Lane
    # Ex: Aisle 1 - Lane 1 = 101; aisle 1 - Lane 2 = 201; Aisle 2 - Lane 1 =
    laneCount = 100
    # First aisle for query
    aisleQuery = 1

    # Loop excel
    for x in range(row_cont):
        # To display row information and generate file
        location = str(df.iloc[x][_consHeaderLoc]).strip()

        # To use in the process
        loc_value = location.split("-")
        lane_value = str(df.iloc[x][_consHeaderLane]).strip()

        # For errors logs
        rowExcelCount += 1

        # Check if the retrieved fields are not empty and the positions array have enough information
        if lane_value.split() and (loc_value[0].split() and len(loc_value) == 4):
            # Recovery initial aisle and check if there is change to the following
            aisle_value = int(loc_value[1])
            if aisle != aisle_value:
                aisle = aisle_value

                # You can only change aisles when you have traveled both sides of each aisle
                if aisle_value % 2 != 0:
                    aisleQuery += 1
                    if len(lstPositions) > 0:
                        # Generate file with aisle values
                        fn.generateFile(
                            str(finalAisle)[-2:], pathOutputFolder, lstPositions
                        )
                        # Variable reboot for save positions
                        lstPositions = []

                        print("Asile: " + str(finalAisle)[-2:] + " finished!")

                isChangeAisle = True
            else:
                isChangeAisle = False

            # Check change lane
            if lane != lane_value:
                lane = lane_value
                # With the lane change, the lane resets to 100
                laneCount = 100 if isChangeAisle else laneCount + 100

            # Change real aisle value for query in table dbo.POSICION
            finalAisle = laneCount + aisleQuery

            # Get aisle foreach iteration for calculate side
            finalSide = 2 if aisle_value % 2 == 0 else 1

            # Get POS_X
            finalPosX = int(loc_value[2])

            # Get POS_Y
            arrayYZ = loc_value[3].split("_")
            if arrayYZ and len(arrayYZ) == 2:
                finalPosY = int(arrayYZ[0])
                finalPosZ = int(arrayYZ[1])

                isContinue = True
            else:
                isContinue = False

            if isContinue:
                # region Json Query
                # TODO Cuando tengamos la tabla final quitar todo el código siguiente para enviar el finalAsile que contenga el id de pastilla
                finalAisleSTR = str(finalAisle)
                idPosicion = fn.queryJson(
                    [
                        pathJSON,
                        int(finalAisleSTR[-2:]),
                        finalSide,
                        finalPosX,
                        finalPosY,
                        finalPosZ,
                    ]
                )

                # Código final (como parte del ToDo)
                # idPosicion = fn.queryJson(
                #     [pathJSON, finalAisle, finalSide, finalPosX, finalPosY, finalPosZ]
                # )

                if idPosicion:
                    query = str(
                        "("
                        + idPosicion
                        + ","
                        + _consIdInstalacion
                        + ",'"
                        + location
                        + "')"
                    )

                    lstPositions.append(query)

                    print(
                        "Processing! idPosicion: "
                        + idPosicion
                        + "Excel_Loc: "
                        + location
                        + " Aisle: "
                        + str(finalAisle)
                        + " Side: "
                        + str(finalSide)
                        + " Lane: "
                        + str(laneCount)
                    )
                else:
                    print(
                        "Location: "
                        + location
                        + " not found in query to dbo.Position. Excel row: "
                        + str(rowExcelCount)
                    )

                # endregion

            else:
                print(
                    "Error retrieving location information "
                    + location
                    + " in row number: "
                    + str(rowExcelCount)
                )

        # Print error
        else:
            print(
                "Error to recovery Excel value. In row number: "
                + str(rowExcelCount)
                + " Location value: "
                + location
                + "Lane value: "
                + lane_value
            )

    # Generate file with final aisle values
    if len(lstPositions) > 0:
        fn.generateFile(str(finalAisle)[-2:], pathOutputFolder, lstPositions)
        # Variable reboot for save positions
        lstPositions = []

    print("Process succeed! Total positions in loop from Excel: " + str(rowExcelCount))

    # endregion
else:
    print("Error at the beginning of the process and cannot continue.")
