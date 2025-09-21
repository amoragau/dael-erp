from datetime import date, datetime, time
from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Any
import models, schemas
import bcrypt

class TipoProductoCRUD:

    def get_tipo_producto(self, db: Session, tipo_producto_id: int) -> Optional[models.TipoProducto]:
        """Obtener tipo de producto por ID"""
        return db.query(models.TipoProducto).filter(models.TipoProducto.id_tipo_producto == tipo_producto_id).first()

    def get_tipo_producto_by_codigo(self, db: Session, codigo: str) -> Optional[models.TipoProducto]:
        """Obtener tipo de producto por código"""
        return db.query(models.TipoProducto).filter(models.TipoProducto.codigo_tipo == codigo).first()

    def get_tipos_productos(self, db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[models.TipoProducto]:
        """Obtener lista de tipos de producto con paginación"""
        query = db.query(models.TipoProducto)

        # Filtrar por activo si se especifica
        if activo is not None:
            query = query.filter(models.TipoProducto.activo == activo)

        return query.offset(skip).limit(limit).all()

    def create_tipo_producto(self, db: Session, tipo_producto: schemas.TipoProductoCreate) -> models.TipoProducto:
        """Crear nuevo tipo de producto"""
        db_tipo_producto = models.TipoProducto(**tipo_producto.dict())
        db.add(db_tipo_producto)
        db.commit()
        db.refresh(db_tipo_producto)
        return db_tipo_producto

    def update_tipo_producto(self, db: Session, tipo_producto_id: int, tipo_producto_update: schemas.TipoProductoUpdate) -> Optional[models.TipoProducto]:
        """Actualizar tipo de producto"""
        db_tipo_producto = self.get_tipo_producto(db, tipo_producto_id)
        if not db_tipo_producto:
            return None

        # Actualizar solo campos que no sean None
        update_data = tipo_producto_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_tipo_producto, field, value)

        db.commit()
        db.refresh(db_tipo_producto)
        return db_tipo_producto

    def delete_tipo_producto(self, db: Session, tipo_producto_id: int) -> bool:
        """Eliminar tipo de producto (soft delete)"""
        db_tipo_producto = self.get_tipo_producto(db, tipo_producto_id)
        if not db_tipo_producto:
            return False

        # Soft delete: marcar como inactivo
        db_tipo_producto.activo = False
        db.commit()
        return True

# Instancia global
tipo_producto_crud = TipoProductoCRUD()

class UnidadMedidaCRUD:

    def get_unidad(self, db: Session, unidad_id: int) -> Optional[models.UnidadMedida]:
        """Obtener unidad por ID"""
        return db.query(models.UnidadMedida).filter(models.UnidadMedida.id_unidad == unidad_id).first()

    def get_unidad_by_codigo(self, db: Session, codigo: str) -> Optional[models.UnidadMedida]:
        """Obtener unidad por código"""
        return db.query(models.UnidadMedida).filter(models.UnidadMedida.codigo_unidad == codigo).first()

    def get_unidades(self, db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[models.UnidadMedida]:
        """Obtener lista de unidades con paginación"""
        query = db.query(models.UnidadMedida)

        # Filtrar por activo si se especifica
        if activo is not None:
            query = query.filter(models.UnidadMedida.activo == activo)

        return query.offset(skip).limit(limit).all()

    def create_unidad(self, db: Session, unidad: schemas.UnidadMedidaCreate) -> models.UnidadMedida:
        """Crear nueva unidad de medida"""
        db_unidad = models.UnidadMedida(**unidad.dict())
        db.add(db_unidad)
        db.commit()
        db.refresh(db_unidad)
        return db_unidad

    def update_unidad(self, db: Session, unidad_id: int, unidad_update: schemas.UnidadMedidaUpdate) -> Optional[models.UnidadMedida]:
        """Actualizar unidad de medida"""
        db_unidad = self.get_unidad(db, unidad_id)
        if not db_unidad:
            return None

        # Actualizar solo campos que no sean None
        update_data = unidad_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_unidad, field, value)

        db.commit()
        db.refresh(db_unidad)
        return db_unidad

    def delete_unidad(self, db: Session, unidad_id: int) -> bool:
        """Eliminar unidad de medida (soft delete)"""
        db_unidad = self.get_unidad(db, unidad_id)
        if not db_unidad:
            return False

        # Soft delete: marcar como inactivo
        db_unidad.activo = False
        db.commit()
        return True

# Instancia global
unidad_medida_crud = UnidadMedidaCRUD()

class TipoMovimientoCRUD:

    def get_movimiento(self, db: Session, movimiento_id: int) -> Optional[models.TipoMovimiento]:
        """Obtener tipo de movimiento por ID"""
        return db.query(models.TipoMovimiento).filter(models.TipoMovimiento.id_tipo_movimiento == movimiento_id).first()

    def get_movimiento_by_codigo(self, db: Session, codigo: str) -> Optional[models.TipoMovimiento]:
        """Obtener tipo de movimiento por código"""
        return db.query(models.TipoMovimiento).filter(models.TipoMovimiento.codigo_tipo == codigo).first()

    def get_movimientos(self, db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[models.TipoMovimiento]:
        """Obtener lista de tipos de movimiento con paginación"""
        query = db.query(models.TipoMovimiento)

        # Filtrar por activo si se especifica
        if activo is not None:
            query = query.filter(models.TipoMovimiento.activo == activo)

        return query.offset(skip).limit(limit).all()

    def create_movimiento(self, db: Session, movimiento: schemas.TipoMovimientoCreate) -> models.TipoMovimiento:
        """Crear nuevo tipo de movimiento"""
        db_movimiento = models.TipoMovimiento(**movimiento.dict())
        db.add(db_movimiento)
        db.commit()
        db.refresh(db_movimiento)
        return db_movimiento

    def update_movimiento(self, db: Session, movimiento_id: int, movimiento_update: schemas.TipoMovimientoUpdate) -> Optional[models.TipoMovimiento]:
        """Actualizar tipo de movimiento"""
        db_movimiento = self.get_movimiento(db, movimiento_id)
        if not db_movimiento:
            return None

        # Actualizar solo campos que no sean None
        update_data = movimiento_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_movimiento, field, value)

        db.commit()
        db.refresh(db_movimiento)
        return db_movimiento

    def delete_movimiento(self, db: Session, movimiento_id: int) -> bool:
        """Eliminar tipo de movimiento (soft delete)"""
        db_movimiento = self.get_movimiento(db, movimiento_id)
        if not db_movimiento:
            return False

        # Soft delete: marcar como inactivo
        db_movimiento.activo = False
        db.commit()
        return True

# Instancia global
tipo_movimiento_crud = TipoMovimientoCRUD()

class CategoriaCRUD:

    def get_categoria(self, db: Session, categoria_id: int) -> Optional[models.Categoria]:
        """Obtener categoría por ID"""
        return db.query(models.Categoria).filter(models.Categoria.id_categoria == categoria_id).first()

    def get_categorias(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        activo: Optional[bool] = None
    ) -> List[models.Categoria]:
        """Obtener lista de categorías con paginación"""
        query = db.query(models.Categoria)
        # Filtrar por activo si se especifica
        if activo is not None:
            query = query.filter(models.Categoria.activo == activo)
        return query.offset(skip).limit(limit).all()

    def create_categoria(self, db: Session, categoria: schemas.CategoriaCreate) -> models.Categoria:
        """Crear nueva categoría"""
        db_categoria = models.Categoria(**categoria.dict())
        db.add(db_categoria)
        db.commit()
        db.refresh(db_categoria)
        return db_categoria

    def update_categoria(
        self,
        db: Session,
        categoria_id: int,
        categoria_update: schemas.CategoriaUpdate
    ) -> Optional[models.Categoria]:
        """Actualizar categoría"""
        db_categoria = self.get_categoria(db, categoria_id)
        if not db_categoria:
            return None
        # Actualizar solo campos que no sean None
        update_data = categoria_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_categoria, field, value)
        db.commit()
        db.refresh(db_categoria)
        return db_categoria

    def delete_categoria(self, db: Session, categoria_id: int) -> bool:
        """Eliminar categoría (soft delete)"""
        db_categoria = self.get_categoria(db, categoria_id)
        if not db_categoria:
            return False
        # Soft delete: marcar como inactivo
        db_categoria.activo = False
        db.commit()
        return True

# Instancia global
categoria_crud = CategoriaCRUD()

class MarcaCRUD:

    def get_marca(self, db: Session, marca_id: int) -> Optional[models.Marca]:
        """Obtener marca por ID"""
        return db.query(models.Marca).filter(models.Marca.id_marca == marca_id).first()

    def get_marca_by_nombre(self, db: Session, nombre: str) -> Optional[models.Marca]:
        """Obtener marca por nombre"""
        return db.query(models.Marca).filter(models.Marca.nombre_marca == nombre).first()

    def get_marcas(self, db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[models.Marca]:
        """Obtener lista de marcas con paginación"""
        query = db.query(models.Marca)

        # Filtrar por activo si se especifica
        if activo is not None:
            query = query.filter(models.Marca.activo == activo)

        return query.offset(skip).limit(limit).all()

    def create_marca(self, db: Session, marca: schemas.MarcaCreate) -> models.Marca:
        """Crear nueva marca"""
        db_marca = models.Marca(**marca.dict())
        db.add(db_marca)
        db.commit()
        db.refresh(db_marca)
        return db_marca

    def update_marca(self, db: Session, marca_id: int, marca_update: schemas.MarcaUpdate) -> Optional[models.Marca]:
        """Actualizar marca"""
        db_marca = self.get_marca(db, marca_id)
        if not db_marca:
            return None

        # Actualizar solo campos que no sean None
        update_data = marca_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_marca, field, value)

        db.commit()
        db.refresh(db_marca)
        return db_marca

    def delete_marca(self, db: Session, marca_id: int) -> bool:
        """Eliminar marca (soft delete)"""
        db_marca = self.get_marca(db, marca_id)
        if not db_marca:
            return False

        # Soft delete: marcar como inactivo
        db_marca.activo = False
        db.commit()
        return True

# Instancia global
marca_crud = MarcaCRUD()

class ProveedorCRUD:

    def get_proveedor(self, db: Session, proveedor_id: int) -> Optional[models.Proveedor]:
        """Obtener proveedor por ID"""
        return db.query(models.Proveedor).filter(models.Proveedor.id_proveedor == proveedor_id).first()

    def get_proveedor_by_codigo(self, db: Session, codigo: str) -> Optional[models.Proveedor]:
        """Obtener proveedor por código"""
        return db.query(models.Proveedor).filter(models.Proveedor.codigo_proveedor == codigo).first()

    def get_proveedor_by_nombre(self, db: Session, nombre: str) -> Optional[models.Proveedor]:
        """Obtener proveedor por nombre"""
        return db.query(models.Proveedor).filter(models.Proveedor.nombre_proveedor == nombre).first()

    def get_proveedor_by_rfc(self, db: Session, rfc: str) -> Optional[models.Proveedor]:
        """Obtener proveedor por RFC"""
        return db.query(models.Proveedor).filter(models.Proveedor.rfc == rfc).first()

    def get_proveedores(self, db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[models.Proveedor]:
        """Obtener lista de proveedores con paginación"""
        query = db.query(models.Proveedor)

        # Filtrar por activo si se especifica
        if activo is not None:
            query = query.filter(models.Proveedor.activo == activo)

        return query.offset(skip).limit(limit).all()

    def search_proveedores(self, db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[models.Proveedor]:
        """Buscar proveedores por nombre, código o razón social"""
        search_pattern = f"%{search_term}%"
        return db.query(models.Proveedor).filter(
            (models.Proveedor.nombre_proveedor.ilike(search_pattern)) |
            (models.Proveedor.codigo_proveedor.ilike(search_pattern)) |
            (models.Proveedor.razon_social.ilike(search_pattern))
        ).offset(skip).limit(limit).all()

    def create_proveedor(self, db: Session, proveedor: schemas.ProveedorCreate) -> models.Proveedor:
        """Crear nuevo proveedor"""
        db_proveedor = models.Proveedor(**proveedor.dict())
        db.add(db_proveedor)
        db.commit()
        db.refresh(db_proveedor)
        return db_proveedor

    def update_proveedor(self, db: Session, proveedor_id: int, proveedor_update: schemas.ProveedorUpdate) -> Optional[models.Proveedor]:
        """Actualizar proveedor"""
        db_proveedor = self.get_proveedor(db, proveedor_id)
        if not db_proveedor:
            return None

        # Actualizar solo campos que no sean None
        update_data = proveedor_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_proveedor, field, value)

        db.commit()
        db.refresh(db_proveedor)
        return db_proveedor

    def delete_proveedor(self, db: Session, proveedor_id: int) -> bool:
        """Eliminar proveedor (soft delete)"""
        db_proveedor = self.get_proveedor(db, proveedor_id)
        if not db_proveedor:
            return False

        # Soft delete: marcar como inactivo
        db_proveedor.activo = False
        db.commit()
        return True

# Instancia global
proveedor_crud = ProveedorCRUD()

# ========================================
# CRUD PARA ALMACÉN - BODEGAS
# ========================================

class BodegaCRUD:

    def get_bodega(self, db: Session, bodega_id: int) -> Optional[models.Bodega]:
        """Obtener bodega por ID"""
        return db.query(models.Bodega).filter(models.Bodega.id_bodega == bodega_id).first()

    def get_bodega_by_codigo(self, db: Session, codigo: str) -> Optional[models.Bodega]:
        """Obtener bodega por código"""
        return db.query(models.Bodega).filter(models.Bodega.codigo_bodega == codigo).first()

    def get_bodegas(self, db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[models.Bodega]:
        """Obtener lista de bodegas con paginación"""
        query = db.query(models.Bodega)

        if activo is not None:
            query = query.filter(models.Bodega.activo == activo)

        return query.offset(skip).limit(limit).all()

    def create_bodega(self, db: Session, bodega: schemas.BodegaCreate) -> models.Bodega:
        """Crear nueva bodega"""
        db_bodega = models.Bodega(**bodega.dict())
        db.add(db_bodega)
        db.commit()
        db.refresh(db_bodega)
        return db_bodega

    def update_bodega(self, db: Session, bodega_id: int, bodega_update: schemas.BodegaUpdate) -> Optional[models.Bodega]:
        """Actualizar bodega"""
        db_bodega = self.get_bodega(db, bodega_id)
        if not db_bodega:
            return None

        update_data = bodega_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_bodega, field, value)

        db.commit()
        db.refresh(db_bodega)
        return db_bodega

    def delete_bodega(self, db: Session, bodega_id: int) -> bool:
        """Eliminar bodega (soft delete)"""
        db_bodega = self.get_bodega(db, bodega_id)
        if not db_bodega:
            return False

        db_bodega.activo = False
        db.commit()
        return True

class PasilloCRUD:

    def get_pasillo(self, db: Session, pasillo_id: int) -> Optional[models.Pasillo]:
        """Obtener pasillo por ID"""
        return db.query(models.Pasillo).filter(models.Pasillo.id_pasillo == pasillo_id).first()

    def get_pasillos_by_bodega(self, db: Session, bodega_id: int, activo: Optional[bool] = None) -> List[models.Pasillo]:
        """Obtener pasillos de una bodega"""
        query = db.query(models.Pasillo).filter(models.Pasillo.id_bodega == bodega_id)

        if activo is not None:
            query = query.filter(models.Pasillo.activo == activo)

        return query.all()

    def get_pasillos(self, db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[models.Pasillo]:
        """Obtener lista de pasillos con paginación"""
        query = db.query(models.Pasillo)

        if activo is not None:
            query = query.filter(models.Pasillo.activo == activo)

        return query.offset(skip).limit(limit).all()

    def create_pasillo(self, db: Session, pasillo: schemas.PasilloCreate) -> models.Pasillo:
        """Crear nuevo pasillo"""
        db_pasillo = models.Pasillo(**pasillo.dict())
        db.add(db_pasillo)
        db.commit()
        db.refresh(db_pasillo)
        return db_pasillo

    def update_pasillo(self, db: Session, pasillo_id: int, pasillo_update: schemas.PasilloUpdate) -> Optional[models.Pasillo]:
        """Actualizar pasillo"""
        db_pasillo = self.get_pasillo(db, pasillo_id)
        if not db_pasillo:
            return None

        update_data = pasillo_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_pasillo, field, value)

        db.commit()
        db.refresh(db_pasillo)
        return db_pasillo

    def delete_pasillo(self, db: Session, pasillo_id: int) -> bool:
        """Eliminar pasillo (soft delete)"""
        db_pasillo = self.get_pasillo(db, pasillo_id)
        if not db_pasillo:
            return False

        db_pasillo.activo = False
        db.commit()
        return True

class EstanteCRUD:

    def get_estante(self, db: Session, estante_id: int) -> Optional[models.Estante]:
        """Obtener estante por ID"""
        return db.query(models.Estante).filter(models.Estante.id_estante == estante_id).first()

    def get_estantes_by_pasillo(self, db: Session, pasillo_id: int, activo: Optional[bool] = None) -> List[models.Estante]:
        """Obtener estantes de un pasillo"""
        query = db.query(models.Estante).filter(models.Estante.id_pasillo == pasillo_id)

        if activo is not None:
            query = query.filter(models.Estante.activo == activo)

        return query.all()

    def get_estantes(self, db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[models.Estante]:
        """Obtener lista de estantes con paginación"""
        query = db.query(models.Estante)

        if activo is not None:
            query = query.filter(models.Estante.activo == activo)

        return query.offset(skip).limit(limit).all()

    def create_estante(self, db: Session, estante: schemas.EstanteCreate) -> models.Estante:
        """Crear nuevo estante"""
        db_estante = models.Estante(**estante.dict())
        db.add(db_estante)
        db.commit()
        db.refresh(db_estante)
        return db_estante

    def update_estante(self, db: Session, estante_id: int, estante_update: schemas.EstanteUpdate) -> Optional[models.Estante]:
        """Actualizar estante"""
        db_estante = self.get_estante(db, estante_id)
        if not db_estante:
            return None

        update_data = estante_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_estante, field, value)

        db.commit()
        db.refresh(db_estante)
        return db_estante

    def delete_estante(self, db: Session, estante_id: int) -> bool:
        """Eliminar estante (soft delete)"""
        db_estante = self.get_estante(db, estante_id)
        if not db_estante:
            return False

        db_estante.activo = False
        db.commit()
        return True

# Instancias globales
bodega_crud = BodegaCRUD()
pasillo_crud = PasilloCRUD()
estante_crud = EstanteCRUD()

# ========================================
# CRUD PARA PRODUCTOS
# ========================================

class ProductoCRUD:

    def get_producto(self, db: Session, producto_id: int) -> Optional[models.Producto]:
        """Obtener producto por ID"""
        return db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()

    def get_producto_by_sku(self, db: Session, sku: str) -> Optional[models.Producto]:
        """Obtener producto por SKU"""
        return db.query(models.Producto).filter(models.Producto.sku == sku).first()

    def get_productos(self, db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[models.Producto]:
        """Obtener lista de productos con paginación"""
        query = db.query(models.Producto)

        if activo is not None:
            query = query.filter(models.Producto.activo == activo)

        return query.offset(skip).limit(limit).all()

    def search_productos(self, db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[models.Producto]:
        """Buscar productos por SKU, nombre o descripción"""
        search_pattern = f"%{search_term}%"
        return db.query(models.Producto).filter(
            (models.Producto.sku.ilike(search_pattern)) |
            (models.Producto.nombre_producto.ilike(search_pattern)) |
            (models.Producto.descripcion_corta.ilike(search_pattern))
        ).offset(skip).limit(limit).all()

    def get_productos_by_marca(self, db: Session, marca_id: int, activo: Optional[bool] = None) -> List[models.Producto]:
        """Obtener productos por marca"""
        query = db.query(models.Producto).filter(models.Producto.id_marca == marca_id)

        if activo is not None:
            query = query.filter(models.Producto.activo == activo)

        return query.all()

    def get_productos_by_tipo(self, db: Session, tipo_id: int, activo: Optional[bool] = None) -> List[models.Producto]:
        """Obtener productos por tipo"""
        query = db.query(models.Producto).filter(models.Producto.id_tipo_producto == tipo_id)

        if activo is not None:
            query = query.filter(models.Producto.activo == activo)

        return query.all()

    def get_productos_bajo_stock(self, db: Session) -> List[models.Producto]:
        """Obtener productos con stock bajo el punto de reorden"""
        return db.query(models.Producto).filter(
            models.Producto.activo == True,
            models.Producto.stock_actual <= models.Producto.punto_reorden
        ).all()

    def create_producto(self, db: Session, producto: schemas.ProductoCreate) -> models.Producto:
        """Crear nuevo producto"""
        db_producto = models.Producto(**producto.dict())
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        return db_producto

    def update_producto(self, db: Session, producto_id: int, producto_update: schemas.ProductoUpdate) -> Optional[models.Producto]:
        """Actualizar producto"""
        db_producto = self.get_producto(db, producto_id)
        if not db_producto:
            return None

        update_data = producto_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_producto, field, value)

        db.commit()
        db.refresh(db_producto)
        return db_producto

    def delete_producto(self, db: Session, producto_id: int) -> bool:
        """Eliminar producto (soft delete)"""
        db_producto = self.get_producto(db, producto_id)
        if not db_producto:
            return False

        db_producto.activo = False
        db.commit()
        return True

    def update_stock(self, db: Session, producto_id: int, nuevo_stock: int) -> Optional[models.Producto]:
        """Actualizar stock de un producto"""
        db_producto = self.get_producto(db, producto_id)
        if not db_producto:
            return None

        db_producto.stock_actual = nuevo_stock
        db.commit()
        db.refresh(db_producto)
        return db_producto

class ProductoProveedorCRUD:

    def get_producto_proveedor(self, db: Session, producto_proveedor_id: int) -> Optional[models.ProductoProveedor]:
        """Obtener relación producto-proveedor por ID"""
        return db.query(models.ProductoProveedor).filter(
            models.ProductoProveedor.id_producto_proveedor == producto_proveedor_id
        ).first()

    def get_proveedores_by_producto(self, db: Session, producto_id: int, activo: Optional[bool] = None) -> List[models.ProductoProveedor]:
        """Obtener proveedores de un producto"""
        query = db.query(models.ProductoProveedor).filter(models.ProductoProveedor.id_producto == producto_id)

        if activo is not None:
            query = query.filter(models.ProductoProveedor.activo == activo)

        return query.all()

    def get_productos_by_proveedor(self, db: Session, proveedor_id: int, activo: Optional[bool] = None) -> List[models.ProductoProveedor]:
        """Obtener productos de un proveedor"""
        query = db.query(models.ProductoProveedor).filter(models.ProductoProveedor.id_proveedor == proveedor_id)

        if activo is not None:
            query = query.filter(models.ProductoProveedor.activo == activo)

        return query.all()

    def get_proveedor_principal(self, db: Session, producto_id: int) -> Optional[models.ProductoProveedor]:
        """Obtener el proveedor principal de un producto"""
        return db.query(models.ProductoProveedor).filter(
            models.ProductoProveedor.id_producto == producto_id,
            models.ProductoProveedor.es_principal == True,
            models.ProductoProveedor.activo == True
        ).first()

    def get_producto_proveedores(self, db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[models.ProductoProveedor]:
        """Obtener lista de relaciones producto-proveedor"""
        query = db.query(models.ProductoProveedor)

        if activo is not None:
            query = query.filter(models.ProductoProveedor.activo == activo)

        return query.offset(skip).limit(limit).all()

    def create_producto_proveedor(self, db: Session, producto_proveedor: schemas.ProductoProveedorCreate) -> models.ProductoProveedor:
        """Crear nueva relación producto-proveedor"""
        # Si se marca como principal, desmarcar otros proveedores principales del mismo producto
        if producto_proveedor.es_principal:
            self._unset_principal_proveedores(db, producto_proveedor.id_producto)

        db_producto_proveedor = models.ProductoProveedor(**producto_proveedor.dict())
        db.add(db_producto_proveedor)
        db.commit()
        db.refresh(db_producto_proveedor)
        return db_producto_proveedor

    def update_producto_proveedor(self, db: Session, producto_proveedor_id: int,
                                 producto_proveedor_update: schemas.ProductoProveedorUpdate) -> Optional[models.ProductoProveedor]:
        """Actualizar relación producto-proveedor"""
        db_producto_proveedor = self.get_producto_proveedor(db, producto_proveedor_id)
        if not db_producto_proveedor:
            return None

        update_data = producto_proveedor_update.dict(exclude_unset=True)

        # Si se marca como principal, desmarcar otros proveedores principales del mismo producto
        if update_data.get('es_principal') == True:
            self._unset_principal_proveedores(db, db_producto_proveedor.id_producto, producto_proveedor_id)

        for field, value in update_data.items():
            setattr(db_producto_proveedor, field, value)

        db.commit()
        db.refresh(db_producto_proveedor)
        return db_producto_proveedor

    def delete_producto_proveedor(self, db: Session, producto_proveedor_id: int) -> bool:
        """Eliminar relación producto-proveedor (soft delete)"""
        db_producto_proveedor = self.get_producto_proveedor(db, producto_proveedor_id)
        if not db_producto_proveedor:
            return False

        db_producto_proveedor.activo = False
        db.commit()
        return True

    def _unset_principal_proveedores(self, db: Session, producto_id: int, exclude_id: Optional[int] = None):
        """Desmarcar todos los proveedores principales de un producto"""
        query = db.query(models.ProductoProveedor).filter(
            models.ProductoProveedor.id_producto == producto_id,
            models.ProductoProveedor.es_principal == True
        )

        if exclude_id:
            query = query.filter(models.ProductoProveedor.id_producto_proveedor != exclude_id)

        for pp in query.all():
            pp.es_principal = False

        db.commit()

# Instancias globales
producto_crud = ProductoCRUD()
producto_proveedor_crud = ProductoProveedorCRUD()

# ========================================
# CRUD PARA UBICACIONES E INVENTARIO
# ========================================

class ProductoUbicacionCRUD:

    def get_ubicacion(self, db: Session, ubicacion_id: int) -> Optional[models.ProductoUbicacion]:
        """Obtener ubicación por ID"""
        return db.query(models.ProductoUbicacion).filter(models.ProductoUbicacion.id_ubicacion == ubicacion_id).first()

    def get_ubicaciones_by_producto(self, db: Session, producto_id: int, activo: Optional[bool] = None) -> List[models.ProductoUbicacion]:
        """Obtener ubicaciones de un producto"""
        query = db.query(models.ProductoUbicacion).filter(models.ProductoUbicacion.id_producto == producto_id)

        if activo is not None:
            query = query.filter(models.ProductoUbicacion.activo == activo)

        return query.all()

    def get_ubicaciones_by_nivel(self, db: Session, nivel_id: int, activo: Optional[bool] = None) -> List[models.ProductoUbicacion]:
        """Obtener ubicaciones en un nivel"""
        query = db.query(models.ProductoUbicacion).filter(models.ProductoUbicacion.id_nivel == nivel_id)

        if activo is not None:
            query = query.filter(models.ProductoUbicacion.activo == activo)

        return query.all()

    def get_ubicaciones(self, db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[models.ProductoUbicacion]:
        """Obtener lista de ubicaciones con paginación"""
        query = db.query(models.ProductoUbicacion)

        if activo is not None:
            query = query.filter(models.ProductoUbicacion.activo == activo)

        return query.offset(skip).limit(limit).all()

    def create_ubicacion(self, db: Session, ubicacion: schemas.ProductoUbicacionCreate) -> models.ProductoUbicacion:
        """Crear nueva ubicación de producto"""
        db_ubicacion = models.ProductoUbicacion(**ubicacion.dict())
        db.add(db_ubicacion)
        db.commit()
        db.refresh(db_ubicacion)
        return db_ubicacion

    def update_ubicacion(self, db: Session, ubicacion_id: int, ubicacion_update: schemas.ProductoUbicacionUpdate) -> Optional[models.ProductoUbicacion]:
        """Actualizar ubicación de producto"""
        db_ubicacion = self.get_ubicacion(db, ubicacion_id)
        if not db_ubicacion:
            return None

        update_data = ubicacion_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ubicacion, field, value)

        db.commit()
        db.refresh(db_ubicacion)
        return db_ubicacion

    def delete_ubicacion(self, db: Session, ubicacion_id: int) -> bool:
        """Eliminar ubicación (soft delete)"""
        db_ubicacion = self.get_ubicacion(db, ubicacion_id)
        if not db_ubicacion:
            return False

        db_ubicacion.activo = False
        db.commit()
        return True

    def update_cantidad(self, db: Session, ubicacion_id: int, nueva_cantidad: int) -> Optional[models.ProductoUbicacion]:
        """Actualizar cantidad en ubicación"""
        db_ubicacion = self.get_ubicacion(db, ubicacion_id)
        if not db_ubicacion:
            return None

        db_ubicacion.cantidad = nueva_cantidad
        db.commit()
        db.refresh(db_ubicacion)
        return db_ubicacion

class DocumentoMovimientoCRUD:

    def get_documento(self, db: Session, documento_id: int) -> Optional[models.DocumentoMovimiento]:
        """Obtener documento por ID"""
        return db.query(models.DocumentoMovimiento).filter(models.DocumentoMovimiento.id_documento == documento_id).first()

    def get_documento_by_tipo_numero(self, db: Session, tipo: str, numero: str) -> Optional[models.DocumentoMovimiento]:
        """Obtener documento por tipo y número"""
        return db.query(models.DocumentoMovimiento).filter(
            models.DocumentoMovimiento.tipo_documento == tipo,
            models.DocumentoMovimiento.numero_documento == numero
        ).first()

    def get_documentos(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.DocumentoMovimiento]:
        """Obtener lista de documentos con paginación"""
        return db.query(models.DocumentoMovimiento).offset(skip).limit(limit).all()

    def get_documentos_by_proveedor(self, db: Session, proveedor_id: int) -> List[models.DocumentoMovimiento]:
        """Obtener documentos de un proveedor"""
        return db.query(models.DocumentoMovimiento).filter(models.DocumentoMovimiento.id_proveedor == proveedor_id).all()

    def create_documento(self, db: Session, documento: schemas.DocumentoMovimientoCreate) -> models.DocumentoMovimiento:
        """Crear nuevo documento"""
        db_documento = models.DocumentoMovimiento(**documento.dict())
        db.add(db_documento)
        db.commit()
        db.refresh(db_documento)
        return db_documento

    def update_documento(self, db: Session, documento_id: int, documento_update: schemas.DocumentoMovimientoUpdate) -> Optional[models.DocumentoMovimiento]:
        """Actualizar documento"""
        db_documento = self.get_documento(db, documento_id)
        if not db_documento:
            return None

        update_data = documento_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_documento, field, value)

        db.commit()
        db.refresh(db_documento)
        return db_documento

class MovimientoInventarioCRUD:

    def get_movimiento(self, db: Session, movimiento_id: int) -> Optional[models.MovimientoInventario]:
        """Obtener movimiento por ID"""
        return db.query(models.MovimientoInventario).filter(models.MovimientoInventario.id_movimiento == movimiento_id).first()

    def get_movimiento_by_numero(self, db: Session, numero: str) -> Optional[models.MovimientoInventario]:
        """Obtener movimiento por número"""
        return db.query(models.MovimientoInventario).filter(models.MovimientoInventario.numero_movimiento == numero).first()

    def get_movimientos(self, db: Session, skip: int = 0, limit: int = 100, estado: Optional[str] = None) -> List[models.MovimientoInventario]:
        """Obtener lista de movimientos con paginación"""
        query = db.query(models.MovimientoInventario)

        if estado:
            query = query.filter(models.MovimientoInventario.estado == estado)

        return query.order_by(models.MovimientoInventario.fecha_movimiento.desc()).offset(skip).limit(limit).all()

    def get_movimientos_by_usuario(self, db: Session, usuario_id: int) -> List[models.MovimientoInventario]:
        """Obtener movimientos de un usuario"""
        return db.query(models.MovimientoInventario).filter(models.MovimientoInventario.id_usuario == usuario_id).all()

    def create_movimiento(self, db: Session, movimiento: schemas.MovimientoInventarioCreate) -> models.MovimientoInventario:
        """Crear nuevo movimiento"""
        db_movimiento = models.MovimientoInventario(**movimiento.dict())
        db.add(db_movimiento)
        db.commit()
        db.refresh(db_movimiento)
        return db_movimiento

    def update_movimiento(self, db: Session, movimiento_id: int, movimiento_update: schemas.MovimientoInventarioUpdate) -> Optional[models.MovimientoInventario]:
        """Actualizar movimiento"""
        db_movimiento = self.get_movimiento(db, movimiento_id)
        if not db_movimiento:
            return None

        update_data = movimiento_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_movimiento, field, value)

        db.commit()
        db.refresh(db_movimiento)
        return db_movimiento

    def autorizar_movimiento(self, db: Session, movimiento_id: int, autorizado_por: int) -> Optional[models.MovimientoInventario]:
        """Autorizar un movimiento"""
        db_movimiento = self.get_movimiento(db, movimiento_id)
        if not db_movimiento:
            return None

        db_movimiento.estado = 'AUTORIZADO'
        db_movimiento.autorizado_por = autorizado_por
        db_movimiento.fecha_autorizacion = func.now()

        db.commit()
        db.refresh(db_movimiento)
        return db_movimiento

    def procesar_movimiento(self, db: Session, movimiento_id: int) -> Optional[models.MovimientoInventario]:
        """Procesar un movimiento (actualizar stocks)"""
        db_movimiento = self.get_movimiento(db, movimiento_id)
        if not db_movimiento or db_movimiento.estado != 'AUTORIZADO':
            return None

        # Procesar cada detalle del movimiento
        for detalle in db_movimiento.detalles:
            self._procesar_detalle_movimiento(db, detalle, db_movimiento.tipo_movimiento.afecta_stock)

        db_movimiento.estado = 'PROCESADO'
        db.commit()
        db.refresh(db_movimiento)
        return db_movimiento

    def _procesar_detalle_movimiento(self, db: Session, detalle: models.MovimientoDetalle, afecta_stock: str):
        """Procesar un detalle de movimiento actualizando las ubicaciones"""
        if afecta_stock == 'AUMENTA':
            if detalle.id_ubicacion_destino:
                ubicacion = producto_ubicacion_crud.get_ubicacion(db, detalle.id_ubicacion_destino)
                if ubicacion:
                    ubicacion.cantidad += detalle.cantidad

        elif afecta_stock == 'DISMINUYE':
            if detalle.id_ubicacion_origen:
                ubicacion = producto_ubicacion_crud.get_ubicacion(db, detalle.id_ubicacion_origen)
                if ubicacion:
                    ubicacion.cantidad = max(0, ubicacion.cantidad - detalle.cantidad)

        elif afecta_stock == 'NO_AFECTA':
            # Para transferencias, quitar de origen y agregar a destino
            if detalle.id_ubicacion_origen:
                ubicacion_origen = producto_ubicacion_crud.get_ubicacion(db, detalle.id_ubicacion_origen)
                if ubicacion_origen:
                    ubicacion_origen.cantidad = max(0, ubicacion_origen.cantidad - detalle.cantidad)

            if detalle.id_ubicacion_destino:
                ubicacion_destino = producto_ubicacion_crud.get_ubicacion(db, detalle.id_ubicacion_destino)
                if ubicacion_destino:
                    ubicacion_destino.cantidad += detalle.cantidad

class MovimientoDetalleCRUD:

    def get_detalle(self, db: Session, detalle_id: int) -> Optional[models.MovimientoDetalle]:
        """Obtener detalle por ID"""
        return db.query(models.MovimientoDetalle).filter(models.MovimientoDetalle.id_detalle == detalle_id).first()

    def get_detalles_by_movimiento(self, db: Session, movimiento_id: int) -> List[models.MovimientoDetalle]:
        """Obtener detalles de un movimiento"""
        return db.query(models.MovimientoDetalle).filter(models.MovimientoDetalle.id_movimiento == movimiento_id).all()

    def create_detalle(self, db: Session, detalle: schemas.MovimientoDetalleCreate) -> models.MovimientoDetalle:
        """Crear nuevo detalle"""
        db_detalle = models.MovimientoDetalle(**detalle.dict())
        db.add(db_detalle)
        db.commit()
        db.refresh(db_detalle)
        return db_detalle

    def update_detalle(self, db: Session, detalle_id: int, detalle_update: schemas.MovimientoDetalleUpdate) -> Optional[models.MovimientoDetalle]:
        """Actualizar detalle"""
        db_detalle = self.get_detalle(db, detalle_id)
        if not db_detalle:
            return None

        update_data = detalle_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_detalle, field, value)

        db.commit()
        db.refresh(db_detalle)
        return db_detalle

    def delete_detalle(self, db: Session, detalle_id: int) -> bool:
        """Eliminar detalle"""
        db_detalle = self.get_detalle(db, detalle_id)
        if not db_detalle:
            return False

        db.delete(db_detalle)
        db.commit()
        return True

