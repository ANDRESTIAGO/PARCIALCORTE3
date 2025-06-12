from pydantic import BaseModel
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from Enum import snack, paises

class usuarios(SQLModel):
    nombre: str
    id_compra: int
    edad: str
    sexo: str
class UsuarioConId(usuarios):
    id: int

class mascota(SQLModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    tipo: Optional[str] = Field(None, min_length=2, max_length=30)
    marca: Optional[str] = Field(None, min_length=2, max_length=30)
    modelo: Optional[str] = Field(None, min_length=2, max_length=30)
    
class MascotaConId(mascota):
    id: int

class boleto(SQLModel, table=True):
    
    Ciudad_origen: str
    Ciudad_destino: str
    fecha: datetime
    disponibilidad: bool
    snack: Optional[snack] = Field(default=None)
    paises: Optional[paises] = Field(default=None)

class boleto_id(boleto):
    id_boleto:int