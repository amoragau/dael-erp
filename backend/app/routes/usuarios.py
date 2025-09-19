from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from database import get_db
from models import Usuarios
from schemas import (
    UsuariosCreate,
    UsuariosUpdate,
    UsuariosResponse,
    UsuariosWithRelations,
    CambiarPasswordRequest,
    LoginRequest,
    LoginResponse
)
from crud import usuarios_crud

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.post("/", response_model=UsuariosResponse)
def crear_usuario(
    usuario: UsuariosCreate,
    db: Session = Depends(get_db)
):
    try:
        return usuarios_crud.create_usuario(db, usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[UsuariosResponse])
def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return usuarios_crud.get_usuarios(db, skip=skip, limit=limit)

@router.get("/con-relaciones", response_model=List[UsuariosWithRelations])
def listar_usuarios_con_relaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return (db.query(Usuarios)
            .options(joinedload(Usuarios.rol))
            .offset(skip)
            .limit(limit)
            .all())

@router.get("/{id_usuario}", response_model=UsuariosWithRelations)
def obtener_usuario(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    usuario = (db.query(Usuarios)
               .options(joinedload(Usuarios.rol))
               .filter(Usuarios.id_usuario == id_usuario)
               .first())
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{id_usuario}", response_model=UsuariosResponse)
def actualizar_usuario(
    id_usuario: int,
    usuario: UsuariosUpdate,
    db: Session = Depends(get_db)
):
    try:
        db_usuario = usuarios_crud.update_usuario(db, id_usuario, usuario)
        if not db_usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return db_usuario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_usuario}")
def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    success = usuarios_crud.delete_usuario(db, id_usuario)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}

@router.get("/username/{username}", response_model=UsuariosWithRelations)
def obtener_usuario_por_username(
    username: str,
    db: Session = Depends(get_db)
):
    usuario = (db.query(Usuarios)
               .options(joinedload(Usuarios.rol))
               .filter(Usuarios.username == username)
               .first())
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.get("/email/{email}", response_model=UsuariosWithRelations)
def obtener_usuario_por_email(
    email: str,
    db: Session = Depends(get_db)
):
    usuario = (db.query(Usuarios)
               .options(joinedload(Usuarios.rol))
               .filter(Usuarios.email == email)
               .first())
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.get("/activos/listar", response_model=List[UsuariosWithRelations])
def listar_usuarios_activos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    usuarios = (db.query(Usuarios)
                .options(joinedload(Usuarios.rol))
                .filter(Usuarios.activo == True)
                .offset(skip)
                .limit(limit)
                .all())
    return usuarios

