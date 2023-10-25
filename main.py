import pandas as pd
import modules.functions as fn
from os.path import exists

# region Parameter

# input parameters
lstParameters = fn.queryParameterJson("C:/WorkPlace/Phyton/parameters.json")

pathJSON = lstParameters[0]
# pathExcelLocation = 'C:/WorkPlace/Phyton/OyshoLocation_complete.xlsx'
pathExcelLocation = lstParameters[1]
pathOutputFolder = lstParameters[2]
sheet_name_param = lstParameters[3]
columns_for_query = lstParameters[4]

# Constants
_consHeaderLoc = "LocationCode"
_consIdInstalacion = "38"

# Parameter class
isContinue = True
rowExcelCount = 0
isChangeAisle = False
# isChangeLane = False
isChangeOutputFile = False

finalAisle = 0
posXInitial = 1
posXQuery = 1

# Complex data structure
posXDisabledCount = []

lstPositions = []
# lstLane = [24, 47, 75]

# endregion

# Check files exists
if not exists(pathJSON) or not exists(pathExcelLocation):
    isContinue = False

if isContinue:
    # Output folder management
    isContinue = fn.createFolder(pathOutputFolder)
else:
    print("Files for loaded not exists!")

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

    # Initialize aisle & Lane
    # Ex: Aisle 1 - Lane 1 = 101; aisle 1 - Lane 2 = 201; Aisle 2 - Lane 1 =
    laneCount = 100
    # First aisle for query
    aisleQuery = 1

    # Initialize counter for X positions that do not exist in the ITX database
    posXDisabledCount = fn.rebootDisableXList()
    posXDisabledCompare = 0

    # Loop excel
    for x in range(row_cont):
        # To display row information and generate file
        location = str(df.iloc[x][_consHeaderLoc]).strip()

        # To use in the process
        loc_value = location.split("-")

        # For errors logs
        rowExcelCount += 1

        # Check if the retrieved fields are not empty and the positions array have enough information
        if loc_value[0].split() and len(loc_value) == 4:
            # Recovery initial aisle and check if there is change to the following
            aisle_value = int(loc_value[1])
            if aisle != aisle_value:
                aisle = aisle_value
                posXDisabledCount = fn.rebootDisableXList()
                posXDisabledCompare = 0

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

            # Get POS_Y
            arrayYZ = loc_value[3].split("_")
            if arrayYZ and len(arrayYZ) == 2:
                finalPosY = int(arrayYZ[0])
                finalPosZ = int(arrayYZ[1])

                isContinue = True
            else:
                isContinue = False

            if isContinue:
                # Check change lane
                # Get POS_X
                finalPosX = int(loc_value[2])

                # Check the posX change to increase the counter and be able to reset it with lane changes
                if posXInitial != finalPosX:
                    posXInitial = finalPosX
                    if (
                        fn.isChangeLane(laneCount, (posXQuery + posXDisabledCompare))
                        or isChangeAisle
                    ):
                        # Reboot variables
                        posXDisabledCount = fn.rebootDisableXList()
                        posXQuery = 1

                        # With the lane change, the lane resets to 100
                        laneCount = 100 if isChangeAisle else laneCount + 100
                    else:
                        posXQuery += 1

                # Change real aisle value for query in table dbo.POSICION
                finalAisle = laneCount + aisleQuery

                # Get aisle foreach iteration for calculate side
                finalSide = 2 if aisle_value % 2 == 0 else 1

                # region Json Query
                finalAisleSTR = str(finalAisle)
                idPosicion = fn.queryPositionJson(
                    [
                        pathJSON,
                        int(finalAisleSTR),
                        # int(finalAisleSTR[-2:]),
                        finalSide,
                        # finalPosX,
                        posXQuery,
                        finalPosY,
                        finalPosZ,
                    ],
                    lstX_compare=posXDisabledCount,
                )

                posXDisabledCompare = int(posXDisabledCount[0])

                # It is verified that the position is informed and
                # has not been an error generated by not finding a specific height
                if idPosicion and idPosicion != fn.ConsYNotFound:
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
                        + " Excel_Loc: "
                        + location
                        + " Aisle: "
                        + str(finalAisle)
                        + " Side: "
                        + str(finalSide)
                        + " Lane: "
                        + str(laneCount)
                        + " PosXQuery: "
                        + str(posXQuery)
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
            )

    # Generate file with final aisle values
    if len(lstPositions) > 0:
        # fn.generateFile(str(finalAisle), pathOutputFolder, lstPositions)
        fn.generateFile(str(finalAisle)[-2:], pathOutputFolder, lstPositions)
        # Variable reboot for save positions
        lstPositions = []

    print("Process succeed! Total positions in loop from Excel: " + str(rowExcelCount))

    # endregion
else:
    print("Error: One or more of the files to be processed does not exist!")
