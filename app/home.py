from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import pandas.errors
import numpy as np
from models import usuarios, UsuarioConId, mascota, MascotaConId, boleto
from typing import Optional
from sqlmodel import Session, select
templates = Jinja2Templates(directory="templates")
router = APIRouter()
csv_file = "vuelos.csv"
prueba_file = "pruebas.csv"
csv_eliminados = "eliminados.csv"

@router.get("/home", response_class=HTMLResponse)
async def ver_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/", response_class=HTMLResponse)
async def ver_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/info", response_class=HTMLResponse)
async def leer_info(request:Request):
    csv_file = "vuelos.csv"
    sesiones = pd.read_csv(csv_file)
    sesiones["id"] = sesiones.index
    lista = sesiones.to_dict(orient="records")
    return templates.TemplateResponse("info.html",{"request":request, "sesiones":lista, "titulo":"Datos en tabla"})

@router.get("/ver_eliminados", response_class=HTMLResponse)
async def ver_eliminados(request: Request):
    orden_file = "eliminados.csv"

    try:
        df = pd.read_csv(orden_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["orden", "id", "nombre", "tipo", "marca", "modelo"])

    ordenes_agrupadas = {}
    for _, row in df.iterrows():
        nombre_orden = row["orden"]
        if nombre_orden not in ordenes_agrupadas:
            ordenes_agrupadas[nombre_orden] = []
        ordenes_agrupadas[nombre_orden].append(row.to_dict())

    return templates.TemplateResponse(
        "ver_eliminados.html",
        {"request": request, "ordenes": ordenes_agrupadas}
    )

@router.get("/comparacion", response_class=HTMLResponse)
async def mostrar_componentes(request: Request):
    csv_file = "componentes.csv"
    sesiones = pd.read_csv(csv_file)
    sesiones["id"] = sesiones.index  
    lista = sesiones.to_dict(orient="records")
    return templates.TemplateResponse(
        "comparacion.html",
        {"request": request, "sesiones": lista, "titulo": "Comparación de Componentes"}
    )

@router.post("/comparar", response_class=HTMLResponse)
async def comparar_componentes(request: Request, seleccionados: list[int] = Form(...)):
    csv_file = "componentes.csv"
    sesiones = pd.read_csv(csv_file)
    sesiones["id"] = sesiones.index

    seleccionados_df = sesiones[sesiones["id"].isin(seleccionados)]
    lista_seleccionados = seleccionados_df.to_dict(orient="records")

    return templates.TemplateResponse(
        "comparacion_seleccionada.html",
        {"request": request, "sesiones": lista_seleccionados, "titulo": "Componentes Seleccionados"}
    )

@router.get("/compatiblesi", response_class=HTMLResponse)
async def ver_componentes_compatibles(request: Request, socket: str, tipo_ram: Optional[str] = None):
    csv_file = "componentes.csv"
    df = pd.read_csv(csv_file)

    cpus = df[(df["tipo"] == "CPU") & (df["socket"] == socket)].to_dict(orient="records")
    ram = []
    if tipo_ram:
        ram = df[(df["tipo"] == "RAM") & (df["tipo_ram"] == tipo_ram)].to_dict(orient="records")
    gpus = df[df["tipo"] == "GPU"].to_dict(orient="records")
    fuentes = df[df["tipo"] == "Power Supply"].to_dict(orient="records")

    return templates.TemplateResponse(
        "compatibles.html",
        {"request": request, "cpus": cpus, "ram": ram, "gpus": gpus, "fuentes": fuentes}
    )

@router.get("/orden", response_class=HTMLResponse)
async def ver_orden(request: Request):
    orden_file = "orden.csv"

    try:
        orden = pd.read_csv(orden_file)
    except FileNotFoundError:
        orden = pd.DataFrame()

    if orden.empty:
        componentes = []
    else:
        componentes = orden.to_dict(orient="records")

    return templates.TemplateResponse(
        "orden.html", {"request": request, "componentes": componentes}
    )