# ========================================
# CRUD PARA LOTES
# ========================================

class LoteCRUD:
    def get_lote(self, db: Session, lote_id: int) -> Optional[models.Lote]:
        """Obtener lote por ID"""
        return db.query(models.Lote).filter(models.Lote.id_lote == lote_id).first()

    def get_lote_by_numero(self, db: Session, producto_id: int, numero_lote: str) -> Optional[models.Lote]:
        """Obtener lote por producto y número"""
        return db.query(models.Lote).filter(
            models.Lote.id_producto == producto_id,
            models.Lote.numero_lote == numero_lote
        ).first()

    def get_lotes(self, db: Session, skip: int = 0, limit: int = 100, estado: Optional[str] = None) -> List[models.Lote]:
        """Obtener lista de lotes con paginación"""
        query = db.query(models.Lote)

        if estado:
            query = query.filter(models.Lote.estado == estado)

        return query.order_by(models.Lote.fecha_creacion.desc()).offset(skip).limit(limit).all()

    def get_lotes_by_producto(self, db: Session, producto_id: int, estado: Optional[str] = None) -> List[models.Lote]:
        """Obtener lotes de un producto específico"""
        query = db.query(models.Lote).filter(models.Lote.id_producto == producto_id)

        if estado:
            query = query.filter(models.Lote.estado == estado)

        return query.order_by(models.Lote.fecha_vencimiento.asc()).all()

    def get_lotes_by_proveedor(self, db: Session, proveedor_id: int, estado: Optional[str] = None) -> List[models.Lote]:
        """Obtener lotes de un proveedor específico"""
        query = db.query(models.Lote).filter(models.Lote.id_proveedor == proveedor_id)

        if estado:
            query = query.filter(models.Lote.estado == estado)

        return query.order_by(models.Lote.fecha_creacion.desc()).all()

    def get_lotes_vencidos(self, db: Session) -> List[models.Lote]:
        """Obtener lotes vencidos"""
        from datetime import date
        return db.query(models.Lote).filter(
            models.Lote.fecha_vencimiento < date.today(),
            models.Lote.estado != 'VENCIDO'
        ).all()

    def get_lotes_por_vencer(self, db: Session, dias: int = 30) -> List[models.Lote]:
        """Obtener lotes que vencen en X días"""
        from datetime import date, timedelta
        fecha_limite = date.today() + timedelta(days=dias)
        return db.query(models.Lote).filter(
            models.Lote.fecha_vencimiento <= fecha_limite,
            models.Lote.fecha_vencimiento >= date.today(),
            models.Lote.estado == 'ACTIVO'
        ).all()

    def create_lote(self, db: Session, lote: schemas.LoteCreate) -> models.Lote:
        """Crear nuevo lote"""
        db_lote = models.Lote(**lote.model_dump())
        db.add(db_lote)
        db.commit()
        db.refresh(db_lote)
        return db_lote

    def update_lote(self, db: Session, lote_id: int, lote_update: schemas.LoteUpdate) -> Optional[models.Lote]:
        """Actualizar lote"""
        db_lote = self.get_lote(db, lote_id)
        if not db_lote:
            return None

        update_data = lote_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_lote, key, value)

        db.commit()
        db.refresh(db_lote)
        return db_lote

    def update_cantidad_lote(self, db: Session, lote_id: int, nueva_cantidad: int) -> Optional[models.Lote]:
        """Actualizar cantidad actual de un lote"""
        db_lote = self.get_lote(db, lote_id)
        if not db_lote:
            return None

        db_lote.cantidad_actual = nueva_cantidad

        # Cambiar estado automáticamente si se agota
        if nueva_cantidad == 0:
            db_lote.estado = 'AGOTADO'

        db.commit()
        db.refresh(db_lote)
        return db_lote

    def delete_lote(self, db: Session, lote_id: int) -> bool:
        """Eliminar lote (verificar que no tenga números de serie)"""
        db_lote = self.get_lote(db, lote_id)
        if not db_lote:
            return False

        # Verificar que no tenga números de serie asociados
        numeros_serie = db.query(models.NumeroSerie).filter(models.NumeroSerie.id_lote == lote_id).count()
        if numeros_serie > 0:
            return False

        db.delete(db_lote)
        db.commit()
        return True


# ========================================
# CRUD PARA NÚMEROS DE SERIE
# ========================================

class NumeroSerieCRUD:
    def get_numero_serie(self, db: Session, serie_id: int) -> Optional[models.NumeroSerie]:
        """Obtener número de serie por ID"""
        return db.query(models.NumeroSerie).filter(models.NumeroSerie.id_serie == serie_id).first()

    def get_numero_serie_by_numero(self, db: Session, producto_id: int, numero_serie: str) -> Optional[models.NumeroSerie]:
        """Obtener número de serie por producto y número"""
        return db.query(models.NumeroSerie).filter(
            models.NumeroSerie.id_producto == producto_id,
            models.NumeroSerie.numero_serie == numero_serie
        ).first()

    def get_numeros_serie(self, db: Session, skip: int = 0, limit: int = 100, estado: Optional[str] = None) -> List[models.NumeroSerie]:
        """Obtener lista de números de serie con paginación"""
        query = db.query(models.NumeroSerie)

        if estado:
            query = query.filter(models.NumeroSerie.estado == estado)

        return query.order_by(models.NumeroSerie.fecha_ingreso.desc()).offset(skip).limit(limit).all()

    def get_numeros_serie_by_producto(self, db: Session, producto_id: int, estado: Optional[str] = None) -> List[models.NumeroSerie]:
        """Obtener números de serie de un producto específico"""
        query = db.query(models.NumeroSerie).filter(models.NumeroSerie.id_producto == producto_id)

        if estado:
            query = query.filter(models.NumeroSerie.estado == estado)

        return query.order_by(models.NumeroSerie.fecha_ingreso.desc()).all()

    def get_numeros_serie_by_lote(self, db: Session, lote_id: int, estado: Optional[str] = None) -> List[models.NumeroSerie]:
        """Obtener números de serie de un lote específico"""
        query = db.query(models.NumeroSerie).filter(models.NumeroSerie.id_lote == lote_id)

        if estado:
            query = query.filter(models.NumeroSerie.estado == estado)

        return query.order_by(models.NumeroSerie.numero_serie.asc()).all()

    def get_numeros_serie_by_ubicacion(self, db: Session, ubicacion_id: int, estado: Optional[str] = None) -> List[models.NumeroSerie]:
        """Obtener números de serie en una ubicación específica"""
        query = db.query(models.NumeroSerie).filter(models.NumeroSerie.id_ubicacion == ubicacion_id)

        if estado:
            query = query.filter(models.NumeroSerie.estado == estado)

        return query.order_by(models.NumeroSerie.numero_serie.asc()).all()

    def get_numeros_serie_disponibles(self, db: Session, producto_id: Optional[int] = None) -> List[models.NumeroSerie]:
        """Obtener números de serie disponibles"""
        query = db.query(models.NumeroSerie).filter(models.NumeroSerie.estado == 'DISPONIBLE')

        if producto_id:
            query = query.filter(models.NumeroSerie.id_producto == producto_id)

        return query.all()

    def create_numero_serie(self, db: Session, numero_serie: schemas.NumeroSerieCreate) -> models.NumeroSerie:
        """Crear nuevo número de serie"""
        db_numero_serie = models.NumeroSerie(**numero_serie.model_dump())
        db.add(db_numero_serie)
        db.commit()
        db.refresh(db_numero_serie)
        return db_numero_serie

    def update_numero_serie(self, db: Session, serie_id: int, numero_serie_update: schemas.NumeroSerieUpdate) -> Optional[models.NumeroSerie]:
        """Actualizar número de serie"""
        db_numero_serie = self.get_numero_serie(db, serie_id)
        if not db_numero_serie:
            return None

        update_data = numero_serie_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_numero_serie, key, value)

        db.commit()
        db.refresh(db_numero_serie)
        return db_numero_serie

    def reservar_numero_serie(self, db: Session, serie_id: int, cliente: str) -> Optional[models.NumeroSerie]:
        """Reservar número de serie para un cliente"""
        db_numero_serie = self.get_numero_serie(db, serie_id)
        if not db_numero_serie or db_numero_serie.estado != 'DISPONIBLE':
            return None

        db_numero_serie.estado = 'RESERVADO'
        db_numero_serie.cliente_asignado = cliente

        db.commit()
        db.refresh(db_numero_serie)
        return db_numero_serie

    def vender_numero_serie(self, db: Session, serie_id: int, cliente: str, fecha_venta: Optional[date] = None) -> Optional[models.NumeroSerie]:
        """Marcar número de serie como vendido"""

        db_numero_serie = self.get_numero_serie(db, serie_id)
        if not db_numero_serie or db_numero_serie.estado not in ['DISPONIBLE', 'RESERVADO']:
            return None

        db_numero_serie.estado = 'VENDIDO'
        db_numero_serie.cliente_asignado = cliente
        db_numero_serie.fecha_venta = fecha_venta or date.today()

        db.commit()
        db.refresh(db_numero_serie)
        return db_numero_serie

    def liberar_numero_serie(self, db: Session, serie_id: int) -> Optional[models.NumeroSerie]:
        """Liberar número de serie (volver a disponible)"""
        db_numero_serie = self.get_numero_serie(db, serie_id)
        if not db_numero_serie:
            return None

        db_numero_serie.estado = 'DISPONIBLE'
        db_numero_serie.cliente_asignado = None
        db_numero_serie.fecha_venta = None

        db.commit()
        db.refresh(db_numero_serie)
        return db_numero_serie

    def delete_numero_serie(self, db: Session, serie_id: int) -> bool:
        """Eliminar número de serie"""
        db_numero_serie = self.get_numero_serie(db, serie_id)
        if not db_numero_serie:
            return False

        db.delete(db_numero_serie)
        db.commit()
        return True


# ========================================
# CRUD PARA CLIENTES
# ========================================

class ClienteCRUD:
    def get_cliente(self, db: Session, cliente_id: int) -> Optional[models.Cliente]:
        """Obtener cliente por ID"""
        return db.query(models.Cliente).filter(models.Cliente.id_cliente == cliente_id).first()

    def get_cliente_by_codigo(self, db: Session, codigo_cliente: str) -> Optional[models.Cliente]:
        """Obtener cliente por código"""
        return db.query(models.Cliente).filter(models.Cliente.codigo_cliente == codigo_cliente).first()

    def get_clientes(self, db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[models.Cliente]:
        """Obtener lista de clientes con paginación"""
        query = db.query(models.Cliente)

        if activo is not None:
            query = query.filter(models.Cliente.activo == activo)

        return query.order_by(models.Cliente.nombre_cliente.asc()).offset(skip).limit(limit).all()

    def get_clientes_by_tipo(self, db: Session, tipo_cliente: str, activo: Optional[bool] = None) -> List[models.Cliente]:
        """Obtener clientes por tipo"""
        query = db.query(models.Cliente).filter(models.Cliente.tipo_cliente == tipo_cliente)

        if activo is not None:
            query = query.filter(models.Cliente.activo == activo)

        return query.order_by(models.Cliente.nombre_cliente.asc()).all()

    def get_clientes_by_ciudad(self, db: Session, ciudad: str, activo: Optional[bool] = None) -> List[models.Cliente]:
        """Obtener clientes por ciudad"""
        query = db.query(models.Cliente).filter(models.Cliente.ciudad.ilike(f"%{ciudad}%"))

        if activo is not None:
            query = query.filter(models.Cliente.activo == activo)

        return query.order_by(models.Cliente.nombre_cliente.asc()).all()

    def get_clientes_by_estado(self, db: Session, estado: str, activo: Optional[bool] = None) -> List[models.Cliente]:
        """Obtener clientes por estado/provincia"""
        query = db.query(models.Cliente).filter(models.Cliente.estado.ilike(f"%{estado}%"))

        if activo is not None:
            query = query.filter(models.Cliente.activo == activo)

        return query.order_by(models.Cliente.nombre_cliente.asc()).all()

    def search_clientes(self, db: Session, search_term: str, activo: Optional[bool] = None) -> List[models.Cliente]:
        """Buscar clientes por nombre, código o razón social"""
        search_pattern = f"%{search_term}%"
        query = db.query(models.Cliente).filter(
            (models.Cliente.nombre_cliente.ilike(search_pattern)) |
            (models.Cliente.codigo_cliente.ilike(search_pattern)) |
            (models.Cliente.razon_social.ilike(search_pattern))
        )

        if activo is not None:
            query = query.filter(models.Cliente.activo == activo)

        return query.order_by(models.Cliente.nombre_cliente.asc()).all()

    def create_cliente(self, db: Session, cliente: schemas.ClienteCreate) -> models.Cliente:
        """Crear nuevo cliente"""
        db_cliente = models.Cliente(**cliente.model_dump())
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente

    def update_cliente(self, db: Session, cliente_id: int, cliente_update: schemas.ClienteUpdate) -> Optional[models.Cliente]:
        """Actualizar cliente"""
        db_cliente = self.get_cliente(db, cliente_id)
        if not db_cliente:
            return None

        update_data = cliente_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_cliente, key, value)

        db.commit()
        db.refresh(db_cliente)
        return db_cliente

    def toggle_cliente_activo(self, db: Session, cliente_id: int) -> Optional[models.Cliente]:
        """Cambiar estado activo/inactivo de un cliente"""
        db_cliente = self.get_cliente(db, cliente_id)
        if not db_cliente:
            return None

        db_cliente.activo = not db_cliente.activo
        db.commit()
        db.refresh(db_cliente)
        return db_cliente

    def delete_cliente(self, db: Session, cliente_id: int) -> bool:
        """Eliminar cliente (soft delete - marcar como inactivo)"""
        db_cliente = self.get_cliente(db, cliente_id)
        if not db_cliente:
            return False

        # Soft delete - marcar como inactivo en lugar de eliminar
        db_cliente.activo = False
        db.commit()
        return True

    def get_estadisticas_clientes(self, db: Session):
        """Obtener estadísticas generales de clientes"""
        from sqlalchemy import func

        stats = db.query(
            func.count(models.Cliente.id_cliente).label('total_clientes'),
            func.count(func.case([(models.Cliente.activo == True, 1)])).label('clientes_activos'),
            func.count(func.case([(models.Cliente.activo == False, 1)])).label('clientes_inactivos')
        ).first()

        # Estadísticas por tipo
        stats_por_tipo = db.query(
            models.Cliente.tipo_cliente,
            func.count(models.Cliente.id_cliente).label('total'),
            func.count(func.case([(models.Cliente.activo == True, 1)])).label('activos')
        ).group_by(models.Cliente.tipo_cliente).all()

        return {
            "resumen": {
                "total_clientes": stats.total_clientes or 0,
                "clientes_activos": stats.clientes_activos or 0,
                "clientes_inactivos": stats.clientes_inactivos or 0
            },
            "por_tipo": [
                {
                    "tipo_cliente": stat.tipo_cliente,
                    "total": stat.total or 0,
                    "activos": stat.activos or 0
                }
                for stat in stats_por_tipo
            ]
        }


# ========================================
# CRUD PARA OBRAS
# ========================================

class ObraCRUD:
    def get_obra(self, db: Session, obra_id: int) -> Optional[models.Obra]:
        """Obtener obra por ID"""
        return db.query(models.Obra).filter(models.Obra.id_obra == obra_id).first()

    def get_obra_by_codigo(self, db: Session, codigo_obra: str) -> Optional[models.Obra]:
        """Obtener obra por código"""
        return db.query(models.Obra).filter(models.Obra.codigo_obra == codigo_obra).first()

    def get_obras(self, db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[models.Obra]:
        """Obtener lista de obras con paginación"""
        query = db.query(models.Obra)

        if activo is not None:
            query = query.filter(models.Obra.activo == activo)

        return query.order_by(models.Obra.fecha_creacion.desc()).offset(skip).limit(limit).all()

    def get_obras_by_cliente(self, db: Session, cliente_id: int, activo: Optional[bool] = None) -> List[models.Obra]:
        """Obtener obras de un cliente específico"""
        query = db.query(models.Obra).filter(models.Obra.id_cliente == cliente_id)

        if activo is not None:
            query = query.filter(models.Obra.activo == activo)

        return query.order_by(models.Obra.fecha_creacion.desc()).all()

    def get_obras_by_estado(self, db: Session, estado: str, activo: Optional[bool] = None) -> List[models.Obra]:
        """Obtener obras por estado"""
        query = db.query(models.Obra).filter(models.Obra.estado == estado)

        if activo is not None:
            query = query.filter(models.Obra.activo == activo)

        return query.order_by(models.Obra.fecha_inicio_programada.asc()).all()

    def get_obras_by_prioridad(self, db: Session, prioridad: str, activo: Optional[bool] = None) -> List[models.Obra]:
        """Obtener obras por prioridad"""
        query = db.query(models.Obra).filter(models.Obra.prioridad == prioridad)

        if activo is not None:
            query = query.filter(models.Obra.activo == activo)

        return query.order_by(models.Obra.fecha_inicio_programada.asc()).all()

    def get_obras_by_ciudad(self, db: Session, ciudad: str, activo: Optional[bool] = None) -> List[models.Obra]:
        """Obtener obras por ciudad"""
        query = db.query(models.Obra).filter(models.Obra.ciudad.ilike(f"%{ciudad}%"))

        if activo is not None:
            query = query.filter(models.Obra.activo == activo)

        return query.order_by(models.Obra.nombre_obra.asc()).all()

    def search_obras(self, db: Session, search_term: str, activo: Optional[bool] = None) -> List[models.Obra]:
        """Buscar obras por nombre o código"""
        search_pattern = f"%{search_term}%"
        query = db.query(models.Obra).filter(
            (models.Obra.nombre_obra.ilike(search_pattern)) |
            (models.Obra.codigo_obra.ilike(search_pattern)) |
            (models.Obra.descripcion.ilike(search_pattern))
        )

        if activo is not None:
            query = query.filter(models.Obra.activo == activo)

        return query.order_by(models.Obra.nombre_obra.asc()).all()

    def get_obras_vencidas(self, db: Session) -> List[models.Obra]:
        """Obtener obras que deberían haber terminado (vencidas)"""
        from datetime import date
        return db.query(models.Obra).filter(
            models.Obra.fecha_fin_programada < date.today(),
            models.Obra.estado.in_(['PLANIFICACION', 'EN_EJECUCION']),
            models.Obra.activo == True
        ).all()

    def get_obras_proximas_inicio(self, db: Session, dias: int = 7) -> List[models.Obra]:
        """Obtener obras que inician en los próximos X días"""
        from datetime import date, timedelta
        fecha_limite = date.today() + timedelta(days=dias)
        return db.query(models.Obra).filter(
            models.Obra.fecha_inicio_programada <= fecha_limite,
            models.Obra.fecha_inicio_programada >= date.today(),
            models.Obra.estado == 'PLANIFICACION',
            models.Obra.activo == True
        ).all()

    def get_obras_proximas_fin(self, db: Session, dias: int = 7) -> List[models.Obra]:
        """Obtener obras que terminan en los próximos X días"""
        from datetime import date, timedelta
        fecha_limite = date.today() + timedelta(days=dias)
        return db.query(models.Obra).filter(
            models.Obra.fecha_fin_programada <= fecha_limite,
            models.Obra.fecha_fin_programada >= date.today(),
            models.Obra.estado == 'EN_EJECUCION',
            models.Obra.activo == True
        ).all()

    def create_obra(self, db: Session, obra: schemas.ObraCreate, usuario_id: Optional[int] = None) -> models.Obra:
        """Crear nueva obra"""
        obra_data = obra.model_dump()
        if usuario_id:
            obra_data['usuario_creacion'] = usuario_id

        db_obra = models.Obra(**obra_data)
        db.add(db_obra)
        db.commit()
        db.refresh(db_obra)
        return db_obra

    def update_obra(self, db: Session, obra_id: int, obra_update: schemas.ObraUpdate) -> Optional[models.Obra]:
        """Actualizar obra"""
        db_obra = self.get_obra(db, obra_id)
        if not db_obra:
            return None

        update_data = obra_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obra, key, value)

        db.commit()
        db.refresh(db_obra)
        return db_obra

    def cambiar_estado_obra(self, db: Session, obra_id: int, nuevo_estado: str, usuario_id: Optional[int] = None) -> Optional[models.Obra]:
        """Cambiar estado de una obra con validaciones de negocio"""
        db_obra = self.get_obra(db, obra_id)
        if not db_obra:
            return None

        # Validaciones de transición de estado
        estado_actual = db_obra.estado
        transiciones_validas = {
            'PLANIFICACION': ['EN_EJECUCION', 'CANCELADA'],
            'EN_EJECUCION': ['SUSPENDIDA', 'FINALIZADA', 'CANCELADA'],
            'SUSPENDIDA': ['EN_EJECUCION', 'CANCELADA'],
            'FINALIZADA': [],  # No se puede cambiar desde finalizada
            'CANCELADA': []    # No se puede cambiar desde cancelada
        }

        if nuevo_estado not in transiciones_validas.get(estado_actual, []):
            return None

        # Actualizar fechas automáticamente según el estado
        from datetime import date
        if nuevo_estado == 'EN_EJECUCION' and not db_obra.fecha_inicio_real:
            db_obra.fecha_inicio_real = date.today()
        elif nuevo_estado == 'FINALIZADA' and not db_obra.fecha_fin_real:
            db_obra.fecha_fin_real = date.today()

        db_obra.estado = nuevo_estado
        if usuario_id:
            db_obra.usuario_modificacion = usuario_id

        db.commit()
        db.refresh(db_obra)
        return db_obra

    def toggle_obra_activa(self, db: Session, obra_id: int) -> Optional[models.Obra]:
        """Cambiar estado activo/inactivo de una obra"""
        db_obra = self.get_obra(db, obra_id)
        if not db_obra:
            return None

        db_obra.activo = not db_obra.activo
        db.commit()
        db.refresh(db_obra)
        return db_obra

    def delete_obra(self, db: Session, obra_id: int) -> bool:
        """Eliminar obra (soft delete - marcar como inactiva)"""
        db_obra = self.get_obra(db, obra_id)
        if not db_obra:
            return False

        # Verificar que se pueda eliminar (solo en planificación)
        if db_obra.estado not in ['PLANIFICACION', 'CANCELADA']:
            return False

        # Soft delete - marcar como inactiva
        db_obra.activo = False
        db.commit()
        return True

    def get_estadisticas_obras(self, db: Session):
        """Obtener estadísticas generales de obras"""
        from sqlalchemy import func

        # Estadísticas generales
        stats_generales = db.query(
            func.count(models.Obra.id_obra).label('total_obras'),
            func.count(func.case([(models.Obra.activo == True, 1)])).label('obras_activas'),
            func.sum(models.Obra.valor_contrato).label('valor_total_contratos')
        ).first()

        # Estadísticas por estado
        stats_por_estado = db.query(
            models.Obra.estado,
            func.count(models.Obra.id_obra).label('total'),
            func.sum(models.Obra.valor_contrato).label('valor_total')
        ).filter(models.Obra.activo == True).group_by(models.Obra.estado).all()

        # Estadísticas por prioridad
        stats_por_prioridad = db.query(
            models.Obra.prioridad,
            func.count(models.Obra.id_obra).label('total')
        ).filter(models.Obra.activo == True).group_by(models.Obra.prioridad).all()

        return {
            "resumen": {
                "total_obras": stats_generales.total_obras or 0,
                "obras_activas": stats_generales.obras_activas or 0,
                "valor_total_contratos": float(stats_generales.valor_total_contratos or 0)
            },
            "por_estado": [
                {
                    "estado": stat.estado,
                    "total": stat.total or 0,
                    "valor_total": float(stat.valor_total or 0)
                }
                for stat in stats_por_estado
            ],
            "por_prioridad": [
                {
                    "prioridad": stat.prioridad,
                    "total": stat.total or 0
                }
                for stat in stats_por_prioridad
            ]
        }


# ========================================
# CRUD PARA ALMACÉN DE OBRA
# ========================================

class AlmacenObraCRUD:
    def get_almacen_obra(self, db: Session, almacen_id: int) -> Optional[models.AlmacenObra]:
        """Obtener almacén de obra por ID"""
        return db.query(models.AlmacenObra).filter(models.AlmacenObra.id_almacen_obra == almacen_id).first()

    def get_almacen_by_obra(self, db: Session, obra_id: int) -> Optional[models.AlmacenObra]:
        """Obtener almacén por ID de obra"""
        return db.query(models.AlmacenObra).filter(models.AlmacenObra.id_obra == obra_id).first()

    def get_almacenes_obra(self, db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[models.AlmacenObra]:
        """Obtener lista de almacenes de obra con paginación"""
        query = db.query(models.AlmacenObra)

        if activo is not None:
            query = query.filter(models.AlmacenObra.activo == activo)

        return query.order_by(models.AlmacenObra.fecha_creacion.desc()).offset(skip).limit(limit).all()

    def get_almacenes_by_responsable(self, db: Session, responsable: str, activo: Optional[bool] = None) -> List[models.AlmacenObra]:
        """Obtener almacenes por responsable"""
        query = db.query(models.AlmacenObra).filter(models.AlmacenObra.responsable.ilike(f"%{responsable}%"))

        if activo is not None:
            query = query.filter(models.AlmacenObra.activo == activo)

        return query.order_by(models.AlmacenObra.nombre_almacen.asc()).all()

    def get_almacenes_con_seguridad(self, db: Session, activo: Optional[bool] = None) -> List[models.AlmacenObra]:
        """Obtener almacenes que tienen seguridad"""
        query = db.query(models.AlmacenObra).filter(models.AlmacenObra.tiene_seguridad == True)

        if activo is not None:
            query = query.filter(models.AlmacenObra.activo == activo)

        return query.order_by(models.AlmacenObra.nombre_almacen.asc()).all()

    def get_almacenes_sin_techo(self, db: Session, activo: Optional[bool] = None) -> List[models.AlmacenObra]:
        """Obtener almacenes sin techo (a la intemperie)"""
        query = db.query(models.AlmacenObra).filter(models.AlmacenObra.tiene_techo == False)

        if activo is not None:
            query = query.filter(models.AlmacenObra.activo == activo)

        return query.order_by(models.AlmacenObra.nombre_almacen.asc()).all()

    def search_almacenes(self, db: Session, search_term: str, activo: Optional[bool] = None) -> List[models.AlmacenObra]:
        """Buscar almacenes por nombre, descripción o responsable"""
        search_pattern = f"%{search_term}%"
        query = db.query(models.AlmacenObra).filter(
            (models.AlmacenObra.nombre_almacen.ilike(search_pattern)) |
            (models.AlmacenObra.descripcion.ilike(search_pattern)) |
            (models.AlmacenObra.responsable.ilike(search_pattern))
        )

        if activo is not None:
            query = query.filter(models.AlmacenObra.activo == activo)

        return query.order_by(models.AlmacenObra.nombre_almacen.asc()).all()

    def create_almacen_obra(self, db: Session, almacen: schemas.AlmacenObraCreate) -> models.AlmacenObra:
        """Crear nuevo almacén de obra"""
        db_almacen = models.AlmacenObra(**almacen.model_dump())
        db.add(db_almacen)
        db.commit()
        db.refresh(db_almacen)
        return db_almacen

    def update_almacen_obra(self, db: Session, almacen_id: int, almacen_update: schemas.AlmacenObraUpdate) -> Optional[models.AlmacenObra]:
        """Actualizar almacén de obra"""
        db_almacen = self.get_almacen_obra(db, almacen_id)
        if not db_almacen:
            return None

        update_data = almacen_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_almacen, key, value)

        db.commit()
        db.refresh(db_almacen)
        return db_almacen

    def toggle_almacen_activo(self, db: Session, almacen_id: int) -> Optional[models.AlmacenObra]:
        """Cambiar estado activo/inactivo de un almacén"""
        db_almacen = self.get_almacen_obra(db, almacen_id)
        if not db_almacen:
            return None

        db_almacen.activo = not db_almacen.activo
        db.commit()
        db.refresh(db_almacen)
        return db_almacen

    def delete_almacen_obra(self, db: Session, almacen_id: int) -> bool:
        """Eliminar almacén de obra (soft delete - marcar como inactivo)"""
        db_almacen = self.get_almacen_obra(db, almacen_id)
        if not db_almacen:
            return False

        # Soft delete - marcar como inactivo
        db_almacen.activo = False
        db.commit()
        return True

    def get_estadisticas_almacenes(self, db: Session):
        """Obtener estadísticas generales de almacenes de obra"""
        from sqlalchemy import func

        # Estadísticas generales
        stats_generales = db.query(
            func.count(models.AlmacenObra.id_almacen_obra).label('total_almacenes'),
            func.count(func.case([(models.AlmacenObra.activo == True, 1)])).label('almacenes_activos'),
            func.count(func.case([(models.AlmacenObra.tiene_seguridad == True, 1)])).label('con_seguridad'),
            func.count(func.case([(models.AlmacenObra.tiene_techo == True, 1)])).label('con_techo'),
            func.sum(models.AlmacenObra.capacidad_m3).label('capacidad_total'),
            func.avg(models.AlmacenObra.capacidad_m3).label('capacidad_promedio')
        ).first()

        return {
            "resumen": {
                "total_almacenes": stats_generales.total_almacenes or 0,
                "almacenes_activos": stats_generales.almacenes_activos or 0,
                "con_seguridad": stats_generales.con_seguridad or 0,
                "con_techo": stats_generales.con_techo or 0,
                "capacidad_total_m3": float(stats_generales.capacidad_total or 0),
                "capacidad_promedio_m3": float(stats_generales.capacidad_promedio or 0)
            }
        }

    def get_almacenes_por_capacidad(self, db: Session, capacidad_minima: Optional[float] = None, capacidad_maxima: Optional[float] = None) -> List[models.AlmacenObra]:
        """Obtener almacenes filtrados por rango de capacidad"""
        query = db.query(models.AlmacenObra).filter(
            models.AlmacenObra.capacidad_m3.isnot(None),
            models.AlmacenObra.activo == True
        )

        if capacidad_minima is not None:
            query = query.filter(models.AlmacenObra.capacidad_m3 >= capacidad_minima)

        if capacidad_maxima is not None:
            query = query.filter(models.AlmacenObra.capacidad_m3 <= capacidad_maxima)

        return query.order_by(models.AlmacenObra.capacidad_m3.desc()).all()


# Instancias globales
producto_ubicacion_crud = ProductoUbicacionCRUD()
documento_movimiento_crud = DocumentoMovimientoCRUD()
movimiento_inventario_crud = MovimientoInventarioCRUD()
movimiento_detalle_crud = MovimientoDetalleCRUD()
lote_crud = LoteCRUD()
numero_serie_crud = NumeroSerieCRUD()
cliente_crud = ClienteCRUD()
obra_crud = ObraCRUD()
almacen_obra_crud = AlmacenObraCRUD()


# ========================================
# CRUD PARA DESPACHOS DE OBRA
# ========================================