@router.get("/rol/{id_rol}", response_model=List[UsuariosWithRelations])
def listar_usuarios_por_rol(
    id_rol: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    usuarios = (db.query(Usuarios)
                .options(joinedload(Usuarios.rol))
                .filter(Usuarios.id_rol == id_rol)
                .offset(skip)
                .limit(limit)
                .all())
    return usuarios

@router.patch("/{id_usuario}/activar", response_model=UsuariosResponse)
def activar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    usuario = usuarios_crud.activar_usuario(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.patch("/{id_usuario}/desactivar", response_model=UsuariosResponse)
def desactivar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    usuario = usuarios_crud.desactivar_usuario(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/login", response_model=LoginResponse)
def login_usuario(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    usuario = usuarios_crud.authenticate_usuario(db, login_data.username, login_data.password)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not usuario.activo:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    return LoginResponse(
        usuario=usuario,
        token=None,  # TODO: Implementar JWT
        mensaje="Login exitoso"
    )

@router.patch("/{id_usuario}/cambiar-password")
def cambiar_password(
    id_usuario: int,
    request: CambiarPasswordRequest,
    db: Session = Depends(get_db)
):
    success = usuarios_crud.cambiar_password(
        db,
        id_usuario,
        request.password_actual,
        request.password_nueva
    )
    if not success:
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta o usuario no encontrado")
    return {"message": "Contraseña actualizada correctamente"}

@router.patch("/{id_usuario}/reset-password")
def reset_password(
    id_usuario: int,
    nueva_password: str = Body(..., min_length=8, description="Nueva contraseña"),
    db: Session = Depends(get_db)
):
    success = usuarios_crud.reset_password(db, id_usuario, nueva_password)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Contraseña reseteada correctamente"}

@router.get("/buscar/texto", response_model=List[UsuariosWithRelations])
def buscar_usuarios(
    q: str = Query(..., min_length=2, description="Texto a buscar en username, email o nombre completo"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    usuarios = usuarios_crud.buscar_usuarios(db, q, skip=skip, limit=limit)
    # Cargar relaciones manualmente
    for usuario in usuarios:
        db.refresh(usuario)
    return usuarios

@router.get("/sin-acceso-reciente/listar", response_model=List[UsuariosWithRelations])
def listar_usuarios_sin_acceso_reciente(
    dias: int = Query(30, ge=1, description="Días sin acceso"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    usuarios = usuarios_crud.get_usuarios_sin_acceso_reciente(db, dias, skip=skip, limit=limit)
    # Cargar relaciones manualmente
    for usuario in usuarios:
        db.refresh(usuario)
    return usuarios

@router.get("/ordenados/listar", response_model=List[UsuariosWithRelations])
def listar_usuarios_ordenados(
    campo_orden: str = Query("nombre_completo", description="Campo por el que ordenar: username, email, nombre_completo, activo, ultimo_acceso, fecha_creacion"),
    ascendente: bool = Query(True, description="True para orden ascendente, False para descendente"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    usuarios = usuarios_crud.get_usuarios_ordenados(db, campo_orden, ascendente, skip=skip, limit=limit)
    # Cargar relaciones manualmente
    for usuario in usuarios:
        db.refresh(usuario)
    return usuarios

@router.get("/validar/username-unico")
def validar_username_unico(
    username: str = Query(..., description="Username a validar"),
    excluir_id: Optional[int] = Query(None, description="ID del usuario a excluir de la validación"),
    db: Session = Depends(get_db)
):
    es_unico = usuarios_crud.validar_username_unico(db, username, excluir_id)
    return {
        "username": username,
        "es_unico": es_unico,
        "mensaje": "Username disponible" if es_unico else "Username ya está en uso"
    }

@router.get("/validar/email-unico")
def validar_email_unico(
    email: str = Query(..., description="Email a validar"),
    excluir_id: Optional[int] = Query(None, description="ID del usuario a excluir de la validación"),
    db: Session = Depends(get_db)
):
    es_unico = usuarios_crud.validar_email_unico(db, email, excluir_id)
    return {
        "email": email,
        "es_unico": es_unico,
        "mensaje": "Email disponible" if es_unico else "Email ya está en uso"
    }

@router.get("/estadisticas/generales")
def obtener_estadisticas_usuarios(db: Session = Depends(get_db)):
    return usuarios_crud.get_estadisticas_usuarios(db)

@router.get("/dashboard/resumen")
def obtener_resumen_dashboard(db: Session = Depends(get_db)):
    """Obtener resumen para dashboard de usuarios"""
    estadisticas = usuarios_crud.get_estadisticas_usuarios(db)
    usuarios_sin_acceso = usuarios_crud.get_usuarios_sin_acceso_reciente(db, 30, limit=1000)
    usuarios_nuevos = usuarios_crud.get_usuarios_ordenados(db, "fecha_creacion", False, limit=5)

    return {
        "estadisticas": estadisticas,
        "usuarios_sin_acceso_30d": len(usuarios_sin_acceso),
        "usuarios_mas_recientes": usuarios_nuevos,
        "total_usuarios_sistema": estadisticas["total_usuarios"]
    }

@router.get("/analisis/actividad")
def analizar_actividad_usuarios(
    dias_analisis: int = Query(30, ge=7, le=365, description="Días hacia atrás para analizar"),
    db: Session = Depends(get_db)
):
    """Analizar actividad de usuarios en los últimos días"""
    from datetime import datetime, timedelta

    fecha_limite = datetime.now() - timedelta(days=dias_analisis)

    # Usuarios con acceso en el período
    usuarios_activos = (db.query(Usuarios)
                       .filter(
                           Usuarios.activo == True,
                           Usuarios.ultimo_acceso >= fecha_limite
                       )
                       .count())

    # Usuarios sin acceso en el período
    usuarios_inactivos = (db.query(Usuarios)
                         .filter(
                             Usuarios.activo == True,
                             (Usuarios.ultimo_acceso.is_(None)) |
                             (Usuarios.ultimo_acceso < fecha_limite)
                         )
                         .count())

    # Usuarios creados en el período
    usuarios_nuevos = (db.query(Usuarios)
                      .filter(Usuarios.fecha_creacion >= fecha_limite)
                      .count())

    return {
        "periodo_analisis": f"{dias_analisis} días",
        "fecha_inicio": fecha_limite.date(),
        "fecha_fin": datetime.now().date(),
        "usuarios_con_actividad": usuarios_activos,
        "usuarios_sin_actividad": usuarios_inactivos,
        "usuarios_nuevos": usuarios_nuevos,
        "tasa_actividad": round(usuarios_activos / (usuarios_activos + usuarios_inactivos) * 100, 2) if (usuarios_activos + usuarios_inactivos) > 0 else 0
    }