#-----------------------------------------------------------------------------------------------------
#muestra formuladio crear usuario
@router.get("/usuario-add", response_class=HTMLResponse)
async def mostrar_formulario_usuario(request: Request):
    return templates.TemplateResponse("usuario_add.html", {"request": request})
#crea el usuario con base a el formlario
@router.post("/usuario-add")
async def crear_usuario(
    cedula: str = Form(...),
    nombre: str = Form(...),
    id_compra: int = Form(...), 
    edad: int = Form(...),
    sexo: str = Form(...)
):
    usuario_file = "usuarios.csv"

    try:
        df = pd.read_csv(usuario_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["cedula", "nombre", "id_compra", "edad", "sexo"])

    nuevo_usuario = {
        "cedula": cedula,
        "nombre": nombre,
        "id_compra": id_compra,
        "edad": edad,
        "sexo": sexo
    }

    df = pd.concat([df, pd.DataFrame([nuevo_usuario])], ignore_index=True)
    df.to_csv(usuario_file, index=False)

    return RedirectResponse(url="/usuarios", status_code=303)


from Enum import *

@router.post("/boleto_add")
async def crear_boleto(
    id_usuario: int = Form(...),
    id_compra: int = Form(...),
    Ciudad_origen: paises = Form(...),
    Ciudad_destino: paises = Form(...),
    fecha: str = Form(...),
    disponibilidad: bool = Form(True),
    snack : snack = Form(...)
    ):
    
    boleto_file = "vuelos.csv"

    try: 
        df = pd.read_csv(boleto_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["id_usuario", "id_compra", "Ciudad_origen", "Ciudad_destino", "fecha", "disponibilidad", "snack"])

    nuevo_boleto = {
        "id_usuario": id_usuario,
        "id_compra": id_compra,
        "Ciudad_origen": Ciudad_origen,
        "Ciudad_destino": Ciudad_destino,
        "fecha": fecha,
        "disponibilidad": disponibilidad,
        "snack": snack
    }

    df = pd.concat([df,pd.DataFrame([nuevo_boleto])], ignore_index=True)
    df. to_csv(boleto_file, index=False)

    return RedirectResponse(url="boletos", status_code=303)
 

@router.get("/boletos", response_class=HTMLResponse)
async def listar_boletos(request:Request):
    try:
        df = pd.read_csv("vuelos.csv")
        boleto = df.to_dict(orient="records")
    except FileExistsError:
        boleto = []

    return templates.TemplateResponse("boletos.html",{
    "request": Request,
    "boleto": boleto
    })


@router.get("/usuarios", response_class=HTMLResponse)
async def listar_usuarios(request: Request):
    try:
        df = pd.read_csv("usuarios.csv")
        usuarios = df.to_dict(orient="records")
    except FileNotFoundError:
        usuarios = []

    return templates.TemplateResponse("usuarios.html", {
        "request": request,
        "usuarios": usuarios
    })

@router.get("/usuario-eliminar", response_class=HTMLResponse)
async def mostrar_formulario_eliminar_usuario(request: Request):
    return templates.TemplateResponse("usuario_eliminar.html", {"request": request})

@router.post("/usuario-eliminar", response_class=RedirectResponse)
async def eliminar_usuario(request: Request, cedula: str = Form(...)):
    archivo_usuarios = "usuarios.csv"

    try:
        df = pd.read_csv(archivo_usuarios)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No hay usuarios registrados")

    if cedula not in df["cedula"].astype(str).values:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    df = df[df["cedula"].astype(str) != cedula]
    df.to_csv(archivo_usuarios, index=False)

    return RedirectResponse(url="/usuarios", status_code=303)





@router.get("/mascotas-add", response_class=HTMLResponse)
async def mostrar_formulario_mascota(request: Request):
    return templates.TemplateResponse("mascotas_add.html", {"request": request})