class DespachosObraCRUD:

    def get_despacho(self, db: Session, despacho_id: int) -> Optional[models.DespachosObra]:
        """Obtener despacho por ID"""
        return db.query(models.DespachosObra).filter(models.DespachosObra.id_despacho == despacho_id).first()

    def get_despacho_by_numero(self, db: Session, numero_despacho: str) -> Optional[models.DespachosObra]:
        """Obtener despacho por número"""
        return db.query(models.DespachosObra).filter(models.DespachosObra.numero_despacho == numero_despacho).first()

    def get_despachos(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.DespachosObra]:
        """Obtener lista de despachos con paginación"""
        return db.query(models.DespachosObra).offset(skip).limit(limit).all()

    def get_despachos_by_obra(self, db: Session, id_obra: int, skip: int = 0, limit: int = 100) -> List[models.DespachosObra]:
        """Obtener despachos por obra"""
        return (db.query(models.DespachosObra)
                .filter(models.DespachosObra.id_obra == id_obra)
                .offset(skip)
                .limit(limit)
                .all())

    def get_despachos_by_estado(self, db: Session, estado: str, skip: int = 0, limit: int = 100) -> List[models.DespachosObra]:
        """Obtener despachos por estado"""
        return (db.query(models.DespachosObra)
                .filter(models.DespachosObra.estado == estado)
                .offset(skip)
                .limit(limit)
                .all())

    def get_despachos_pendientes_devolucion(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.DespachosObra]:
        """Obtener despachos pendientes de devolución"""
        return (db.query(models.DespachosObra)
                .filter(
                    models.DespachosObra.requiere_devolucion == True,
                    models.DespachosObra.estado.in_(["ENTREGADO", "DEVOLUCION_PARCIAL"]),
                    models.DespachosObra.fecha_limite_devolucion.isnot(None)
                )
                .offset(skip)
                .limit(limit)
                .all())

    def get_despachos_vencidos(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.DespachosObra]:
        """Obtener despachos vencidos de devolución"""
        return (db.query(models.DespachosObra)
                .filter(
                    models.DespachosObra.requiere_devolucion == True,
                    models.DespachosObra.estado.in_(["ENTREGADO", "DEVOLUCION_PARCIAL"]),
                    models.DespachosObra.fecha_limite_devolucion < date.today()
                )
                .offset(skip)
                .limit(limit)
                .all())

    def search_despachos(self, db: Session, termino: str, skip: int = 0, limit: int = 100) -> List[models.DespachosObra]:
        """Buscar despachos por múltiples campos"""
        return (db.query(models.DespachosObra)
                .filter(
                    or_(
                        models.DespachosObra.numero_despacho.contains(termino),
                        models.DespachosObra.transportista.contains(termino),
                        models.DespachosObra.vehiculo.contains(termino),
                        models.DespachosObra.chofer.contains(termino),
                        models.DespachosObra.recibido_por.contains(termino),
                        models.DespachosObra.motivo_despacho.contains(termino)
                    )
                )
                .offset(skip)
                .limit(limit)
                .all())

    def create_despacho(self, db: Session, despacho: schemas.DespachosObraCreate) -> models.DespachosObra:
        """Crear nuevo despacho"""
        db_despacho = models.DespachosObra(**despacho.dict())
        db.add(db_despacho)
        db.commit()
        db.refresh(db_despacho)
        return db_despacho

    def update_despacho(self, db: Session, despacho_id: int, despacho_update: schemas.DespachosObraUpdate) -> Optional[models.DespachosObra]:
        """Actualizar despacho"""
        db_despacho = self.get_despacho(db, despacho_id)
        if not db_despacho:
            return None

        update_data = despacho_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_despacho, field, value)

        db.commit()
        db.refresh(db_despacho)
        return db_despacho

    def delete_despacho(self, db: Session, despacho_id: int) -> bool:
        """Eliminar despacho"""
        db_despacho = self.get_despacho(db, despacho_id)
        if not db_despacho:
            return False

        db.delete(db_despacho)
        db.commit()
        return True

    def cambiar_estado_despacho(self, db: Session, despacho_id: int, nuevo_estado: str, observaciones: str = None) -> Optional[models.DespachosObra]:
        """Cambiar estado del despacho"""
        db_despacho = self.get_despacho(db, despacho_id)
        if not db_despacho:
            return None

        db_despacho.estado = nuevo_estado
        if observaciones:
            if db_despacho.observaciones:
                db_despacho.observaciones += f"\n{observaciones}"
            else:
                db_despacho.observaciones = observaciones

        db.commit()
        db.refresh(db_despacho)
        return db_despacho

    def get_estadisticas_despachos(self, db: Session) -> dict:
        """Obtener estadísticas de despachos"""
        from sqlalchemy import func
        stats = {}

        # Total de despachos
        stats["total_despachos"] = db.query(models.DespachosObra).count()

        # Por estado
        estados = db.query(models.DespachosObra.estado, func.count(models.DespachosObra.id_despacho)).group_by(models.DespachosObra.estado).all()
        stats["por_estado"] = {estado: count for estado, count in estados}

        # Despachos pendientes de devolución
        stats["pendientes_devolucion"] = db.query(models.DespachosObra).filter(
            models.DespachosObra.requiere_devolucion == True,
            models.DespachosObra.estado.in_(["ENTREGADO", "DEVOLUCION_PARCIAL"])
        ).count()

        # Despachos vencidos
        stats["vencidos"] = db.query(models.DespachosObra).filter(
            models.DespachosObra.requiere_devolucion == True,
            models.DespachosObra.fecha_limite_devolucion < date.today()
        ).count()

        # Por obra (top 10)
        obras = (db.query(models.Obra.nombre_obra, func.count(models.DespachosObra.id_despacho))
                .join(models.DespachosObra)
                .group_by(models.Obra.nombre_obra)
                .order_by(func.count(models.DespachosObra.id_despacho).desc())
                .limit(10)
                .all())
        stats["por_obra"] = {obra: count for obra, count in obras}

        return stats

despachos_obra_crud = DespachosObraCRUD()


# ========================================
# CRUD PARA DETALLE DE DESPACHOS DE OBRA
# ========================================

class DespachosObraDetalleCRUD:

    def get_detalle(self, db: Session, detalle_id: int) -> Optional[models.DespachosObraDetalle]:
        """Obtener detalle de despacho por ID"""
        return db.query(models.DespachosObraDetalle).filter(models.DespachosObraDetalle.id_despacho_detalle == detalle_id).first()

    def get_detalles(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.DespachosObraDetalle]:
        """Obtener lista de detalles de despacho con paginación"""
        return db.query(models.DespachosObraDetalle).offset(skip).limit(limit).all()

    def get_detalles_by_despacho(self, db: Session, id_despacho: int, skip: int = 0, limit: int = 100) -> List[models.DespachosObraDetalle]:
        """Obtener detalles por despacho"""
        return (db.query(models.DespachosObraDetalle)
                .filter(models.DespachosObraDetalle.id_despacho == id_despacho)
                .offset(skip)
                .limit(limit)
                .all())

    def get_detalles_by_producto(self, db: Session, id_producto: int, skip: int = 0, limit: int = 100) -> List[models.DespachosObraDetalle]:
        """Obtener detalles por producto"""
        return (db.query(models.DespachosObraDetalle)
                .filter(models.DespachosObraDetalle.id_producto == id_producto)
                .offset(skip)
                .limit(limit)
                .all())

    def get_herramientas_despachadas(self, db: Session, id_obra: int = None, skip: int = 0, limit: int = 100) -> List[models.DespachosObraDetalle]:
        """Obtener herramientas despachadas"""
        query = (db.query(models.DespachosObraDetalle)
                .filter(models.DespachosObraDetalle.es_herramienta == True))

        if id_obra:
            query = query.join(models.DespachosObra).filter(models.DespachosObra.id_obra == id_obra)

        return query.offset(skip).limit(limit).all()

    def get_herramientas_pendientes_devolucion(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.DespachosObraDetalle]:
        """Obtener herramientas pendientes de devolución"""
        return (db.query(models.DespachosObraDetalle)
                .filter(
                    models.DespachosObraDetalle.es_herramienta == True,
                    models.DespachosObraDetalle.requiere_devolucion_obligatoria == True,
                    models.DespachosObraDetalle.cantidad_devuelta < models.DespachosObraDetalle.cantidad_despachada
                )
                .offset(skip)
                .limit(limit)
                .all())

    def get_productos_perdidos(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.DespachosObraDetalle]:
        """Obtener productos con pérdidas reportadas"""
        return (db.query(models.DespachosObraDetalle)
                .filter(models.DespachosObraDetalle.cantidad_perdida > 0)
                .offset(skip)
                .limit(limit)
                .all())

    def create_detalle(self, db: Session, detalle: schemas.DespachosObraDetalleCreate) -> models.DespachosObraDetalle:
        """Crear nuevo detalle de despacho"""
        db_detalle = models.DespachosObraDetalle(**detalle.dict())
        db.add(db_detalle)
        db.commit()
        db.refresh(db_detalle)
        return db_detalle

    def update_detalle(self, db: Session, detalle_id: int, detalle_update: schemas.DespachosObraDetalleUpdate) -> Optional[models.DespachosObraDetalle]:
        """Actualizar detalle de despacho"""
        db_detalle = self.get_detalle(db, detalle_id)
        if not db_detalle:
            return None

        update_data = detalle_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_detalle, field, value)

        db.commit()
        db.refresh(db_detalle)
        return db_detalle

    def delete_detalle(self, db: Session, detalle_id: int) -> bool:
        """Eliminar detalle de despacho"""
        db_detalle = self.get_detalle(db, detalle_id)
        if not db_detalle:
            return False

        db.delete(db_detalle)
        db.commit()
        return True

    def actualizar_cantidades_utilizadas(self, db: Session, detalle_id: int, cantidad_utilizada: int, cantidad_devuelta: int = 0, cantidad_perdida: int = 0) -> Optional[models.DespachosObraDetalle]:
        """Actualizar cantidades utilizadas, devueltas y perdidas"""
        db_detalle = self.get_detalle(db, detalle_id)
        if not db_detalle:
            return None

        # Validar que las cantidades no excedan lo despachado
        total = cantidad_utilizada + cantidad_devuelta + cantidad_perdida
        if total > db_detalle.cantidad_despachada:
            return None

        db_detalle.cantidad_utilizada = cantidad_utilizada
        db_detalle.cantidad_devuelta = cantidad_devuelta
        db_detalle.cantidad_perdida = cantidad_perdida

        db.commit()
        db.refresh(db_detalle)
        return db_detalle

    def get_resumen_por_despacho(self, db: Session, id_despacho: int) -> dict:
        """Obtener resumen de cantidades por despacho"""
        from sqlalchemy import func

        result = (db.query(
                    func.sum(models.DespachosObraDetalle.cantidad_despachada).label('total_despachado'),
                    func.sum(models.DespachosObraDetalle.cantidad_utilizada).label('total_utilizado'),
                    func.sum(models.DespachosObraDetalle.cantidad_devuelta).label('total_devuelto'),
                    func.sum(models.DespachosObraDetalle.cantidad_perdida).label('total_perdido'),
                    func.sum(models.DespachosObraDetalle.costo_total).label('costo_total')
                )
                .filter(models.DespachosObraDetalle.id_despacho == id_despacho)
                .first())

        return {
            "total_despachado": result.total_despachado or 0,
            "total_utilizado": result.total_utilizado or 0,
            "total_devuelto": result.total_devuelto or 0,
            "total_perdido": result.total_perdido or 0,
            "total_pendiente": (result.total_despachado or 0) - (result.total_utilizado or 0) - (result.total_devuelto or 0) - (result.total_perdido or 0),
            "costo_total": float(result.costo_total or 0)
        }

    def get_estadisticas_herramientas(self, db: Session) -> dict:
        """Obtener estadísticas de herramientas"""
        from sqlalchemy import func
        stats = {}

        # Total de herramientas despachadas
        stats["total_herramientas_despachadas"] = (db.query(func.count(models.DespachosObraDetalle.id_despacho_detalle))
                                                  .filter(models.DespachosObraDetalle.es_herramienta == True)
                                                  .scalar())

        # Herramientas pendientes de devolución
        stats["herramientas_pendientes_devolucion"] = (db.query(func.count(models.DespachosObraDetalle.id_despacho_detalle))
                                                      .filter(
                                                          models.DespachosObraDetalle.es_herramienta == True,
                                                          models.DespachosObraDetalle.requiere_devolucion_obligatoria == True,
                                                          models.DespachosObraDetalle.cantidad_devuelta < models.DespachosObraDetalle.cantidad_despachada
                                                      )
                                                      .scalar())

        # Total de productos perdidos
        stats["productos_perdidos"] = (db.query(func.sum(models.DespachosObraDetalle.cantidad_perdida))
                                      .scalar() or 0)

        # Costo total de pérdidas
        costo_perdidas = (db.query(func.sum(models.DespachosObraDetalle.cantidad_perdida * models.DespachosObraDetalle.costo_unitario))
                         .filter(models.DespachosObraDetalle.cantidad_perdida > 0)
                         .scalar())
        stats["costo_total_perdidas"] = float(costo_perdidas or 0)

        return stats

despachos_obra_detalle_crud = DespachosObraDetalleCRUD()


# ========================================
# CRUD PARA DEVOLUCIONES DE OBRA
# ========================================

class DevolucionesObraCRUD:

    def get_devolucion(self, db: Session, devolucion_id: int) -> Optional[models.DevolucionesObra]:
        """Obtener devolución por ID"""
        return db.query(models.DevolucionesObra).filter(models.DevolucionesObra.id_devolucion == devolucion_id).first()

    def get_devolucion_by_numero(self, db: Session, numero_devolucion: str) -> Optional[models.DevolucionesObra]:
        """Obtener devolución por número"""
        return db.query(models.DevolucionesObra).filter(models.DevolucionesObra.numero_devolucion == numero_devolucion).first()

    def get_devoluciones(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObra]:
        """Obtener lista de devoluciones con paginación"""
        return db.query(models.DevolucionesObra).offset(skip).limit(limit).all()

    def get_devoluciones_by_obra(self, db: Session, id_obra: int, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObra]:
        """Obtener devoluciones por obra"""
        return (db.query(models.DevolucionesObra)
                .filter(models.DevolucionesObra.id_obra == id_obra)
                .offset(skip)
                .limit(limit)
                .all())

    def get_devoluciones_by_despacho(self, db: Session, id_despacho: int, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObra]:
        """Obtener devoluciones por despacho"""
        return (db.query(models.DevolucionesObra)
                .filter(models.DevolucionesObra.id_despacho == id_despacho)
                .offset(skip)
                .limit(limit)
                .all())

    def get_devoluciones_by_estado(self, db: Session, estado: str, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObra]:
        """Obtener devoluciones por estado"""
        return (db.query(models.DevolucionesObra)
                .filter(models.DevolucionesObra.estado == estado)
                .offset(skip)
                .limit(limit)
                .all())

    def get_devoluciones_by_motivo(self, db: Session, motivo: str, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObra]:
        """Obtener devoluciones por motivo"""
        return (db.query(models.DevolucionesObra)
                .filter(models.DevolucionesObra.motivo_devolucion == motivo)
                .offset(skip)
                .limit(limit)
                .all())

    def get_devoluciones_pendientes_recepcion(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObra]:
        """Obtener devoluciones pendientes de recepción"""
        return (db.query(models.DevolucionesObra)
                .filter(models.DevolucionesObra.estado.in_(["EN_TRANSITO", "RECIBIDA"]))
                .offset(skip)
                .limit(limit)
                .all())

    def search_devoluciones(self, db: Session, termino: str, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObra]:
        """Buscar devoluciones por múltiples campos"""
        return (db.query(models.DevolucionesObra)
                .filter(
                    or_(
                        models.DevolucionesObra.numero_devolucion.contains(termino),
                        models.DevolucionesObra.transportista.contains(termino),
                        models.DevolucionesObra.vehiculo.contains(termino),
                        models.DevolucionesObra.chofer.contains(termino),
                        models.DevolucionesObra.entregado_por.contains(termino),
                        models.DevolucionesObra.observaciones.contains(termino)
                    )
                )
                .offset(skip)
                .limit(limit)
                .all())

    def create_devolucion(self, db: Session, devolucion: schemas.DevolucionesObraCreate) -> models.DevolucionesObra:
        """Crear nueva devolución"""
        db_devolucion = models.DevolucionesObra(**devolucion.dict())
        db.add(db_devolucion)
        db.commit()
        db.refresh(db_devolucion)
        return db_devolucion

    def update_devolucion(self, db: Session, devolucion_id: int, devolucion_update: schemas.DevolucionesObraUpdate) -> Optional[models.DevolucionesObra]:
        """Actualizar devolución"""
        db_devolucion = self.get_devolucion(db, devolucion_id)
        if not db_devolucion:
            return None

        update_data = devolucion_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_devolucion, field, value)

        db.commit()
        db.refresh(db_devolucion)
        return db_devolucion

    def delete_devolucion(self, db: Session, devolucion_id: int) -> bool:
        """Eliminar devolución"""
        db_devolucion = self.get_devolucion(db, devolucion_id)
        if not db_devolucion:
            return False

        db.delete(db_devolucion)
        db.commit()
        return True

    def cambiar_estado_devolucion(self, db: Session, devolucion_id: int, nuevo_estado: str, observaciones: str = None) -> Optional[models.DevolucionesObra]:
        """Cambiar estado de la devolución"""
        db_devolucion = self.get_devolucion(db, devolucion_id)
        if not db_devolucion:
            return None

        db_devolucion.estado = nuevo_estado
        if observaciones:
            if db_devolucion.observaciones:
                db_devolucion.observaciones += f"\n{observaciones}"
            else:
                db_devolucion.observaciones = observaciones

        db.commit()
        db.refresh(db_devolucion)
        return db_devolucion

    def marcar_como_recibida(self, db: Session, devolucion_id: int, fecha_recepcion: date = None, hora_recepcion: time = None) -> Optional[models.DevolucionesObra]:
        """Marcar devolución como recibida"""

        db_devolucion = self.get_devolucion(db, devolucion_id)
        if not db_devolucion:
            return None

        db_devolucion.estado = "RECIBIDA"
        db_devolucion.fecha_recepcion = fecha_recepcion or date.today()
        db_devolucion.hora_recepcion = hora_recepcion or datetime.now().time()

        db.commit()
        db.refresh(db_devolucion)
        return db_devolucion

    def get_estadisticas_devoluciones(self, db: Session) -> dict:
        """Obtener estadísticas de devoluciones"""
        from sqlalchemy import func
        stats = {}

        # Total de devoluciones
        stats["total_devoluciones"] = db.query(models.DevolucionesObra).count()

        # Por estado
        estados = db.query(models.DevolucionesObra.estado, func.count(models.DevolucionesObra.id_devolucion)).group_by(models.DevolucionesObra.estado).all()
        stats["por_estado"] = {estado: count for estado, count in estados}

        # Por motivo
        motivos = db.query(models.DevolucionesObra.motivo_devolucion, func.count(models.DevolucionesObra.id_devolucion)).group_by(models.DevolucionesObra.motivo_devolucion).all()
        stats["por_motivo"] = {motivo: count for motivo, count in motivos}

        # Devoluciones pendientes
        stats["pendientes_recepcion"] = db.query(models.DevolucionesObra).filter(
            models.DevolucionesObra.estado.in_(["EN_TRANSITO", "RECIBIDA"])
        ).count()

        # Por obra (top 10)
        obras = (db.query(models.Obra.nombre_obra, func.count(models.DevolucionesObra.id_devolucion))
                .join(models.DevolucionesObra)
                .group_by(models.Obra.nombre_obra)
                .order_by(func.count(models.DevolucionesObra.id_devolucion).desc())
                .limit(10)
                .all())
        stats["por_obra"] = {obra: count for obra, count in obras}

        return stats

devoluciones_obra_crud = DevolucionesObraCRUD()


# ========================================
# CRUD PARA DETALLE DE DEVOLUCIONES DE OBRA
# ========================================

class DevolucionesObraDetalleCRUD:

    def get_detalle(self, db: Session, detalle_id: int) -> Optional[models.DevolucionesObraDetalle]:
        """Obtener detalle de devolución por ID"""
        return db.query(models.DevolucionesObraDetalle).filter(models.DevolucionesObraDetalle.id_devolucion_detalle == detalle_id).first()

    def get_detalles(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObraDetalle]:
        """Obtener lista de detalles de devolución con paginación"""
        return db.query(models.DevolucionesObraDetalle).offset(skip).limit(limit).all()

    def get_detalles_by_devolucion(self, db: Session, id_devolucion: int, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObraDetalle]:
        """Obtener detalles por devolución"""
        return (db.query(models.DevolucionesObraDetalle)
                .filter(models.DevolucionesObraDetalle.id_devolucion == id_devolucion)
                .offset(skip)
                .limit(limit)
                .all())

    def get_detalles_by_producto(self, db: Session, id_producto: int, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObraDetalle]:
        """Obtener detalles por producto"""
        return (db.query(models.DevolucionesObraDetalle)
                .filter(models.DevolucionesObraDetalle.id_producto == id_producto)
                .offset(skip)
                .limit(limit)
                .all())

    def get_productos_by_estado(self, db: Session, estado_producto: str, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObraDetalle]:
        """Obtener productos devueltos por estado"""
        return (db.query(models.DevolucionesObraDetalle)
                .filter(models.DevolucionesObraDetalle.estado_producto == estado_producto)
                .offset(skip)
                .limit(limit)
                .all())

    def get_productos_requieren_limpieza(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObraDetalle]:
        """Obtener productos que requieren limpieza"""
        return (db.query(models.DevolucionesObraDetalle)
                .filter(models.DevolucionesObraDetalle.requiere_limpieza == True)
                .offset(skip)
                .limit(limit)
                .all())

    def get_productos_requieren_reparacion(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObraDetalle]:
        """Obtener productos que requieren reparación"""
        return (db.query(models.DevolucionesObraDetalle)
                .filter(models.DevolucionesObraDetalle.requiere_reparacion == True)
                .offset(skip)
                .limit(limit)
                .all())

    def get_productos_requieren_calibracion(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObraDetalle]:
        """Obtener productos que requieren calibración"""
        return (db.query(models.DevolucionesObraDetalle)
                .filter(models.DevolucionesObraDetalle.requiere_calibracion == True)
                .offset(skip)
                .limit(limit)
                .all())

    def get_productos_defectuosos(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.DevolucionesObraDetalle]:
        """Obtener productos defectuosos o no reutilizables"""
        return (db.query(models.DevolucionesObraDetalle)
                .filter(models.DevolucionesObraDetalle.estado_producto.in_(["DEFECTUOSO", "NO_REUTILIZABLE"]))
                .offset(skip)
                .limit(limit)
                .all())

    def create_detalle(self, db: Session, detalle: schemas.DevolucionesObraDetalleCreate) -> models.DevolucionesObraDetalle:
        """Crear nuevo detalle de devolución"""
        db_detalle = models.DevolucionesObraDetalle(**detalle.dict())
        db.add(db_detalle)
        db.commit()
        db.refresh(db_detalle)
        return db_detalle

    def update_detalle(self, db: Session, detalle_id: int, detalle_update: schemas.DevolucionesObraDetalleUpdate) -> Optional[models.DevolucionesObraDetalle]:
        """Actualizar detalle de devolución"""
        db_detalle = self.get_detalle(db, detalle_id)
        if not db_detalle:
            return None

        update_data = detalle_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_detalle, field, value)

        db.commit()
        db.refresh(db_detalle)
        return db_detalle

    def delete_detalle(self, db: Session, detalle_id: int) -> bool:
        """Eliminar detalle de devolución"""
        db_detalle = self.get_detalle(db, detalle_id)
        if not db_detalle:
            return False

        db.delete(db_detalle)
        db.commit()
        return True

    def procesar_producto_devuelto(self, db: Session, detalle_id: int, nueva_ubicacion: int = None) -> Optional[models.DevolucionesObraDetalle]:
        """Procesar producto devuelto y asignar ubicación"""
        db_detalle = self.get_detalle(db, detalle_id)
        if not db_detalle:
            return None

        if nueva_ubicacion:
            db_detalle.id_ubicacion_recepcion = nueva_ubicacion

        db.commit()
        db.refresh(db_detalle)
        return db_detalle

    def get_resumen_por_devolucion(self, db: Session, id_devolucion: int) -> dict:
        """Obtener resumen de productos por devolución"""
        from sqlalchemy import func

        result = (db.query(
                    func.sum(models.DevolucionesObraDetalle.cantidad_devuelta).label('total_devuelto'),
                    func.count(models.DevolucionesObraDetalle.id_devolucion_detalle).label('productos_diferentes')
                )
                .filter(models.DevolucionesObraDetalle.id_devolucion == id_devolucion)
                .first())

        # Por estado del producto
        estados = (db.query(models.DevolucionesObraDetalle.estado_producto,
                           func.sum(models.DevolucionesObraDetalle.cantidad_devuelta))
                  .filter(models.DevolucionesObraDetalle.id_devolucion == id_devolucion)
                  .group_by(models.DevolucionesObraDetalle.estado_producto)
                  .all())

        return {
            "total_devuelto": result.total_devuelto or 0,
            "productos_diferentes": result.productos_diferentes or 0,
            "por_estado": {estado: int(cantidad) for estado, cantidad in estados},
            "requieren_limpieza": (db.query(func.sum(models.DevolucionesObraDetalle.cantidad_devuelta))
                                  .filter(
                                      models.DevolucionesObraDetalle.id_devolucion == id_devolucion,
                                      models.DevolucionesObraDetalle.requiere_limpieza == True
                                  ).scalar() or 0),
            "requieren_reparacion": (db.query(func.sum(models.DevolucionesObraDetalle.cantidad_devuelta))
                                    .filter(
                                        models.DevolucionesObraDetalle.id_devolucion == id_devolucion,
                                        models.DevolucionesObraDetalle.requiere_reparacion == True
                                    ).scalar() or 0),
            "requieren_calibracion": (db.query(func.sum(models.DevolucionesObraDetalle.cantidad_devuelta))
                                     .filter(
                                         models.DevolucionesObraDetalle.id_devolucion == id_devolucion,
                                         models.DevolucionesObraDetalle.requiere_calibracion == True
                                     ).scalar() or 0)
        }

    def get_estadisticas_productos_devueltos(self, db: Session) -> dict:
        """Obtener estadísticas de productos devueltos"""
        from sqlalchemy import func
        stats = {}

        # Total de productos devueltos
        stats["total_productos_devueltos"] = (db.query(func.sum(models.DevolucionesObraDetalle.cantidad_devuelta))
                                             .scalar() or 0)

        # Por estado
        estados = (db.query(models.DevolucionesObraDetalle.estado_producto,
                           func.sum(models.DevolucionesObraDetalle.cantidad_devuelta))
                  .group_by(models.DevolucionesObraDetalle.estado_producto)
                  .all())
        stats["por_estado"] = {estado: int(cantidad) for estado, cantidad in estados}

        # Productos que requieren mantenimiento
        stats["requieren_limpieza"] = (db.query(func.sum(models.DevolucionesObraDetalle.cantidad_devuelta))
                                      .filter(models.DevolucionesObraDetalle.requiere_limpieza == True)
                                      .scalar() or 0)

        stats["requieren_reparacion"] = (db.query(func.sum(models.DevolucionesObraDetalle.cantidad_devuelta))
                                        .filter(models.DevolucionesObraDetalle.requiere_reparacion == True)
                                        .scalar() or 0)

        stats["requieren_calibracion"] = (db.query(func.sum(models.DevolucionesObraDetalle.cantidad_devuelta))
                                         .filter(models.DevolucionesObraDetalle.requiere_calibracion == True)
                                         .scalar() or 0)

        # Productos no reutilizables
        stats["no_reutilizables"] = (db.query(func.sum(models.DevolucionesObraDetalle.cantidad_devuelta))
                                     .filter(models.DevolucionesObraDetalle.estado_producto.in_(["DEFECTUOSO", "NO_REUTILIZABLE"]))
                                     .scalar() or 0)

        return stats

devoluciones_obra_detalle_crud = DevolucionesObraDetalleCRUD()


# ========================================
# CRUD PARA INVENTARIO DE OBRA
# ========================================

class InventarioObraCRUD:

    def get_inventario(self, db: Session, inventario_id: int) -> Optional[models.InventarioObra]:
        """Obtener inventario por ID"""
        return db.query(models.InventarioObra).filter(models.InventarioObra.id_inventario_obra == inventario_id).first()

    def get_inventario_by_obra_producto(self, db: Session, id_obra: int, id_producto: int) -> Optional[models.InventarioObra]:
        """Obtener inventario por obra y producto"""
        return db.query(models.InventarioObra).filter(
            models.InventarioObra.id_obra == id_obra,
            models.InventarioObra.id_producto == id_producto
        ).first()

    def get_inventarios(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.InventarioObra]:
        """Obtener lista de inventarios con paginación"""
        return db.query(models.InventarioObra).offset(skip).limit(limit).all()

    def get_inventarios_by_obra(self, db: Session, id_obra: int, skip: int = 0, limit: int = 100) -> List[models.InventarioObra]:
        """Obtener inventarios por obra"""
        return (db.query(models.InventarioObra)
                .filter(models.InventarioObra.id_obra == id_obra)
                .offset(skip)
                .limit(limit)
                .all())

    def get_inventarios_by_producto(self, db: Session, id_producto: int, skip: int = 0, limit: int = 100) -> List[models.InventarioObra]:
        """Obtener inventarios por producto"""
        return (db.query(models.InventarioObra)
                .filter(models.InventarioObra.id_producto == id_producto)
                .offset(skip)
                .limit(limit)
                .all())

    def get_herramientas_by_obra(self, db: Session, id_obra: int, skip: int = 0, limit: int = 100) -> List[models.InventarioObra]:
        """Obtener herramientas por obra"""
        return (db.query(models.InventarioObra)
                .filter(
                    models.InventarioObra.id_obra == id_obra,
                    models.InventarioObra.es_herramienta == True
                )
                .offset(skip)
                .limit(limit)
                .all())

    def get_productos_con_stock(self, db: Session, id_obra: int, skip: int = 0, limit: int = 100) -> List[models.InventarioObra]:
        """Obtener productos con stock disponible en obra"""
        return (db.query(models.InventarioObra)
                .filter(
                    models.InventarioObra.id_obra == id_obra,
                    models.InventarioObra.cantidad_actual > 0
                )
                .offset(skip)
                .limit(limit)
                .all())

    def get_productos_sin_stock(self, db: Session, id_obra: int, skip: int = 0, limit: int = 100) -> List[models.InventarioObra]:
        """Obtener productos sin stock en obra"""
        return (db.query(models.InventarioObra)
                .filter(
                    models.InventarioObra.id_obra == id_obra,
                    models.InventarioObra.cantidad_actual == 0
                )
                .offset(skip)
                .limit(limit)
                .all())

    def create_inventario(self, db: Session, inventario: schemas.InventarioObraCreate) -> models.InventarioObra:
        """Crear nuevo inventario de obra"""
        db_inventario = models.InventarioObra(**inventario.dict())
        db.add(db_inventario)
        db.commit()
        db.refresh(db_inventario)
        return db_inventario

    def update_inventario(self, db: Session, inventario_id: int, inventario_update: schemas.InventarioObraUpdate) -> Optional[models.InventarioObra]:
        """Actualizar inventario de obra"""
        db_inventario = self.get_inventario(db, inventario_id)
        if not db_inventario:
            return None

        update_data = inventario_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_inventario, field, value)

        db.commit()
        db.refresh(db_inventario)
        return db_inventario

    def delete_inventario(self, db: Session, inventario_id: int) -> bool:
        """Eliminar inventario de obra"""
        db_inventario = self.get_inventario(db, inventario_id)
        if not db_inventario:
            return False

        db.delete(db_inventario)
        db.commit()
        return True

    def actualizar_stock(self, db: Session, id_obra: int, id_producto: int, cantidad_cambio: int, motivo: str = None) -> Optional[models.InventarioObra]:
        """Actualizar stock de un producto en obra"""
        from datetime import datetime

        db_inventario = self.get_inventario_by_obra_producto(db, id_obra, id_producto)
        if not db_inventario:
            # Crear nuevo registro si no existe
            db_inventario = models.InventarioObra(
                id_obra=id_obra,
                id_producto=id_producto,
                cantidad_actual=max(0, cantidad_cambio),
                fecha_ultimo_movimiento=datetime.now()
            )
            if motivo:
                db_inventario.observaciones = f"Creado: {motivo}"
            db.add(db_inventario)
        else:
            # Actualizar existente
            nueva_cantidad = db_inventario.cantidad_actual + cantidad_cambio
            db_inventario.cantidad_actual = max(0, nueva_cantidad)
            db_inventario.fecha_ultimo_movimiento = datetime.now()

            if motivo:
                if db_inventario.observaciones:
                    db_inventario.observaciones += f"\n{datetime.now().strftime('%Y-%m-%d %H:%M')}: {motivo}"
                else:
                    db_inventario.observaciones = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: {motivo}"

        db.commit()
        db.refresh(db_inventario)
        return db_inventario

    def asignar_herramienta(self, db: Session, inventario_id: int, responsable: str, ubicacion: str = None) -> Optional[models.InventarioObra]:
        """Asignar herramienta a responsable"""
        db_inventario = self.get_inventario(db, inventario_id)
        if not db_inventario or not db_inventario.es_herramienta:
            return None

        db_inventario.responsable_herramienta = responsable
        if ubicacion:
            db_inventario.ubicacion_especifica = ubicacion

        db.commit()
        db.refresh(db_inventario)
        return db_inventario

    def get_resumen_por_obra(self, db: Session, id_obra: int) -> dict:
        """Obtener resumen de inventario por obra"""
        from sqlalchemy import func

        result = (db.query(
                    func.count(models.InventarioObra.id_inventario_obra).label('total_productos'),
                    func.sum(models.InventarioObra.cantidad_actual).label('total_cantidad'),
                    func.sum(models.InventarioObra.cantidad_utilizada_acumulada).label('total_utilizado'),
                    func.sum(models.InventarioObra.cantidad_devuelta_acumulada).label('total_devuelto')
                )
                .filter(models.InventarioObra.id_obra == id_obra)
                .first())

        # Valor total del inventario
        valor_total = (db.query(func.sum(models.InventarioObra.cantidad_actual * models.InventarioObra.costo_promedio))
                      .filter(
                          models.InventarioObra.id_obra == id_obra,
                          models.InventarioObra.costo_promedio.isnot(None)
                      )
                      .scalar() or 0)

        # Productos con stock
        con_stock = (db.query(func.count(models.InventarioObra.id_inventario_obra))
                    .filter(
                        models.InventarioObra.id_obra == id_obra,
                        models.InventarioObra.cantidad_actual > 0
                    )
                    .scalar())

        # Herramientas
        herramientas = (db.query(func.count(models.InventarioObra.id_inventario_obra))
                       .filter(
                           models.InventarioObra.id_obra == id_obra,
                           models.InventarioObra.es_herramienta == True
                       )
                       .scalar())

        return {
            "total_productos": result.total_productos or 0,
            "total_cantidad": result.total_cantidad or 0,
            "total_utilizado": result.total_utilizado or 0,
            "total_devuelto": result.total_devuelto or 0,
            "valor_total_inventario": float(valor_total),
            "productos_con_stock": con_stock or 0,
            "productos_sin_stock": (result.total_productos or 0) - (con_stock or 0),
            "total_herramientas": herramientas or 0
        }

    def get_estadisticas_generales(self, db: Session) -> dict:
        """Obtener estadísticas generales de inventarios de obra"""
        from sqlalchemy import func
        stats = {}

        # Totales generales
        result = (db.query(
                    func.count(models.InventarioObra.id_inventario_obra).label('total_registros'),
                    func.sum(models.InventarioObra.cantidad_actual).label('total_cantidad'),
                    func.count(func.distinct(models.InventarioObra.id_obra)).label('obras_con_inventario'),
                    func.count(func.distinct(models.InventarioObra.id_producto)).label('productos_diferentes')
                )
                .first())

        stats["total_registros"] = result.total_registros or 0
        stats["total_cantidad"] = result.total_cantidad or 0
        stats["obras_con_inventario"] = result.obras_con_inventario or 0
        stats["productos_diferentes"] = result.productos_diferentes or 0

        # Valor total
        valor_total = (db.query(func.sum(models.InventarioObra.cantidad_actual * models.InventarioObra.costo_promedio))
                      .filter(models.InventarioObra.costo_promedio.isnot(None))
                      .scalar() or 0)
        stats["valor_total_inventarios"] = float(valor_total)

        # Herramientas
        stats["total_herramientas"] = (db.query(func.count(models.InventarioObra.id_inventario_obra))
                                      .filter(models.InventarioObra.es_herramienta == True)
                                      .scalar() or 0)

        return stats

