import pandas as pd
import modules.functions as fn
from os.path import exists

# region Parameter

# input parameters
pathJSON = "C:/WorkPlace/Phyton/bck_grupo_posicion_JSON.json"
# pathExcelLocation = 'C:/WorkPlace/Phyton/OyshoLocation_complete.xlsx'
pathExcelLocation = "C:/WorkPlace/Phyton/OyshoLocation.xlsx"
sheet_name_param = "location"

# Constants
_consHeaderLoc = "LocationCode"
_consHeaderLane = "Lane number"

# Parameter class
isContinue = True
lane = "0"
rowExcelCount = 0

# endregion

# Check files exists
if not exists(pathJSON) or not exists(pathExcelLocation):
    isContinue: False

# Algorithm locations
if isContinue:
    # region Excel management

    # Excel in memory
    # Get two columns in sheet
    df = pd.read_excel(
        pathExcelLocation, sheet_name=sheet_name_param, index_col=None, usecols="B, C"
    )

    # Get total rows in Excel; Does not take header into account
    row_cont = len(df.index)
    print("Total rows: " + str(row_cont))

    # Get first aisle&lane before Excel loop
    aisle = int(str(df.iloc[1][_consHeaderLoc]).split("-")[1])
    lane = str(df.iloc[1][_consHeaderLane])

    # Initialize  aisle & Lane
    aisleQuery = 1
    # Ex: Aisle 1 - Lane 1 = 101; aisle 1 - Lane 2 = 201; Aisle 2 - Lane 1 =
    laneCount = 100

    # Loop excel
    for x in range(row_cont):
        loc_value = str(str(df.iloc[x][_consHeaderLoc]).strip()).split("-")
        lane_value = str(df.iloc[x][_consHeaderLane]).strip()

        # For errors logs
        rowExcelCount += 1

        # Check if the retrieved fields are not empty and the positions array have enough information
        if lane_value.split() and (loc_value[0].split() and len(loc_value) == 4):
            # Check change lane
            if lane != lane_value:
                lane = lane_value
                laneCount += 100

            # Recovery initial laneCount
            aisle_value = int(loc_value[1])

            # Get aisle foreach iteration for calculate side
            side = 2 if aisleQuery % 2 == 0 else 1

        # ToDo: Guardar ficheros con errores
        # else:

        # region Json Query

        print(fn.queryJson(pathFile=pathJSON))

        # endregion

        # region Final sequence

        aisleQuery += 1

        # endregion

    # endregion