@router.post("/mascotas-add")
async def crear_mascota(
    cedula: str = Form(...),
    nombre: str = Form(...),
    id_compra: str = Form(...),
    raza: str = Form(...), 
    edad: str = Form(...)
):
    usuario_file = "mascotas.csv"

    try:
        df = pd.read_csv(usuario_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["cedula","nombre", "id_compra", "raza", "edad"])

    nuevo_mascota = {
        "cedula": cedula,
        "nombre": nombre,
        "id_compra": id_compra,
        "raza": raza,
        "edad": edad
    }

    df = pd.concat([df, pd.DataFrame([nuevo_mascota])], ignore_index=True)
    df.to_csv(usuario_file, index=False)

    return RedirectResponse(url="/mascotas", status_code=303)

@router.get("/mascotas", response_class=HTMLResponse)
async def listar_mascotas(request: Request):
    try:
        df = pd.read_csv("mascotas.csv")
        mascota = df.to_dict(orient="records")
    except FileNotFoundError:
        mascota = []

    return templates.TemplateResponse("mascotas.html", {
        "request": request,
        "mascota": mascota
    })

@router.get("/mascota-eliminar", response_class=HTMLResponse)
async def mostrar_formulario_eliminar_mascota(request: Request):
    return templates.TemplateResponse("mascota_eliminar.html", {"request": request})

@router.post("/mascota-eliminar", response_class=RedirectResponse)
async def eliminar_mascota(request: Request, cedula: str = Form(...)):
    archivo_mascota = "mascotas.csv"

    try:
        df = pd.read_csv(archivo_mascota)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No hay mascotas registrados")

    if cedula not in df["cedula"].astype(str).values:
        raise HTTPException(status_code=404, detail="Mascota no encontrado")
    
    df = df[df["cedula"].astype(str) != cedula]
    df.to_csv(archivo_mascota, index=False)

    return RedirectResponse(url="/mascotas", status_code=303)

@router.get("/add", response_class=HTMLResponse)
async def ver_add(request: Request):
    df = pd.read_csv("usuarios.csv")

    motherboards = df[df["tipo"] == "Motherboard"].to_dict(orient="records")
    cpus = df[df["tipo"] == "CPU"].to_dict(orient="records")
    rams = df[df["tipo"] == "RAM"].to_dict(orient="records")
    gpus = df[df["tipo"] == "GPU"].to_dict(orient="records")
    discos = df[df["tipo"].isin(["HDD", "SSD"])].to_dict(orient="records")

    return templates.TemplateResponse("add.html", {
        "request": request,
        "motherboards": motherboards,
        "cpus": cpus,
        "rams": rams,
        "gpus": gpus,
        "discos": discos
    })



@router.post("/add")
async def enviar_add(
    nombre_orden: str = Form(...),
    motherboard_id: int = Form(...),
    cpu_id: int = Form(...),
    ram_id: int = Form(...),
    gpu_id: int = Form(...),
    disco_id: int = Form(...)
):
    df = pd.read_csv("componentes.csv")
    orden_file = "orden.csv"

    mb = df[df["id"] == motherboard_id].iloc[0]
    cpu = df[df["id"] == cpu_id].iloc[0]
    ram = df[df["id"] == ram_id].iloc[0]
    gpu = df[df["id"] == gpu_id].iloc[0]
    disco = df[df["id"] == disco_id].iloc[0]

    if cpu["socket"] != mb["socket"]:
        return RedirectResponse(url="/cpu-incompa", status_code=303)

    if "tipo_ram" in mb and "tipo_ram" in ram and ram["tipo_ram"] != mb["tipo_ram"]:
        return RedirectResponse(url="/ram-incompa", status_code=303)

    try:
        orden = pd.read_csv(orden_file)
    except FileNotFoundError:
        orden = pd.DataFrame(columns=["orden", "id", "nombre", "tipo", "marca", "modelo"])

    seleccionados = pd.DataFrame([
        {"orden": nombre_orden, **mb.to_dict()},
        {"orden": nombre_orden, **cpu.to_dict()},
        {"orden": nombre_orden, **ram.to_dict()},
        {"orden": nombre_orden, **gpu.to_dict()},
        {"orden": nombre_orden, **disco.to_dict()}
    ])

    orden = pd.concat([orden, seleccionados], ignore_index=True)
    orden.to_csv(orden_file, index=False)

    return RedirectResponse(url="/orden", status_code=303)