inventario_obra_crud = InventarioObraCRUD()


# ========================================
# CRUD PARA RESERVAS
# ========================================

class ReservasCRUD:

    def get_reserva(self, db: Session, reserva_id: int) -> Optional[models.Reservas]:
        """Obtener reserva por ID"""
        return db.query(models.Reservas).filter(models.Reservas.id_reserva == reserva_id).first()

    def get_reserva_by_numero(self, db: Session, numero_reserva: str) -> Optional[models.Reservas]:
        """Obtener reserva por número"""
        return db.query(models.Reservas).filter(models.Reservas.numero_reserva == numero_reserva).first()

    def get_reservas(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Reservas]:
        """Obtener lista de reservas con paginación"""
        return db.query(models.Reservas).offset(skip).limit(limit).all()

    def get_reservas_by_estado(self, db: Session, estado: str, skip: int = 0, limit: int = 100) -> List[models.Reservas]:
        """Obtener reservas por estado"""
        return (db.query(models.Reservas)
                .filter(models.Reservas.estado == estado)
                .offset(skip)
                .limit(limit)
                .all())

    def get_reservas_by_producto(self, db: Session, id_producto: int, skip: int = 0, limit: int = 100) -> List[models.Reservas]:
        """Obtener reservas por producto"""
        return (db.query(models.Reservas)
                .filter(models.Reservas.id_producto == id_producto)
                .offset(skip)
                .limit(limit)
                .all())

    def get_reservas_by_cliente(self, db: Session, id_cliente: int, skip: int = 0, limit: int = 100) -> List[models.Reservas]:
        """Obtener reservas por cliente"""
        return (db.query(models.Reservas)
                .filter(models.Reservas.id_cliente == id_cliente)
                .offset(skip)
                .limit(limit)
                .all())

    def get_reservas_by_obra(self, db: Session, id_obra: int, skip: int = 0, limit: int = 100) -> List[models.Reservas]:
        """Obtener reservas por obra"""
        return (db.query(models.Reservas)
                .filter(models.Reservas.id_obra == id_obra)
                .offset(skip)
                .limit(limit)
                .all())

    def get_reservas_activas(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Reservas]:
        """Obtener reservas activas"""
        return (db.query(models.Reservas)
                .filter(models.Reservas.estado == "ACTIVA")
                .offset(skip)
                .limit(limit)
                .all())

    def get_reservas_vencidas(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Reservas]:
        """Obtener reservas vencidas"""
        from datetime import datetime
        return (db.query(models.Reservas)
                .filter(
                    models.Reservas.estado == "ACTIVA",
                    models.Reservas.fecha_vencimiento_reserva < datetime.now()
                )
                .offset(skip)
                .limit(limit)
                .all())

    def get_reservas_proximas_vencer(self, db: Session, dias: int = 7, skip: int = 0, limit: int = 100) -> List[models.Reservas]:
        """Obtener reservas próximas a vencer"""
        from datetime import datetime, timedelta
        fecha_limite = datetime.now() + timedelta(days=dias)
        return (db.query(models.Reservas)
                .filter(
                    models.Reservas.estado == "ACTIVA",
                    models.Reservas.fecha_vencimiento_reserva <= fecha_limite,
                    models.Reservas.fecha_vencimiento_reserva >= datetime.now()
                )
                .offset(skip)
                .limit(limit)
                .all())

    def search_reservas(self, db: Session, termino: str, skip: int = 0, limit: int = 100) -> List[models.Reservas]:
        """Buscar reservas por múltiples campos"""
        return (db.query(models.Reservas)
                .filter(
                    or_(
                        models.Reservas.numero_reserva.contains(termino),
                        models.Reservas.cliente_externo.contains(termino),
                        models.Reservas.proyecto_externo.contains(termino),
                        models.Reservas.motivo_reserva.contains(termino),
                        models.Reservas.observaciones.contains(termino)
                    )
                )
                .offset(skip)
                .limit(limit)
                .all())

    def create_reserva(self, db: Session, reserva: schemas.ReservasCreate) -> models.Reservas:
        """Crear nueva reserva"""
        db_reserva = models.Reservas(**reserva.dict())
        db.add(db_reserva)
        db.commit()
        db.refresh(db_reserva)
        return db_reserva

    def update_reserva(self, db: Session, reserva_id: int, reserva_update: schemas.ReservasUpdate) -> Optional[models.Reservas]:
        """Actualizar reserva"""
        db_reserva = self.get_reserva(db, reserva_id)
        if not db_reserva:
            return None

        update_data = reserva_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reserva, field, value)

        db.commit()
        db.refresh(db_reserva)
        return db_reserva

    def delete_reserva(self, db: Session, reserva_id: int) -> bool:
        """Eliminar reserva"""
        db_reserva = self.get_reserva(db, reserva_id)
        if not db_reserva:
            return False

        db.delete(db_reserva)
        db.commit()
        return True

    def cambiar_estado_reserva(self, db: Session, reserva_id: int, nuevo_estado: str, observaciones: str = None) -> Optional[models.Reservas]:
        """Cambiar estado de la reserva"""
        db_reserva = self.get_reserva(db, reserva_id)
        if not db_reserva:
            return None

        db_reserva.estado = nuevo_estado
        if observaciones:
            if db_reserva.observaciones:
                db_reserva.observaciones += f"\n{observaciones}"
            else:
                db_reserva.observaciones = observaciones

        db.commit()
        db.refresh(db_reserva)
        return db_reserva

    def utilizar_reserva(self, db: Session, reserva_id: int, observaciones: str = None) -> Optional[models.Reservas]:
        """Marcar reserva como utilizada"""
        return self.cambiar_estado_reserva(db, reserva_id, "UTILIZADA", observaciones)

    def cancelar_reserva(self, db: Session, reserva_id: int, motivo: str = None) -> Optional[models.Reservas]:
        """Cancelar reserva"""
        observaciones = f"Cancelada: {motivo}" if motivo else "Cancelada"
        return self.cambiar_estado_reserva(db, reserva_id, "CANCELADA", observaciones)

    def marcar_vencidas(self, db: Session) -> int:
        """Marcar reservas vencidas automáticamente"""
        from datetime import datetime
        count = (db.query(models.Reservas)
                .filter(
                    models.Reservas.estado == "ACTIVA",
                    models.Reservas.fecha_vencimiento_reserva < datetime.now()
                )
                .update({models.Reservas.estado: "VENCIDA"}))
        db.commit()
        return count

    def get_cantidad_reservada_producto(self, db: Session, id_producto: int, id_ubicacion: int = None) -> int:
        """Obtener cantidad total reservada de un producto"""
        from sqlalchemy import func
        query = (db.query(func.sum(models.Reservas.cantidad_reservada))
                .filter(
                    models.Reservas.id_producto == id_producto,
                    models.Reservas.estado == "ACTIVA"
                ))

        if id_ubicacion:
            query = query.filter(models.Reservas.id_ubicacion == id_ubicacion)

        return query.scalar() or 0

    def get_estadisticas_reservas(self, db: Session) -> dict:
        """Obtener estadísticas de reservas"""
        from sqlalchemy import func
        from datetime import datetime
        stats = {}

        # Total de reservas
        stats["total_reservas"] = db.query(models.Reservas).count()

        # Por estado
        estados = db.query(models.Reservas.estado, func.count(models.Reservas.id_reserva)).group_by(models.Reservas.estado).all()
        stats["por_estado"] = {estado: count for estado, count in estados}

        # Reservas activas
        stats["activas"] = db.query(models.Reservas).filter(models.Reservas.estado == "ACTIVA").count()

        # Reservas vencidas (por actualizar)
        vencidas_no_marcadas = (db.query(models.Reservas)
                               .filter(
                                   models.Reservas.estado == "ACTIVA",
                                   models.Reservas.fecha_vencimiento_reserva < datetime.now()
                               ).count())
        stats["vencidas_no_marcadas"] = vencidas_no_marcadas

        # Reservas próximas a vencer (7 días)
        from datetime import timedelta
        fecha_limite = datetime.now() + timedelta(days=7)
        proximas_vencer = (db.query(models.Reservas)
                          .filter(
                              models.Reservas.estado == "ACTIVA",
                              models.Reservas.fecha_vencimiento_reserva <= fecha_limite,
                              models.Reservas.fecha_vencimiento_reserva >= datetime.now()
                          ).count())
        stats["proximas_vencer"] = proximas_vencer

        # Por tipo de cliente (registrado vs externo)
        con_cliente = db.query(models.Reservas).filter(models.Reservas.id_cliente.isnot(None)).count()
        externos = db.query(models.Reservas).filter(models.Reservas.cliente_externo.isnot(None)).count()
        stats["con_cliente_registrado"] = con_cliente
        stats["clientes_externos"] = externos

        return stats

reservas_crud = ReservasCRUD()

class ProgramacionConteosCRUD:
    """CRUD operations for ProgramacionConteos"""

    def get_programacion(self, db: Session, programacion_id: int) -> Optional[models.ProgramacionConteos]:
        """Obtener programación por ID"""
        return db.query(models.ProgramacionConteos).filter(models.ProgramacionConteos.id_programacion == programacion_id).first()

    def get_programaciones(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.ProgramacionConteos]:
        """Obtener todas las programaciones"""
        return db.query(models.ProgramacionConteos).offset(skip).limit(limit).all()

    def create_programacion(self, db: Session, programacion: schemas.ProgramacionConteosCreate) -> models.ProgramacionConteos:
        """Crear nueva programación de conteo"""
        db_programacion = models.ProgramacionConteos(**programacion.model_dump())
        db.add(db_programacion)
        db.commit()
        db.refresh(db_programacion)
        return db_programacion

    def update_programacion(self, db: Session, programacion_id: int, programacion: schemas.ProgramacionConteosUpdate) -> Optional[models.ProgramacionConteos]:
        """Actualizar programación existente"""
        db_programacion = self.get_programacion(db, programacion_id)
        if not db_programacion:
            return None

        update_data = programacion.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_programacion, field, value)

        db.commit()
        db.refresh(db_programacion)
        return db_programacion

    def delete_programacion(self, db: Session, programacion_id: int) -> bool:
        """Eliminar programación"""
        db_programacion = self.get_programacion(db, programacion_id)
        if not db_programacion:
            return False

        db.delete(db_programacion)
        db.commit()
        return True

    def get_programaciones_by_estado(self, db: Session, estado: str, skip: int = 0, limit: int = 100) -> List[models.ProgramacionConteos]:
        """Obtener programaciones por estado"""
        return (db.query(models.ProgramacionConteos)
                .filter(models.ProgramacionConteos.estado == estado)
                .offset(skip)
                .limit(limit)
                .all())

    def get_programaciones_by_tipo(self, db: Session, tipo: str, skip: int = 0, limit: int = 100) -> List[models.ProgramacionConteos]:
        """Obtener programaciones por tipo"""
        return (db.query(models.ProgramacionConteos)
                .filter(models.ProgramacionConteos.tipo_conteo == tipo)
                .offset(skip)
                .limit(limit)
                .all())

    def get_programaciones_by_bodega(self, db: Session, bodega_id: int, skip: int = 0, limit: int = 100) -> List[models.ProgramacionConteos]:
        """Obtener programaciones por bodega"""
        return (db.query(models.ProgramacionConteos)
                .filter(models.ProgramacionConteos.id_bodega == bodega_id)
                .offset(skip)
                .limit(limit)
                .all())

    def get_programaciones_by_categoria(self, db: Session, categoria_id: int, skip: int = 0, limit: int = 100) -> List[models.ProgramacionConteos]:
        """Obtener programaciones por categoría"""
        return (db.query(models.ProgramacionConteos)
                .filter(models.ProgramacionConteos.id_categoria == categoria_id)
                .offset(skip)
                .limit(limit)
                .all())

    def get_programaciones_by_obra(self, db: Session, obra_id: int, skip: int = 0, limit: int = 100) -> List[models.ProgramacionConteos]:
        """Obtener programaciones por obra"""
        return (db.query(models.ProgramacionConteos)
                .filter(models.ProgramacionConteos.id_obra == obra_id)
                .offset(skip)
                .limit(limit)
                .all())

    def get_programaciones_by_responsable(self, db: Session, usuario_id: int, skip: int = 0, limit: int = 100) -> List[models.ProgramacionConteos]:
        """Obtener programaciones por responsable"""
        return (db.query(models.ProgramacionConteos)
                .filter(models.ProgramacionConteos.id_usuario_responsable == usuario_id)
                .offset(skip)
                .limit(limit)
                .all())

    def get_programaciones_by_fecha_range(self, db: Session, fecha_inicio: date, fecha_fin: date, skip: int = 0, limit: int = 100) -> List[models.ProgramacionConteos]:
        """Obtener programaciones por rango de fechas"""
        return (db.query(models.ProgramacionConteos)
                .filter(
                    models.ProgramacionConteos.fecha_programada >= fecha_inicio,
                    models.ProgramacionConteos.fecha_programada <= fecha_fin
                )
                .offset(skip)
                .limit(limit)
                .all())

    def iniciar_conteo(self, db: Session, programacion_id: int, fecha_inicio: date = None) -> Optional[models.ProgramacionConteos]:
        """Iniciar un conteo programado"""
        db_programacion = self.get_programacion(db, programacion_id)
        if not db_programacion or db_programacion.estado != "PROGRAMADO":
            return None

        if fecha_inicio is None:
            from datetime import date
            fecha_inicio = date.today()

        db_programacion.estado = "EN_PROCESO"
        db_programacion.fecha_inicio = fecha_inicio

        db.commit()
        db.refresh(db_programacion)
        return db_programacion

    def completar_conteo(self, db: Session, programacion_id: int, fecha_fin: date = None, observaciones: str = None) -> Optional[models.ProgramacionConteos]:
        """Completar un conteo en proceso"""
        db_programacion = self.get_programacion(db, programacion_id)
        if not db_programacion or db_programacion.estado != "EN_PROCESO":
            return None

        if fecha_fin is None:
            from datetime import date
            fecha_fin = date.today()

        db_programacion.estado = "COMPLETADO"
        db_programacion.fecha_fin = fecha_fin
        if observaciones:
            db_programacion.observaciones = observaciones

        db.commit()
        db.refresh(db_programacion)
        return db_programacion

    def cancelar_conteo(self, db: Session, programacion_id: int, motivo: str = None) -> Optional[models.ProgramacionConteos]:
        """Cancelar un conteo"""
        db_programacion = self.get_programacion(db, programacion_id)
        if not db_programacion or db_programacion.estado in ["COMPLETADO", "CANCELADO"]:
            return None

        db_programacion.estado = "CANCELADO"
        if motivo:
            observaciones_actuales = db_programacion.observaciones or ""
            db_programacion.observaciones = f"{observaciones_actuales}\nCancelado: {motivo}".strip()

        db.commit()
        db.refresh(db_programacion)
        return db_programacion

    def get_estadisticas_generales(self, db: Session) -> dict:
        """Obtener estadísticas generales de programaciones"""
        from sqlalchemy import func

        total = db.query(func.count(models.ProgramacionConteos.id_programacion)).scalar()
        programados = db.query(func.count(models.ProgramacionConteos.id_programacion)).filter(models.ProgramacionConteos.estado == "PROGRAMADO").scalar()
        en_proceso = db.query(func.count(models.ProgramacionConteos.id_programacion)).filter(models.ProgramacionConteos.estado == "EN_PROCESO").scalar()
        completados = db.query(func.count(models.ProgramacionConteos.id_programacion)).filter(models.ProgramacionConteos.estado == "COMPLETADO").scalar()
        cancelados = db.query(func.count(models.ProgramacionConteos.id_programacion)).filter(models.ProgramacionConteos.estado == "CANCELADO").scalar()

        return {
            "total_programaciones": total,
            "programados": programados,
            "en_proceso": en_proceso,
            "completados": completados,
            "cancelados": cancelados
        }

    def get_estadisticas_por_tipo(self, db: Session) -> List[dict]:
        """Obtener estadísticas por tipo de conteo"""
        from sqlalchemy import func

        stats = (db.query(
                    models.ProgramacionConteos.tipo_conteo,
                    func.count(models.ProgramacionConteos.id_programacion).label('total')
                )
                .group_by(models.ProgramacionConteos.tipo_conteo)
                .all())

        return [{"tipo_conteo": stat.tipo_conteo, "total": stat.total} for stat in stats]

    def get_programaciones_pendientes(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.ProgramacionConteos]:
        """Obtener programaciones pendientes (programadas y en proceso)"""
        return (db.query(models.ProgramacionConteos)
                .filter(models.ProgramacionConteos.estado.in_(["PROGRAMADO", "EN_PROCESO"]))
                .offset(skip)
                .limit(limit)
                .all())

    def get_programaciones_vencidas(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.ProgramacionConteos]:
        """Obtener programaciones vencidas (fecha programada pasada y aún en estado PROGRAMADO)"""
        from datetime import date
        fecha_hoy = date.today()

        return (db.query(models.ProgramacionConteos)
                .filter(
                    models.ProgramacionConteos.fecha_programada < fecha_hoy,
                    models.ProgramacionConteos.estado == "PROGRAMADO"
                )
                .offset(skip)
                .limit(limit)
                .all())

# Instancia global
programacion_conteos_crud = ProgramacionConteosCRUD()

class ConteosFisicosCRUD:
    """CRUD operations for ConteosFisicos"""

    def get_conteo(self, db: Session, conteo_id: int) -> Optional[models.ConteosFisicos]:
        """Obtener conteo por ID"""
        return db.query(models.ConteosFisicos).filter(models.ConteosFisicos.id_conteo == conteo_id).first()

    def get_conteos(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.ConteosFisicos]:
        """Obtener todos los conteos"""
        return db.query(models.ConteosFisicos).offset(skip).limit(limit).all()

    def create_conteo(self, db: Session, conteo: schemas.ConteosFisicosCreate) -> models.ConteosFisicos:
        """Crear nuevo conteo físico"""
        db_conteo = models.ConteosFisicos(**conteo.model_dump())
        db.add(db_conteo)
        db.commit()
        db.refresh(db_conteo)
        return db_conteo

    def update_conteo(self, db: Session, conteo_id: int, conteo: schemas.ConteosFisicosUpdate) -> Optional[models.ConteosFisicos]:
        """Actualizar conteo existente"""
        db_conteo = self.get_conteo(db, conteo_id)
        if not db_conteo:
            return None

        update_data = conteo.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_conteo, field, value)

        db.commit()
        db.refresh(db_conteo)
        return db_conteo

    def delete_conteo(self, db: Session, conteo_id: int) -> bool:
        """Eliminar conteo"""
        db_conteo = self.get_conteo(db, conteo_id)
        if not db_conteo:
            return False

        db.delete(db_conteo)
        db.commit()
        return True

    def get_conteos_by_programacion(self, db: Session, programacion_id: int, skip: int = 0, limit: int = 100) -> List[models.ConteosFisicos]:
        """Obtener conteos por programación"""
        return (db.query(models.ConteosFisicos)
                .filter(models.ConteosFisicos.id_programacion == programacion_id)
                .offset(skip)
                .limit(limit)
                .all())

    def get_conteos_by_producto(self, db: Session, producto_id: int, skip: int = 0, limit: int = 100) -> List[models.ConteosFisicos]:
        """Obtener conteos por producto"""
        return (db.query(models.ConteosFisicos)
                .filter(models.ConteosFisicos.id_producto == producto_id)
                .offset(skip)
                .limit(limit)
                .all())

    def get_conteos_by_obra(self, db: Session, obra_id: int, skip: int = 0, limit: int = 100) -> List[models.ConteosFisicos]:
        """Obtener conteos por obra"""
        return (db.query(models.ConteosFisicos)
                .filter(models.ConteosFisicos.id_obra == obra_id)
                .offset(skip)
                .limit(limit)
                .all())

    def get_conteos_by_ubicacion(self, db: Session, ubicacion_id: int, skip: int = 0, limit: int = 100) -> List[models.ConteosFisicos]:
        """Obtener conteos por ubicación"""
        return (db.query(models.ConteosFisicos)
                .filter(models.ConteosFisicos.id_ubicacion == ubicacion_id)
                .offset(skip)
                .limit(limit)
                .all())

    def get_conteos_by_contador(self, db: Session, usuario_id: int, skip: int = 0, limit: int = 100) -> List[models.ConteosFisicos]:
        """Obtener conteos por usuario contador"""
        return (db.query(models.ConteosFisicos)
                .filter(models.ConteosFisicos.id_usuario_contador == usuario_id)
                .offset(skip)
                .limit(limit)
                .all())

    def get_conteos_con_diferencias(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.ConteosFisicos]:
        """Obtener conteos que tienen diferencias (cantidad_fisica != cantidad_sistema)"""
        return (db.query(models.ConteosFisicos)
                .filter(models.ConteosFisicos.cantidad_fisica != models.ConteosFisicos.cantidad_sistema)
                .offset(skip)
                .limit(limit)
                .all())

    def get_conteos_pendientes_ajuste(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.ConteosFisicos]:
        """Obtener conteos con diferencias que no han sido ajustados"""
        return (db.query(models.ConteosFisicos)
                .filter(
                    models.ConteosFisicos.cantidad_fisica != models.ConteosFisicos.cantidad_sistema,
                    models.ConteosFisicos.ajuste_procesado == False
                )
                .offset(skip)
                .limit(limit)
                .all())

    def get_conteos_by_fecha_range(self, db: Session, fecha_inicio: datetime, fecha_fin: datetime, skip: int = 0, limit: int = 100) -> List[models.ConteosFisicos]:
        """Obtener conteos por rango de fechas"""
        return (db.query(models.ConteosFisicos)
                .filter(
                    models.ConteosFisicos.fecha_conteo >= fecha_inicio,
                    models.ConteosFisicos.fecha_conteo <= fecha_fin
                )
                .offset(skip)
                .limit(limit)
                .all())

    def marcar_ajuste_procesado(self, db: Session, conteo_id: int, id_movimiento_ajuste: int) -> Optional[models.ConteosFisicos]:
        """Marcar que el ajuste ha sido procesado"""
        db_conteo = self.get_conteo(db, conteo_id)
        if not db_conteo:
            return None

        db_conteo.ajuste_procesado = True
        db_conteo.id_movimiento_ajuste = id_movimiento_ajuste

        db.commit()
        db.refresh(db_conteo)
        return db_conteo

    def procesar_ajustes_automaticos(self, db: Session, programacion_id: int) -> List[dict]:
        """Procesar ajustes automáticos para una programación"""
        conteos_pendientes = (db.query(models.ConteosFisicos)
                             .filter(
                                 models.ConteosFisicos.id_programacion == programacion_id,
                                 models.ConteosFisicos.cantidad_fisica != models.ConteosFisicos.cantidad_sistema,
                                 models.ConteosFisicos.ajuste_procesado == False
                             )
                             .all())

        ajustes_procesados = []
        for conteo in conteos_pendientes:
            diferencia = conteo.cantidad_fisica - conteo.cantidad_sistema

            # Aquí se podría implementar la lógica para crear automáticamente
            # un movimiento de inventario de ajuste
            # Por ahora solo se marca como pendiente de ajuste manual

            ajustes_procesados.append({
                "id_conteo": conteo.id_conteo,
                "id_producto": conteo.id_producto,
                "diferencia": diferencia,
                "cantidad_sistema": conteo.cantidad_sistema,
                "cantidad_fisica": conteo.cantidad_fisica,
                "requiere_ajuste": True
            })

        return ajustes_procesados

    def get_estadisticas_programacion(self, db: Session, programacion_id: int) -> dict:
        """Obtener estadísticas de conteos para una programación"""
        from sqlalchemy import func

        conteos = (db.query(models.ConteosFisicos)
                  .filter(models.ConteosFisicos.id_programacion == programacion_id)
                  .all())

        total_conteos = len(conteos)
        con_diferencias = len([c for c in conteos if c.cantidad_fisica != c.cantidad_sistema])
        ajustes_procesados = len([c for c in conteos if c.ajuste_procesado])
        ajustes_pendientes = con_diferencias - ajustes_procesados

        diferencias_positivas = len([c for c in conteos if c.cantidad_fisica > c.cantidad_sistema])
        diferencias_negativas = len([c for c in conteos if c.cantidad_fisica < c.cantidad_sistema])

        return {
            "total_conteos": total_conteos,
            "con_diferencias": con_diferencias,
            "sin_diferencias": total_conteos - con_diferencias,
            "ajustes_procesados": ajustes_procesados,
            "ajustes_pendientes": ajustes_pendientes,
            "diferencias_positivas": diferencias_positivas,
            "diferencias_negativas": diferencias_negativas,
            "porcentaje_exactitud": round((total_conteos - con_diferencias) / total_conteos * 100, 2) if total_conteos > 0 else 0
        }

    def get_estadisticas_generales(self, db: Session) -> dict:
        """Obtener estadísticas generales de conteos"""
        from sqlalchemy import func

        total = db.query(func.count(models.ConteosFisicos.id_conteo)).scalar()
        con_diferencias = db.query(func.count(models.ConteosFisicos.id_conteo)).filter(
            models.ConteosFisicos.cantidad_fisica != models.ConteosFisicos.cantidad_sistema
        ).scalar()
        ajustes_procesados = db.query(func.count(models.ConteosFisicos.id_conteo)).filter(
            models.ConteosFisicos.ajuste_procesado == True
        ).scalar()

        return {
            "total_conteos": total,
            "con_diferencias": con_diferencias,
            "sin_diferencias": total - con_diferencias,
            "ajustes_procesados": ajustes_procesados,
            "ajustes_pendientes": con_diferencias - ajustes_procesados,
            "porcentaje_exactitud": round((total - con_diferencias) / total * 100, 2) if total > 0 else 0
        }

    def get_conteos_por_exactitud(self, db: Session, exactos: bool = True, skip: int = 0, limit: int = 100) -> List[models.ConteosFisicos]:
        """Obtener conteos exactos o con diferencias"""
        if exactos:
            # Conteos exactos (sin diferencias)
            return (db.query(models.ConteosFisicos)
                    .filter(models.ConteosFisicos.cantidad_fisica == models.ConteosFisicos.cantidad_sistema)
                    .offset(skip)
                    .limit(limit)
                    .all())
        else:
            # Conteos con diferencias
            return (db.query(models.ConteosFisicos)
                    .filter(models.ConteosFisicos.cantidad_fisica != models.ConteosFisicos.cantidad_sistema)
                    .offset(skip)
                    .limit(limit)
                    .all())

    def get_resumen_por_producto(self, db: Session, producto_id: int) -> dict:
        """Obtener resumen de conteos para un producto específico"""
        from sqlalchemy import func

        conteos = (db.query(models.ConteosFisicos)
                  .filter(models.ConteosFisicos.id_producto == producto_id)
                  .all())

        total_conteos = len(conteos)
        if total_conteos == 0:
            return {"producto_id": producto_id, "total_conteos": 0}

        con_diferencias = len([c for c in conteos if c.cantidad_fisica != c.cantidad_sistema])
        ultimo_conteo = max(conteos, key=lambda x: x.fecha_conteo) if conteos else None

        return {
            "producto_id": producto_id,
            "total_conteos": total_conteos,
            "con_diferencias": con_diferencias,
            "sin_diferencias": total_conteos - con_diferencias,
            "porcentaje_exactitud": round((total_conteos - con_diferencias) / total_conteos * 100, 2),
            "ultimo_conteo": {
                "fecha": ultimo_conteo.fecha_conteo,
                "cantidad_sistema": ultimo_conteo.cantidad_sistema,
                "cantidad_fisica": ultimo_conteo.cantidad_fisica,
                "diferencia": ultimo_conteo.diferencia
            } if ultimo_conteo else None
        }

# Instancia global
conteos_fisicos_crud = ConteosFisicosCRUD()

class ConfiguracionAlertasCRUD:
    """CRUD operations for ConfiguracionAlertas"""

    def get_alerta(self, db: Session, alerta_id: int) -> Optional[models.ConfiguracionAlertas]:
        """Obtener configuración de alerta por ID"""
        return db.query(models.ConfiguracionAlertas).filter(models.ConfiguracionAlertas.id_alerta == alerta_id).first()

    def get_alertas(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.ConfiguracionAlertas]:
        """Obtener todas las configuraciones de alertas"""
        return db.query(models.ConfiguracionAlertas).offset(skip).limit(limit).all()

    def create_alerta(self, db: Session, alerta: schemas.ConfiguracionAlertasCreate) -> models.ConfiguracionAlertas:
        """Crear nueva configuración de alerta"""
        alerta_data = alerta.model_dump()

        # Convertir listas a strings CSV
        usuarios_list = alerta_data.pop('usuarios_notificar', None)
        emails_list = alerta_data.pop('email_notificar', None)

        db_alerta = models.ConfiguracionAlertas(**alerta_data)

        if usuarios_list:
            db_alerta.set_usuarios_lista(usuarios_list)
        if emails_list:
            db_alerta.set_emails_lista(emails_list)

        db.add(db_alerta)
        db.commit()
        db.refresh(db_alerta)
        return db_alerta

    def update_alerta(self, db: Session, alerta_id: int, alerta: schemas.ConfiguracionAlertasUpdate) -> Optional[models.ConfiguracionAlertas]:
        """Actualizar configuración de alerta existente"""
        db_alerta = self.get_alerta(db, alerta_id)
        if not db_alerta:
            return None

        update_data = alerta.model_dump(exclude_unset=True)

        # Manejar listas especiales
        usuarios_list = update_data.pop('usuarios_notificar', None)
        emails_list = update_data.pop('email_notificar', None)

        # Actualizar campos regulares
        for field, value in update_data.items():
            setattr(db_alerta, field, value)

        # Actualizar listas CSV
        if usuarios_list is not None:
            db_alerta.set_usuarios_lista(usuarios_list)
        if emails_list is not None:
            db_alerta.set_emails_lista(emails_list)

        db.commit()
        db.refresh(db_alerta)
        return db_alerta

    def delete_alerta(self, db: Session, alerta_id: int) -> bool:
        """Eliminar configuración de alerta"""
        db_alerta = self.get_alerta(db, alerta_id)
        if not db_alerta:
            return False

        db.delete(db_alerta)
        db.commit()
        return True

    def get_alertas_activas(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.ConfiguracionAlertas]:
        """Obtener solo las alertas activas"""
        return (db.query(models.ConfiguracionAlertas)
                .filter(models.ConfiguracionAlertas.activa == True)
                .offset(skip)
                .limit(limit)
                .all())

    def get_alertas_by_tipo(self, db: Session, tipo: str, skip: int = 0, limit: int = 100) -> List[models.ConfiguracionAlertas]:
        """Obtener alertas por tipo"""
        return (db.query(models.ConfiguracionAlertas)
                .filter(models.ConfiguracionAlertas.tipo_alerta == tipo)
                .offset(skip)
                .limit(limit)
                .all())

    def activar_alerta(self, db: Session, alerta_id: int) -> Optional[models.ConfiguracionAlertas]:
        """Activar una alerta"""
        db_alerta = self.get_alerta(db, alerta_id)
        if not db_alerta:
            return None

        db_alerta.activa = True
        db.commit()
        db.refresh(db_alerta)
        return db_alerta

    def desactivar_alerta(self, db: Session, alerta_id: int) -> Optional[models.ConfiguracionAlertas]:
        """Desactivar una alerta"""
        db_alerta = self.get_alerta(db, alerta_id)
        if not db_alerta:
            return None

        db_alerta.activa = False
        db.commit()
        db.refresh(db_alerta)
        return db_alerta

    def actualizar_frecuencia(self, db: Session, alerta_id: int, nuevas_horas: int) -> Optional[models.ConfiguracionAlertas]:
        """Actualizar la frecuencia de revisión de una alerta"""
        db_alerta = self.get_alerta(db, alerta_id)
        if not db_alerta:
            return None

        db_alerta.frecuencia_revision_horas = nuevas_horas
        db.commit()
        db.refresh(db_alerta)
        return db_alerta

    def agregar_usuario_notificacion(self, db: Session, alerta_id: int, usuario_id: int) -> Optional[models.ConfiguracionAlertas]:
        """Agregar un usuario a las notificaciones de una alerta"""
        db_alerta = self.get_alerta(db, alerta_id)
        if not db_alerta:
            return None

        usuarios_actuales = db_alerta.get_usuarios_lista()
        if usuario_id not in usuarios_actuales:
            usuarios_actuales.append(usuario_id)
            db_alerta.set_usuarios_lista(usuarios_actuales)
            db.commit()
            db.refresh(db_alerta)

        return db_alerta

    def remover_usuario_notificacion(self, db: Session, alerta_id: int, usuario_id: int) -> Optional[models.ConfiguracionAlertas]:
        """Remover un usuario de las notificaciones de una alerta"""
        db_alerta = self.get_alerta(db, alerta_id)
        if not db_alerta:
            return None

        usuarios_actuales = db_alerta.get_usuarios_lista()
        if usuario_id in usuarios_actuales:
            usuarios_actuales.remove(usuario_id)
            db_alerta.set_usuarios_lista(usuarios_actuales)
            db.commit()
            db.refresh(db_alerta)

        return db_alerta

    def agregar_email_notificacion(self, db: Session, alerta_id: int, email: str) -> Optional[models.ConfiguracionAlertas]:
        """Agregar un email a las notificaciones de una alerta"""
        db_alerta = self.get_alerta(db, alerta_id)
        if not db_alerta:
            return None

        emails_actuales = db_alerta.get_emails_lista()
        if email not in emails_actuales:
            emails_actuales.append(email)
            db_alerta.set_emails_lista(emails_actuales)
            db.commit()
            db.refresh(db_alerta)

        return db_alerta

    def remover_email_notificacion(self, db: Session, alerta_id: int, email: str) -> Optional[models.ConfiguracionAlertas]:
        """Remover un email de las notificaciones de una alerta"""
        db_alerta = self.get_alerta(db, alerta_id)
        if not db_alerta:
            return None

        emails_actuales = db_alerta.get_emails_lista()
        if email in emails_actuales:
            emails_actuales.remove(email)
            db_alerta.set_emails_lista(emails_actuales)
            db.commit()
            db.refresh(db_alerta)

        return db_alerta

    def get_estadisticas_alertas(self, db: Session) -> dict:
        """Obtener estadísticas de configuración de alertas"""
        from sqlalchemy import func

        total = db.query(func.count(models.ConfiguracionAlertas.id_alerta)).scalar()
        activas = db.query(func.count(models.ConfiguracionAlertas.id_alerta)).filter(models.ConfiguracionAlertas.activa == True).scalar()
        inactivas = total - activas

        # Contar por tipo
        tipos = db.query(
            models.ConfiguracionAlertas.tipo_alerta,
            func.count(models.ConfiguracionAlertas.id_alerta).label('cantidad')
        ).group_by(models.ConfiguracionAlertas.tipo_alerta).all()

        tipos_dict = {tipo.tipo_alerta: tipo.cantidad for tipo in tipos}

        return {
            "total_alertas": total,
            "alertas_activas": activas,
            "alertas_inactivas": inactivas,
            "por_tipo": tipos_dict
        }

    def validar_emails_formato(self, emails: List[str]) -> List[str]:
        """Validar formato de emails y retornar solo los válidos"""
        import re
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return [email for email in emails if email_pattern.match(email)]

    def duplicar_alerta(self, db: Session, alerta_id: int, nuevo_nombre: str) -> Optional[models.ConfiguracionAlertas]:
        """Duplicar una configuración de alerta existente"""
        alerta_original = self.get_alerta(db, alerta_id)
        if not alerta_original:
            return None

        nueva_alerta = models.ConfiguracionAlertas(
            nombre_alerta=nuevo_nombre,
            tipo_alerta=alerta_original.tipo_alerta,
            activa=alerta_original.activa,
            dias_anticipacion=alerta_original.dias_anticipacion,
            usuarios_notificar=alerta_original.usuarios_notificar,
            email_notificar=alerta_original.email_notificar,
            frecuencia_revision_horas=alerta_original.frecuencia_revision_horas
        )

        db.add(nueva_alerta)
        db.commit()
        db.refresh(nueva_alerta)
        return nueva_alerta

    def get_alertas_para_revision(self, db: Session) -> List[models.ConfiguracionAlertas]:
        """Obtener alertas que necesitan ser revisadas basado en su frecuencia"""
        from datetime import datetime, timedelta

        # Esta función podría extenderse para incluir lógica de última revisión
        # Por ahora retorna todas las alertas activas
        return (db.query(models.ConfiguracionAlertas)
                .filter(models.ConfiguracionAlertas.activa == True)
                .all())

    def buscar_alertas(self, db: Session, texto_busqueda: str, skip: int = 0, limit: int = 100) -> List[models.ConfiguracionAlertas]:
        """Buscar alertas por nombre"""
        return (db.query(models.ConfiguracionAlertas)
                .filter(models.ConfiguracionAlertas.nombre_alerta.ilike(f"%{texto_busqueda}%"))
                .offset(skip)
                .limit(limit)
                .all())

