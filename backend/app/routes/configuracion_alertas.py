from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import ConfiguracionAlertas
from schemas import (
    ConfiguracionAlertasCreate,
    ConfiguracionAlertasUpdate,
    ConfiguracionAlertasResponse
)
from crud import configuracion_alertas_crud

router = APIRouter(
    prefix="/configuracion-alertas",
    tags=["Configuración de Alertas"]
)

@router.post("/", response_model=ConfiguracionAlertasResponse)
def crear_configuracion_alerta(
    alerta: ConfiguracionAlertasCreate,
    db: Session = Depends(get_db)
):
    db_alerta = configuracion_alertas_crud.create_alerta(db, alerta)
    return ConfiguracionAlertasResponse.from_orm(db_alerta)

@router.get("/", response_model=List[ConfiguracionAlertasResponse])
def listar_configuraciones_alertas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    alertas = configuracion_alertas_crud.get_alertas(db, skip=skip, limit=limit)
    return [ConfiguracionAlertasResponse.from_orm(alerta) for alerta in alertas]

@router.get("/{id_alerta}", response_model=ConfiguracionAlertasResponse)
def obtener_configuracion_alerta(
    id_alerta: int,
    db: Session = Depends(get_db)
):
    alerta = configuracion_alertas_crud.get_alerta(db, id_alerta)
    if not alerta:
        raise HTTPException(status_code=404, detail="Configuración de alerta no encontrada")
    return ConfiguracionAlertasResponse.from_orm(alerta)

@router.put("/{id_alerta}", response_model=ConfiguracionAlertasResponse)
def actualizar_configuracion_alerta(
    id_alerta: int,
    alerta: ConfiguracionAlertasUpdate,
    db: Session = Depends(get_db)
):
    db_alerta = configuracion_alertas_crud.update_alerta(db, id_alerta, alerta)
    if not db_alerta:
        raise HTTPException(status_code=404, detail="Configuración de alerta no encontrada")
    return ConfiguracionAlertasResponse.from_orm(db_alerta)

@router.delete("/{id_alerta}")
def eliminar_configuracion_alerta(
    id_alerta: int,
    db: Session = Depends(get_db)
):
    success = configuracion_alertas_crud.delete_alerta(db, id_alerta)
    if not success:
        raise HTTPException(status_code=404, detail="Configuración de alerta no encontrada")
    return {"message": "Configuración de alerta eliminada correctamente"}

@router.get("/activas/listar", response_model=List[ConfiguracionAlertasResponse])
def listar_alertas_activas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    alertas = configuracion_alertas_crud.get_alertas_activas(db, skip=skip, limit=limit)
    return [ConfiguracionAlertasResponse.from_orm(alerta) for alerta in alertas]

