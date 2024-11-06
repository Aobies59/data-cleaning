import pandas as pd

def main():
    encuestas = pd.read_csv('datasets/EncuestasSatisfaccionSucio.csv')

    # fijar el formato de FECHA
    defaultDate = "01-01-1996"
    for i, currentEncuesta in encuestas.iterrows():
        currDate: str = str(currentEncuesta["FECHA"][:10])
        currDate = currDate.replace("/", "-")
        currDateSplit = currDate.split("-")
        if len(currDateSplit) != 3:
            currentEncuesta.at[i, "FECHA"] = defaultDate
            continue
        for currDateSplitElement in currDateSplit:
            if not currDateSplitElement.isdigit():
                currentEncuesta.at[i, "FECHA"] = defaultDate
                continue

        day:str = ""
        month:str = ""
        year:str = ""
        if len(currDateSplit[0]) == 4:
            year = currDateSplit[0]
            if int(currDateSplit[1]) > 12:
                day = currDateSplit[1]
                month = currDateSplit[2]
            else:
                day = currDateSplit[2]
                month = currDateSplit[1]
        elif len(currDateSplit[1]) == 4:  # wtf
            year = currDateSplit[1]
            if int(currDateSplit[2]) > 12:
                day = currDateSplit[2]
                month = currDateSplit[0]
            else:
                day = currDateSplit[0]
                month = currDateSplit[2]
        elif len(currDateSplit[2]) == 4:
            year = currDateSplit[2]
            if int(currDateSplit[1]) > 12:
                day = currDateSplit[1]
                month = currDateSplit[0]
            else:
                day = currDateSplit[0]
                month = currDateSplit[1]

        currUpdatedDate = f"{day}-{month}-{year}"
        encuestas.at[i, "FECHA"] = currUpdatedDate

    encuestas.to_csv('datasets/EncuestasSatisfaccionLimpio.csv')


if __name__ == '__main__':
    main()
