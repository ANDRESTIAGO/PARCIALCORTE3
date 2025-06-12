from pydantic import BaseModel
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from Enum import snack, paises

class usuarios(SQLModel):
    cedula:str
    nombre: str
    id_compra: int
    edad: str
    sexo: str
class UsuarioConId(usuarios):
    id: int

class mascota(SQLModel):
    cedula: str
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    id_compra: Optional[str] = Field(None, min_length=2, max_length=30)
    raza: Optional[str] = Field(None, min_length=2, max_length=30)
    edad: Optional[str] = Field(None, min_length=2, max_length=30)
    
class MascotaConId(mascota):
    id: int

class boleto(SQLModel):
    Ciudad_origen: str
    Ciudad_destino: str
    fecha: datetime
    disponibilidad: bool
    snack: Optional[str] = Field(default=None)
    paises: Optional[str] = Field(default=None)

class boleto_id(boleto):
    id_boleto:int