@router.get("/cpu-incompa", response_class=HTMLResponse)
async def ver_cpu_incompa(request: Request):
    return templates.TemplateResponse("cpu-incompa.html", {"request": request})

@router.get("/ram-incompa", response_class=HTMLResponse)
async def ver_ram_incompa(request: Request):
    return templates.TemplateResponse("ram-incompa.html", {"request": request})

@router.get("/modificar", response_class=HTMLResponse)
async def ver_modificar_orden(request: Request):
    try:
        df_orden = pd.read_csv("orden.csv")
        df_componentes = pd.read_csv("componentes.csv")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No se encontraron archivos de orden o componentes")

    ordenes = df_orden["orden"].unique().tolist()
    componentes_por_orden = {
        nombre: df_orden[df_orden["orden"] == nombre].to_dict(orient="records")
        for nombre in ordenes
    }

    return templates.TemplateResponse("modificar_orden.html", {
        "request": request,
        "ordenes": ordenes,
        "componentes_por_orden": componentes_por_orden,
        "todos_componentes": df_componentes.to_dict(orient="records")
    })

@router.post("/modificar", response_class=HTMLResponse)
async def aplicar_modificacion(
    orden: str = Form(...),
    componente_id_original: int = Form(...),
    nuevo_id: int = Form(...)
):
    df_orden = pd.read_csv("orden.csv")
    df_componentes = pd.read_csv("componentes.csv")

    nuevo = df_componentes[df_componentes["id"] == nuevo_id]
    if nuevo.empty:
        raise HTTPException(status_code=404, detail="Nuevo componente no encontrado")

    index = df_orden[(df_orden["orden"] == orden) & (df_orden["id"] == componente_id_original)].index
    if index.empty:
        raise HTTPException(status_code=404, detail="Componente original no encontrado en la orden")

    for col in nuevo.columns:
        df_orden.loc[index, col] = nuevo.iloc[0][col]

    df_orden.to_csv("orden.csv", index=False)
    return RedirectResponse(url="/ordenes", status_code=303)


@router.get("/eliminar", response_class=HTMLResponse)
async def mostrar_ordenes_para_eliminar(request: Request):
    try:
        df = pd.read_csv("orden.csv")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No hay órdenes registradas")

    nombres_ordenes = df["orden"].unique().tolist()

    return templates.TemplateResponse("eliminar.html", {
        "request": request,
        "ordenes": nombres_ordenes
    })

@router.post("/eliminar", response_class=HTMLResponse)
async def mover_orden_a_eliminados(orden: str = Form(...)):
    print(f"Orden recibida para eliminar: {orden}")
    orden_file = "orden.csv"
    eliminados_file = "eliminados.csv"

    try:
        df = pd.read_csv(orden_file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No hay órdenes registradas")

    filas_eliminadas = df[df["orden"] == orden]
    if filas_eliminadas.empty:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    try:
        df_eliminados = pd.read_csv(eliminados_file)
        df_eliminados = pd.concat([df_eliminados, filas_eliminadas], ignore_index=True)
    except (FileNotFoundError, pandas.errors.EmptyDataError):
        df_eliminados = filas_eliminadas.copy()

    df_eliminados.to_csv(eliminados_file, index=False)


    df = df[df["orden"] != orden]
    df.to_csv(orden_file, index=False)

    return RedirectResponse(url="/orden", status_code=303)


@router.get("/menu", response_class=HTMLResponse)
async def ver_menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})

@router.get("/ordenes", response_class=HTMLResponse)
async def ver_ordenes(request: Request):
    orden_file = "orden.csv"

    try:
        df = pd.read_csv(orden_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["orden", "id", "nombre", "tipo", "marca", "modelo"])

    ordenes_agrupadas = {}
    for _, row in df.iterrows():
        nombre_orden = row["orden"]
        if nombre_orden not in ordenes_agrupadas:
            ordenes_agrupadas[nombre_orden] = []
        ordenes_agrupadas[nombre_orden].append(row.to_dict())

    return templates.TemplateResponse(
        "orden.html",
        {"request": request, "ordenes": ordenes_agrupadas}
    )