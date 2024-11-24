
import pytest
import calendar
from datetime import date
from app.utils.fechas import calcular_fechas

def test_calcular_fechas():
    
    fecha_inicial_esperada = date.today()
    
    fecha_inicial_calculada, fecha_fin_calculada = calcular_fechas()

    assert fecha_inicial_calculada == fecha_inicial_esperada.__str__()