@router.get("/tipo/{tipo}", response_model=List[ConfiguracionAlertasResponse])
def listar_alertas_por_tipo(
    tipo: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    alertas = configuracion_alertas_crud.get_alertas_by_tipo(db, tipo, skip=skip, limit=limit)
    return [ConfiguracionAlertasResponse.from_orm(alerta) for alerta in alertas]

@router.patch("/{id_alerta}/activar", response_model=ConfiguracionAlertasResponse)
def activar_alerta(
    id_alerta: int,
    db: Session = Depends(get_db)
):
    alerta = configuracion_alertas_crud.activar_alerta(db, id_alerta)
    if not alerta:
        raise HTTPException(status_code=404, detail="Configuración de alerta no encontrada")
    return ConfiguracionAlertasResponse.from_orm(alerta)

@router.patch("/{id_alerta}/desactivar", response_model=ConfiguracionAlertasResponse)
def desactivar_alerta(
    id_alerta: int,
    db: Session = Depends(get_db)
):
    alerta = configuracion_alertas_crud.desactivar_alerta(db, id_alerta)
    if not alerta:
        raise HTTPException(status_code=404, detail="Configuración de alerta no encontrada")
    return ConfiguracionAlertasResponse.from_orm(alerta)

@router.patch("/{id_alerta}/frecuencia", response_model=ConfiguracionAlertasResponse)
def actualizar_frecuencia_revision(
    id_alerta: int,
    nuevas_horas: int = Query(..., ge=1, description="Nueva frecuencia de revisión en horas"),
    db: Session = Depends(get_db)
):
    alerta = configuracion_alertas_crud.actualizar_frecuencia(db, id_alerta, nuevas_horas)
    if not alerta:
        raise HTTPException(status_code=404, detail="Configuración de alerta no encontrada")
    return ConfiguracionAlertasResponse.from_orm(alerta)

@router.patch("/{id_alerta}/usuarios/agregar", response_model=ConfiguracionAlertasResponse)
def agregar_usuario_notificacion(
    id_alerta: int,
    usuario_id: int = Query(..., description="ID del usuario a agregar"),
    db: Session = Depends(get_db)
):
    alerta = configuracion_alertas_crud.agregar_usuario_notificacion(db, id_alerta, usuario_id)
    if not alerta:
        raise HTTPException(status_code=404, detail="Configuración de alerta no encontrada")
    return ConfiguracionAlertasResponse.from_orm(alerta)

@router.patch("/{id_alerta}/usuarios/remover", response_model=ConfiguracionAlertasResponse)
def remover_usuario_notificacion(
    id_alerta: int,
    usuario_id: int = Query(..., description="ID del usuario a remover"),
    db: Session = Depends(get_db)
):
    alerta = configuracion_alertas_crud.remover_usuario_notificacion(db, id_alerta, usuario_id)
    if not alerta:
        raise HTTPException(status_code=404, detail="Configuración de alerta no encontrada")
    return ConfiguracionAlertasResponse.from_orm(alerta)

@router.patch("/{id_alerta}/emails/agregar", response_model=ConfiguracionAlertasResponse)
def agregar_email_notificacion(
    id_alerta: int,
    email: str = Query(..., description="Email a agregar"),
    db: Session = Depends(get_db)
):
    # Validar formato de email
    emails_validos = configuracion_alertas_crud.validar_emails_formato([email])
    if not emails_validos:
        raise HTTPException(status_code=400, detail="Formato de email inválido")

    alerta = configuracion_alertas_crud.agregar_email_notificacion(db, id_alerta, email)
    if not alerta:
        raise HTTPException(status_code=404, detail="Configuración de alerta no encontrada")
    return ConfiguracionAlertasResponse.from_orm(alerta)

@router.patch("/{id_alerta}/emails/remover", response_model=ConfiguracionAlertasResponse)
def remover_email_notificacion(
    id_alerta: int,
    email: str = Query(..., description="Email a remover"),
    db: Session = Depends(get_db)
):
    alerta = configuracion_alertas_crud.remover_email_notificacion(db, id_alerta, email)
    if not alerta:
        raise HTTPException(status_code=404, detail="Configuración de alerta no encontrada")
    return ConfiguracionAlertasResponse.from_orm(alerta)

@router.post("/{id_alerta}/duplicar", response_model=ConfiguracionAlertasResponse)
def duplicar_configuracion_alerta(
    id_alerta: int,
    nuevo_nombre: str = Query(..., description="Nombre para la nueva configuración"),
    db: Session = Depends(get_db)
):
    nueva_alerta = configuracion_alertas_crud.duplicar_alerta(db, id_alerta, nuevo_nombre)
    if not nueva_alerta:
        raise HTTPException(status_code=404, detail="Configuración de alerta original no encontrada")
    return ConfiguracionAlertasResponse.from_orm(nueva_alerta)

@router.get("/buscar/nombre", response_model=List[ConfiguracionAlertasResponse])
def buscar_alertas_por_nombre(
    q: str = Query(..., min_length=2, description="Texto a buscar en el nombre"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    alertas = configuracion_alertas_crud.buscar_alertas(db, q, skip=skip, limit=limit)
    return [ConfiguracionAlertasResponse.from_orm(alerta) for alerta in alertas]

@router.get("/revision/pendientes", response_model=List[ConfiguracionAlertasResponse])
def obtener_alertas_para_revision(db: Session = Depends(get_db)):
    alertas = configuracion_alertas_crud.get_alertas_para_revision(db)
    return [ConfiguracionAlertasResponse.from_orm(alerta) for alerta in alertas]

@router.get("/estadisticas/general")
def obtener_estadisticas_alertas(db: Session = Depends(get_db)):
    return configuracion_alertas_crud.get_estadisticas_alertas(db)

@router.post("/validar-emails")
def validar_formato_emails(
    emails: List[str],
    db: Session = Depends(get_db)
):
    emails_validos = configuracion_alertas_crud.validar_emails_formato(emails)
    emails_invalidos = [email for email in emails if email not in emails_validos]

    return {
        "emails_validos": emails_validos,
        "emails_invalidos": emails_invalidos,
        "total_validos": len(emails_validos),
        "total_invalidos": len(emails_invalidos)
    }

@router.get("/tipos/disponibles")
def obtener_tipos_alertas_disponibles():
    """Obtener lista de tipos de alertas disponibles"""
    from schemas import TipoAlerta
    return {
        "tipos_disponibles": [tipo.value for tipo in TipoAlerta],
        "descripciones": {
            "STOCK_MINIMO": "Alerta cuando el stock de un producto está por debajo del mínimo",
            "VENCIMIENTO": "Alerta para productos próximos a vencer",
            "SIN_MOVIMIENTO": "Alerta para productos sin movimiento en un período",
            "CERTIFICACION_VENCIDA": "Alerta para certificaciones vencidas o próximas a vencer",
            "DEVOLUCION_PENDIENTE": "Alerta para devoluciones pendientes de procesamiento",
            "OBRA_SIN_ACTIVIDAD": "Alerta para obras sin actividad reciente",
            "MATERIAL_VENCIDO_EN_OBRA": "Alerta para materiales vencidos en obras",
            "DESPACHO_NO_ENTREGADO": "Alerta para despachos no entregados en tiempo"
        }
    }

@router.get("/resumen/configuracion")
def obtener_resumen_configuracion(db: Session = Depends(get_db)):
    """Obtener resumen de la configuración actual de alertas"""
    estadisticas = configuracion_alertas_crud.get_estadisticas_alertas(db)
    alertas_activas = configuracion_alertas_crud.get_alertas_activas(db, limit=1000)

    # Calcular usuarios únicos notificados
    usuarios_notificados = set()
    emails_notificados = set()

    for alerta in alertas_activas:
        usuarios_notificados.update(alerta.get_usuarios_lista())
        emails_notificados.update(alerta.get_emails_lista())

    return {
        **estadisticas,
        "usuarios_notificados": len(usuarios_notificados),
        "emails_notificados": len(emails_notificados),
        "frecuencia_promedio_horas": sum(a.frecuencia_revision_horas for a in alertas_activas) / len(alertas_activas) if alertas_activas else 0
    }