import pandas as pd
from flask import send_file
from flask import Flask, render_template, request, redirect, send_file
import pandas
import json
import os

app = Flask(__name__)

# --- Funciones auxiliares ---


def cargar_tareas():
    if os.path.exists("tareas.json"):
        with open("tareas.json", "r") as archivo:
            return json.load(archivo)
    return []


def guardar_tareas(tareas):
    with open("tareas.json", "w") as archivo:
        json.dump(tareas, archivo, indent=4)

# --- Rutas ---


@app.route("/")
def index():
    tareas = cargar_tareas()
    return render_template("index.html", tareas=tareas)


@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    tareas = cargar_tareas()
    tareas.append({"nombre": nombre, "completada": False})
    guardar_tareas(tareas)
    return redirect("/")


@app.route("/completar/<int:indice>")
def completar(indice):
    tareas = cargar_tareas()
    if 0 <= indice < len(tareas):
        tareas[indice]["completada"] = not tareas[indice]["completada"]
        guardar_tareas(tareas)
    return redirect("/")


@app.route("/eliminar/<int:indice>")
def eliminar(indice):
    tareas = cargar_tareas()
    if 0 <= indice < len(tareas):
        tareas.pop(indice)
        guardar_tareas(tareas)
    return redirect("/")


@app.route("/exportar")
def exportar():
    tareas = cargar_tareas()
    if not tareas:
        return "No hay tareas para exportar."

    df = pd.DataFrame(tareas)
    archivo_excel = "tareas_exportadas.xlsx"
    df.to_excel(archivo_excel, index=False)

    return send_file(archivo_excel, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
