import pandas as pd

def main():
    usuarios = pd.read_csv("datasets/UsuariosSucio.csv").drop("Email", axis=1)
    cleanUsuarios = usuarios

    # asegurar que el NIF sea único, eliminando usuarios hasta dejar uno por cada uno
    previousNifs = set({})
    for i, currUsuario in usuarios.iterrows():
        if currUsuario["NIF"] in previousNifs:
            cleanUsuarios.drop(i, inplace=True)
        else:
            previousNifs.add(currUsuario["NIF"])

    # darle un email por defecto a los que no tengan
    for i, currUsuario in usuarios.iterrows():
        if pd.isnull(currUsuario["EMAIL"]):
            usuarios.at[i, "EMAIL"] = f"'{currUsuario['NIF']}'-EMAIL-ausente"

    # eliminar los caracteres no deseados de los teléfonos
    for i, currUsuario in cleanUsuarios.iterrows():
        currTelefono = currUsuario["TELEFONO"]
        currCleanTelefono: str = ""
        for currLeter in currTelefono:
            if currLeter.isdigit() or currLeter == "+":
                currCleanTelefono += currLeter

        cleanUsuarios.at[i, "TELEFONO"] = currCleanTelefono

    # corregir el uso de las mayúsculas en los nombres
    for i, currUsuario in cleanUsuarios.iterrows():
        currNombre:str = str(currUsuario["NOMBRE"])
        previousLetter:str = " "
        currCleanNombre: str = ""
        for currLetter in currNombre:
            if previousLetter == " ":
                currCleanNombre += currLetter.upper()
            else:
                currCleanNombre += currLetter.lower()
            previousLetter = currLetter

        cleanUsuarios.at[i, "NOMBRE"] = currCleanNombre

    cleanUsuarios.to_csv("datasets/UsuariosLimpio.csv")


if __name__ == "__main__":
    main()
