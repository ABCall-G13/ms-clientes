from datetime import date, datetime, timedelta
import calendar
import pytz

def calcular_fechas():

    zona_horaria_bogota = pytz.timezone('America/Bogota')
    fecha_inicial = datetime.now(zona_horaria_bogota).date()

    mes_siguiente = fecha_inicial.month % 12 + 1
    anio_siguiente = fecha_inicial.year + (fecha_inicial.month // 12)

    ultimo_dia_mes_siguiente = calendar.monthrange(anio_siguiente, mes_siguiente)[1]
    
    dia = min(fecha_inicial.day, ultimo_dia_mes_siguiente)
    fecha_fin = date(anio_siguiente, mes_siguiente, dia)
    
    fecha_inicial_str = fecha_inicial.strftime('%Y-%m-%d')
    fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')

    return fecha_inicial_str, fecha_fin_str