# Instancia global
configuracion_alertas_crud = ConfiguracionAlertasCRUD()

class LogAlertasCRUD:
    """CRUD operations for LogAlertas"""

    def get_log_alerta(self, db: Session, log_id: int) -> Optional[models.LogAlertas]:
        """Obtener log de alerta por ID"""
        return db.query(models.LogAlertas).filter(models.LogAlertas.id_log_alerta == log_id).first()

    def get_logs_alertas(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.LogAlertas]:
        """Obtener todos los logs de alertas"""
        return db.query(models.LogAlertas).order_by(models.LogAlertas.fecha_generacion.desc()).offset(skip).limit(limit).all()

    def create_log_alerta(self, db: Session, log_alerta: schemas.LogAlertasCreate) -> models.LogAlertas:
        """Crear nuevo log de alerta"""
        db_log = models.LogAlertas(**log_alerta.model_dump())
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log

    def update_log_alerta(self, db: Session, log_id: int, log_alerta: schemas.LogAlertasUpdate) -> Optional[models.LogAlertas]:
        """Actualizar log de alerta existente"""
        db_log = self.get_log_alerta(db, log_id)
        if not db_log:
            return None

        update_data = log_alerta.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_log, field, value)

        db.commit()
        db.refresh(db_log)
        return db_log

    def delete_log_alerta(self, db: Session, log_id: int) -> bool:
        """Eliminar log de alerta"""
        db_log = self.get_log_alerta(db, log_id)
        if not db_log:
            return False

        db.delete(db_log)
        db.commit()
        return True

    def get_logs_by_configuracion(self, db: Session, configuracion_id: int, skip: int = 0, limit: int = 100) -> List[models.LogAlertas]:
        """Obtener logs por configuración de alerta"""
        return (db.query(models.LogAlertas)
                .filter(models.LogAlertas.id_alerta == configuracion_id)
                .order_by(models.LogAlertas.fecha_generacion.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_logs_by_estado(self, db: Session, estado: str, skip: int = 0, limit: int = 100) -> List[models.LogAlertas]:
        """Obtener logs por estado"""
        return (db.query(models.LogAlertas)
                .filter(models.LogAlertas.estado == estado)
                .order_by(models.LogAlertas.fecha_generacion.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_logs_by_prioridad(self, db: Session, prioridad: str, skip: int = 0, limit: int = 100) -> List[models.LogAlertas]:
        """Obtener logs por nivel de prioridad"""
        return (db.query(models.LogAlertas)
                .filter(models.LogAlertas.nivel_prioridad == prioridad)
                .order_by(models.LogAlertas.fecha_generacion.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_logs_by_producto(self, db: Session, producto_id: int, skip: int = 0, limit: int = 100) -> List[models.LogAlertas]:
        """Obtener logs por producto"""
        return (db.query(models.LogAlertas)
                .filter(models.LogAlertas.id_producto == producto_id)
                .order_by(models.LogAlertas.fecha_generacion.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_logs_by_obra(self, db: Session, obra_id: int, skip: int = 0, limit: int = 100) -> List[models.LogAlertas]:
        """Obtener logs por obra"""
        return (db.query(models.LogAlertas)
                .filter(models.LogAlertas.id_obra == obra_id)
                .order_by(models.LogAlertas.fecha_generacion.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_logs_by_despacho(self, db: Session, despacho_id: int, skip: int = 0, limit: int = 100) -> List[models.LogAlertas]:
        """Obtener logs por despacho"""
        return (db.query(models.LogAlertas)
                .filter(models.LogAlertas.id_despacho == despacho_id)
                .order_by(models.LogAlertas.fecha_generacion.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_logs_by_usuario_resolucion(self, db: Session, usuario_id: int, skip: int = 0, limit: int = 100) -> List[models.LogAlertas]:
        """Obtener logs por usuario que los resolvió"""
        return (db.query(models.LogAlertas)
                .filter(models.LogAlertas.usuario_resolucion == usuario_id)
                .order_by(models.LogAlertas.fecha_generacion.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_logs_pendientes(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.LogAlertas]:
        """Obtener logs pendientes"""
        return (db.query(models.LogAlertas)
                .filter(models.LogAlertas.estado == 'PENDIENTE')
                .order_by(models.LogAlertas.fecha_generacion.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_logs_criticos(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.LogAlertas]:
        """Obtener logs críticos"""
        return (db.query(models.LogAlertas)
                .filter(models.LogAlertas.nivel_prioridad == 'CRITICA')
                .order_by(models.LogAlertas.fecha_generacion.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_logs_sin_resolver(self, db: Session, horas_limite: int = 24, skip: int = 0, limit: int = 100) -> List[models.LogAlertas]:
        """Obtener logs sin resolver después de X horas"""
        from datetime import datetime, timedelta
        fecha_limite = datetime.now() - timedelta(hours=horas_limite)

        return (db.query(models.LogAlertas)
                .filter(
                    models.LogAlertas.estado.in_(['PENDIENTE', 'VISTA']),
                    models.LogAlertas.fecha_generacion <= fecha_limite
                )
                .order_by(models.LogAlertas.fecha_generacion.asc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_logs_by_fecha_range(self, db: Session, fecha_inicio: datetime, fecha_fin: datetime, skip: int = 0, limit: int = 100) -> List[models.LogAlertas]:
        """Obtener logs por rango de fechas"""
        return (db.query(models.LogAlertas)
                .filter(
                    models.LogAlertas.fecha_generacion >= fecha_inicio,
                    models.LogAlertas.fecha_generacion <= fecha_fin
                )
                .order_by(models.LogAlertas.fecha_generacion.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def marcar_como_vista(self, db: Session, log_id: int, fecha_vista: datetime = None) -> Optional[models.LogAlertas]:
        """Marcar log como visto"""
        db_log = self.get_log_alerta(db, log_id)
        if not db_log:
            return None

        if fecha_vista is None:
            from datetime import datetime
            fecha_vista = datetime.now()

        db_log.marcar_como_vista(fecha_vista)
        db.commit()
        db.refresh(db_log)
        return db_log

    def resolver_alerta(self, db: Session, log_id: int, usuario_id: int, observaciones: str = None, fecha_resolucion: datetime = None) -> Optional[models.LogAlertas]:
        """Resolver alerta"""
        db_log = self.get_log_alerta(db, log_id)
        if not db_log:
            return None

        db_log.resolver(usuario_id, observaciones, fecha_resolucion)
        db.commit()
        db.refresh(db_log)
        return db_log

    def ignorar_alerta(self, db: Session, log_id: int, usuario_id: int, motivo: str = None) -> Optional[models.LogAlertas]:
        """Ignorar alerta"""
        db_log = self.get_log_alerta(db, log_id)
        if not db_log:
            return None

        db_log.ignorar(usuario_id, motivo)
        db.commit()
        db.refresh(db_log)
        return db_log

    def marcar_multiples_como_vistas(self, db: Session, log_ids: List[int]) -> int:
        """Marcar múltiples logs como vistos"""
        from datetime import datetime
        fecha_vista = datetime.now()

        count = (db.query(models.LogAlertas)
                .filter(
                    models.LogAlertas.id_log_alerta.in_(log_ids),
                    models.LogAlertas.estado == 'PENDIENTE'
                )
                .update({
                    'estado': 'VISTA',
                    'fecha_visualizacion': fecha_vista
                }, synchronize_session=False))

        db.commit()
        return count

    def resolver_multiples_alertas(self, db: Session, log_ids: List[int], usuario_id: int, observaciones: str = None) -> int:
        """Resolver múltiples alertas"""
        from datetime import datetime
        fecha_resolucion = datetime.now()

        update_data = {
            'estado': 'RESUELTA',
            'fecha_resolucion': fecha_resolucion,
            'usuario_resolucion': usuario_id
        }

        if observaciones:
            update_data['observaciones_resolucion'] = observaciones

        count = (db.query(models.LogAlertas)
                .filter(
                    models.LogAlertas.id_log_alerta.in_(log_ids),
                    models.LogAlertas.estado.in_(['PENDIENTE', 'VISTA'])
                )
                .update(update_data, synchronize_session=False))

        db.commit()
        return count

    def get_estadisticas_logs(self, db: Session) -> dict:
        """Obtener estadísticas de logs de alertas"""
        from sqlalchemy import func

        total = db.query(func.count(models.LogAlertas.id_log_alerta)).scalar()
        pendientes = db.query(func.count(models.LogAlertas.id_log_alerta)).filter(models.LogAlertas.estado == 'PENDIENTE').scalar()
        vistas = db.query(func.count(models.LogAlertas.id_log_alerta)).filter(models.LogAlertas.estado == 'VISTA').scalar()
        resueltas = db.query(func.count(models.LogAlertas.id_log_alerta)).filter(models.LogAlertas.estado == 'RESUELTA').scalar()
        ignoradas = db.query(func.count(models.LogAlertas.id_log_alerta)).filter(models.LogAlertas.estado == 'IGNORADA').scalar()

        # Estadísticas por prioridad
        criticas = db.query(func.count(models.LogAlertas.id_log_alerta)).filter(models.LogAlertas.nivel_prioridad == 'CRITICA').scalar()
        altas = db.query(func.count(models.LogAlertas.id_log_alerta)).filter(models.LogAlertas.nivel_prioridad == 'ALTA').scalar()
        medias = db.query(func.count(models.LogAlertas.id_log_alerta)).filter(models.LogAlertas.nivel_prioridad == 'MEDIA').scalar()
        bajas = db.query(func.count(models.LogAlertas.id_log_alerta)).filter(models.LogAlertas.nivel_prioridad == 'BAJA').scalar()

        return {
            "total_logs": total,
            "por_estado": {
                "pendientes": pendientes,
                "vistas": vistas,
                "resueltas": resueltas,
                "ignoradas": ignoradas
            },
            "por_prioridad": {
                "criticas": criticas,
                "altas": altas,
                "medias": medias,
                "bajas": bajas
            },
            "pendientes_criticas": db.query(func.count(models.LogAlertas.id_log_alerta)).filter(
                models.LogAlertas.estado == 'PENDIENTE',
                models.LogAlertas.nivel_prioridad == 'CRITICA'
            ).scalar()
        }

    def get_resumen_por_configuracion(self, db: Session, configuracion_id: int) -> dict:
        """Obtener resumen de logs para una configuración específica"""
        from sqlalchemy import func

        logs = self.get_logs_by_configuracion(db, configuracion_id, limit=1000)
        total = len(logs)

        if total == 0:
            return {"configuracion_id": configuracion_id, "total_logs": 0}

        pendientes = len([log for log in logs if log.estado == 'PENDIENTE'])
        resueltas = len([log for log in logs if log.estado == 'RESUELTA'])
        tiempo_promedio_resolucion = 0

        logs_resueltos = [log for log in logs if log.fecha_resolucion]
        if logs_resueltos:
            tiempos = [(log.fecha_resolucion - log.fecha_generacion).total_seconds() / 3600 for log in logs_resueltos]
            tiempo_promedio_resolucion = sum(tiempos) / len(tiempos)

        return {
            "configuracion_id": configuracion_id,
            "total_logs": total,
            "pendientes": pendientes,
            "resueltas": resueltas,
            "tasa_resolucion": round(resueltas / total * 100, 2) if total > 0 else 0,
            "tiempo_promedio_resolucion_horas": round(tiempo_promedio_resolucion, 2)
        }

    def limpiar_logs_antiguos(self, db: Session, dias_antiguedad: int = 90) -> int:
        """Limpiar logs antiguos resueltos o ignorados"""
        from datetime import datetime, timedelta
        fecha_limite = datetime.now() - timedelta(days=dias_antiguedad)

        count = (db.query(models.LogAlertas)
                .filter(
                    models.LogAlertas.estado.in_(['RESUELTA', 'IGNORADA']),
                    models.LogAlertas.fecha_generacion <= fecha_limite
                )
                .delete(synchronize_session=False))

        db.commit()
        return count

    def buscar_logs(self, db: Session, texto_busqueda: str, skip: int = 0, limit: int = 100) -> List[models.LogAlertas]:
        """Buscar logs por contenido del mensaje"""
        return (db.query(models.LogAlertas)
                .filter(models.LogAlertas.mensaje.ilike(f"%{texto_busqueda}%"))
                .order_by(models.LogAlertas.fecha_generacion.desc())
                .offset(skip)
                .limit(limit)
                .all())

# Instancia global
log_alertas_crud = LogAlertasCRUD()

class RolesCRUD:
    """CRUD operations for Roles"""

    def get_rol(self, db: Session, rol_id: int) -> Optional[models.Roles]:
        """Obtener rol por ID"""
        return db.query(models.Roles).filter(models.Roles.id_rol == rol_id).first()

    def get_rol_by_nombre(self, db: Session, nombre_rol: str) -> Optional[models.Roles]:
        """Obtener rol por nombre"""
        return db.query(models.Roles).filter(models.Roles.nombre_rol == nombre_rol).first()

    def get_roles(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Roles]:
        """Obtener todos los roles"""
        return db.query(models.Roles).offset(skip).limit(limit).all()

    def create_rol(self, db: Session, rol: schemas.RolesCreate) -> models.Roles:
        """Crear nuevo rol"""
        # Verificar si ya existe un rol con ese nombre
        existing_rol = self.get_rol_by_nombre(db, rol.nombre_rol)
        if existing_rol:
            raise ValueError(f"Ya existe un rol con el nombre '{rol.nombre_rol}'")

        db_rol = models.Roles(**rol.model_dump())
        db.add(db_rol)
        db.commit()
        db.refresh(db_rol)
        return db_rol

    def update_rol(self, db: Session, rol_id: int, rol: schemas.RolesUpdate) -> Optional[models.Roles]:
        """Actualizar rol existente"""
        db_rol = self.get_rol(db, rol_id)
        if not db_rol:
            return None

        update_data = rol.model_dump(exclude_unset=True)

        # Verificar que el nuevo nombre no esté en uso por otro rol
        if 'nombre_rol' in update_data:
            existing_rol = self.get_rol_by_nombre(db, update_data['nombre_rol'])
            if existing_rol and existing_rol.id_rol != rol_id:
                raise ValueError(f"Ya existe un rol con el nombre '{update_data['nombre_rol']}'")

        for field, value in update_data.items():
            setattr(db_rol, field, value)

        db.commit()
        db.refresh(db_rol)
        return db_rol

    def delete_rol(self, db: Session, rol_id: int) -> bool:
        """Eliminar rol"""
        db_rol = self.get_rol(db, rol_id)
        if not db_rol:
            return False

        db.delete(db_rol)
        db.commit()
        return True

    def get_roles_activos(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Roles]:
        """Obtener solo los roles activos"""
        return (db.query(models.Roles)
                .filter(models.Roles.activo == True)
                .offset(skip)
                .limit(limit)
                .all())

    def activar_rol(self, db: Session, rol_id: int) -> Optional[models.Roles]:
        """Activar un rol"""
        db_rol = self.get_rol(db, rol_id)
        if not db_rol:
            return None

        db_rol.activo = True
        db.commit()
        db.refresh(db_rol)
        return db_rol

    def desactivar_rol(self, db: Session, rol_id: int) -> Optional[models.Roles]:
        """Desactivar un rol"""
        db_rol = self.get_rol(db, rol_id)
        if not db_rol:
            return None

        db_rol.activo = False
        db.commit()
        db.refresh(db_rol)
        return db_rol

    def buscar_roles(self, db: Session, texto_busqueda: str, skip: int = 0, limit: int = 100) -> List[models.Roles]:
        """Buscar roles por nombre o descripción"""
        return (db.query(models.Roles)
                .filter(
                    models.Roles.nombre_rol.ilike(f"%{texto_busqueda}%") |
                    models.Roles.descripcion.ilike(f"%{texto_busqueda}%")
                )
                .offset(skip)
                .limit(limit)
                .all())

    def get_estadisticas_roles(self, db: Session) -> dict:
        """Obtener estadísticas de roles"""
        from sqlalchemy import func

        total = db.query(func.count(models.Roles.id_rol)).scalar()
        activos = db.query(func.count(models.Roles.id_rol)).filter(models.Roles.activo == True).scalar()
        inactivos = total - activos

        return {
            "total_roles": total,
            "roles_activos": activos,
            "roles_inactivos": inactivos
        }

    def validar_nombre_unico(self, db: Session, nombre_rol: str, excluir_id: int = None) -> bool:
        """Validar que el nombre del rol sea único"""
        query = db.query(models.Roles).filter(models.Roles.nombre_rol == nombre_rol)
        if excluir_id:
            query = query.filter(models.Roles.id_rol != excluir_id)

        existing_rol = query.first()
        return existing_rol is None

    def duplicar_rol(self, db: Session, rol_id: int, nuevo_nombre: str) -> Optional[models.Roles]:
        """Duplicar un rol existente con un nuevo nombre"""
        rol_original = self.get_rol(db, rol_id)
        if not rol_original:
            return None

        # Verificar que el nuevo nombre no esté en uso
        if not self.validar_nombre_unico(db, nuevo_nombre):
            raise ValueError(f"Ya existe un rol con el nombre '{nuevo_nombre}'")

        nuevo_rol = models.Roles(
            nombre_rol=nuevo_nombre,
            descripcion=f"Copia de: {rol_original.descripcion}" if rol_original.descripcion else None,
            activo=rol_original.activo
        )

        db.add(nuevo_rol)
        db.commit()
        db.refresh(nuevo_rol)
        return nuevo_rol

    def get_roles_ordenados(self, db: Session, campo_orden: str = "nombre_rol", ascendente: bool = True, skip: int = 0, limit: int = 100) -> List[models.Roles]:
        """Obtener roles ordenados por un campo específico"""
        campos_validos = ["nombre_rol", "activo", "id_rol"]
        if campo_orden not in campos_validos:
            campo_orden = "nombre_rol"

        query = db.query(models.Roles)

        if campo_orden == "nombre_rol":
            order_field = models.Roles.nombre_rol
        elif campo_orden == "activo":
            order_field = models.Roles.activo
        else:  # id_rol
            order_field = models.Roles.id_rol

        if ascendente:
            query = query.order_by(order_field.asc())
        else:
            query = query.order_by(order_field.desc())

        return query.offset(skip).limit(limit).all()

# Instancia global
roles_crud = RolesCRUD()

class UsuariosCRUD:
    """CRUD operations for Usuarios"""

    def _hash_password(self, password: str) -> str:
        """Hash de contraseña usando bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verificar contraseña contra hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def get_usuario(self, db: Session, usuario_id: int) -> Optional[models.Usuarios]:
        """Obtener usuario por ID"""
        return db.query(models.Usuarios).filter(models.Usuarios.id_usuario == usuario_id).first()

    def get_usuario_by_username(self, db: Session, username: str) -> Optional[models.Usuarios]:
        """Obtener usuario por username"""
        return db.query(models.Usuarios).filter(models.Usuarios.username == username).first()

    def get_usuario_by_email(self, db: Session, email: str) -> Optional[models.Usuarios]:
        """Obtener usuario por email"""
        return db.query(models.Usuarios).filter(models.Usuarios.email == email).first()

    def get_usuarios(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Usuarios]:
        """Obtener todos los usuarios"""
        return db.query(models.Usuarios).offset(skip).limit(limit).all()

    def create_usuario(self, db: Session, usuario: schemas.UsuariosCreate) -> models.Usuarios:
        """Crear nuevo usuario"""
        # Verificar si ya existe un usuario con ese username
        existing_user = self.get_usuario_by_username(db, usuario.username)
        if existing_user:
            raise ValueError(f"Ya existe un usuario con el username '{usuario.username}'")

        # Verificar si ya existe un usuario con ese email
        existing_email = self.get_usuario_by_email(db, usuario.email)
        if existing_email:
            raise ValueError(f"Ya existe un usuario con el email '{usuario.email}'")

        # Verificar que el rol existe
        rol = db.query(models.Roles).filter(models.Roles.id_rol == usuario.id_rol).first()
        if not rol:
            raise ValueError(f"El rol con ID {usuario.id_rol} no existe")

        # Crear el usuario con contraseña hasheada
        usuario_data = usuario.model_dump()
        password = usuario_data.pop('password')
        password_hash = self._hash_password(password)

        db_usuario = models.Usuarios(
            **usuario_data,
            password_hash=password_hash
        )

        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    def update_usuario(self, db: Session, usuario_id: int, usuario: schemas.UsuariosUpdate) -> Optional[models.Usuarios]:
        """Actualizar usuario existente"""
        db_usuario = self.get_usuario(db, usuario_id)
        if not db_usuario:
            return None

        update_data = usuario.model_dump(exclude_unset=True)

        # Verificar que el nuevo username no esté en uso por otro usuario
        if 'username' in update_data:
            existing_user = self.get_usuario_by_username(db, update_data['username'])
            if existing_user and existing_user.id_usuario != usuario_id:
                raise ValueError(f"Ya existe un usuario con el username '{update_data['username']}'")

        # Verificar que el nuevo email no esté en uso por otro usuario
        if 'email' in update_data:
            existing_email = self.get_usuario_by_email(db, update_data['email'])
            if existing_email and existing_email.id_usuario != usuario_id:
                raise ValueError(f"Ya existe un usuario con el email '{update_data['email']}'")

        # Verificar que el rol existe si se está actualizando
        if 'id_rol' in update_data:
            rol = db.query(models.Roles).filter(models.Roles.id_rol == update_data['id_rol']).first()
            if not rol:
                raise ValueError(f"El rol con ID {update_data['id_rol']} no existe")

        for field, value in update_data.items():
            setattr(db_usuario, field, value)

        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    def delete_usuario(self, db: Session, usuario_id: int) -> bool:
        """Eliminar usuario"""
        db_usuario = self.get_usuario(db, usuario_id)
        if not db_usuario:
            return False

        db.delete(db_usuario)
        db.commit()
        return True

    def authenticate_usuario(self, db: Session, username: str, password: str) -> Optional[models.Usuarios]:
        """Autenticar usuario por username y contraseña"""
        usuario = self.get_usuario_by_username(db, username)
        if not usuario:
            return None

        if not self._verify_password(password, usuario.password_hash):
            return None

        # Actualizar último acceso
        usuario.actualizar_ultimo_acceso()
        db.commit()
        db.refresh(usuario)

        return usuario

    def cambiar_password(self, db: Session, usuario_id: int, password_actual: str, password_nueva: str) -> bool:
        """Cambiar contraseña de usuario"""
        usuario = self.get_usuario(db, usuario_id)
        if not usuario:
            return False

        # Verificar contraseña actual
        if not self._verify_password(password_actual, usuario.password_hash):
            return False

        # Actualizar con nueva contraseña
        usuario.password_hash = self._hash_password(password_nueva)
        db.commit()

        return True

    def get_usuarios_activos(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Usuarios]:
        """Obtener solo los usuarios activos"""
        return (db.query(models.Usuarios)
                .filter(models.Usuarios.activo == True)
                .offset(skip)
                .limit(limit)
                .all())

    def get_usuarios_by_rol(self, db: Session, rol_id: int, skip: int = 0, limit: int = 100) -> List[models.Usuarios]:
        """Obtener usuarios por rol"""
        return (db.query(models.Usuarios)
                .filter(models.Usuarios.id_rol == rol_id)
                .offset(skip)
                .limit(limit)
                .all())

    def activar_usuario(self, db: Session, usuario_id: int) -> Optional[models.Usuarios]:
        """Activar un usuario"""
        db_usuario = self.get_usuario(db, usuario_id)
        if not db_usuario:
            return None

        db_usuario.activo = True
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    def desactivar_usuario(self, db: Session, usuario_id: int) -> Optional[models.Usuarios]:
        """Desactivar un usuario"""
        db_usuario = self.get_usuario(db, usuario_id)
        if not db_usuario:
            return None

        db_usuario.activo = False
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    def buscar_usuarios(self, db: Session, texto_busqueda: str, skip: int = 0, limit: int = 100) -> List[models.Usuarios]:
        """Buscar usuarios por username, email o nombre completo"""
        return (db.query(models.Usuarios)
                .filter(
                    models.Usuarios.username.ilike(f"%{texto_busqueda}%") |
                    models.Usuarios.email.ilike(f"%{texto_busqueda}%") |
                    models.Usuarios.nombre_completo.ilike(f"%{texto_busqueda}%")
                )
                .offset(skip)
                .limit(limit)
                .all())

    def get_usuarios_sin_acceso_reciente(self, db: Session, dias: int = 30, skip: int = 0, limit: int = 100) -> List[models.Usuarios]:
        """Obtener usuarios que no han accedido en X días"""
        from datetime import datetime, timedelta
        fecha_limite = datetime.now() - timedelta(days=dias)

        return (db.query(models.Usuarios)
                .filter(
                    models.Usuarios.activo == True,
                    (models.Usuarios.ultimo_acceso.is_(None)) |
                    (models.Usuarios.ultimo_acceso <= fecha_limite)
                )
                .offset(skip)
                .limit(limit)
                .all())

    def get_estadisticas_usuarios(self, db: Session) -> dict:
        """Obtener estadísticas de usuarios"""
        from sqlalchemy import func

        total = db.query(func.count(models.Usuarios.id_usuario)).scalar()
        activos = db.query(func.count(models.Usuarios.id_usuario)).filter(models.Usuarios.activo == True).scalar()
        inactivos = total - activos

        # Usuarios por rol
        usuarios_por_rol = (db.query(
                models.Roles.nombre_rol,
                func.count(models.Usuarios.id_usuario).label('cantidad')
            )
            .join(models.Usuarios)
            .group_by(models.Roles.nombre_rol)
            .all())

        roles_dict = {rol.nombre_rol: rol.cantidad for rol in usuarios_por_rol}

        # Usuarios con acceso reciente (últimos 30 días)
        from datetime import datetime, timedelta
        fecha_limite = datetime.now() - timedelta(days=30)

        acceso_reciente = db.query(func.count(models.Usuarios.id_usuario)).filter(
            models.Usuarios.ultimo_acceso >= fecha_limite
        ).scalar()

        return {
            "total_usuarios": total,
            "usuarios_activos": activos,
            "usuarios_inactivos": inactivos,
            "por_rol": roles_dict,
            "con_acceso_reciente": acceso_reciente,
            "sin_acceso_reciente": total - acceso_reciente
        }

    def validar_username_unico(self, db: Session, username: str, excluir_id: int = None) -> bool:
        """Validar que el username sea único"""
        query = db.query(models.Usuarios).filter(models.Usuarios.username == username)
        if excluir_id:
            query = query.filter(models.Usuarios.id_usuario != excluir_id)

        existing_user = query.first()
        return existing_user is None

    def validar_email_unico(self, db: Session, email: str, excluir_id: int = None) -> bool:
        """Validar que el email sea único"""
        query = db.query(models.Usuarios).filter(models.Usuarios.email == email)
        if excluir_id:
            query = query.filter(models.Usuarios.id_usuario != excluir_id)

        existing_email = query.first()
        return existing_email is None

    def reset_password(self, db: Session, usuario_id: int, nueva_password: str) -> bool:
        """Resetear contraseña de usuario (para administradores)"""
        usuario = self.get_usuario(db, usuario_id)
        if not usuario:
            return False

        usuario.password_hash = self._hash_password(nueva_password)
        db.commit()

        return True

    def get_usuarios_ordenados(self, db: Session, campo_orden: str = "nombre_completo", ascendente: bool = True, skip: int = 0, limit: int = 100) -> List[models.Usuarios]:
        """Obtener usuarios ordenados por un campo específico"""
        campos_validos = ["username", "email", "nombre_completo", "activo", "ultimo_acceso", "fecha_creacion"]
        if campo_orden not in campos_validos:
            campo_orden = "nombre_completo"

        query = db.query(models.Usuarios)

        if campo_orden == "username":
            order_field = models.Usuarios.username
        elif campo_orden == "email":
            order_field = models.Usuarios.email
        elif campo_orden == "nombre_completo":
            order_field = models.Usuarios.nombre_completo
        elif campo_orden == "activo":
            order_field = models.Usuarios.activo
        elif campo_orden == "ultimo_acceso":
            order_field = models.Usuarios.ultimo_acceso
        else:  # fecha_creacion
            order_field = models.Usuarios.fecha_creacion

        if ascendente:
            query = query.order_by(order_field.asc())
        else:
            query = query.order_by(order_field.desc())

        return query.offset(skip).limit(limit).all()

# Instancia global
usuarios_crud = UsuariosCRUD()

# ========================================
# CRUD PARA PERMISOS
# ========================================

class PermisoCRUD:
    """CRUD operations for Permisos"""

    def get_permiso(self, db: Session, permiso_id: int) -> Optional[models.Permisos]:
        """Obtener permiso por ID"""
        return db.query(models.Permisos).filter(models.Permisos.id_permiso == permiso_id).first()

    def get_permisos_by_rol(self, db: Session, rol_id: int, modulo: Optional[str] = None) -> List[models.Permisos]:
        """Obtener permisos de un rol"""
        query = db.query(models.Permisos).filter(models.Permisos.id_rol == rol_id)

        if modulo:
            query = query.filter(models.Permisos.modulo == modulo.upper())

        return query.all()

    def get_permisos(self, db: Session, skip: int = 0, limit: int = 100, modulo: Optional[str] = None) -> List[models.Permisos]:
        """Obtener lista de permisos con paginación"""
        query = db.query(models.Permisos)

        if modulo:
            query = query.filter(models.Permisos.modulo == modulo.upper())

        return query.offset(skip).limit(limit).all()

    def create_permiso(self, db: Session, permiso: schemas.PermisoCreate) -> models.Permisos:
        """Crear nuevo permiso"""
        permiso_data = permiso.dict()
        permiso_data['modulo'] = permiso_data['modulo'].upper()

        db_permiso = models.Permisos(**permiso_data)
        db.add(db_permiso)
        db.commit()
        db.refresh(db_permiso)
        return db_permiso

    def update_permiso(self, db: Session, permiso_id: int, permiso_update: schemas.PermisoUpdate) -> Optional[models.Permisos]:
        """Actualizar permiso"""
        db_permiso = self.get_permiso(db, permiso_id)
        if not db_permiso:
            return None

        update_data = permiso_update.dict(exclude_unset=True)

        # Convertir módulo a mayúsculas si está presente
        if 'modulo' in update_data and update_data['modulo']:
            update_data['modulo'] = update_data['modulo'].upper()

        for field, value in update_data.items():
            setattr(db_permiso, field, value)

        db.commit()
        db.refresh(db_permiso)
        return db_permiso

    def delete_permiso(self, db: Session, permiso_id: int) -> bool:
        """Eliminar permiso"""
        db_permiso = self.get_permiso(db, permiso_id)
        if not db_permiso:
            return False

        db.delete(db_permiso)
        db.commit()
        return True

# Instancia global
permiso_crud = PermisoCRUD()

# ========================================
# CRUD PARA CONFIGURACION SISTEMA
# ========================================

class ConfiguracionSistemaCRUD:
    """CRUD operations for ConfiguracionSistema"""

    def get_configuracion(self, db: Session, config_id: int) -> Optional[models.ConfiguracionSistema]:
        """Obtener configuración por ID"""
        return db.query(models.ConfiguracionSistema).filter(models.ConfiguracionSistema.id_config == config_id).first()

    def get_configuracion_by_parametro(self, db: Session, parametro: str) -> Optional[models.ConfiguracionSistema]:
        """Obtener configuración por parámetro"""
        return db.query(models.ConfiguracionSistema).filter(models.ConfiguracionSistema.parametro == parametro).first()

    def get_configuraciones_by_tipo(self, db: Session, tipo_dato: str) -> List[models.ConfiguracionSistema]:
        """Obtener configuraciones por tipo de dato"""
        return db.query(models.ConfiguracionSistema).filter(models.ConfiguracionSistema.tipo_dato == tipo_dato).all()

    def get_configuraciones(self, db: Session, skip: int = 0, limit: int = 100, modificable: Optional[bool] = None, tipo_dato: Optional[str] = None) -> List[models.ConfiguracionSistema]:
        """Obtener lista de configuraciones con paginación"""
        query = db.query(models.ConfiguracionSistema)

        if modificable is not None:
            query = query.filter(models.ConfiguracionSistema.modificable == modificable)

        if tipo_dato:
            query = query.filter(models.ConfiguracionSistema.tipo_dato == tipo_dato.upper())

        return query.offset(skip).limit(limit).all()

    def create_configuracion(self, db: Session, configuracion: schemas.ConfiguracionSistemaCreate) -> models.ConfiguracionSistema:
        """Crear nueva configuración"""
        db_configuracion = models.ConfiguracionSistema(**configuracion.dict())
        db.add(db_configuracion)
        db.commit()
        db.refresh(db_configuracion)
        return db_configuracion

    def update_configuracion(self, db: Session, config_id: int, configuracion_update: schemas.ConfiguracionSistemaUpdate) -> Optional[models.ConfiguracionSistema]:
        """Actualizar configuración"""
        db_configuracion = self.get_configuracion(db, config_id)
        if not db_configuracion:
            return None

        # Verificar si es modificable
        if not db_configuracion.es_modificable():
            raise ValueError("Esta configuración no es modificable")

        update_data = configuracion_update.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_configuracion, field, value)

        # Actualizar timestamp automáticamente
        from datetime import datetime
        db_configuracion.fecha_modificacion = datetime.now()

        db.commit()
        db.refresh(db_configuracion)
        return db_configuracion

    def delete_configuracion(self, db: Session, config_id: int) -> bool:
        """Eliminar configuración"""
        db_configuracion = self.get_configuracion(db, config_id)
        if not db_configuracion:
            return False

        # Verificar si es modificable
        if not db_configuracion.es_modificable():
            raise ValueError("Esta configuración no es modificable")

        db.delete(db_configuracion)
        db.commit()
        return True

    def actualizar_valor_parametro(self, db: Session, parametro: str, nuevo_valor: str, usuario_id: Optional[int] = None) -> Optional[models.ConfiguracionSistema]:
        """Actualizar solo el valor de un parámetro específico"""
        db_configuracion = self.get_configuracion_by_parametro(db, parametro)
        if not db_configuracion:
            return None

        if not db_configuracion.es_modificable():
            raise ValueError(f"El parámetro '{parametro}' no es modificable")

        db_configuracion.valor = nuevo_valor
        if usuario_id:
            db_configuracion.usuario_modificacion = usuario_id

        from datetime import datetime
        db_configuracion.fecha_modificacion = datetime.now()

        db.commit()
        db.refresh(db_configuracion)
        return db_configuracion

# Instancia global
configuracion_sistema_crud = ConfiguracionSistemaCRUD()

# ========================================
# CRUD PARA INVENTARIO CONSOLIDADO
# ========================================

class InventarioConsolidadoCRUD:
    """CRUD operations for VistaInventarioConsolidado (readonly)"""

    def get_inventario_consolidado(self, db: Session, skip: int = 0, limit: int = 100,
                                  filtros: Optional[schemas.InventarioConsolidadoFilters] = None) -> List[models.VistaInventarioConsolidado]:
        """Obtener inventario consolidado con filtros avanzados"""
        query = db.query(models.VistaInventarioConsolidado)

        if filtros:
            # Filtrar por nivel de stock
            if filtros.nivel_stock:
                # Este filtro se aplicará en Python después de la consulta debido a que es una property
                pass

            # Filtrar por necesidad de reposición
            if filtros.necesita_reposicion is not None:
                if filtros.necesita_reposicion:
                    query = query.filter(models.VistaInventarioConsolidado.stock_total < models.VistaInventarioConsolidado.stock_minimo)
                else:
                    query = query.filter(models.VistaInventarioConsolidado.stock_total >= models.VistaInventarioConsolidado.stock_minimo)

            # Filtrar por exceso de stock
            if filtros.exceso_stock is not None:
                if filtros.exceso_stock:
                    query = query.filter(models.VistaInventarioConsolidado.stock_total > models.VistaInventarioConsolidado.stock_maximo)
                else:
                    query = query.filter(models.VistaInventarioConsolidado.stock_total <= models.VistaInventarioConsolidado.stock_maximo)

            # Filtrar por rangos de stock
            if filtros.stock_minimo_desde:
                query = query.filter(models.VistaInventarioConsolidado.stock_minimo >= filtros.stock_minimo_desde)

            if filtros.stock_maximo_hasta:
                query = query.filter(models.VistaInventarioConsolidado.stock_maximo <= filtros.stock_maximo_hasta)

            # Filtrar por valor
            if filtros.valor_minimo:
                query = query.filter(models.VistaInventarioConsolidado.valor_total >= filtros.valor_minimo)

            if filtros.valor_maximo:
                query = query.filter(models.VistaInventarioConsolidado.valor_total <= filtros.valor_maximo)

            # Filtrar por alto valor
            if filtros.es_alto_valor is not None:
                if filtros.es_alto_valor:
                    query = query.filter(models.VistaInventarioConsolidado.valor_total > 10000.0)
                else:
                    query = query.filter(models.VistaInventarioConsolidado.valor_total <= 10000.0)

            # Búsqueda por SKU
            if filtros.buscar_sku:
                query = query.filter(models.VistaInventarioConsolidado.sku.ilike(f"%{filtros.buscar_sku}%"))

            # Búsqueda por nombre
            if filtros.buscar_nombre:
                query = query.filter(models.VistaInventarioConsolidado.nombre_producto.ilike(f"%{filtros.buscar_nombre}%"))

        results = query.offset(skip).limit(limit).all()

        # Aplicar filtros de nivel de stock en Python (ya que son properties)
        if filtros and filtros.nivel_stock:
            results = [r for r in results if r.nivel_stock == filtros.nivel_stock.value]

        return results

    def get_productos_criticos(self, db: Session, limit: int = 100) -> List[models.VistaInventarioConsolidado]:
        """Obtener productos con stock crítico (por debajo del mínimo)"""
        return (db.query(models.VistaInventarioConsolidado)
                .filter(models.VistaInventarioConsolidado.stock_total < models.VistaInventarioConsolidado.stock_minimo)
                .order_by(models.VistaInventarioConsolidado.stock_total.asc())
                .limit(limit)
                .all())

    def get_productos_agotados(self, db: Session, limit: int = 100) -> List[models.VistaInventarioConsolidado]:
        """Obtener productos agotados"""
        return (db.query(models.VistaInventarioConsolidado)
                .filter(models.VistaInventarioConsolidado.stock_total == 0)
                .order_by(models.VistaInventarioConsolidado.valor_total.desc())
                .limit(limit)
                .all())

    def get_productos_exceso(self, db: Session, limit: int = 100) -> List[models.VistaInventarioConsolidado]:
        """Obtener productos con exceso de stock (por encima del máximo)"""
        return (db.query(models.VistaInventarioConsolidado)
                .filter(models.VistaInventarioConsolidado.stock_total > models.VistaInventarioConsolidado.stock_maximo)
                .order_by(models.VistaInventarioConsolidado.stock_total.desc())
                .limit(limit)
                .all())

    def get_productos_alto_valor(self, db: Session, valor_minimo: float = 10000.0, limit: int = 100) -> List[models.VistaInventarioConsolidado]:
        """Obtener productos de alto valor"""
        return (db.query(models.VistaInventarioConsolidado)
                .filter(models.VistaInventarioConsolidado.valor_total > valor_minimo)
                .order_by(models.VistaInventarioConsolidado.valor_total.desc())
                .limit(limit)
                .all())

    def get_producto_by_sku(self, db: Session, sku: str) -> Optional[models.VistaInventarioConsolidado]:
        """Obtener producto específico por SKU"""
        return db.query(models.VistaInventarioConsolidado).filter(models.VistaInventarioConsolidado.sku == sku).first()

    def get_estadisticas_inventario(self, db: Session) -> Dict:
        """Obtener estadísticas generales del inventario"""
        from sqlalchemy import func

        # Consulta base
        total_stats = db.query(
            func.count(models.VistaInventarioConsolidado.id_producto).label('total_productos'),
            func.sum(models.VistaInventarioConsolidado.valor_total).label('total_valor'),
            func.avg(models.VistaInventarioConsolidado.valor_total).label('valor_promedio')
        ).first()

        # Productos críticos
        criticos = db.query(func.count(models.VistaInventarioConsolidado.id_producto)).filter(
            models.VistaInventarioConsolidado.stock_total < models.VistaInventarioConsolidado.stock_minimo
        ).scalar()

        # Productos agotados
        agotados = db.query(func.count(models.VistaInventarioConsolidado.id_producto)).filter(
            models.VistaInventarioConsolidado.stock_total == 0
        ).scalar()

        # Productos con exceso
        exceso = db.query(func.count(models.VistaInventarioConsolidado.id_producto)).filter(
            models.VistaInventarioConsolidado.stock_total > models.VistaInventarioConsolidado.stock_maximo
        ).scalar()

        total_productos = total_stats.total_productos or 0
        productos_normales = total_productos - (criticos + agotados + exceso)

        return {
            'total_productos': total_productos,
            'total_valor_inventario': float(total_stats.total_valor or 0),
            'productos_criticos': criticos,
            'productos_exceso': exceso,
            'productos_agotados': agotados,
            'productos_normales': productos_normales,
            'valor_promedio_por_producto': float(total_stats.valor_promedio or 0),
            'porcentaje_productos_criticos': round((criticos / total_productos * 100), 2) if total_productos > 0 else 0,
            'distribucion_por_nivel': {
                'AGOTADO': agotados,
                'CRITICO': criticos,
                'NORMAL': productos_normales,
                'EXCESO': exceso
            }
        }

    def get_alertas_inventario(self, db: Session) -> List[Dict]:
        """Generar alertas de inventario"""
        alertas = []

        # Productos críticos
        productos_criticos = self.get_productos_criticos(db, limit=50)
        for producto in productos_criticos:
            porcentaje_diff = round(((producto.stock_minimo - producto.stock_total) / producto.stock_minimo * 100), 2) if producto.stock_minimo > 0 else 0
            alertas.append({
                'id_producto': producto.id_producto,
                'sku': producto.sku,
                'nombre_producto': producto.nombre_producto,
                'tipo_alerta': 'CRITICO',
                'nivel_actual': producto.stock_total,
                'nivel_referencia': producto.stock_minimo,
                'porcentaje_diferencia': porcentaje_diff,
                'valor_total': float(producto.valor_total),
                'mensaje': f'Stock crítico: {producto.stock_total} unidades (mínimo: {producto.stock_minimo})'
            })

        # Productos agotados
        productos_agotados = self.get_productos_agotados(db, limit=20)
        for producto in productos_agotados:
            alertas.append({
                'id_producto': producto.id_producto,
                'sku': producto.sku,
                'nombre_producto': producto.nombre_producto,
                'tipo_alerta': 'AGOTADO',
                'nivel_actual': 0,
                'nivel_referencia': producto.stock_minimo,
                'porcentaje_diferencia': 100.0,
                'valor_total': 0.0,
                'mensaje': f'Producto agotado - Reposición urgente requerida'
            })

        return alertas

    def get_recomendaciones_reposicion(self, db: Session) -> List[Dict]:
        """Generar recomendaciones de reposición"""
        productos_criticos = self.get_productos_criticos(db, limit=100)
        recomendaciones = []

        for producto in productos_criticos:
            # Calcular cantidad sugerida (diferencia hasta stock máximo o 1.5 veces el mínimo)
            stock_objetivo = producto.stock_maximo if producto.stock_maximo else int(producto.stock_minimo * 1.5)
            cantidad_sugerida = max(0, stock_objetivo - producto.stock_total)
            costo_estimado = cantidad_sugerida * float(producto.costo_promedio) if producto.costo_promedio else 0

            # Determinar prioridad
            if producto.stock_total == 0:
                prioridad = "ALTA"
                justificacion = "Producto agotado - reposición urgente"
            elif producto.stock_total < (producto.stock_minimo * 0.5):
                prioridad = "ALTA"
                justificacion = "Stock crítico - menos del 50% del mínimo"
            else:
                prioridad = "MEDIA"
                justificacion = "Stock por debajo del mínimo"

            recomendaciones.append({
                'id_producto': producto.id_producto,
                'sku': producto.sku,
                'nombre_producto': producto.nombre_producto,
                'stock_actual': producto.stock_total,
                'stock_minimo': producto.stock_minimo,
                'stock_recomendado': stock_objetivo,
                'cantidad_sugerida': cantidad_sugerida,
                'costo_estimado': costo_estimado,
                'prioridad': prioridad,
                'justificacion': justificacion
            })

        # Ordenar por prioridad y valor
        recomendaciones.sort(key=lambda x: (x['prioridad'] == 'ALTA', x['costo_estimado']), reverse=True)
        return recomendaciones

    def get_inventario_por_rango_valor(self, db: Session, valor_min: float, valor_max: float) -> List[models.VistaInventarioConsolidado]:
        """Obtener inventario por rango de valor"""
        return (db.query(models.VistaInventarioConsolidado)
                .filter(
                    models.VistaInventarioConsolidado.valor_total >= valor_min,
                    models.VistaInventarioConsolidado.valor_total <= valor_max
                )
                .order_by(models.VistaInventarioConsolidado.valor_total.desc())
                .all())

    def buscar_productos(self, db: Session, termino_busqueda: str, limit: int = 50) -> List[models.VistaInventarioConsolidado]:
        """Buscar productos por SKU o nombre"""
        return (db.query(models.VistaInventarioConsolidado)
                .filter(
                    db.or_(
                        models.VistaInventarioConsolidado.sku.ilike(f"%{termino_busqueda}%"),
                        models.VistaInventarioConsolidado.nombre_producto.ilike(f"%{termino_busqueda}%")
                    )
                )
                .order_by(models.VistaInventarioConsolidado.valor_total.desc())
                .limit(limit)
                .all())

# Instancia global
inventario_consolidado_crud = InventarioConsolidadoCRUD()

# ========================================
# CRUD PARA OBRAS INVENTARIO
# ========================================

class ObrasInventarioCRUD:
    """CRUD operations for VistaObrasInventario (readonly)"""

    def get_obras_inventario(self, db: Session, skip: int = 0, limit: int = 100,
                            filtros: Optional[schemas.ObrasInventarioFilters] = None) -> List[models.VistaObrasInventario]:
        """Obtener obras con inventario con filtros avanzados"""
        query = db.query(models.VistaObrasInventario)

        if filtros:
            # Filtrar por estado
            if filtros.estado:
                query = query.filter(models.VistaObrasInventario.estado == filtros.estado.value)

            # Filtrar por inventario
            if filtros.tiene_inventario is not None:
                if filtros.tiene_inventario:
                    query = query.filter(models.VistaObrasInventario.productos_diferentes > 0)
                else:
                    query = query.filter(
                        db.or_(
                            models.VistaObrasInventario.productos_diferentes == 0,
                            models.VistaObrasInventario.productos_diferentes.is_(None)
                        )
                    )

            # Filtrar por retraso
            if filtros.esta_retrasada is not None:
                from datetime import date
                today = date.today()
                if filtros.esta_retrasada:
                    query = query.filter(
                        db.and_(
                            models.VistaObrasInventario.fecha_fin_programada < today,
                            models.VistaObrasInventario.estado.in_(['EN_EJECUCION', 'SUSPENDIDA'])
                        )
                    )

            # Filtrar por valor
            if filtros.valor_minimo:
                query = query.filter(models.VistaObrasInventario.valor_total_inventario >= filtros.valor_minimo)

            if filtros.valor_maximo:
                query = query.filter(models.VistaObrasInventario.valor_total_inventario <= filtros.valor_maximo)

            # Filtrar por número de productos
            if filtros.productos_minimos:
                query = query.filter(models.VistaObrasInventario.productos_diferentes >= filtros.productos_minimos)

            if filtros.productos_maximos:
                query = query.filter(models.VistaObrasInventario.productos_diferentes <= filtros.productos_maximos)

            # Búsquedas por texto
            if filtros.buscar_codigo:
                query = query.filter(models.VistaObrasInventario.codigo_obra.ilike(f"%{filtros.buscar_codigo}%"))

            if filtros.buscar_nombre:
                query = query.filter(models.VistaObrasInventario.nombre_obra.ilike(f"%{filtros.buscar_nombre}%"))

            if filtros.buscar_cliente:
                query = query.filter(models.VistaObrasInventario.nombre_cliente.ilike(f"%{filtros.buscar_cliente}%"))

        results = query.offset(skip).limit(limit).all()

        # Aplicar filtros que requieren properties en Python
        if filtros:
            if filtros.estado_categoria:
                results = [r for r in results if r.estado_obra_categoria == filtros.estado_categoria.value]

            if filtros.densidad_inventario:
                results = [r for r in results if r.densidad_inventario == filtros.densidad_inventario.value]

            if filtros.categoria_valor:
                results = [r for r in results if r.categoria_valor == filtros.categoria_valor.value]

            if filtros.urgencia_finalizacion:
                results = [r for r in results if r.urgencia_finalizacion == filtros.urgencia_finalizacion.value]

            if filtros.requiere_atencion is not None:
                results = [r for r in results if r.requiere_atencion == filtros.requiere_atencion]

        return results

    def get_obras_activas(self, db: Session, limit: int = 100) -> List[models.VistaObrasInventario]:
        """Obtener obras actualmente en ejecución"""
        return (db.query(models.VistaObrasInventario)
                .filter(models.VistaObrasInventario.estado == 'EN_EJECUCION')
                .order_by(models.VistaObrasInventario.valor_total_inventario.desc())
                .limit(limit)
                .all())

    def get_obras_retrasadas(self, db: Session, limit: int = 100) -> List[models.VistaObrasInventario]:
        """Obtener obras retrasadas"""
        from datetime import date
        today = date.today()

        return (db.query(models.VistaObrasInventario)
                .filter(
                    models.VistaObrasInventario.fecha_fin_programada < today,
                    models.VistaObrasInventario.estado.in_(['EN_EJECUCION', 'SUSPENDIDA'])
                )
                .order_by(models.VistaObrasInventario.fecha_fin_programada.asc())
                .limit(limit)
                .all())

    def get_obras_urgentes(self, db: Session, dias_limite: int = 7, limit: int = 100) -> List[models.VistaObrasInventario]:
        """Obtener obras que vencen pronto"""
        from datetime import date, timedelta
        fecha_limite = date.today() + timedelta(days=dias_limite)

        return (db.query(models.VistaObrasInventario)
                .filter(
                    models.VistaObrasInventario.fecha_fin_programada <= fecha_limite,
                    models.VistaObrasInventario.fecha_fin_programada >= date.today(),
                    models.VistaObrasInventario.estado == 'EN_EJECUCION'
                )
                .order_by(models.VistaObrasInventario.fecha_fin_programada.asc())
                .limit(limit)
                .all())

    def get_obras_alto_valor(self, db: Session, valor_minimo: float = 100000.0, limit: int = 100) -> List[models.VistaObrasInventario]:
        """Obtener obras de alto valor en inventario"""
        return (db.query(models.VistaObrasInventario)
                .filter(models.VistaObrasInventario.valor_total_inventario >= valor_minimo)
                .order_by(models.VistaObrasInventario.valor_total_inventario.desc())
                .limit(limit)
                .all())

    def get_obras_suspendidas_con_inventario(self, db: Session, limit: int = 100) -> List[models.VistaObrasInventario]:
        """Obtener obras suspendidas que tienen inventario"""
        return (db.query(models.VistaObrasInventario)
                .filter(
                    models.VistaObrasInventario.estado == 'SUSPENDIDA',
                    models.VistaObrasInventario.productos_diferentes > 0
                )
                .order_by(models.VistaObrasInventario.valor_total_inventario.desc())
                .limit(limit)
                .all())

    def get_obra_by_codigo(self, db: Session, codigo_obra: str) -> Optional[models.VistaObrasInventario]:
        """Obtener obra específica por código"""
        return db.query(models.VistaObrasInventario).filter(models.VistaObrasInventario.codigo_obra == codigo_obra).first()

    def get_estadisticas_obras(self, db: Session) -> Dict:
        """Obtener estadísticas generales de obras"""
        from sqlalchemy import func

        # Estadísticas básicas
        total_stats = db.query(
            func.count(models.VistaObrasInventario.id_obra).label('total_obras'),
            func.sum(models.VistaObrasInventario.valor_total_inventario).label('valor_total'),
            func.avg(models.VistaObrasInventario.valor_total_inventario).label('valor_promedio'),
            func.avg(models.VistaObrasInventario.productos_diferentes).label('productos_promedio')
        ).first()

        # Obras por estado
        obras_activas = db.query(func.count(models.VistaObrasInventario.id_obra)).filter(
            models.VistaObrasInventario.estado == 'EN_EJECUCION'
        ).scalar()

        obras_suspendidas = db.query(func.count(models.VistaObrasInventario.id_obra)).filter(
            models.VistaObrasInventario.estado == 'SUSPENDIDA'
        ).scalar()

        obras_finalizadas = db.query(func.count(models.VistaObrasInventario.id_obra)).filter(
            models.VistaObrasInventario.estado == 'FINALIZADA'
        ).scalar()

        # Obras con/sin inventario
        obras_con_inventario = db.query(func.count(models.VistaObrasInventario.id_obra)).filter(
            models.VistaObrasInventario.productos_diferentes > 0
        ).scalar()

        # Obras retrasadas
        from datetime import date
        today = date.today()
        obras_retrasadas = db.query(func.count(models.VistaObrasInventario.id_obra)).filter(
            models.VistaObrasInventario.fecha_fin_programada < today,
            models.VistaObrasInventario.estado.in_(['EN_EJECUCION', 'SUSPENDIDA'])
        ).scalar()

        total_obras = total_stats.total_obras or 0
        obras_sin_inventario = total_obras - (obras_con_inventario or 0)

        # Distribución por estado
        distribucion_estado = {
            'EN_EJECUCION': obras_activas or 0,
            'SUSPENDIDA': obras_suspendidas or 0,
            'FINALIZADA': obras_finalizadas or 0,
            'OTROS': total_obras - (obras_activas or 0) - (obras_suspendidas or 0) - (obras_finalizadas or 0)
        }

        return {
            'total_obras': total_obras,
            'obras_activas': obras_activas or 0,
            'obras_suspendidas': obras_suspendidas or 0,
            'obras_finalizadas': obras_finalizadas or 0,
            'obras_con_inventario': obras_con_inventario or 0,
            'obras_sin_inventario': obras_sin_inventario,
            'obras_retrasadas': obras_retrasadas or 0,
            'obras_requieren_atencion': 0,  # Se calculará después
            'valor_total_inventario_obras': float(total_stats.valor_total or 0),
            'valor_promedio_por_obra': float(total_stats.valor_promedio or 0),
            'productos_promedio_por_obra': float(total_stats.productos_promedio or 0),
            'distribucion_por_estado': distribucion_estado,
            'distribucion_por_categoria_valor': {}  # Se calculará después
        }

    def get_alertas_obras(self, db: Session) -> List[Dict]:
        """Generar alertas de obras"""
        alertas = []

        # Obras retrasadas
        obras_retrasadas = self.get_obras_retrasadas(db, limit=20)
        for obra in obras_retrasadas:
            dias_retraso = obra.dias_restantes if obra.dias_restantes is not None else 0
            dias_retraso = abs(dias_retraso)

            alertas.append({
                'id_obra': obra.id_obra,
                'codigo_obra': obra.codigo_obra,
                'nombre_obra': obra.nombre_obra,
                'nombre_cliente': obra.nombre_cliente,
                'tipo_alerta': 'RETRASADA',
                'nivel_criticidad': 'ALTA' if dias_retraso > 30 else 'MEDIA',
                'descripcion': f'Obra retrasada por {dias_retraso} días',
                'valor_inventario': float(obra.valor_total_inventario) if obra.valor_total_inventario else 0,
                'dias_retraso': dias_retraso,
                'fecha_limite': obra.fecha_fin_programada,
                'acciones_recomendadas': ['Revisar cronograma', 'Evaluar recursos', 'Contactar cliente']
            })

        # Obras urgentes
        obras_urgentes = self.get_obras_urgentes(db, limit=10)
        for obra in obras_urgentes:
            alertas.append({
                'id_obra': obra.id_obra,
                'codigo_obra': obra.codigo_obra,
                'nombre_obra': obra.nombre_obra,
                'nombre_cliente': obra.nombre_cliente,
                'tipo_alerta': 'URGENTE',
                'nivel_criticidad': 'ALTA',
                'descripcion': f'Obra vence en {obra.dias_restantes} días',
                'valor_inventario': float(obra.valor_total_inventario) if obra.valor_total_inventario else 0,
                'dias_retraso': None,
                'fecha_limite': obra.fecha_fin_programada,
                'acciones_recomendadas': ['Acelerar ejecución', 'Revisar inventario', 'Planificar devoluciones']
            })

        # Obras suspendidas con alto valor
        obras_suspendidas = self.get_obras_suspendidas_con_inventario(db, limit=10)
        for obra in obras_suspendidas:
            if obra.categoria_valor == "ALTO_VALOR":
                alertas.append({
                    'id_obra': obra.id_obra,
                    'codigo_obra': obra.codigo_obra,
                    'nombre_obra': obra.nombre_obra,
                    'nombre_cliente': obra.nombre_cliente,
                    'tipo_alerta': 'ALTO_VALOR_SUSPENDIDA',
                    'nivel_criticidad': 'ALTA',
                    'descripcion': f'Obra suspendida con inventario de alto valor: ${obra.valor_total_inventario:,.2f}',
                    'valor_inventario': float(obra.valor_total_inventario),
                    'dias_retraso': None,
                    'fecha_limite': None,
                    'acciones_recomendadas': ['Revisar causa suspensión', 'Evaluar traslado inventario', 'Renegociar contrato']
                })

        return alertas

    def get_ranking_obras_valor(self, db: Session, limit: int = 20) -> List[Dict]:
        """Obtener ranking de obras por valor de inventario"""
        obras = (db.query(models.VistaObrasInventario)
                .filter(models.VistaObrasInventario.valor_total_inventario > 0)
                .order_by(models.VistaObrasInventario.valor_total_inventario.desc())
                .limit(limit)
                .all())

        # Calcular valor total para porcentajes
        valor_total_general = sum(float(obra.valor_total_inventario) for obra in obras if obra.valor_total_inventario)

        ranking = []
        for i, obra in enumerate(obras, 1):
            valor_obra = float(obra.valor_total_inventario) if obra.valor_total_inventario else 0
            porcentaje = (valor_obra / valor_total_general * 100) if valor_total_general > 0 else 0

            ranking.append({
                'posicion': i,
                'id_obra': obra.id_obra,
                'codigo_obra': obra.codigo_obra,
                'nombre_obra': obra.nombre_obra,
                'nombre_cliente': obra.nombre_cliente,
                'valor_total_inventario': valor_obra,
                'productos_diferentes': obra.productos_diferentes or 0,
                'categoria_valor': obra.categoria_valor,
                'porcentaje_del_total': round(porcentaje, 2)
            })

        return ranking

    def get_recomendaciones_obras(self, db: Session) -> List[Dict]:
        """Generar recomendaciones para obras"""
        recomendaciones = []

        # Obtener todas las obras que requieren atención
        obras = self.get_obras_inventario(db, skip=0, limit=1000)

        for obra in obras:
            if obra.requiere_atencion:
                riesgos = obra.indicadores_riesgo

                if "OBRA_RETRASADA" in riesgos:
                    recomendaciones.append({
                        'id_obra': obra.id_obra,
                        'codigo_obra': obra.codigo_obra,
                        'nombre_obra': obra.nombre_obra,
                        'tipo_recomendacion': 'ACELERAR_PROYECTO',
                        'prioridad': 'ALTA',
                        'descripcion': 'Obra con retraso significativo requiere aceleración',
                        'acciones_sugeridas': [
                            'Revisar cronograma y recursos',
                            'Aumentar personal si es necesario',
                            'Replantear alcance con cliente'
                        ],
                        'impacto_estimado': 'Reducción de días de retraso',
                        'plazo_recomendado': 'Inmediato'
                    })

                if "ALTO_VALOR_SUSPENDIDA" in riesgos:
                    recomendaciones.append({
                        'id_obra': obra.id_obra,
                        'codigo_obra': obra.codigo_obra,
                        'nombre_obra': obra.nombre_obra,
                        'tipo_recomendacion': 'REVISAR_INVENTARIO',
                        'prioridad': 'ALTA',
                        'descripcion': 'Obra suspendida con inventario de alto valor',
                        'acciones_sugeridas': [
                            'Evaluar traslado de inventario a otras obras',
                            'Renegociar términos del contrato',
                            'Considerar liquidación parcial'
                        ],
                        'impacto_estimado': 'Optimización de recursos',
                        'plazo_recomendado': '7 días'
                    })

        return recomendaciones

    def buscar_obras(self, db: Session, termino_busqueda: str, limit: int = 50) -> List[models.VistaObrasInventario]:
        """Buscar obras por código, nombre o cliente"""
        return (db.query(models.VistaObrasInventario)
                .filter(
                    db.or_(
                        models.VistaObrasInventario.codigo_obra.ilike(f"%{termino_busqueda}%"),
                        models.VistaObrasInventario.nombre_obra.ilike(f"%{termino_busqueda}%"),
                        models.VistaObrasInventario.nombre_cliente.ilike(f"%{termino_busqueda}%")
                    )
                )
                .order_by(models.VistaObrasInventario.valor_total_inventario.desc())
                .limit(limit)
                .all())

# Instancia global
obras_inventario_crud = ObrasInventarioCRUD()


# ========================================
# CRUD PARA DEVOLUCIONES PENDIENTES
# ========================================

class DevolucionesPendientesCRUD:
    """CRUD para manejo de devoluciones pendientes"""

    def __init__(self, db: Session = None):
        self.db = db
        self.model = models.VistaDevolucionesPendientes

    def get(self, id: int) -> Optional[models.VistaDevolucionesPendientes]:
        """Obtener devolución pendiente por ID"""
        return self.db.query(self.model).filter(self.model.id_despacho == id).first()

    def get_multi_filtered(
        self,
        filtro: Optional[schemas.VistaDevolucionesPendientesFilter] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.VistaDevolucionesPendientes]:
        """Obtener devoluciones pendientes con filtros"""
        query = self.db.query(models.VistaDevolucionesPendientes)

        if filtro:
            if filtro.id_despacho:
                query = query.filter(models.VistaDevolucionesPendientes.id_despacho == filtro.id_despacho)

            if filtro.numero_despacho:
                query = query.filter(
                    models.VistaDevolucionesPendientes.numero_despacho.ilike(f"%{filtro.numero_despacho}%")
                )

            if filtro.codigo_obra:
                query = query.filter(
                    models.VistaDevolucionesPendientes.codigo_obra.ilike(f"%{filtro.codigo_obra}%")
                )

            if filtro.fecha_despacho_desde:
                query = query.filter(
                    models.VistaDevolucionesPendientes.fecha_despacho >= filtro.fecha_despacho_desde
                )

            if filtro.fecha_despacho_hasta:
                query = query.filter(
                    models.VistaDevolucionesPendientes.fecha_despacho <= filtro.fecha_despacho_hasta
                )

            if filtro.fecha_limite_desde:
                query = query.filter(
                    models.VistaDevolucionesPendientes.fecha_limite_devolucion >= filtro.fecha_limite_desde
                )

            if filtro.fecha_limite_hasta:
                query = query.filter(
                    models.VistaDevolucionesPendientes.fecha_limite_devolucion <= filtro.fecha_limite_hasta
                )

            if filtro.dias_para_limite_min is not None:
                query = query.filter(
                    models.VistaDevolucionesPendientes.dias_para_limite >= filtro.dias_para_limite_min
                )

            if filtro.dias_para_limite_max is not None:
                query = query.filter(
                    models.VistaDevolucionesPendientes.dias_para_limite <= filtro.dias_para_limite_max
                )

            if filtro.valor_pendiente_min:
                query = query.filter(
                    models.VistaDevolucionesPendientes.valor_pendiente >= filtro.valor_pendiente_min
                )

            if filtro.valor_pendiente_max:
                query = query.filter(
                    models.VistaDevolucionesPendientes.valor_pendiente <= filtro.valor_pendiente_max
                )

            if filtro.productos_min:
                query = query.filter(
                    models.VistaDevolucionesPendientes.productos_diferentes >= filtro.productos_min
                )

            if filtro.productos_max:
                query = query.filter(
                    models.VistaDevolucionesPendientes.productos_diferentes <= filtro.productos_max
                )

            if filtro.solo_vencidas:
                from datetime import date
                query = query.filter(
                    or_(
                        models.VistaDevolucionesPendientes.fecha_limite_devolucion < date.today(),
                        models.VistaDevolucionesPendientes.dias_para_limite <= 0
                    )
                )

            if filtro.solo_urgentes:
                query = query.filter(
                    models.VistaDevolucionesPendientes.dias_para_limite <= 7
                )

        return query.offset(skip).limit(limit).all()

    def get_devoluciones_vencidas(self, skip: int = 0, limit: int = 100) -> List[models.VistaDevolucionesPendientes]:
        """Obtener devoluciones vencidas"""
        from datetime import date
        return (self.db.query(models.VistaDevolucionesPendientes)
                .filter(
                    or_(
                        models.VistaDevolucionesPendientes.fecha_limite_devolucion < date.today(),
                        models.VistaDevolucionesPendientes.dias_para_limite <= 0
                    )
                )
                .order_by(models.VistaDevolucionesPendientes.valor_pendiente.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_devoluciones_urgentes(self, skip: int = 0, limit: int = 100) -> List[models.VistaDevolucionesPendientes]:
        """Obtener devoluciones urgentes (vencen en 7 días o menos)"""
        return (self.db.query(models.VistaDevolucionesPendientes)
                .filter(
                    and_(
                        models.VistaDevolucionesPendientes.dias_para_limite <= 7,
                        models.VistaDevolucionesPendientes.dias_para_limite > 0
                    )
                )
                .order_by(models.VistaDevolucionesPendientes.dias_para_limite.asc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_devoluciones_alto_valor(
        self,
        valor_minimo: float = 50000.0,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.VistaDevolucionesPendientes]:
        """Obtener devoluciones de alto valor"""
        return (self.db.query(models.VistaDevolucionesPendientes)
                .filter(models.VistaDevolucionesPendientes.valor_pendiente >= valor_minimo)
                .order_by(models.VistaDevolucionesPendientes.valor_pendiente.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_devoluciones_atencion_inmediata(self, skip: int = 0, limit: int = 100) -> List[models.VistaDevolucionesPendientes]:
        """Obtener devoluciones que requieren atención inmediata"""
        from datetime import date
        return (self.db.query(models.VistaDevolucionesPendientes)
                .filter(
                    or_(
                        models.VistaDevolucionesPendientes.fecha_limite_devolucion < date.today(),
                        models.VistaDevolucionesPendientes.dias_para_limite <= 3,
                        models.VistaDevolucionesPendientes.valor_pendiente >= 50000
                    )
                )
                .order_by(models.VistaDevolucionesPendientes.valor_pendiente.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_estadisticas_generales(self) -> Dict[str, Any]:
        """Obtener estadísticas generales de devoluciones pendientes"""
        from datetime import date

        total_query = self.db.query(models.VistaDevolucionesPendientes)
        total_devoluciones = total_query.count()

        if total_devoluciones == 0:
            return {
                "total_devoluciones": 0,
                "total_valor_pendiente": 0,
                "total_productos_pendientes": 0,
                "total_cantidad_pendiente": 0,
                "devoluciones_vencidas": 0,
                "devoluciones_urgentes": 0,
                "devoluciones_en_plazo": 0,
                "valor_promedio_devolucion": 0,
                "productos_promedio_devolucion": 0,
                "porcentaje_vencidas": 0,
                "porcentaje_urgentes": 0
            }

        # Estadísticas básicas
        stats = (self.db.query(
            func.sum(models.VistaDevolucionesPendientes.valor_pendiente).label('total_valor'),
            func.sum(models.VistaDevolucionesPendientes.productos_diferentes).label('total_productos'),
            func.sum(models.VistaDevolucionesPendientes.cantidad_pendiente_devolucion).label('total_cantidad'),
            func.avg(models.VistaDevolucionesPendientes.valor_pendiente).label('valor_promedio'),
            func.avg(models.VistaDevolucionesPendientes.productos_diferentes).label('productos_promedio')
        ).first())

        # Contar por estados
        vencidas = total_query.filter(
            or_(
                models.VistaDevolucionesPendientes.fecha_limite_devolucion < date.today(),
                models.VistaDevolucionesPendientes.dias_para_limite <= 0
            )
        ).count()

        urgentes = total_query.filter(
            and_(
                models.VistaDevolucionesPendientes.dias_para_limite <= 7,
                models.VistaDevolucionesPendientes.dias_para_limite > 0
            )
        ).count()

        en_plazo = total_devoluciones - vencidas - urgentes

        return {
            "total_devoluciones": total_devoluciones,
            "total_valor_pendiente": float(stats.total_valor or 0),
            "total_productos_pendientes": int(stats.total_productos or 0),
            "total_cantidad_pendiente": float(stats.total_cantidad or 0),
            "devoluciones_vencidas": vencidas,
            "devoluciones_urgentes": urgentes,
            "devoluciones_en_plazo": en_plazo,
            "valor_promedio_devolucion": float(stats.valor_promedio or 0),
            "productos_promedio_devolucion": float(stats.productos_promedio or 0),
            "porcentaje_vencidas": round((vencidas / total_devoluciones) * 100, 2),
            "porcentaje_urgentes": round((urgentes / total_devoluciones) * 100, 2)
        }

    def get_estadisticas_por_estado(self) -> Dict[str, Any]:
        """Obtener estadísticas agrupadas por estado de devolución"""
        from datetime import date

        query = self.db.query(models.VistaDevolucionesPendientes)

        # Clasificar por estados
        vencidas = query.filter(
            or_(
                models.VistaDevolucionesPendientes.fecha_limite_devolucion < date.today(),
                models.VistaDevolucionesPendientes.dias_para_limite <= 0
            )
        )

        urgentes = query.filter(
            and_(
                models.VistaDevolucionesPendientes.dias_para_limite <= 7,
                models.VistaDevolucionesPendientes.dias_para_limite > 0
            )
        )

        proximo_vencimiento = query.filter(
            and_(
                models.VistaDevolucionesPendientes.dias_para_limite <= 15,
                models.VistaDevolucionesPendientes.dias_para_limite > 7
            )
        )

        en_plazo = query.filter(models.VistaDevolucionesPendientes.dias_para_limite > 15)

        def get_stats_grupo(grupo_query):
            stats = grupo_query.with_entities(
                func.count().label('cantidad'),
                func.sum(models.VistaDevolucionesPendientes.valor_pendiente).label('valor_total'),
                func.avg(models.VistaDevolucionesPendientes.valor_pendiente).label('valor_promedio')
            ).first()

            return {
                "cantidad": stats.cantidad or 0,
                "valor_total": float(stats.valor_total or 0),
                "valor_promedio": float(stats.valor_promedio or 0)
            }

        return {
            "vencidas": get_stats_grupo(vencidas),
            "urgentes": get_stats_grupo(urgentes),
            "proximo_vencimiento": get_stats_grupo(proximo_vencimiento),
            "en_plazo": get_stats_grupo(en_plazo)
        }

    def get_ranking_por_valor(self, top: int = 10) -> List[Dict[str, Any]]:
        """Obtener ranking de devoluciones por valor pendiente"""
        devoluciones = (self.db.query(models.VistaDevolucionesPendientes)
                       .order_by(models.VistaDevolucionesPendientes.valor_pendiente.desc())
                       .limit(top)
                       .all())

        total_valor = (self.db.query(func.sum(models.VistaDevolucionesPendientes.valor_pendiente))
                      .scalar() or 0)

        ranking = []
        for i, dev in enumerate(devoluciones, 1):
            categoria_valor = dev.categoria_valor
            porcentaje = (float(dev.valor_pendiente) / float(total_valor)) * 100 if total_valor > 0 else 0

            ranking.append({
                "posicion": i,
                "id_despacho": dev.id_despacho,
                "numero_despacho": dev.numero_despacho,
                "codigo_obra": dev.codigo_obra,
                "nombre_obra": dev.nombre_obra,
                "valor_pendiente": float(dev.valor_pendiente),
                "productos_diferentes": dev.productos_diferentes,
                "dias_para_limite": dev.dias_para_limite,
                "categoria_valor": categoria_valor,
                "porcentaje_del_total": round(porcentaje, 2)
            })

        return ranking

    def get_alertas(self, tipo_alerta: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener alertas de devoluciones pendientes"""
        devoluciones = self.db.query(models.VistaDevolucionesPendientes).all()
        alertas = []

        for dev in devoluciones:
            alerta_tipo = dev.alerta_generada
            if tipo_alerta and alerta_tipo != tipo_alerta:
                continue

            alertas.append({
                "id_despacho": dev.id_despacho,
                "numero_despacho": dev.numero_despacho,
                "codigo_obra": dev.codigo_obra,
                "nombre_obra": dev.nombre_obra,
                "tipo_alerta": alerta_tipo,
                "nivel_criticidad": dev.nivel_criticidad,
                "descripcion": self._generar_descripcion_alerta(dev),
                "valor_pendiente": float(dev.valor_pendiente),
                "dias_para_limite": dev.dias_para_limite,
                "fecha_limite": dev.fecha_limite_devolucion,
                "acciones_recomendadas": dev.acciones_recomendadas,
                "fecha_generacion": datetime.now()
            })

        return sorted(alertas, key=lambda x: self._get_prioridad_alerta(x["tipo_alerta"]), reverse=True)

    def _generar_descripcion_alerta(self, devolucion: models.VistaDevolucionesPendientes) -> str:
        """Generar descripción de alerta"""
        if devolucion.esta_vencida:
            dias_vencida = abs(devolucion.dias_para_limite) if devolucion.dias_para_limite else "varios"
            return f"Devolución vencida hace {dias_vencida} días con valor pendiente de ${devolucion.valor_pendiente:,.2f}"
        elif devolucion.dias_para_limite and devolucion.dias_para_limite <= 3:
            return f"Devolución urgente: vence en {devolucion.dias_para_limite} días con valor de ${devolucion.valor_pendiente:,.2f}"
        elif float(devolucion.valor_pendiente or 0) > 50000:
            return f"Alto valor pendiente de devolución: ${devolucion.valor_pendiente:,.2f}"
        else:
            return f"Seguimiento normal de devolución con {devolucion.productos_diferentes} productos pendientes"

    def _get_prioridad_alerta(self, tipo: str) -> int:
        """Obtener prioridad numérica de alerta"""
        prioridades = {
            "DEVOLUCION_VENCIDA": 5,
            "DEVOLUCION_URGENTE": 4,
            "ALTO_VALOR_PENDIENTE": 3,
            "MUCHOS_PRODUCTOS_PENDIENTES": 2,
            "SEGUIMIENTO_NORMAL": 1
        }
        return prioridades.get(tipo, 0)

    def get_recomendaciones(self, limite: int = 10) -> List[Dict[str, Any]]:
        """Obtener recomendaciones para devoluciones pendientes"""
        devoluciones = (self.db.query(models.VistaDevolucionesPendientes)
                       .filter(
                           or_(
                               models.VistaDevolucionesPendientes.dias_para_limite <= 7,
                               models.VistaDevolucionesPendientes.valor_pendiente >= 30000
                           )
                       )
                       .order_by(models.VistaDevolucionesPendientes.valor_pendiente.desc())
                       .limit(limite)
                       .all())

        recomendaciones = []
        for dev in devoluciones:
            tipo_rec = self._determinar_tipo_recomendacion(dev)

            recomendaciones.append({
                "id_despacho": dev.id_despacho,
                "numero_despacho": dev.numero_despacho,
                "codigo_obra": dev.codigo_obra,
                "tipo_recomendacion": tipo_rec,
                "prioridad": dev.nivel_criticidad,
                "descripcion": self._generar_descripcion_recomendacion(dev, tipo_rec),
                "acciones_sugeridas": dev.acciones_recomendadas,
                "impacto_estimado": self._calcular_impacto_estimado(dev),
                "plazo_recomendado": self._calcular_plazo_recomendado(dev)
            })

        return recomendaciones

    def _determinar_tipo_recomendacion(self, devolucion: models.VistaDevolucionesPendientes) -> str:
        """Determinar tipo de recomendación"""
        if devolucion.esta_vencida:
            return "CONTACTAR_CLIENTE_URGENTE"
        elif devolucion.dias_para_limite and devolucion.dias_para_limite <= 3:
            return "VISITA_SEGUIMIENTO"
        elif float(devolucion.valor_pendiente or 0) > 50000:
            return "ESCALAR_GERENCIA"
        else:
            return "RECORDATORIO_CLIENTE"

    def _generar_descripcion_recomendacion(self, devolucion: models.VistaDevolucionesPendientes, tipo: str) -> str:
        """Generar descripción de recomendación"""
        descripciones = {
            "CONTACTAR_CLIENTE_URGENTE": f"Contacto inmediato requerido para devolución vencida de ${devolucion.valor_pendiente:,.2f}",
            "VISITA_SEGUIMIENTO": f"Programar visita de seguimiento para devolución que vence en {devolucion.dias_para_limite} días",
            "ESCALAR_GERENCIA": f"Escalar a gerencia por alto valor pendiente de ${devolucion.valor_pendiente:,.2f}",
            "RECORDATORIO_CLIENTE": f"Enviar recordatorio al cliente sobre {devolucion.productos_diferentes} productos pendientes"
        }
        return descripciones.get(tipo, "Seguimiento general requerido")

    def _calcular_impacto_estimado(self, devolucion: models.VistaDevolucionesPendientes) -> str:
        """Calcular impacto estimado"""
        valor = float(devolucion.valor_pendiente or 0)
        if valor > 100000:
            return "ALTO"
        elif valor > 30000:
            return "MEDIO"
        else:
            return "BAJO"

    def _calcular_plazo_recomendado(self, devolucion: models.VistaDevolucionesPendientes) -> str:
        """Calcular plazo recomendado para acción"""
        if devolucion.esta_vencida:
            return "INMEDIATO"
        elif devolucion.dias_para_limite and devolucion.dias_para_limite <= 3:
            return "1-2 DIAS"
        elif devolucion.dias_para_limite and devolucion.dias_para_limite <= 7:
            return "3-5 DIAS"
        else:
            return "1 SEMANA"

    def get_dashboard_kpis(self) -> Dict[str, Any]:
        """Obtener KPIs principales para dashboard"""
        stats_generales = self.get_estadisticas_generales()
        vencidas = self.get_devoluciones_vencidas(limit=5)
        urgentes = self.get_devoluciones_urgentes(limit=5)
        alto_valor = self.get_devoluciones_alto_valor(limit=5)

        return {
            "resumen_general": stats_generales,
            "devoluciones_criticas": len([d for d in vencidas if d.requiere_atencion_inmediata]),
            "total_valor_riesgo": sum([float(d.valor_pendiente) for d in vencidas + urgentes]),
            "promedio_dias_vencimiento": self._calcular_promedio_dias_vencimiento(),
            "top_devoluciones_valor": [
                {
                    "id_despacho": d.id_despacho,
                    "numero_despacho": d.numero_despacho,
                    "codigo_obra": d.codigo_obra,
                    "valor_pendiente": float(d.valor_pendiente),
                    "estado": d.estado_devolucion
                } for d in alto_valor
            ]
        }

    def _calcular_promedio_dias_vencimiento(self) -> float:
        """Calcular promedio de días para vencimiento"""
        promedio = (self.db.query(func.avg(models.VistaDevolucionesPendientes.dias_para_limite))
                   .filter(models.VistaDevolucionesPendientes.dias_para_limite.isnot(None))
                   .scalar())
        return round(float(promedio or 0), 2)

    def buscar_por_texto(self, texto: str, skip: int = 0, limit: int = 50) -> List[models.VistaDevolucionesPendientes]:
        """Buscar devoluciones por texto"""
        termino_busqueda = texto.strip()
        return (self.db.query(models.VistaDevolucionesPendientes)
                .filter(
                    or_(
                        models.VistaDevolucionesPendientes.numero_despacho.ilike(f"%{termino_busqueda}%"),
                        models.VistaDevolucionesPendientes.codigo_obra.ilike(f"%{termino_busqueda}%"),
                        models.VistaDevolucionesPendientes.nombre_obra.ilike(f"%{termino_busqueda}%")
                    )
                )
                .order_by(models.VistaDevolucionesPendientes.valor_pendiente.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def contar_con_filtros(self, filtro: Optional[schemas.VistaDevolucionesPendientesFilter] = None) -> int:
        """Contar devoluciones con filtros aplicados"""
        query = self.db.query(models.VistaDevolucionesPendientes)

        if filtro:
            # Aplicar los mismos filtros que en get_multi_filtered
            if filtro.id_despacho:
                query = query.filter(models.VistaDevolucionesPendientes.id_despacho == filtro.id_despacho)
            # ... (resto de filtros igual que en get_multi_filtered)

        return query.count()

# Instancia global
devoluciones_pendientes_crud = DevolucionesPendientesCRUD()


# ========================================
# CRUD PARA PRODUCTOS ABC
# ========================================

class ProductosABCCRUD:
    """CRUD para manejo de análisis ABC de productos"""

    def __init__(self, db: Session = None):
        self.db = db
        self.model = models.VistaProductosABC

    def get(self, id: int) -> Optional[models.VistaProductosABC]:
        """Obtener producto ABC por ID"""
        return self.db.query(self.model).filter(self.model.id_producto == id).first()

    def get_multi_filtered(
        self,
        filtro: Optional[schemas.VistaProductosABCFilter] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.VistaProductosABC]:
        """Obtener productos ABC con filtros"""
        query = self.db.query(models.VistaProductosABC)

        if filtro:
            if filtro.id_producto:
                query = query.filter(models.VistaProductosABC.id_producto == filtro.id_producto)

            if filtro.sku:
                query = query.filter(models.VistaProductosABC.sku.ilike(f"%{filtro.sku}%"))

            if filtro.nombre_producto:
                query = query.filter(
                    models.VistaProductosABC.nombre_producto.ilike(f"%{filtro.nombre_producto}%")
                )

            if filtro.stock_actual_min is not None:
                query = query.filter(models.VistaProductosABC.stock_actual >= filtro.stock_actual_min)

            if filtro.stock_actual_max is not None:
                query = query.filter(models.VistaProductosABC.stock_actual <= filtro.stock_actual_max)

            if filtro.valor_inventario_min:
                query = query.filter(models.VistaProductosABC.valor_inventario >= filtro.valor_inventario_min)

            if filtro.valor_inventario_max:
                query = query.filter(models.VistaProductosABC.valor_inventario <= filtro.valor_inventario_max)

            if filtro.movimientos_anuales_min is not None:
                query = query.filter(models.VistaProductosABC.movimientos_anuales >= filtro.movimientos_anuales_min)

            if filtro.movimientos_anuales_max is not None:
                query = query.filter(models.VistaProductosABC.movimientos_anuales <= filtro.movimientos_anuales_max)

            if filtro.solo_sin_stock:
                query = query.filter(models.VistaProductosABC.stock_actual <= 0)

            if filtro.solo_sin_movimiento:
                query = query.filter(models.VistaProductosABC.movimientos_anuales == 0)

        return query.offset(skip).limit(limit).all()

    def get_productos_clase_a(self, skip: int = 0, limit: int = 100) -> List[models.VistaProductosABC]:
        """Obtener productos clasificados como A"""
        productos = self.db.query(models.VistaProductosABC).offset(skip).limit(limit * 3).all()
        clase_a = [p for p in productos if p.clasificacion_abc_calculada == "A"]
        return clase_a[:limit]

    def get_productos_clase_b(self, skip: int = 0, limit: int = 100) -> List[models.VistaProductosABC]:
        """Obtener productos clasificados como B"""
        productos = self.db.query(models.VistaProductosABC).offset(skip).limit(limit * 3).all()
        clase_b = [p for p in productos if p.clasificacion_abc_calculada == "B"]
        return clase_b[:limit]

    def get_productos_clase_c(self, skip: int = 0, limit: int = 100) -> List[models.VistaProductosABC]:
        """Obtener productos clasificados como C"""
        productos = self.db.query(models.VistaProductosABC).offset(skip).limit(limit * 3).all()
        clase_c = [p for p in productos if p.clasificacion_abc_calculada == "C"]
        return clase_c[:limit]

    def get_productos_sin_movimiento(self, skip: int = 0, limit: int = 100) -> List[models.VistaProductosABC]:
        """Obtener productos sin movimiento"""
        return (self.db.query(models.VistaProductosABC)
                .filter(models.VistaProductosABC.movimientos_anuales == 0)
                .order_by(models.VistaProductosABC.valor_inventario.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_productos_requieren_atencion(self, skip: int = 0, limit: int = 100) -> List[models.VistaProductosABC]:
        """Obtener productos que requieren atención especial"""
        productos = self.db.query(models.VistaProductosABC).offset(skip).limit(limit * 2).all()
        requieren_atencion = [p for p in productos if p.requiere_atencion]
        return requieren_atencion[:limit]

    def get_productos_obsolescencia_alta(self, skip: int = 0, limit: int = 100) -> List[models.VistaProductosABC]:
        """Obtener productos con alta obsolescencia"""
        productos = self.db.query(models.VistaProductosABC).offset(skip).limit(limit * 2).all()
        obsolescencia_alta = [p for p in productos if p.indicador_obsolescencia >= 7]
        return sorted(obsolescencia_alta, key=lambda x: x.indicador_obsolescencia, reverse=True)[:limit]

    def get_estadisticas_generales(self) -> Dict[str, Any]:
        """Obtener estadísticas generales de productos ABC"""
        productos = self.db.query(models.VistaProductosABC).all()

        if not productos:
            return {
                "total_productos": 0,
                "total_valor_inventario": 0,
                "total_movimientos_anuales": 0,
                "promedio_rotacion": 0,
                "productos_clase_a": 0,
                "productos_clase_b": 0,
                "productos_clase_c": 0,
                "productos_sin_movimiento": 0,
                "valor_clase_a": 0,
                "valor_clase_b": 0,
                "valor_clase_c": 0,
                "valor_sin_movimiento": 0,
                "porcentaje_valor_a": 0,
                "porcentaje_valor_b": 0,
                "porcentaje_valor_c": 0,
                "porcentaje_sin_movimiento": 0,
                "productos_requieren_atencion": 0,
                "productos_obsolescencia_alta": 0
            }

        # Calcular estadísticas básicas
        total_productos = len(productos)
        total_valor = sum([float(p.valor_inventario) for p in productos])
        total_movimientos = sum([p.movimientos_anuales for p in productos])
        promedio_rotacion = sum([p.rotacion_inventario for p in productos]) / total_productos

        # Clasificar productos
        clase_a = [p for p in productos if p.clasificacion_abc_calculada == "A"]
        clase_b = [p for p in productos if p.clasificacion_abc_calculada == "B"]
        clase_c = [p for p in productos if p.clasificacion_abc_calculada == "C"]
        sin_movimiento = [p for p in productos if p.clasificacion_abc_calculada == "SIN_MOVIMIENTO"]

        # Calcular valores por clase
        valor_a = sum([float(p.valor_inventario) for p in clase_a])
        valor_b = sum([float(p.valor_inventario) for p in clase_b])
        valor_c = sum([float(p.valor_inventario) for p in clase_c])
        valor_sin_mov = sum([float(p.valor_inventario) for p in sin_movimiento])

        # Productos especiales
        requieren_atencion = len([p for p in productos if p.requiere_atencion])
        obsolescencia_alta = len([p for p in productos if p.indicador_obsolescencia >= 7])

        return {
            "total_productos": total_productos,
            "total_valor_inventario": total_valor,
            "total_movimientos_anuales": total_movimientos,
            "promedio_rotacion": round(promedio_rotacion, 2),
            "productos_clase_a": len(clase_a),
            "productos_clase_b": len(clase_b),
            "productos_clase_c": len(clase_c),
            "productos_sin_movimiento": len(sin_movimiento),
            "valor_clase_a": valor_a,
            "valor_clase_b": valor_b,
            "valor_clase_c": valor_c,
            "valor_sin_movimiento": valor_sin_mov,
            "porcentaje_valor_a": round((valor_a / total_valor) * 100, 2) if total_valor > 0 else 0,
            "porcentaje_valor_b": round((valor_b / total_valor) * 100, 2) if total_valor > 0 else 0,
            "porcentaje_valor_c": round((valor_c / total_valor) * 100, 2) if total_valor > 0 else 0,
            "porcentaje_sin_movimiento": round((valor_sin_mov / total_valor) * 100, 2) if total_valor > 0 else 0,
            "productos_requieren_atencion": requieren_atencion,
            "productos_obsolescencia_alta": obsolescencia_alta
        }

    def get_ranking_por_valor(self, top: int = 20) -> List[Dict[str, Any]]:
        """Obtener ranking de productos por valor de inventario"""
        productos = (self.db.query(models.VistaProductosABC)
                    .order_by(models.VistaProductosABC.valor_inventario.desc())
                    .limit(top)
                    .all())

        total_valor = (self.db.query(func.sum(models.VistaProductosABC.valor_inventario))
                      .scalar() or 0)

        ranking = []
        for i, producto in enumerate(productos, 1):
            porcentaje = (float(producto.valor_inventario) / float(total_valor)) * 100 if total_valor > 0 else 0

            ranking.append({
                "posicion": i,
                "id_producto": producto.id_producto,
                "sku": producto.sku,
                "nombre_producto": producto.nombre_producto,
                "clasificacion_abc": producto.clasificacion_abc_calculada,
                "valor_inventario": float(producto.valor_inventario),
                "valor_movimiento_anual": producto.valor_movimiento_anual,
                "rotacion_inventario": producto.rotacion_inventario,
                "porcentaje_del_total": round(porcentaje, 2)
            })

        return ranking

    def get_analisis_obsolescencia(self, limite: int = 50) -> List[Dict[str, Any]]:
        """Obtener análisis de obsolescencia de productos"""
        productos = self.db.query(models.VistaProductosABC).all()
        productos_obsolescencia = [p for p in productos if p.indicador_obsolescencia >= 4]
        productos_sorted = sorted(productos_obsolescencia, key=lambda x: x.indicador_obsolescencia, reverse=True)

        analisis = []
        for producto in productos_sorted[:limite]:
            # Determinar nivel de riesgo
            if producto.indicador_obsolescencia >= 7:
                nivel_riesgo = "ALTO"
            elif producto.indicador_obsolescencia >= 5:
                nivel_riesgo = "MEDIO"
            else:
                nivel_riesgo = "BAJO"

            analisis.append({
                "id_producto": producto.id_producto,
                "sku": producto.sku,
                "nombre_producto": producto.nombre_producto,
                "valor_inventario": float(producto.valor_inventario),
                "movimientos_anuales": producto.movimientos_anuales,
                "dias_inventario": producto.dias_inventario,
                "indicador_obsolescencia": producto.indicador_obsolescencia,
                "nivel_riesgo": nivel_riesgo,
                "acciones_sugeridas": producto.acciones_recomendadas,
                "impacto_financiero": producto.impacto_financiero
            })

        return analisis

    def get_alertas(self, nivel_criticidad: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener alertas de productos ABC"""
        productos = self.db.query(models.VistaProductosABC).all()
        alertas = []

        for producto in productos:
            alertas_producto = []

            # Alerta por producto A sin stock
            if producto.clasificacion_abc_calculada == "A" and producto.stock_actual <= 0:
                alertas_producto.append({
                    "tipo_alerta": "SIN_STOCK_CLASE_A",
                    "nivel_criticidad": "CRITICA",
                    "descripcion": f"Producto clase A sin stock: {producto.nombre_producto}"
                })

            # Alerta por obsolescencia alta
            if producto.indicador_obsolescencia >= 7:
                alertas_producto.append({
                    "tipo_alerta": "OBSOLESCENCIA_ALTA",
                    "nivel_criticidad": "ALTA",
                    "descripcion": f"Producto con alta obsolescencia: {producto.nombre_producto}"
                })

            # Alerta por rotación crítica
            if producto.rotacion_inventario > 20:
                alertas_producto.append({
                    "tipo_alerta": "ROTACION_CRITICA",
                    "nivel_criticidad": "ALTA",
                    "descripcion": f"Rotación crítica, posible desabasto: {producto.nombre_producto}"
                })

            # Agregar alertas encontradas
            for alerta in alertas_producto:
                if not nivel_criticidad or alerta["nivel_criticidad"] == nivel_criticidad:
                    alertas.append({
                        "id_producto": producto.id_producto,
                        "sku": producto.sku,
                        "nombre_producto": producto.nombre_producto,
                        "tipo_alerta": alerta["tipo_alerta"],
                        "nivel_criticidad": alerta["nivel_criticidad"],
                        "descripcion": alerta["descripcion"],
                        "valor_afectado": float(producto.valor_inventario),
                        "acciones_recomendadas": producto.acciones_recomendadas,
                        "fecha_generacion": datetime.now()
                    })

        return sorted(alertas, key=lambda x: self._get_prioridad_criticidad(x["nivel_criticidad"]), reverse=True)

    def _get_prioridad_criticidad(self, criticidad: str) -> int:
        """Obtener prioridad numérica de criticidad"""
        prioridades = {
            "CRITICA": 5,
            "ALTA": 4,
            "MEDIA": 3,
            "NORMAL": 2,
            "BAJA": 1
        }
        return prioridades.get(criticidad, 0)

    def get_recomendaciones(self, limite: int = 20) -> List[Dict[str, Any]]:
        """Obtener recomendaciones para productos ABC"""
        productos = self.db.query(models.VistaProductosABC).all()
        productos_prioritarios = [p for p in productos if p.requiere_atencion or p.indicador_obsolescencia >= 5]
        productos_sorted = sorted(productos_prioritarios,
                                key=lambda x: (x.indicador_obsolescencia, float(x.valor_inventario)),
                                reverse=True)

        recomendaciones = []
        for producto in productos_sorted[:limite]:
            # Determinar prioridad
            if producto.nivel_criticidad == "CRITICA":
                prioridad = "CRITICA"
            elif producto.nivel_criticidad == "ALTA":
                prioridad = "ALTA"
            elif producto.indicador_obsolescencia >= 7:
                prioridad = "ALTA"
            else:
                prioridad = "MEDIA"

            recomendaciones.append({
                "id_producto": producto.id_producto,
                "sku": producto.sku,
                "nombre_producto": producto.nombre_producto,
                "clasificacion_abc": producto.clasificacion_abc_calculada,
                "tipo_recomendacion": producto.recomendacion_accion,
                "prioridad": prioridad,
                "descripcion": self._generar_descripcion_recomendacion(producto),
                "acciones_sugeridas": producto.acciones_recomendadas,
                "impacto_estimado": producto.impacto_financiero,
                "punto_reorden_sugerido": producto.punto_reorden_sugerido,
                "stock_maximo_sugerido": producto.stock_maximo_sugerido
            })

        return recomendaciones

    def _generar_descripcion_recomendacion(self, producto: models.VistaProductosABC) -> str:
        """Generar descripción de recomendación"""
        clasificacion = producto.clasificacion_abc_calculada
        accion = producto.recomendacion_accion

        descripciones = {
            "REPOSICION_URGENTE": f"Producto clase {clasificacion} requiere reposición urgente",
            "AUMENTAR_STOCK_MINIMO": f"Revisar stock mínimo por alta rotación ({producto.rotacion_inventario:.1f})",
            "REVISAR_DEMANDA": f"Evaluar demanda real - baja rotación para clase {clasificacion}",
            "EVALUAR_DESCONTINUAR": f"Considerar descontinuar por baja rotación y alto valor",
            "CONSIDERAR_LIQUIDACION": f"Evaluar liquidación - sin movimiento con valor ${producto.valor_inventario:,.2f}",
            "EVALUAR_LIQUIDACION": f"Evaluar liquidación por exceso de inventario"
        }

        return descripciones.get(accion, f"Revisar producto clase {clasificacion} - {accion}")

    def get_dashboard_kpis(self) -> Dict[str, Any]:
        """Obtener KPIs principales para dashboard ABC"""
        stats_generales = self.get_estadisticas_generales()
        clase_a = self.get_productos_clase_a(limit=5)
        criticos = self.get_productos_requieren_atencion(limit=10)
        obsolescencia = self.get_productos_obsolescencia_alta(limit=5)

        return {
            "resumen_general": stats_generales,
            "productos_criticos": len(criticos),
            "valor_clase_a": stats_generales["valor_clase_a"],
            "productos_sin_stock_a": len([p for p in clase_a if p.stock_actual <= 0]),
            "productos_obsolescencia_alta": len(obsolescencia),
            "valor_en_riesgo": sum([float(p.valor_inventario) for p in obsolescencia]),
            "eficiencia_inventario": self._calcular_eficiencia_inventario(),
            "alertas_activas": len(self.get_alertas()),
            "recomendaciones_pendientes": len(self.get_recomendaciones())
        }

    def _calcular_eficiencia_inventario(self) -> float:
        """Calcular eficiencia general del inventario"""
        productos = self.db.query(models.VistaProductosABC).all()
        if not productos:
            return 0.0

        # Productos con movimiento vs total
        con_movimiento = len([p for p in productos if p.movimientos_anuales > 0])
        eficiencia = (con_movimiento / len(productos)) * 100

        return round(eficiencia, 2)

    def get_optimizacion_inventario(self, limite: int = 50) -> List[Dict[str, Any]]:
        """Obtener recomendaciones de optimización de inventario"""
        productos = self.db.query(models.VistaProductosABC).all()
        optimizaciones = []

        for producto in productos:
            stock_actual = producto.stock_actual
            stock_optimo = (producto.punto_reorden_sugerido + producto.stock_maximo_sugerido) / 2
            ajuste_requerido = stock_optimo - stock_actual

            # Determinar tipo de ajuste
            if abs(ajuste_requerido) / stock_actual > 0.2 if stock_actual > 0 else abs(ajuste_requerido) > 5:
                if ajuste_requerido > 0:
                    tipo_ajuste = "AUMENTAR"
                    prioridad = "ALTA" if producto.clasificacion_abc_calculada == "A" else "MEDIA"
                else:
                    tipo_ajuste = "REDUCIR"
                    prioridad = "ALTA" if producto.indicador_obsolescencia >= 7 else "MEDIA"
            else:
                tipo_ajuste = "MANTENER"
                prioridad = "BAJA"

            if tipo_ajuste != "MANTENER":
                optimizaciones.append({
                    "id_producto": producto.id_producto,
                    "sku": producto.sku,
                    "nombre_producto": producto.nombre_producto,
                    "stock_actual": stock_actual,
                    "stock_optimo": round(stock_optimo, 1),
                    "punto_reorden_sugerido": producto.punto_reorden_sugerido,
                    "stock_maximo_sugerido": producto.stock_maximo_sugerido,
                    "ajuste_requerido": round(ajuste_requerido, 1),
                    "tipo_ajuste": tipo_ajuste,
                    "prioridad_ajuste": prioridad
                })

        # Ordenar por prioridad y valor
        prioridad_orden = {"ALTA": 3, "MEDIA": 2, "BAJA": 1}
        optimizaciones_sorted = sorted(optimizaciones,
                                     key=lambda x: (prioridad_orden[x["prioridad_ajuste"]],
                                                   abs(x["ajuste_requerido"])),
                                     reverse=True)

        return optimizaciones_sorted[:limite]

    def buscar_por_texto(self, texto: str, skip: int = 0, limit: int = 50) -> List[models.VistaProductosABC]:
        """Buscar productos ABC por texto"""
        termino_busqueda = texto.strip()
        return (self.db.query(models.VistaProductosABC)
                .filter(
                    or_(
                        models.VistaProductosABC.sku.ilike(f"%{termino_busqueda}%"),
                        models.VistaProductosABC.nombre_producto.ilike(f"%{termino_busqueda}%")
                    )
                )
                .order_by(models.VistaProductosABC.valor_inventario.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def contar_con_filtros(self, filtro: Optional[schemas.VistaProductosABCFilter] = None) -> int:
        """Contar productos ABC con filtros aplicados"""
        query = self.db.query(models.VistaProductosABC)

        if filtro:
            # Aplicar los mismos filtros que en get_multi_filtered
            if filtro.id_producto:
                query = query.filter(models.VistaProductosABC.id_producto == filtro.id_producto)
            # ... (resto de filtros igual que en get_multi_filtered)

        return query.count()

# Instancia global
productos_abc_crud = ProductosABCCRUD()


# ========================================
# CRUD PARA ESTADOS DE ORDEN DE COMPRA
# ========================================

class EstadoOrdenCompraCRUD:
    """CRUD operations for EstadoOrdenCompra"""

    def get_estado(self, db: Session, estado_id: int) -> Optional[models.EstadoOrdenCompra]:
        """Obtener estado por ID"""
        return db.query(models.EstadoOrdenCompra).filter(models.EstadoOrdenCompra.id_estado == estado_id).first()

    def get_estado_by_codigo(self, db: Session, codigo_estado: str) -> Optional[models.EstadoOrdenCompra]:
        """Obtener estado por código"""
        return db.query(models.EstadoOrdenCompra).filter(models.EstadoOrdenCompra.codigo_estado == codigo_estado).first()

    def get_estado_inicial(self, db: Session) -> Optional[models.EstadoOrdenCompra]:
        """Obtener estado inicial"""
        return db.query(models.EstadoOrdenCompra).filter(
            models.EstadoOrdenCompra.es_estado_inicial == True,
            models.EstadoOrdenCompra.activo == True
        ).first()

    def get_estados_finales(self, db: Session) -> List[models.EstadoOrdenCompra]:
        """Obtener estados finales"""
        return db.query(models.EstadoOrdenCompra).filter(
            models.EstadoOrdenCompra.es_estado_final == True,
            models.EstadoOrdenCompra.activo == True
        ).all()

    def get_estados(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.EstadoOrdenCompra]:
        """Obtener todos los estados"""
        return db.query(models.EstadoOrdenCompra).filter(
            models.EstadoOrdenCompra.activo == True
        ).order_by(models.EstadoOrdenCompra.codigo_estado).offset(skip).limit(limit).all()

    def create_estado(self, db: Session, estado: schemas.EstadoOrdenCompraCreate) -> models.EstadoOrdenCompra:
        """Crear nuevo estado"""
        # Verificar que el código no exista
        existing = self.get_estado_by_codigo(db, estado.codigo_estado)
        if existing:
            raise ValueError(f"Ya existe un estado con código '{estado.codigo_estado}'")

        # Si es estado inicial, desactivar otros estados iniciales
        if estado.es_estado_inicial:
            db.query(models.EstadoOrdenCompra).filter(
                models.EstadoOrdenCompra.es_estado_inicial == True
            ).update({"es_estado_inicial": False})

        db_estado = models.EstadoOrdenCompra(**estado.model_dump())
        db.add(db_estado)
        db.commit()
        db.refresh(db_estado)
        return db_estado

    def update_estado(self, db: Session, estado_id: int, estado: schemas.EstadoOrdenCompraUpdate) -> Optional[models.EstadoOrdenCompra]:
        """Actualizar estado"""
        db_estado = self.get_estado(db, estado_id)
        if not db_estado:
            return None

        # Verificar código único si se está actualizando
        if estado.codigo_estado and estado.codigo_estado != db_estado.codigo_estado:
            existing = self.get_estado_by_codigo(db, estado.codigo_estado)
            if existing:
                raise ValueError(f"Ya existe un estado con código '{estado.codigo_estado}'")

        # Si es estado inicial, desactivar otros estados iniciales
        if estado.es_estado_inicial:
            db.query(models.EstadoOrdenCompra).filter(
                models.EstadoOrdenCompra.es_estado_inicial == True,
                models.EstadoOrdenCompra.id_estado != estado_id
            ).update({"es_estado_inicial": False})

        update_data = estado.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_estado, field, value)

        db.commit()
        db.refresh(db_estado)
        return db_estado

    def delete_estado(self, db: Session, estado_id: int) -> bool:
        """Eliminar estado (soft delete)"""
        db_estado = self.get_estado(db, estado_id)
        if not db_estado:
            return False

        # Verificar que no esté siendo usado en órdenes de compra
        # (cuando se implemente la tabla ordenes_compra)

        db_estado.activo = False
        db.commit()
        return True

    def count_estados(self, db: Session) -> int:
        """Contar estados activos"""
        return db.query(models.EstadoOrdenCompra).filter(models.EstadoOrdenCompra.activo == True).count()

    def validate_transicion(self, db: Session, estado_origen_id: int, estado_destino_id: int) -> bool:
        """Validar si es posible la transición entre estados"""
        estado_origen = self.get_estado(db, estado_origen_id)
        estado_destino = self.get_estado(db, estado_destino_id)

        if not estado_origen or not estado_destino:
            return False

        # Lógica de validación de transiciones
        # Por ejemplo: no se puede ir de un estado final a otro estado
        if estado_origen.es_estado_final:
            return False

        return True


# Instancia global
estado_orden_compra_crud = EstadoOrdenCompraCRUD()


# ========================================
# CRUD PARA ÓRDENES DE COMPRA
# ========================================

class OrdenCompraCRUD:
    """CRUD operations for OrdenCompra"""

    def get_orden(self, db: Session, orden_id: int) -> Optional[models.OrdenCompra]:
        """Obtener orden por ID"""
        return db.query(models.OrdenCompra).filter(models.OrdenCompra.id_orden_compra == orden_id).first()

    def get_orden_by_numero(self, db: Session, numero_orden: str) -> Optional[models.OrdenCompra]:
        """Obtener orden por número"""
        return db.query(models.OrdenCompra).filter(models.OrdenCompra.numero_orden == numero_orden).first()

    def get_ordenes(self, db: Session, skip: int = 0, limit: int = 100,
                   filtros: Optional[schemas.OrdenCompraFilters] = None) -> List[models.OrdenCompra]:
        """Obtener órdenes con filtros"""
        query = db.query(models.OrdenCompra).filter(models.OrdenCompra.activo == True)

        if filtros:
            if filtros.id_proveedor:
                query = query.filter(models.OrdenCompra.id_proveedor == filtros.id_proveedor)
            if filtros.id_estado:
                query = query.filter(models.OrdenCompra.id_estado == filtros.id_estado)
            if filtros.fecha_desde:
                query = query.filter(models.OrdenCompra.fecha_orden >= filtros.fecha_desde)
            if filtros.fecha_hasta:
                query = query.filter(models.OrdenCompra.fecha_orden <= filtros.fecha_hasta)
            if filtros.numero_orden:
                query = query.filter(models.OrdenCompra.numero_orden.like(f"%{filtros.numero_orden}%"))
            if filtros.total_minimo:
                query = query.filter(models.OrdenCompra.total >= filtros.total_minimo)
            if filtros.total_maximo:
                query = query.filter(models.OrdenCompra.total <= filtros.total_maximo)
            if filtros.activo is not None:
                query = query.filter(models.OrdenCompra.activo == filtros.activo)

        return query.order_by(models.OrdenCompra.fecha_orden.desc()).offset(skip).limit(limit).all()

    def create_orden(self, db: Session, orden: schemas.OrdenCompraCreate) -> models.OrdenCompra:
        """Crear nueva orden"""
        # Verificar que el número no exista
        existing = self.get_orden_by_numero(db, orden.numero_orden)
        if existing:
            raise ValueError(f"Ya existe una orden con número '{orden.numero_orden}'")

        # Verificar que existan las referencias
        proveedor = db.query(models.Proveedor).filter(models.Proveedor.id_proveedor == orden.id_proveedor).first()
        if not proveedor:
            raise ValueError(f"El proveedor con ID {orden.id_proveedor} no existe")

        usuario = db.query(models.Usuarios).filter(models.Usuarios.id_usuario == orden.id_usuario_solicitante).first()
        if not usuario:
            raise ValueError(f"El usuario con ID {orden.id_usuario_solicitante} no existe")

        # Obtener estado inicial si no se especifica
        orden_data = orden.model_dump()
        if 'id_estado' not in orden_data:
            estado_inicial = estado_orden_compra_crud.get_estado_inicial(db)
            if not estado_inicial:
                raise ValueError("No hay estado inicial configurado")
            orden_data['id_estado'] = estado_inicial.id_estado

        db_orden = models.OrdenCompra(**orden_data)
        db.add(db_orden)
        db.commit()
        db.refresh(db_orden)
        return db_orden

    def update_orden(self, db: Session, orden_id: int, orden: schemas.OrdenCompraUpdate) -> Optional[models.OrdenCompra]:
        """Actualizar orden"""
        db_orden = self.get_orden(db, orden_id)
        if not db_orden:
            return None

        # Verificar número único si se está actualizando
        if orden.numero_orden and orden.numero_orden != db_orden.numero_orden:
            existing = self.get_orden_by_numero(db, orden.numero_orden)
            if existing:
                raise ValueError(f"Ya existe una orden con número '{orden.numero_orden}'")

        update_data = orden.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_orden, field, value)

        db.commit()
        db.refresh(db_orden)
        return db_orden

    def delete_orden(self, db: Session, orden_id: int) -> bool:
        """Eliminar orden (soft delete)"""
        db_orden = self.get_orden(db, orden_id)
        if not db_orden:
            return False

        db_orden.activo = False
        db.commit()
        return True

    def count_ordenes(self, db: Session, filtros: Optional[schemas.OrdenCompraFilters] = None) -> int:
        """Contar órdenes con filtros"""
        query = db.query(models.OrdenCompra).filter(models.OrdenCompra.activo == True)

        if filtros:
            if filtros.id_proveedor:
                query = query.filter(models.OrdenCompra.id_proveedor == filtros.id_proveedor)
            if filtros.id_estado:
                query = query.filter(models.OrdenCompra.id_estado == filtros.id_estado)

        return query.count()

    def aprobar_orden(self, db: Session, orden_id: int, usuario_aprobador_id: int) -> Optional[models.OrdenCompra]:
        """Aprobar orden"""
        db_orden = self.get_orden(db, orden_id)
        if not db_orden:
            return None

        # Cambiar a estado aprobado
        estado_aprobado = estado_orden_compra_crud.get_estado_by_codigo(db, "APROBADA")
        if not estado_aprobado:
            raise ValueError("No existe el estado 'APROBADA'")

        db_orden.id_estado = estado_aprobado.id_estado
        db_orden.id_usuario_aprobador = usuario_aprobador_id
        db_orden.fecha_aprobacion = func.current_timestamp()

        db.commit()
        db.refresh(db_orden)
        return db_orden

    def cancelar_orden(self, db: Session, orden_id: int, motivo: str) -> Optional[models.OrdenCompra]:
        """Cancelar orden"""
        db_orden = self.get_orden(db, orden_id)
        if not db_orden:
            return None

        # Cambiar a estado cancelado
        estado_cancelado = estado_orden_compra_crud.get_estado_by_codigo(db, "CANCELADA")
        if not estado_cancelado:
            raise ValueError("No existe el estado 'CANCELADA'")

        db_orden.id_estado = estado_cancelado.id_estado
        db_orden.motivo_cancelacion = motivo
        db_orden.fecha_cancelacion = func.current_timestamp()

        db.commit()
        db.refresh(db_orden)
        return db_orden


class OrdenCompraDetalleCRUD:
    """CRUD operations for OrdenCompraDetalle"""

    def get_detalle(self, db: Session, detalle_id: int) -> Optional[models.OrdenCompraDetalle]:
        """Obtener detalle por ID"""
        return db.query(models.OrdenCompraDetalle).filter(models.OrdenCompraDetalle.id_detalle == detalle_id).first()

    def get_detalles_by_orden(self, db: Session, orden_id: int) -> List[models.OrdenCompraDetalle]:
        """Obtener detalles por orden"""
        return db.query(models.OrdenCompraDetalle).filter(
            models.OrdenCompraDetalle.id_orden_compra == orden_id,
            models.OrdenCompraDetalle.activo == True
        ).order_by(models.OrdenCompraDetalle.numero_linea).all()

    def create_detalle(self, db: Session, detalle: schemas.OrdenCompraDetalleCreate, orden_id: int) -> models.OrdenCompraDetalle:
        """Crear detalle de orden"""
        # Verificar que la orden existe
        orden = db.query(models.OrdenCompra).filter(models.OrdenCompra.id_orden_compra == orden_id).first()
        if not orden:
            raise ValueError(f"La orden con ID {orden_id} no existe")

        # Verificar que el producto existe
        producto = db.query(models.Producto).filter(models.Producto.id_producto == detalle.id_producto).first()
        if not producto:
            raise ValueError(f"El producto con ID {detalle.id_producto} no existe")

        # Calcular cantidad pendiente
        detalle_data = detalle.model_dump()
        detalle_data['id_orden_compra'] = orden_id
        detalle_data['cantidad_pendiente'] = detalle.cantidad_solicitada

        db_detalle = models.OrdenCompraDetalle(**detalle_data)
        db.add(db_detalle)
        db.commit()
        db.refresh(db_detalle)

        # Actualizar totales de la orden
        self._actualizar_totales_orden(db, orden_id)

        return db_detalle

    def update_detalle(self, db: Session, detalle_id: int, detalle: schemas.OrdenCompraDetalleUpdate) -> Optional[models.OrdenCompraDetalle]:
        """Actualizar detalle"""
        db_detalle = self.get_detalle(db, detalle_id)
        if not db_detalle:
            return None

        update_data = detalle.model_dump(exclude_unset=True)

        # Recalcular cantidad pendiente si se actualiza cantidad solicitada o recibida
        if 'cantidad_solicitada' in update_data or 'cantidad_recibida' in update_data:
            cantidad_solicitada = update_data.get('cantidad_solicitada', db_detalle.cantidad_solicitada)
            cantidad_recibida = update_data.get('cantidad_recibida', db_detalle.cantidad_recibida)
            update_data['cantidad_pendiente'] = cantidad_solicitada - cantidad_recibida

        for field, value in update_data.items():
            setattr(db_detalle, field, value)

        db.commit()
        db.refresh(db_detalle)

        # Actualizar totales de la orden
        self._actualizar_totales_orden(db, db_detalle.id_orden_compra)

        return db_detalle

    def delete_detalle(self, db: Session, detalle_id: int) -> bool:
        """Eliminar detalle (soft delete)"""
        db_detalle = self.get_detalle(db, detalle_id)
        if not db_detalle:
            return False

        orden_id = db_detalle.id_orden_compra
        db_detalle.activo = False
        db.commit()

        # Actualizar totales de la orden
        self._actualizar_totales_orden(db, orden_id)

        return True

    def _actualizar_totales_orden(self, db: Session, orden_id: int):
        """Actualizar totales de la orden basado en sus detalles"""
        detalles = self.get_detalles_by_orden(db, orden_id)
        subtotal = sum(detalle.importe_total for detalle in detalles)

        orden = db.query(models.OrdenCompra).filter(models.OrdenCompra.id_orden_compra == orden_id).first()
        if orden:
            orden.subtotal = subtotal
            orden.total = subtotal + orden.impuestos - orden.descuentos
            db.commit()


# Instancias globales
orden_compra_crud = OrdenCompraCRUD()
orden_compra_detalle_crud = OrdenCompraDetalleCRUD()


# ========================================
# CRUD PARA RECEPCIONES DE MERCANCÍA
# ========================================

class RecepcionMercanciaCRUD:
    """CRUD operations for RecepcionMercancia"""

    def get_recepcion(self, db: Session, recepcion_id: int) -> Optional[models.RecepcionMercancia]:
        """Obtener recepción por ID"""
        return db.query(models.RecepcionMercancia).filter(models.RecepcionMercancia.id_recepcion == recepcion_id).first()

    def get_recepcion_by_numero(self, db: Session, numero_recepcion: str) -> Optional[models.RecepcionMercancia]:
        """Obtener recepción por número"""
        return db.query(models.RecepcionMercancia).filter(models.RecepcionMercancia.numero_recepcion == numero_recepcion).first()

    def get_recepciones_by_orden(self, db: Session, orden_id: int) -> List[models.RecepcionMercancia]:
        """Obtener recepciones por orden de compra"""
        return db.query(models.RecepcionMercancia).filter(
            models.RecepcionMercancia.id_orden_compra == orden_id,
            models.RecepcionMercancia.activo == True
        ).order_by(models.RecepcionMercancia.fecha_recepcion.desc()).all()

    def get_recepciones(self, db: Session, skip: int = 0, limit: int = 100,
                       filtros: Optional[schemas.RecepcionMercanciaFilters] = None) -> List[models.RecepcionMercancia]:
        """Obtener recepciones con filtros"""
        query = db.query(models.RecepcionMercancia).filter(models.RecepcionMercancia.activo == True)

        if filtros:
            if filtros.id_orden_compra:
                query = query.filter(models.RecepcionMercancia.id_orden_compra == filtros.id_orden_compra)
            if filtros.id_usuario_receptor:
                query = query.filter(models.RecepcionMercancia.id_usuario_receptor == filtros.id_usuario_receptor)
            if filtros.fecha_desde:
                query = query.filter(models.RecepcionMercancia.fecha_recepcion >= filtros.fecha_desde)
            if filtros.fecha_hasta:
                query = query.filter(models.RecepcionMercancia.fecha_recepcion <= filtros.fecha_hasta)
            if filtros.numero_recepcion:
                query = query.filter(models.RecepcionMercancia.numero_recepcion.like(f"%{filtros.numero_recepcion}%"))
            if filtros.numero_factura_proveedor:
                query = query.filter(models.RecepcionMercancia.numero_factura_proveedor.like(f"%{filtros.numero_factura_proveedor}%"))
            if filtros.recepcion_completa is not None:
                query = query.filter(models.RecepcionMercancia.recepcion_completa == filtros.recepcion_completa)
            if filtros.activo is not None:
                query = query.filter(models.RecepcionMercancia.activo == filtros.activo)

        return query.order_by(models.RecepcionMercancia.fecha_recepcion.desc()).offset(skip).limit(limit).all()

    def create_recepcion(self, db: Session, recepcion: schemas.RecepcionMercanciaCreate) -> models.RecepcionMercancia:
        """Crear nueva recepción"""
        # Verificar que el número no exista
        existing = self.get_recepcion_by_numero(db, recepcion.numero_recepcion)
        if existing:
            raise ValueError(f"Ya existe una recepción con número '{recepcion.numero_recepcion}'")

        # Verificar que la orden existe
        orden = db.query(models.OrdenCompra).filter(models.OrdenCompra.id_orden_compra == recepcion.id_orden_compra).first()
        if not orden:
            raise ValueError(f"La orden con ID {recepcion.id_orden_compra} no existe")

        # Verificar que el usuario existe
        usuario = db.query(models.Usuarios).filter(models.Usuarios.id_usuario == recepcion.id_usuario_receptor).first()
        if not usuario:
            raise ValueError(f"El usuario con ID {recepcion.id_usuario_receptor} no existe")

        db_recepcion = models.RecepcionMercancia(**recepcion.model_dump())
        db.add(db_recepcion)
        db.commit()
        db.refresh(db_recepcion)
        return db_recepcion

    def update_recepcion(self, db: Session, recepcion_id: int, recepcion: schemas.RecepcionMercanciaUpdate) -> Optional[models.RecepcionMercancia]:
        """Actualizar recepción"""
        db_recepcion = self.get_recepcion(db, recepcion_id)
        if not db_recepcion:
            return None

        # Verificar número único si se está actualizando
        if recepcion.numero_recepcion and recepcion.numero_recepcion != db_recepcion.numero_recepcion:
            existing = self.get_recepcion_by_numero(db, recepcion.numero_recepcion)
            if existing:
                raise ValueError(f"Ya existe una recepción con número '{recepcion.numero_recepcion}'")

        update_data = recepcion.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_recepcion, field, value)

        db.commit()
        db.refresh(db_recepcion)
        return db_recepcion

    def delete_recepcion(self, db: Session, recepcion_id: int) -> bool:
        """Eliminar recepción (soft delete)"""
        db_recepcion = self.get_recepcion(db, recepcion_id)
        if not db_recepcion:
            return False

        db_recepcion.activo = False
        db.commit()
        return True

    def count_recepciones(self, db: Session, filtros: Optional[schemas.RecepcionMercanciaFilters] = None) -> int:
        """Contar recepciones con filtros"""
        query = db.query(models.RecepcionMercancia).filter(models.RecepcionMercancia.activo == True)

        if filtros:
            if filtros.id_orden_compra:
                query = query.filter(models.RecepcionMercancia.id_orden_compra == filtros.id_orden_compra)
            if filtros.id_usuario_receptor:
                query = query.filter(models.RecepcionMercancia.id_usuario_receptor == filtros.id_usuario_receptor)

        return query.count()

    def marcar_como_completa(self, db: Session, recepcion_id: int) -> Optional[models.RecepcionMercancia]:
        """Marcar recepción como completa"""
        db_recepcion = self.get_recepcion(db, recepcion_id)
        if not db_recepcion:
            return None

        db_recepcion.recepcion_completa = True
        db.commit()
        db.refresh(db_recepcion)
        return db_recepcion


class RecepcionMercanciaDetalleCRUD:
    """CRUD operations for RecepcionMercanciaDetalle"""

    def get_detalle(self, db: Session, detalle_id: int) -> Optional[models.RecepcionMercanciaDetalle]:
        """Obtener detalle por ID"""
        return db.query(models.RecepcionMercanciaDetalle).filter(models.RecepcionMercanciaDetalle.id_detalle_recepcion == detalle_id).first()

    def get_detalles_by_recepcion(self, db: Session, recepcion_id: int) -> List[models.RecepcionMercanciaDetalle]:
        """Obtener detalles por recepción"""
        return db.query(models.RecepcionMercanciaDetalle).filter(
            models.RecepcionMercanciaDetalle.id_recepcion == recepcion_id
        ).all()

    def create_detalle(self, db: Session, detalle: schemas.RecepcionMercanciaDetalleCreate, recepcion_id: int) -> models.RecepcionMercanciaDetalle:
        """Crear detalle de recepción"""
        # Verificar que la recepción existe
        recepcion = db.query(models.RecepcionMercancia).filter(models.RecepcionMercancia.id_recepcion == recepcion_id).first()
        if not recepcion:
            raise ValueError(f"La recepción con ID {recepcion_id} no existe")

        # Verificar que el detalle de orden existe
        detalle_orden = db.query(models.OrdenCompraDetalle).filter(models.OrdenCompraDetalle.id_detalle == detalle.id_detalle_orden).first()
        if not detalle_orden:
            raise ValueError(f"El detalle de orden con ID {detalle.id_detalle_orden} no existe")

        # Validar que cantidad recibida = cantidad aceptada + cantidad rechazada
        if detalle.cantidad_recibida != (detalle.cantidad_aceptada + detalle.cantidad_rechazada):
            raise ValueError("La cantidad recibida debe ser igual a la suma de cantidad aceptada y rechazada")

        detalle_data = detalle.model_dump()
        detalle_data['id_recepcion'] = recepcion_id

        db_detalle = models.RecepcionMercanciaDetalle(**detalle_data)
        db.add(db_detalle)
        db.commit()
        db.refresh(db_detalle)

        # Actualizar cantidad recibida en el detalle de orden
        self._actualizar_cantidad_recibida_orden(db, detalle.id_detalle_orden)

        return db_detalle

    def update_detalle(self, db: Session, detalle_id: int, detalle: schemas.RecepcionMercanciaDetalleUpdate) -> Optional[models.RecepcionMercanciaDetalle]:
        """Actualizar detalle de recepción"""
        db_detalle = self.get_detalle(db, detalle_id)
        if not db_detalle:
            return None

        update_data = detalle.model_dump(exclude_unset=True)

        # Validar cantidades si se están actualizando
        cantidad_recibida = update_data.get('cantidad_recibida', db_detalle.cantidad_recibida)
        cantidad_aceptada = update_data.get('cantidad_aceptada', db_detalle.cantidad_aceptada)
        cantidad_rechazada = update_data.get('cantidad_rechazada', db_detalle.cantidad_rechazada)

        if cantidad_recibida != (cantidad_aceptada + cantidad_rechazada):
            raise ValueError("La cantidad recibida debe ser igual a la suma de cantidad aceptada y rechazada")

        for field, value in update_data.items():
            setattr(db_detalle, field, value)

        db.commit()
        db.refresh(db_detalle)

        # Actualizar cantidad recibida en el detalle de orden
        self._actualizar_cantidad_recibida_orden(db, db_detalle.id_detalle_orden)

        return db_detalle

    def delete_detalle(self, db: Session, detalle_id: int) -> bool:
        """Eliminar detalle de recepción"""
        db_detalle = self.get_detalle(db, detalle_id)
        if not db_detalle:
            return False

        detalle_orden_id = db_detalle.id_detalle_orden
        db.delete(db_detalle)
        db.commit()

        # Actualizar cantidad recibida en el detalle de orden
        self._actualizar_cantidad_recibida_orden(db, detalle_orden_id)

        return True

    def _actualizar_cantidad_recibida_orden(self, db: Session, detalle_orden_id: int):
        """Actualizar cantidad recibida en el detalle de orden basado en las recepciones"""
        # Sumar todas las cantidades aceptadas de todas las recepciones para este detalle
        total_recibido = db.query(func.sum(models.RecepcionMercanciaDetalle.cantidad_aceptada)).filter(
            models.RecepcionMercanciaDetalle.id_detalle_orden == detalle_orden_id
        ).scalar() or 0

        # Actualizar el detalle de orden
        detalle_orden = db.query(models.OrdenCompraDetalle).filter(models.OrdenCompraDetalle.id_detalle == detalle_orden_id).first()
        if detalle_orden:
            detalle_orden.cantidad_recibida = total_recibido
            detalle_orden.cantidad_pendiente = detalle_orden.cantidad_solicitada - total_recibido
            db.commit()


# Instancias globales
recepcion_mercancia_crud = RecepcionMercanciaCRUD()
recepcion_mercancia_detalle_crud = RecepcionMercanciaDetalleCRUD()


# ========================================
# CRUD PARA VISTAS DE ÓRDENES DE COMPRA
# ========================================

class VistaOrdenesCompraResumenCRUD:
    """CRUD para vista resumen de órdenes de compra"""

    def __init__(self, db: Session = None):
        self.db = db
        self.model = models.VistaOrdenesCompraResumen

    def get_multi_filtered(self, db: Session, skip: int = 0, limit: int = 100,
                          filtro: Optional[schemas.VistaOrdenesCompraResumenFilters] = None) -> List[models.VistaOrdenesCompraResumen]:
        """Obtener múltiples registros con filtros avanzados"""
        query = db.query(self.model)

        if filtro:
            if filtro.numero_orden:
                query = query.filter(self.model.numero_orden.like(f"%{filtro.numero_orden}%"))
            if filtro.nombre_proveedor:
                query = query.filter(self.model.nombre_proveedor.like(f"%{filtro.nombre_proveedor}%"))
            if filtro.codigo_proveedor:
                query = query.filter(self.model.codigo_proveedor.like(f"%{filtro.codigo_proveedor}%"))
            if filtro.solicitante:
                query = query.filter(self.model.solicitante.like(f"%{filtro.solicitante}%"))
            if filtro.nombre_estado:
                query = query.filter(self.model.nombre_estado == filtro.nombre_estado)
            if filtro.fecha_desde:
                query = query.filter(self.model.fecha_orden >= filtro.fecha_desde)
            if filtro.fecha_hasta:
                query = query.filter(self.model.fecha_orden <= filtro.fecha_hasta)
            if filtro.total_minimo:
                query = query.filter(self.model.total >= filtro.total_minimo)
            if filtro.total_maximo:
                query = query.filter(self.model.total <= filtro.total_maximo)
            if filtro.estado_recepcion:
                query = query.filter(self.model.estado_recepcion == filtro.estado_recepcion)
            if filtro.moneda:
                query = query.filter(self.model.moneda == filtro.moneda)

        return query.order_by(self.model.fecha_orden.desc()).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, orden_id: int) -> Optional[models.VistaOrdenesCompraResumen]:
        """Obtener por ID"""
        return db.query(self.model).filter(self.model.id_orden_compra == orden_id).first()

    def contar_con_filtros(self, db: Session, filtro: Optional[schemas.VistaOrdenesCompraResumenFilters] = None) -> int:
        """Contar registros con filtros aplicados"""
        query = db.query(self.model)

        if filtro:
            if filtro.numero_orden:
                query = query.filter(self.model.numero_orden.like(f"%{filtro.numero_orden}%"))
            if filtro.nombre_proveedor:
                query = query.filter(self.model.nombre_proveedor.like(f"%{filtro.nombre_proveedor}%"))
            if filtro.estado_recepcion:
                query = query.filter(self.model.estado_recepcion == filtro.estado_recepcion)

        return query.count()

    def get_estadisticas_resumen(self, db: Session) -> dict:
        """Obtener estadísticas generales de órdenes"""
        total_ordenes = db.query(self.model).count()
        ordenes_pendientes = db.query(self.model).filter(self.model.estado_recepcion == 'PENDIENTE').count()
        ordenes_parciales = db.query(self.model).filter(self.model.estado_recepcion == 'PARCIAL').count()
        ordenes_completas = db.query(self.model).filter(self.model.estado_recepcion == 'COMPLETA').count()

        valor_total = db.query(func.sum(self.model.total)).scalar() or 0
        valor_pendiente = db.query(func.sum(self.model.total)).filter(
            self.model.estado_recepcion.in_(['PENDIENTE', 'PARCIAL'])
        ).scalar() or 0

        return {
            "total_ordenes": total_ordenes,
            "ordenes_pendientes": ordenes_pendientes,
            "ordenes_parciales": ordenes_parciales,
            "ordenes_completas": ordenes_completas,
            "valor_total": float(valor_total),
            "valor_pendiente": float(valor_pendiente)
        }


class VistaOrdenesDetalleCompletoCRUD:
    """CRUD para vista detalle completo de órdenes"""

    def __init__(self, db: Session = None):
        self.db = db
        self.model = models.VistaOrdenesDetalleCompleto

    def get_multi_filtered(self, db: Session, skip: int = 0, limit: int = 100,
                          filtro: Optional[schemas.VistaOrdenesDetalleCompletoFilters] = None) -> List[models.VistaOrdenesDetalleCompleto]:
        """Obtener múltiples registros con filtros avanzados"""
        query = db.query(self.model)

        if filtro:
            if filtro.numero_orden:
                query = query.filter(self.model.numero_orden.like(f"%{filtro.numero_orden}%"))
            if filtro.sku:
                query = query.filter(self.model.sku.like(f"%{filtro.sku}%"))
            if filtro.producto_nombre:
                query = query.filter(self.model.producto_nombre.like(f"%{filtro.producto_nombre}%"))
            if filtro.nombre_proveedor:
                query = query.filter(self.model.nombre_proveedor.like(f"%{filtro.nombre_proveedor}%"))
            if filtro.fecha_entrega_desde:
                query = query.filter(self.model.fecha_entrega_esperada >= filtro.fecha_entrega_desde)
            if filtro.fecha_entrega_hasta:
                query = query.filter(self.model.fecha_entrega_esperada <= filtro.fecha_entrega_hasta)
            if filtro.cantidad_pendiente_mayor_que:
                query = query.filter(self.model.cantidad_pendiente > filtro.cantidad_pendiente_mayor_que)

        return query.order_by(self.model.numero_orden, self.model.numero_linea).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, detalle_id: int) -> Optional[models.VistaOrdenesDetalleCompleto]:
        """Obtener por ID"""
        return db.query(self.model).filter(self.model.id_detalle == detalle_id).first()

    def get_by_orden(self, db: Session, numero_orden: str) -> List[models.VistaOrdenesDetalleCompleto]:
        """Obtener detalles por número de orden"""
        return db.query(self.model).filter(
            self.model.numero_orden == numero_orden
        ).order_by(self.model.numero_linea).all()

    def get_productos_pendientes(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.VistaOrdenesDetalleCompleto]:
        """Obtener productos con cantidades pendientes"""
        return db.query(self.model).filter(
            self.model.cantidad_pendiente > 0
        ).order_by(self.model.fecha_entrega_esperada.asc()).offset(skip).limit(limit).all()

    def contar_con_filtros(self, db: Session, filtro: Optional[schemas.VistaOrdenesDetalleCompletoFilters] = None) -> int:
        """Contar registros con filtros aplicados"""
        query = db.query(self.model)

        if filtro:
            if filtro.numero_orden:
                query = query.filter(self.model.numero_orden.like(f"%{filtro.numero_orden}%"))
            if filtro.sku:
                query = query.filter(self.model.sku.like(f"%{filtro.sku}%"))
            if filtro.cantidad_pendiente_mayor_que:
                query = query.filter(self.model.cantidad_pendiente > filtro.cantidad_pendiente_mayor_que)

        return query.count()


# Instancias globales
vista_ordenes_compra_resumen_crud = VistaOrdenesCompraResumenCRUD()
vista_ordenes_detalle_completo_crud = VistaOrdenesDetalleCompletoCRUD()
