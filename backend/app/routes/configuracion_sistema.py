from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import ConfiguracionSistema
from schemas import ConfiguracionSistemaCreate, ConfiguracionSistemaUpdate, ConfiguracionSistemaResponse, ConfiguracionSistemaCompleta, TipoDatoConfig
from crud import configuracion_sistema_crud

# Configuración del router
router = APIRouter(
    prefix="/configuracion-sistema",
    tags=["Configuración Sistema"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[ConfiguracionSistemaResponse])
def listar_configuraciones(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    modificable: Optional[bool] = Query(None, description="Filtrar por modificable"),
    tipo_dato: Optional[TipoDatoConfig] = Query(None, description="Filtrar por tipo de dato"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de configuraciones del sistema con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **modificable**: Filtrar solo configuraciones modificables (true) o no modificables (false)
    - **tipo_dato**: Filtrar configuraciones por tipo de dato específico
    """
    if tipo_dato:
        return configuracion_sistema_crud.get_configuraciones_by_tipo(db, tipo_dato=tipo_dato.value)

    return configuracion_sistema_crud.get_configuraciones(db, skip=skip, limit=limit, modificable=modificable, tipo_dato=tipo_dato.value if tipo_dato else None)

@router.get("/{config_id}", response_model=ConfiguracionSistemaCompleta)
def obtener_configuracion(
    config_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una configuración por su ID con valor tipado"""
    configuracion = db.query(ConfiguracionSistema).filter(ConfiguracionSistema.id_config == config_id).first()
    if configuracion is None:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")

    # Crear respuesta con valor tipado
    response = ConfiguracionSistemaCompleta.from_orm(configuracion)
    response.valor_typed = configuracion.get_valor_typed()
    return response

@router.get("/parametro/{parametro}", response_model=ConfiguracionSistemaCompleta)
def obtener_configuracion_por_parametro(
    parametro: str,
    db: Session = Depends(get_db)
):
    """Obtener una configuración por su parámetro"""
    configuracion = configuracion_sistema_crud.get_configuracion_by_parametro(db, parametro)
    if not configuracion:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")

    # Crear respuesta con valor tipado
    response = ConfiguracionSistemaCompleta.from_orm(configuracion)
    response.valor_typed = configuracion.get_valor_typed()
    return response

@router.get("/tipo/{tipo_dato}/configuraciones", response_model=List[ConfiguracionSistemaResponse])
def obtener_configuraciones_por_tipo(
    tipo_dato: TipoDatoConfig,
    db: Session = Depends(get_db)
):
    """Obtener todas las configuraciones de un tipo de dato específico"""
    return configuracion_sistema_crud.get_configuraciones_by_tipo(db, tipo_dato=tipo_dato.value)

@router.post("/", response_model=ConfiguracionSistemaResponse, status_code=201)
def crear_configuracion(
    configuracion: ConfiguracionSistemaCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nueva configuración del sistema
    - El parámetro debe ser único
    """
    # Verificar que no existe una configuración con el mismo parámetro
    existing_config = configuracion_sistema_crud.get_configuracion_by_parametro(db, configuracion.parametro)

    if existing_config:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe una configuración con el parámetro '{configuracion.parametro}'"
        )

    return configuracion_sistema_crud.create_configuracion(db=db, configuracion=configuracion)

@router.put("/{config_id}", response_model=ConfiguracionSistemaResponse)
def actualizar_configuracion(
    config_id: int,
    configuracion_update: ConfiguracionSistemaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar configuración existente
    - Solo se actualizan los campos proporcionados
    - Solo se pueden actualizar configuraciones marcadas como modificables
    - Si se cambia el parámetro, debe ser único
    """
    # Verificar que la configuración existe
    db_configuracion = configuracion_sistema_crud.get_configuracion(db, config_id)
    if not db_configuracion:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")

    # Verificar si es modificable
    if not db_configuracion.es_modificable():
        raise HTTPException(status_code=400, detail="Esta configuración no es modificable")

    # Si se está actualizando el parámetro, verificar unicidad
    if configuracion_update.parametro:
        parametro = configuracion_update.parametro

        # Solo verificar si es diferente al actual
        if parametro != db_configuracion.parametro:
            existing_config = db.query(ConfiguracionSistema).filter(
                ConfiguracionSistema.parametro == parametro,
                ConfiguracionSistema.id_config != config_id
            ).first()

            if existing_config:
                raise HTTPException(
                    status_code=400,
                    detail=f"Ya existe una configuración con el parámetro '{parametro}'"
                )

    try:
        updated_configuracion = configuracion_sistema_crud.update_configuracion(db=db, config_id=config_id, configuracion_update=configuracion_update)
        if not updated_configuracion:
            raise HTTPException(status_code=404, detail="Error al actualizar la configuración")

        return updated_configuracion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{config_id}")
def eliminar_configuracion(
    config_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar configuración
    - Solo se pueden eliminar configuraciones marcadas como modificables
    """
    try:
        success = configuracion_sistema_crud.delete_configuracion(db=db, config_id=config_id)
        if not success:
            raise HTTPException(status_code=404, detail="Configuración no encontrada")

        return {"message": "Configuración eliminada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/parametro/{parametro}/valor")
def actualizar_valor_parametro(
    parametro: str,
    nuevo_valor: str = Query(..., description="Nuevo valor para el parámetro"),
    usuario_id: Optional[int] = Query(None, description="ID del usuario que realiza la modificación"),
    db: Session = Depends(get_db)
):
    """
    Actualizar solo el valor de un parámetro específico
    - Método rápido para cambiar valores sin enviar toda la configuración
    """
    try:
        configuracion = configuracion_sistema_crud.actualizar_valor_parametro(db, parametro, nuevo_valor, usuario_id)
        if not configuracion:
            raise HTTPException(status_code=404, detail="Parámetro no encontrado")

        return {"message": f"Valor del parámetro '{parametro}' actualizado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_configuraciones(
    modificable: Optional[bool] = Query(None, description="Filtrar por modificable"),
    tipo_dato: Optional[TipoDatoConfig] = Query(None, description="Filtrar por tipo de dato"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de configuraciones"""
    query = db.query(ConfiguracionSistema)

    if modificable is not None:
        query = query.filter(ConfiguracionSistema.modificable == modificable)

    if tipo_dato is not None:
        query = query.filter(ConfiguracionSistema.tipo_dato == tipo_dato.value)

    total = query.count()
    return {"total_configuraciones": total}

@router.get("/stats/por-tipo")
def estadisticas_por_tipo(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de configuraciones por tipo de dato"""
    from sqlalchemy import func

    stats = db.query(
        ConfiguracionSistema.tipo_dato,
        func.count(ConfiguracionSistema.id_config).label('total_configuraciones'),
        func.sum(func.cast(ConfiguracionSistema.modificable, db.Integer)).label('configuraciones_modificables')
    ).group_by(
        ConfiguracionSistema.tipo_dato
    ).all()

    return [
        {
            "tipo_dato": stat.tipo_dato,
            "total_configuraciones": stat.total_configuraciones or 0,
            "configuraciones_modificables": stat.configuraciones_modificables or 0,
            "configuraciones_bloqueadas": (stat.total_configuraciones or 0) - (stat.configuraciones_modificables or 0)
        }
        for stat in stats
    ]

@router.get("/export/todas")
def exportar_todas_configuraciones(
    db: Session = Depends(get_db)
):
    """Exportar todas las configuraciones del sistema"""
    configuraciones = configuracion_sistema_crud.get_configuraciones(db, limit=10000)

    export_data = []
    for config in configuraciones:
        export_data.append({
            "parametro": config.parametro,
            "valor": config.valor,
            "valor_typed": config.get_valor_typed(),
            "tipo_dato": config.tipo_dato,
            "descripcion": config.descripcion,
            "modificable": config.modificable,
            "fecha_modificacion": config.fecha_modificacion,
            "usuario_modificacion": config.usuario_modificacion
        })

    return {
        "total_configuraciones": len(export_data),
        "configuraciones": export_data
    }