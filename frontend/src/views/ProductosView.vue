<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <h4 class="q-my-none">Catálogo de Productos</h4>
          <p class="text-grey-7 q-mb-none">Gestión integral de productos contra incendios</p>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nuevo Producto"
          @click="abrirFormularioProducto"
        />
      </div>

      <!-- Filters -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="row q-gutter-md items-center">
            <q-input
              v-model="filtros.busqueda"
              placeholder="Buscar por SKU, nombre o modelo..."
              outlined
              dense
              clearable
              style="min-width: 300px"
            >
              <template v-slot:prepend>
                <q-icon name="search" />
              </template>
            </q-input>
            <q-select
              v-model="filtros.marca"
              :options="marcasOptions"
              label="Marca"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 150px"
            />
            <q-select
              v-model="filtros.tipo"
              :options="tiposOptions"
              label="Tipo"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 150px"
            />
            <q-select
              v-model="filtros.estado"
              :options="estadoOptions"
              label="Estado"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 120px"
            />
            <q-btn
              color="primary"
              icon="search"
              label="Buscar"
              @click="buscarProductos"
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Products Table -->
      <q-table
        :rows="productosFiltrados"
        :columns="columnsProductos"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_producto"
        flat
        bordered
        @request="onRequestProductos"
      >
        <template v-slot:body-cell-activo="props">
          <q-td :props="props">
            <q-badge
              :color="props.value ? 'green' : 'red'"
              :label="props.value ? 'Activo' : 'Inactivo'"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-stock_actual="props">
          <q-td :props="props">
            <q-badge
              :color="getStockColor(props.row)"
              :label="props.value || 0"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-marca="props">
          <q-td :props="props">
            {{ getMarcaNombre(props.row.id_marca) }}
          </q-td>
        </template>

        <template v-slot:body-cell-tipo_producto="props">
          <q-td :props="props">
            {{ getTipoNombre(props.row.id_tipo_producto) }}
          </q-td>
        </template>

        <template v-slot:body-cell-precio_venta="props">
          <q-td :props="props">
            <span v-if="props.value" class="text-weight-medium">
              ${{ Number(props.value).toLocaleString() }}
            </span>
            <span v-else class="text-grey-5">-</span>
          </q-td>
        </template>

        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn
              flat
              round
              icon="visibility"
              color="info"
              size="sm"
              @click="verDetalleProducto(props.row as Producto)"
            >
              <q-tooltip>Ver Detalles</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="edit"
              color="primary"
              size="sm"
              @click="editarProducto(props.row as Producto)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              :icon="props.row.activo ? 'block' : 'check_circle'"
              :color="props.row.activo ? 'negative' : 'positive'"
              size="sm"
              @click="toggleEstadoProducto(props.row as Producto)"
            >
              <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Product Dialog -->
      <q-dialog v-model="showCreateProductoDialog" persistent>
        <q-card style="min-width: 1200px; max-width: 1400px; max-height: 90vh">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">{{ editandoProducto ? 'Editar' : 'Nuevo' }} Producto</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section class="q-pt-none" style="max-height: calc(90vh - 120px);">
            <q-form @submit="guardarProducto">
              <div class="row" style="height: calc(90vh - 160px);">
                <div class="col-3">
                  <q-tabs
                    v-model="tabActivo"
                    vertical
                    class="text-primary full-height"
                  >
                    <q-tab name="basica" icon="info" label="Información Básica" />
                    <q-tab name="tecnica" icon="engineering" label="Especificaciones Técnicas" />
                    <q-tab name="certificaciones" icon="verified" label="Certificaciones" />
                    <q-tab name="inventario" icon="inventory" label="Control de Inventario" />
                    <q-tab name="proveedores" icon="business" label="Proveedores" />
                    <q-tab name="ubicaciones" icon="location_on" label="Ubicaciones Físicas" />
                    <q-tab name="almacenamiento" icon="warehouse" label="Almacenamiento" />
                  </q-tabs>
                </div>
                <div class="col-9">
                  <q-tab-panels
                    v-model="tabActivo"
                    animated
                    class="full-height"
                    style="overflow-y: auto;"
                  >
                    <!-- Panel Información Básica -->
                    <q-tab-panel name="basica">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="info" class="q-mr-sm" />
                        Información Básica
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formProducto.sku"
                            label="SKU *"
                            outlined
                            dense
                            maxlength="50"
                            :rules="[val => !!val || 'El SKU es requerido']"
                            hint="Código único del producto"
                          />
                        </div>
                        <div class="col-12 col-md-7">
                          <q-input
                            v-model="formProducto.nombre_producto"
                            label="Nombre del Producto *"
                            outlined
                            dense
                            maxlength="200"
                            :rules="[val => !!val || 'El nombre es requerido']"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-6">
                          <q-select
                            v-model="formProducto.id_marca"
                            :options="marcasOptions"
                            label="Marca"
                            outlined
                            dense
                            emit-value
                            map-options
                            clearable
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formProducto.modelo"
                            label="Modelo"
                            outlined
                            dense
                            maxlength="100"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-6">
                          <q-select
                            v-model="formProducto.id_tipo_producto"
                            :options="tiposOptions"
                            label="Tipo de Producto *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'El tipo es requerido']"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-select
                            v-model="formProducto.id_unidad_medida"
                            :options="unidadesOptions"
                            label="Unidad de Medida *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'La unidad es requerida']"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formProducto.descripcion_corta"
                            label="Descripción Corta"
                            outlined
                            dense
                            maxlength="500"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formProducto.descripcion_detallada"
                            label="Descripción Detallada"
                            outlined
                            type="textarea"
                            rows="4"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12">
                          <q-toggle
                            v-model="formProducto.activo"
                            label="Producto Activo"
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Especificaciones Técnicas -->
                    <q-tab-panel name="tecnica">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="engineering" class="q-mr-sm" />
                        Especificaciones Técnicas
                      </div>

                      <!-- Dimensiones y Peso -->
                      <div class="text-subtitle1 q-mb-sm">Dimensiones y Peso</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-3">
                          <q-input
                            v-model.number="formProducto.dimensiones_largo_cm"
                            label="Largo (cm)"
                            outlined
                            dense
                            type="number"
                            step="0.1"
                            min="0"
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-input
                            v-model.number="formProducto.dimensiones_ancho_cm"
                            label="Ancho (cm)"
                            outlined
                            dense
                            type="number"
                            step="0.1"
                            min="0"
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-input
                            v-model.number="formProducto.dimensiones_alto_cm"
                            label="Alto (cm)"
                            outlined
                            dense
                            type="number"
                            step="0.1"
                            min="0"
                          />
                        </div>
                        <div class="col-12 col-md-2">
                          <q-input
                            v-model.number="formProducto.peso_kg"
                            label="Peso (kg)"
                            outlined
                            dense
                            type="number"
                            step="0.01"
                            min="0"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formProducto.material_principal"
                            label="Material Principal"
                            outlined
                            dense
                            hint="Ej: Bronce, Acero Inoxidable"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formProducto.color"
                            label="Color"
                            outlined
                            dense
                          />
                        </div>
                      </div>

                      <!-- Operación -->
                      <div class="text-subtitle1 q-mb-sm q-mt-lg">Parámetros de Operación</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model.number="formProducto.presion_trabajo_bar"
                            label="Presión de Trabajo (bar)"
                            outlined
                            dense
                            type="number"
                            step="0.1"
                            min="0"
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model.number="formProducto.presion_maxima_bar"
                            label="Presión Máxima (bar)"
                            outlined
                            dense
                            type="number"
                            step="0.1"
                            min="0"
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-input
                            v-model.number="formProducto.factor_k"
                            label="Factor K"
                            outlined
                            dense
                            type="number"
                            step="0.1"
                            hint="Para rociadores"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model.number="formProducto.temperatura_min_celsius"
                            label="Temp. Mín. (°C)"
                            outlined
                            dense
                            type="number"
                            step="1"
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model.number="formProducto.temperatura_max_celsius"
                            label="Temp. Máx. (°C)"
                            outlined
                            dense
                            type="number"
                            step="1"
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-input
                            v-model.number="formProducto.temperatura_activacion_celsius"
                            label="Temp. Activación (°C)"
                            outlined
                            dense
                            type="number"
                            step="1"
                          />
                        </div>
                      </div>

                      <!-- Conexiones -->
                      <div class="text-subtitle1 q-mb-sm q-mt-lg">Conexiones</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formProducto.conexion_entrada"
                            label="Conexión Entrada"
                            outlined
                            dense
                            hint="Ej: NPT 1/2, BSP 3/4"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formProducto.conexion_salida"
                            label="Conexión Salida"
                            outlined
                            dense
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Certificaciones -->
                    <q-tab-panel name="certificaciones">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="verified" class="q-mr-sm" />
                        Certificaciones
                      </div>

                      <!-- Certificaciones Principales -->
                      <div class="text-subtitle1 q-mb-sm">Certificaciones Principales</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formProducto.certificacion_ul"
                            label="Certificación UL"
                            outlined
                            dense
                            hint="Ej: UL 199"
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formProducto.certificacion_fm"
                            label="Certificación FM"
                            outlined
                            dense
                          />
                        </div>
                      </div>


                    </q-tab-panel>

                    <!-- Panel Control de Inventario -->
                    <q-tab-panel name="inventario">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="inventory" class="q-mr-sm" />
                        Control de Inventario
                      </div>

                      <!-- Stock -->
                      <div class="text-subtitle1 q-mb-sm">Niveles de Stock</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model.number="formProducto.stock_minimo"
                            label="Stock Mínimo *"
                            outlined
                            dense
                            type="number"
                            min="0"
                            :rules="[val => val >= 0 || 'Debe ser mayor o igual a 0']"
                          />
                        </div>
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model.number="formProducto.stock_maximo"
                            label="Stock Máximo *"
                            outlined
                            dense
                            type="number"
                            min="0"
                            :rules="[val => val >= 0 || 'Debe ser mayor o igual a 0']"
                          />
                        </div>
                      </div>


                      <!-- Costos -->
                      <div class="text-subtitle1 q-mb-sm q-mt-lg">Información Financiera</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model.number="formProducto.costo_promedio"
                            label="Costo Promedio"
                            outlined
                            dense
                            type="number"
                            step="0.01"
                            min="0"
                            prefix="$"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model.number="formProducto.precio_venta"
                            label="Precio de Venta"
                            outlined
                            dense
                            type="number"
                            step="0.01"
                            min="0"
                            prefix="$"
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Proveedores -->
                    <q-tab-panel name="proveedores">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="business" class="q-mr-sm" />
                        Proveedores del Producto
                      </div>

                      <div class="row items-center justify-between q-mb-md">
                        <div class="text-subtitle2">Relaciones Comerciales</div>
                        <q-btn
                          color="primary"
                          icon="add"
                          label="Agregar Proveedor"
                          size="sm"
                          @click="abrirFormularioProductoProveedor"
                          :disable="!formProducto.id_producto || !proveedoresEndpointDisponible"
                        />
                      </div>

                      <q-card flat bordered v-if="!formProducto.id_producto">
                        <q-card-section class="text-center text-grey-6">
                          <q-icon name="info" size="md" class="q-mb-sm" />
                          <div>Guarde el producto primero para gestionar proveedores</div>
                        </q-card-section>
                      </q-card>

                      <q-card flat bordered v-else-if="!proveedoresEndpointDisponible" class="q-mb-md">
                        <q-card-section class="text-center text-grey-6">
                          <q-icon name="info" size="md" class="q-mb-sm" />
                          <div>Gestión de proveedores temporalmente no disponible</div>
                          <div class="text-caption">El servidor no tiene el endpoint necesario configurado</div>
                        </q-card-section>
                      </q-card>

                      <q-table
                        v-else
                        :rows="productoProveedoresList"
                        :columns="columnsProductoProveedores"
                        :loading="isLoadingProveedores"
                        row-key="id_producto_proveedor"
                        flat
                        bordered
                        dense
                      >
                        <template v-slot:body-cell-es_proveedor_principal="props">
                          <q-td :props="props">
                            <q-badge
                              :color="props.value ? 'primary' : 'grey'"
                              :label="props.value ? 'Principal' : 'Secundario'"
                            />
                          </q-td>
                        </template>

                        <template v-slot:body-cell-precio_proveedor="props">
                          <q-td :props="props">
                            <span v-if="props.value && props.value > 0" class="text-weight-medium">
                              ${{ Number(props.value).toLocaleString() }} {{ props.row.moneda || 'CLP' }}
                            </span>
                            <span v-else class="text-grey-5">-</span>
                          </q-td>
                        </template>


                        <template v-slot:body-cell-activo="props">
                          <q-td :props="props">
                            <q-badge
                              :color="props.value ? 'green' : 'red'"
                              :label="props.value ? 'Activo' : 'Inactivo'"
                            />
                          </q-td>
                        </template>

                        <template v-slot:body-cell-actions="props">
                          <q-td :props="props">
                            <q-btn
                              flat
                              round
                              icon="edit"
                              color="primary"
                              size="sm"
                              @click="editarProductoProveedor(props.row)"
                            >
                              <q-tooltip>Editar</q-tooltip>
                            </q-btn>
                            <q-btn
                              v-if="!props.row.es_proveedor_principal"
                              flat
                              round
                              icon="star"
                              color="warning"
                              size="sm"
                              @click="establecerProveedorPrincipal(props.row)"
                            >
                              <q-tooltip>Establecer como Principal</q-tooltip>
                            </q-btn>
                            <q-btn
                              flat
                              round
                              :icon="props.row.activo ? 'block' : 'check_circle'"
                              :color="props.row.activo ? 'negative' : 'positive'"
                              size="sm"
                              @click="toggleEstadoProductoProveedor(props.row)"
                            >
                              <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
                            </q-btn>
                          </q-td>
                        </template>
                      </q-table>
                    </q-tab-panel>

                    <!-- Panel Ubicaciones Físicas -->
                    <q-tab-panel name="ubicaciones">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="location_on" class="q-mr-sm" />
                        Ubicaciones Físicas del Producto
                      </div>

                      <div class="row items-center justify-between q-mb-md">
                        <div class="text-subtitle2">
                          Distribución en Almacenes
                          <q-badge v-if="stockConsolidado" :label="`Total: ${stockConsolidado.stock_total}`" color="primary" class="q-ml-sm" />
                          <q-badge v-if="stockConsolidado" :label="`Disponible: ${stockConsolidado.stock_disponible}`" color="positive" class="q-ml-xs" />
                          <q-badge v-if="stockConsolidado && stockConsolidado.stock_reservado > 0" :label="`Reservado: ${stockConsolidado.stock_reservado}`" color="warning" class="q-ml-xs" />
                        </div>
                        <div>
                          <q-btn
                            color="primary"
                            icon="add_location"
                            label="Nueva Ubicación"
                            size="sm"
                            @click="abrirFormularioUbicacion"
                            :disable="!formProducto.id_producto"
                          />
                        </div>
                      </div>

                      <q-card flat bordered v-if="!formProducto.id_producto">
                        <q-card-section class="text-center text-grey-6">
                          <q-icon name="info" size="md" class="q-mb-sm" />
                          <div>Guarde el producto primero para gestionar ubicaciones</div>
                        </q-card-section>
                      </q-card>

                      <q-table
                        v-else
                        :rows="productoUbicacionesList"
                        :columns="columnsProductoUbicaciones"
                        :loading="isLoadingUbicaciones"
                        row-key="id_producto_ubicacion"
                        flat
                        bordered
                        dense
                      >
                        <template v-slot:body-cell-ubicacion="props">
                          <q-td :props="props">
                            <div class="text-weight-medium">{{ getUbicacionCompleta(props.row) }}</div>
                            <div class="text-caption text-grey-6" v-if="props.row.ubicacion_descripcion">
                              {{ props.row.ubicacion_descripcion }}
                            </div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-cantidad_actual="props">
                          <q-td :props="props">
                            <div class="text-weight-medium text-center">
                              {{ Number(props.value).toLocaleString() }}
                            </div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-cantidad_reservada="props">
                          <q-td :props="props">
                            <div class="text-center">
                              <q-badge
                                v-if="props.value && props.value > 0"
                                :label="Number(props.value).toLocaleString()"
                                color="warning"
                              />
                              <span v-else class="text-grey-5">-</span>
                            </div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-cantidad_disponible="props">
                          <q-td :props="props">
                            <div class="text-center">
                              <q-badge
                                :label="Number(props.value).toLocaleString()"
                                :color="props.value > 0 ? 'positive' : 'grey'"
                              />
                            </div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-ultimo_conteo="props">
                          <q-td :props="props">
                            <div v-if="props.row.fecha_ultimo_conteo" class="text-center">
                              <div class="text-caption">{{ formatDate(props.row.fecha_ultimo_conteo) }}</div>
                              <q-badge
                                :color="getConteoColor(props.row.fecha_ultimo_conteo)"
                                :label="getConteoLabel(props.row.fecha_ultimo_conteo)"
                                class="q-mt-xs"
                              />
                            </div>
                            <div v-else class="text-center text-grey-5">Sin conteo</div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-activo="props">
                          <q-td :props="props">
                            <q-badge
                              :color="props.value ? 'green' : 'red'"
                              :label="props.value ? 'Activa' : 'Inactiva'"
                            />
                          </q-td>
                        </template>

                        <template v-slot:body-cell-actions="props">
                          <q-td :props="props">
                            <q-btn
                              flat
                              round
                              icon="edit_location"
                              color="primary"
                              size="sm"
                              @click="editarUbicacion(props.row)"
                            >
                              <q-tooltip>Editar Ubicación</q-tooltip>
                            </q-btn>
                            <q-btn
                              flat
                              round
                              icon="swap_horiz"
                              color="info"
                              size="sm"
                              @click="transferirUbicacion(props.row)"
                            >
                              <q-tooltip>Transferir</q-tooltip>
                            </q-btn>
                            <q-btn
                              flat
                              round
                              icon="tune"
                              color="warning"
                              size="sm"
                              @click="ajustarCantidad(props.row)"
                            >
                              <q-tooltip>Ajustar Cantidad</q-tooltip>
                            </q-btn>
                            <q-btn
                              flat
                              round
                              icon="bookmark_border"
                              color="secondary"
                              size="sm"
                              @click="gestionarReserva(props.row)"
                              :disable="props.row.cantidad_disponible <= 0"
                            >
                              <q-tooltip>Gestionar Reserva</q-tooltip>
                            </q-btn>
                            <q-btn
                              flat
                              round
                              icon="history"
                              color="info"
                              size="sm"
                              @click="verMovimientos(props.row)"
                            >
                              <q-tooltip>Ver Movimientos</q-tooltip>
                            </q-btn>
                          </q-td>
                        </template>
                      </q-table>
                    </q-tab-panel>

                    <!-- Panel Almacenamiento -->
                    <q-tab-panel name="almacenamiento">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="warehouse" class="q-mr-sm" />
                        Condiciones de Almacenamiento
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12">
                          <q-input
                            v-model="formProducto.condiciones_especiales"
                            label="Condiciones Especiales"
                            outlined
                            type="textarea"
                            rows="4"
                            hint="Ej: Mantener en lugar seco, evitar exposición solar directa, almacenar a temperatura ambiente"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model.number="formProducto.vida_util_meses"
                            label="Vida Útil (meses)"
                            outlined
                            dense
                            type="number"
                            min="0"
                            hint="Tiempo de vida útil del producto"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-lg">
                        <div class="col-12">
                          <q-toggle
                            v-model="formProducto.requiere_refrigeracion"
                            label="Requiere Refrigeración"
                            size="lg"
                          />
                          <div class="text-caption text-grey-6 q-mt-xs">
                            Activar si el producto requiere almacenamiento refrigerado
                          </div>
                        </div>
                      </div>
                    </q-tab-panel>
                  </q-tab-panels>
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right" class="q-pa-md">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar Producto"
              @click="guardarProducto"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Product Detail Dialog -->
      <q-dialog v-model="showDetalleDialog" persistent>
        <q-card style="min-width: 800px; max-width: 1000px">
          <q-card-section class="row items-center">
            <div class="text-h6">Detalles del Producto</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section v-if="productoDetalle">
            <div class="row q-col-gutter-md">
              <div class="col-12 col-md-6">
                <q-list bordered separator>
                  <q-item-label header>Información Básica</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>SKU</q-item-label>
                      <q-item-label>{{ productoDetalle.sku }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Nombre</q-item-label>
                      <q-item-label>{{ productoDetalle.nombre_producto }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Marca</q-item-label>
                      <q-item-label>{{ getMarcaNombre(productoDetalle.id_marca) }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Modelo</q-item-label>
                      <q-item-label>{{ productoDetalle.modelo || '-' }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>

              <div class="col-12 col-md-6">
                <q-list bordered separator>
                  <q-item-label header>Inventario</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Stock Actual</q-item-label>
                      <q-item-label>
                        <q-badge :color="getStockColor(productoDetalle)">
                          {{ productoDetalle.stock_actual || 0 }}
                        </q-badge>
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Stock Mínimo</q-item-label>
                      <q-item-label>{{ productoDetalle.stock_minimo }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Punto de Reorden</q-item-label>
                      <q-item-label>{{ productoDetalle.punto_reorden }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Precio de Venta</q-item-label>
                      <q-item-label>
                        <span v-if="productoDetalle.precio_venta">
                          ${{ Number(productoDetalle.precio_venta).toLocaleString() }}
                        </span>
                        <span v-else>-</span>
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>
            </div>

            <!-- Especificaciones Técnicas -->
            <q-expansion-item
              icon="engineering"
              label="Especificaciones Técnicas"
              class="q-mt-md"
            >
              <q-card flat bordered>
                <q-card-section>
                  <div class="row q-col-gutter-md">
                    <div class="col-12 col-md-6">
                      <q-list dense>
                        <q-item-label header>Dimensiones y Material</q-item-label>
                        <q-item v-if="productoDetalle.dimensiones_largo_cm">
                          <q-item-section>
                            <q-item-label caption>Dimensiones (L×A×H)</q-item-label>
                            <q-item-label>
                              {{ productoDetalle.dimensiones_largo_cm || '-' }} ×
                              {{ productoDetalle.dimensiones_ancho_cm || '-' }} ×
                              {{ productoDetalle.dimensiones_alto_cm || '-' }} cm
                            </q-item-label>
                          </q-item-section>
                        </q-item>
                        <q-item v-if="productoDetalle.peso_kg">
                          <q-item-section>
                            <q-item-label caption>Peso</q-item-label>
                            <q-item-label>{{ productoDetalle.peso_kg }} kg</q-item-label>
                          </q-item-section>
                        </q-item>
                        <q-item v-if="productoDetalle.material_principal">
                          <q-item-section>
                            <q-item-label caption>Material</q-item-label>
                            <q-item-label>{{ productoDetalle.material_principal }}</q-item-label>
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </div>

                    <div class="col-12 col-md-6">
                      <q-list dense>
                        <q-item-label header>Operación</q-item-label>
                        <q-item v-if="productoDetalle.presion_trabajo_bar">
                          <q-item-section>
                            <q-item-label caption>Presión de Trabajo</q-item-label>
                            <q-item-label>{{ productoDetalle.presion_trabajo_bar }} bar</q-item-label>
                          </q-item-section>
                        </q-item>
                        <q-item v-if="productoDetalle.factor_k">
                          <q-item-section>
                            <q-item-label caption>Factor K</q-item-label>
                            <q-item-label>{{ productoDetalle.factor_k }}</q-item-label>
                          </q-item-section>
                        </q-item>
                        <q-item v-if="productoDetalle.certificacion_ul">
                          <q-item-section>
                            <q-item-label caption>Certificación UL</q-item-label>
                            <q-item-label>{{ productoDetalle.certificacion_ul }}</q-item-label>
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </div>
                  </div>
                </q-card-section>
              </q-card>
            </q-expansion-item>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cerrar" v-close-popup />
            <q-btn
              color="primary"
              label="Editar"
              @click="editarDesdeDetalle"
              v-if="productoDetalle"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Create/Edit Producto Proveedor Dialog -->
      <q-dialog v-model="showCreateProductoProveedorDialog" persistent>
        <q-card style="min-width: 600px; max-width: 800px">
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoProductoProveedor ? 'Editar' : 'Agregar' }} Proveedor</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarProductoProveedor">
              <div class="row q-gutter-md">
                <div class="col-12 col-md-6">
                  <q-select
                    v-model="formProductoProveedor.id_proveedor"
                    :options="proveedoresOptions"
                    label="Proveedor *"
                    outlined
                    dense
                    emit-value
                    map-options
                    :rules="[val => !!val || 'El proveedor es requerido']"
                  />
                </div>
                <div class="col-12 col-md-5">
                  <q-toggle
                    v-model="formProductoProveedor.es_proveedor_principal"
                    label="Proveedor Principal"
                  />
                </div>
              </div>

              <!-- Precios y Condiciones Comerciales -->
              <div class="text-subtitle1 q-mb-sm q-mt-lg">Condiciones Comerciales</div>
              <q-separator class="q-mb-md" />

              <div class="row q-gutter-md">
                <div class="col-12 col-md-4">
                  <q-input
                    v-model.number="formProductoProveedor.precio_proveedor"
                    label="Precio Proveedor"
                    outlined
                    dense
                    type="number"
                    step="0.01"
                    min="0"
                    prefix="$"
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-select
                    v-model="formProductoProveedor.moneda"
                    :options="monedaOptions"
                    label="Moneda"
                    outlined
                    dense
                    emit-value
                    map-options
                  />
                </div>
                <div class="col-12 col-md-3">
                  <q-input
                    v-model.number="formProductoProveedor.descuento_volumen"
                    label="Descuento (%)"
                    outlined
                    dense
                    type="number"
                    step="0.01"
                    min="0"
                    max="100"
                    suffix="%"
                  />
                </div>
              </div>

              <!-- Logística -->
              <div class="text-subtitle1 q-mb-sm q-mt-lg">Logística</div>
              <q-separator class="q-mb-md" />

              <div class="row q-gutter-md">
                <div class="col-12 col-md-4">
                  <q-input
                    v-model.number="formProductoProveedor.tiempo_entrega_dias"
                    label="Tiempo Entrega (días)"
                    outlined
                    dense
                    type="number"
                    min="0"
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-input
                    v-model.number="formProductoProveedor.cantidad_minima"
                    label="Cantidad Mínima"
                    outlined
                    dense
                    type="number"
                    min="1"
                  />
                </div>
              </div>


              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-input
                    v-model="formProductoProveedor.condiciones_especiales"
                    label="Condiciones Especiales"
                    outlined
                    type="textarea"
                    rows="3"
                    hint="Términos comerciales adicionales, garantías, etc."
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-md">
                <div class="col-12">
                  <q-toggle
                    v-model="formProductoProveedor.activo"
                    label="Relación Activa"
                  />
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar"
              @click="guardarProductoProveedor"
              :loading="isGuardandoProveedor"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Create/Edit Ubicación Dialog -->
      <q-dialog v-model="showCreateUbicacionDialog" persistent>
        <q-card style="min-width: 600px; max-width: 800px">
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoUbicacion ? 'Editar' : 'Nueva' }} Ubicación</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarUbicacion">
              <!-- Selección de Ubicación -->
              <div class="text-subtitle1 q-mb-sm">Ubicación Física</div>
              <q-separator class="q-mb-md" />

              <div class="row q-gutter-md">
                <div class="col-12 col-md-4">
                  <q-select
                    v-model="formUbicacion.id_bodega"
                    :options="bodegasOptions"
                    label="Bodega *"
                    outlined
                    dense
                    emit-value
                    map-options
                    :rules="[val => !!val || 'La bodega es requerida']"
                    @update:model-value="cargarPasillos"
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-select
                    v-model="formUbicacion.id_pasillo"
                    :options="pasillosOptions"
                    label="Pasillo"
                    outlined
                    dense
                    emit-value
                    map-options
                    clearable
                    :disable="!formUbicacion.id_bodega"
                    @update:model-value="cargarEstantes"
                  />
                </div>
                <div class="col-12 col-md-3">
                  <q-select
                    v-model="formUbicacion.id_estante"
                    :options="estantesOptions"
                    label="Estante"
                    outlined
                    dense
                    emit-value
                    map-options
                    clearable
                    :disable="!formUbicacion.id_pasillo"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formUbicacion.ubicacion_codigo"
                    label="Código Ubicación"
                    outlined
                    dense
                    hint="Código específico (ej: A1-B2-C3)"
                  />
                </div>
                <div class="col-12 col-md-5">
                  <q-input
                    v-model="formUbicacion.ubicacion_descripcion"
                    label="Descripción"
                    outlined
                    dense
                    hint="Descripción adicional de la ubicación"
                  />
                </div>
              </div>

              <!-- Cantidad Inicial -->
              <div class="text-subtitle1 q-mb-sm q-mt-lg">Cantidad Inicial</div>
              <q-separator class="q-mb-md" />

              <div class="row q-gutter-md">
                <div class="col-12 col-md-4">
                  <q-input
                    v-model.number="formUbicacion.cantidad_actual"
                    label="Cantidad *"
                    outlined
                    dense
                    type="number"
                    min="0"
                    :rules="[val => val >= 0 || 'La cantidad debe ser mayor o igual a 0']"
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-input
                    v-model.number="formUbicacion.cantidad_reservada"
                    label="Cantidad Reservada"
                    outlined
                    dense
                    type="number"
                    min="0"
                    :max="formUbicacion.cantidad_actual"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-input
                    v-model="formUbicacion.observaciones"
                    label="Observaciones"
                    outlined
                    type="textarea"
                    rows="3"
                    hint="Notas sobre la ubicación, condiciones especiales, etc."
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-md">
                <div class="col-12">
                  <q-toggle
                    v-model="formUbicacion.activo"
                    label="Ubicación Activa"
                  />
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar"
              @click="guardarUbicacion"
              :loading="isGuardandoUbicacion"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Transfer Ubicación Dialog -->
      <q-dialog v-model="showTransferDialog" persistent>
        <q-card style="min-width: 500px; max-width: 700px">
          <q-card-section class="row items-center">
            <div class="text-h6">Transferir Producto</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="ejecutarTransferencia">
              <div class="text-subtitle2 q-mb-md">
                Transferir desde: {{ getUbicacionCompleta(ubicacionSeleccionada) }}
              </div>

              <div class="row q-gutter-md">
                <div class="col-12 col-md-4">
                  <q-select
                    v-model="formTransfer.id_bodega"
                    :options="bodegasOptions"
                    label="Nueva Bodega *"
                    outlined
                    dense
                    emit-value
                    map-options
                    @update:model-value="cargarPasillosTransfer"
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-select
                    v-model="formTransfer.id_pasillo"
                    :options="pasillosTransferOptions"
                    label="Nuevo Pasillo"
                    outlined
                    dense
                    emit-value
                    map-options
                    clearable
                    :disable="!formTransfer.id_bodega"
                    @update:model-value="cargarEstantesTransfer"
                  />
                </div>
                <div class="col-12 col-md-3">
                  <q-select
                    v-model="formTransfer.id_estante"
                    :options="estantesTransferOptions"
                    label="Nuevo Estante"
                    outlined
                    dense
                    emit-value
                    map-options
                    clearable
                    :disable="!formTransfer.id_pasillo"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model.number="formTransfer.cantidad"
                    label="Cantidad a Transferir *"
                    outlined
                    dense
                    type="number"
                    min="1"
                    :max="ubicacionSeleccionada?.cantidad_disponible"
                    :rules="[val => val > 0 && val <= (ubicacionSeleccionada?.cantidad_disponible || 0) || 'Cantidad inválida']"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-input
                    v-model="formTransfer.motivo"
                    label="Motivo de Transferencia"
                    outlined
                    dense
                    hint="Razón de la transferencia"
                  />
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Transferir"
              @click="ejecutarTransferencia"
              :loading="isTransfiriendo"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Ajustar Cantidad Dialog -->
      <q-dialog v-model="showAjusteDialog" persistent>
        <q-card style="min-width: 400px; max-width: 600px">
          <q-card-section class="row items-center">
            <div class="text-h6">Ajustar Cantidad</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="ejecutarAjuste">
              <div class="text-subtitle2 q-mb-md">
                Ubicación: {{ getUbicacionCompleta(ubicacionSeleccionada) }}
              </div>

              <div class="q-mb-md">
                <q-badge label="Cantidad Actual" color="info" class="q-mr-sm" />
                <span class="text-h6">{{ ubicacionSeleccionada?.cantidad_actual }}</span>
              </div>

              <div class="row q-gutter-md">
                <div class="col-12 col-md-6">
                  <q-select
                    v-model="formAjuste.tipo_ajuste"
                    :options="tipoAjusteOptions"
                    label="Tipo de Ajuste *"
                    outlined
                    dense
                    emit-value
                    map-options
                  />
                </div>
                <div class="col-12 col-md-5">
                  <q-input
                    v-model.number="formAjuste.cantidad_nueva"
                    label="Nueva Cantidad *"
                    outlined
                    dense
                    type="number"
                    min="0"
                    :rules="[val => val >= 0 || 'La cantidad debe ser mayor o igual a 0']"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-input
                    v-model="formAjuste.motivo"
                    label="Motivo del Ajuste *"
                    outlined
                    dense
                    :rules="[val => !!val || 'El motivo es requerido']"
                    hint="Razón del ajuste de cantidad"
                  />
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Ajustar"
              @click="ejecutarAjuste"
              :loading="isAjustando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Gestionar Reserva Dialog -->
      <q-dialog v-model="showReservaDialog" persistent>
        <q-card style="min-width: 400px; max-width: 600px">
          <q-card-section class="row items-center">
            <div class="text-h6">Gestionar Reserva</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="ejecutarReserva">
              <div class="text-subtitle2 q-mb-md">
                Ubicación: {{ getUbicacionCompleta(ubicacionSeleccionada) }}
              </div>

              <div class="row q-mb-md">
                <div class="col-6">
                  <q-badge label="Disponible" color="positive" class="q-mr-sm" />
                  <span class="text-weight-medium">{{ ubicacionSeleccionada?.cantidad_disponible }}</span>
                </div>
                <div class="col-6">
                  <q-badge label="Reservado" color="warning" class="q-mr-sm" />
                  <span class="text-weight-medium">{{ ubicacionSeleccionada?.cantidad_reservada }}</span>
                </div>
              </div>

              <div class="row q-gutter-md">
                <div class="col-12 col-md-6">
                  <q-select
                    v-model="formReserva.tipo_operacion"
                    :options="tipoReservaOptions"
                    label="Operación *"
                    outlined
                    dense
                    emit-value
                    map-options
                  />
                </div>
                <div class="col-12 col-md-5">
                  <q-input
                    v-model.number="formReserva.cantidad"
                    :label="formReserva.tipo_operacion === 'reservar' ? 'Cantidad a Reservar *' : 'Cantidad a Liberar *'"
                    outlined
                    dense
                    type="number"
                    min="1"
                    :max="formReserva.tipo_operacion === 'reservar' ? ubicacionSeleccionada?.cantidad_disponible : ubicacionSeleccionada?.cantidad_reservada"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-input
                    v-model="formReserva.motivo"
                    label="Motivo"
                    outlined
                    dense
                    hint="Razón de la reserva/liberación"
                  />
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              :label="formReserva.tipo_operacion === 'reservar' ? 'Reservar' : 'Liberar'"
              @click="ejecutarReserva"
              :loading="isGestionandoReserva"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Movimientos Dialog -->
      <q-dialog v-model="showMovimientosDialog" persistent>
        <q-card style="min-width: 800px; max-width: 1000px">
          <q-card-section class="row items-center">
            <div class="text-h6">Historial de Movimientos</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <div class="text-subtitle2 q-mb-md">
              Ubicación: {{ getUbicacionCompleta(ubicacionSeleccionada) }}
            </div>

            <q-table
              :rows="movimientosList"
              :columns="columnsMovimientos"
              :loading="isLoadingMovimientos"
              row-key="id_movimiento"
              flat
              bordered
              dense
            >
              <template v-slot:body-cell-tipo_movimiento="props">
                <q-td :props="props">
                  <q-badge
                    :color="getTipoMovimientoColor(props.value)"
                    :label="getTipoMovimientoLabel(props.value)"
                  />
                </q-td>
              </template>

              <template v-slot:body-cell-cantidad="props">
                <q-td :props="props">
                  <span class="text-weight-medium">{{ Number(props.value).toLocaleString() }}</span>
                </q-td>
              </template>

              <template v-slot:body-cell-fecha_movimiento="props">
                <q-td :props="props">
                  {{ formatDateTime(props.value) }}
                </q-td>
              </template>
            </q-table>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cerrar" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import {
  useProductoStore,
  type Producto,
  type ProductoCreate,
  type ProductoProveedor,
  type ProductoProveedorCreate,
  type ProductoUbicacion,
  type ProductoUbicacionCreate,
  type MovimientoUbicacion
} from '../stores/productos'
import { useProveedorStore } from '../stores/proveedores'
import { useBodegaStore } from '../stores/bodegas'

const $q = useQuasar()
const productoStore = useProductoStore()
const proveedorStore = useProveedorStore()
const bodegaStore = useBodegaStore()

// Reactive data
const productos = ref<Producto[]>([])
const isLoading = ref(false)
const isGuardando = ref(false)
const showCreateProductoDialog = ref(false)
const showDetalleDialog = ref(false)
const editandoProducto = ref(false)
const productoDetalle = ref<Producto | null>(null)

// Product Suppliers
const showCreateProductoProveedorDialog = ref(false)
const editandoProductoProveedor = ref(false)
const isGuardandoProveedor = ref(false)
const isLoadingProveedores = ref(false)
const productoProveedoresList = ref<ProductoProveedor[]>([])
const proveedoresEndpointDisponible = ref(true)
const proveedoresList = ref<any[]>([])

// Product Locations
const showCreateUbicacionDialog = ref(false)
const showTransferDialog = ref(false)
const showAjusteDialog = ref(false)
const showReservaDialog = ref(false)
const showMovimientosDialog = ref(false)
const editandoUbicacion = ref(false)
const isGuardandoUbicacion = ref(false)
const isTransfiriendo = ref(false)
const isAjustando = ref(false)
const isGestionandoReserva = ref(false)
const isLoadingUbicaciones = ref(false)
const isLoadingMovimientos = ref(false)
const productoUbicacionesList = ref<ProductoUbicacion[]>([])
const movimientosList = ref<MovimientoUbicacion[]>([])
const ubicacionSeleccionada = ref<ProductoUbicacion | null>(null)
const stockConsolidado = ref<any>(null)

// Warehouse data
const bodegasList = ref<any[]>([])
const pasillosList = ref<any[]>([])
const estantesList = ref<any[]>([])
const pasillosTransferList = ref<any[]>([])
const estantesTransferList = ref<any[]>([])

const tabActivo = ref('basica')

// Filters
const filtros = ref({
  busqueda: '',
  marca: null as number | null,
  tipo: null as number | null,
  estado: null as boolean | null
})

const estadoOptions = [
  { label: 'Activo', value: true },
  { label: 'Inactivo', value: false }
]

// Pagination
const paginacion = ref({
  sortBy: 'sku',
  descending: false,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Forms
const formProducto = ref<ProductoCreate & { id_producto?: number }>({
  sku: '',
  nombre_producto: '',
  descripcion_corta: '',
  descripcion_detallada: '',
  id_marca: undefined,
  modelo: '',
  numero_parte: '',
  id_tipo_producto: 0,
  id_unidad_medida: 0,

  // Especificaciones técnicas
  peso_kg: undefined,
  dimensiones_largo_cm: undefined,
  dimensiones_ancho_cm: undefined,
  dimensiones_alto_cm: undefined,
  material_principal: '',
  color: '',

  // Información para sistemas contra incendios
  presion_trabajo_bar: undefined,
  presion_maxima_bar: undefined,
  temperatura_min_celsius: undefined,
  temperatura_max_celsius: undefined,
  temperatura_activacion_celsius: undefined,
  factor_k: undefined,
  conexion_entrada: '',
  conexion_salida: '',

  // Certificaciones
  certificacion_ul: '',
  certificacion_fm: '',

  // Control de inventario
  stock_minimo: 0,
  stock_maximo: 0,
  costo_promedio: undefined,
  precio_venta: undefined,

  // Almacenamiento
  condiciones_especiales: '',
  vida_util_meses: undefined,
  requiere_refrigeracion: false,

  activo: true
})

const formProductoProveedor = ref<ProductoProveedorCreate & { id_producto_proveedor?: number }>({
  id_producto: 0,
  id_proveedor: 0,
  es_proveedor_principal: false,
  precio_proveedor: undefined,
  moneda: 'CLP',
  tiempo_entrega_dias: undefined,
  cantidad_minima: undefined,
  descuento_volumen: undefined,
  condiciones_especiales: '',
  activo: true
})

const monedaOptions = [
  { label: 'CLP - Peso Chileno', value: 'CLP' },
  { label: 'USD - Dólar Americano', value: 'USD' },
  { label: 'EUR - Euro', value: 'EUR' }
]

// Computed
const marcasOptions = computed(() => {
  return productoStore.marcas.map(marca => ({
    label: marca.nombre_marca,
    value: marca.id_marca
  }))
})

const tiposOptions = computed(() => {
  return productoStore.tiposProducto.map(tipo => ({
    label: `${tipo.codigo_tipo} - ${tipo.nombre_tipo}`,
    value: tipo.id_tipo_producto
  }))
})

const unidadesOptions = computed(() => {
  return productoStore.unidadesMedida.map(unidad => ({
    label: `${unidad.codigo_unidad} - ${unidad.nombre_unidad}`,
    value: unidad.id_unidad
  }))
})

const proveedoresOptions = computed(() => {
  return proveedoresList.value.map(proveedor => ({
    label: `${proveedor.codigo_proveedor} - ${proveedor.nombre_proveedor}`,
    value: proveedor.id_proveedor
  }))
})

const productosFiltrados = computed(() => {
  let resultado = [...productos.value]

  // Filtrar por búsqueda
  if (filtros.value.busqueda && filtros.value.busqueda.trim()) {
    const busqueda = filtros.value.busqueda.toLowerCase().trim()
    resultado = resultado.filter(producto =>
      producto.sku.toLowerCase().includes(busqueda) ||
      producto.nombre_producto.toLowerCase().includes(busqueda) ||
      (producto.modelo && producto.modelo.toLowerCase().includes(busqueda)) ||
      (producto.descripcion_corta && producto.descripcion_corta.toLowerCase().includes(busqueda))
    )
  }

  // Filtrar por marca
  if (filtros.value.marca !== null) {
    resultado = resultado.filter(producto => producto.id_marca === filtros.value.marca)
  }

  // Filtrar por tipo
  if (filtros.value.tipo !== null) {
    resultado = resultado.filter(producto => producto.id_tipo_producto === filtros.value.tipo)
  }

  // Filtrar por estado
  if (filtros.value.estado !== null) {
    resultado = resultado.filter(producto => producto.activo === filtros.value.estado)
  }

  return resultado
})

// Table columns
const columnsProductos = [
  {
    name: 'sku',
    required: true,
    label: 'SKU',
    align: 'left' as const,
    field: 'sku',
    sortable: true
  },
  {
    name: 'nombre_producto',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_producto',
    sortable: true
  },
  {
    name: 'marca',
    label: 'Marca',
    align: 'left' as const,
    field: 'id_marca'
  },
  {
    name: 'modelo',
    label: 'Modelo',
    align: 'left' as const,
    field: 'modelo',
    sortable: true
  },
  {
    name: 'tipo_producto',
    label: 'Tipo',
    align: 'left' as const,
    field: 'id_tipo_producto'
  },
  {
    name: 'stock_actual',
    label: 'Stock',
    align: 'center' as const,
    field: 'stock_actual',
    sortable: true
  },
  {
    name: 'precio_venta',
    label: 'Precio',
    align: 'right' as const,
    field: 'precio_venta',
    sortable: true
  },
  {
    name: 'activo',
    label: 'Estado',
    align: 'center' as const,
    field: 'activo',
    sortable: true
  },
  {
    name: 'actions',
    label: 'Acciones',
    align: 'center' as const,
    field: 'actions'
  }
]

// Table columns for producto proveedores
const columnsProductoProveedores = [
  {
    name: 'proveedor',
    required: true,
    label: 'Proveedor',
    align: 'left' as const,
    field: (row: ProductoProveedor) => getProveedorNombre(row.id_proveedor),
    sortable: true
  },
  {
    name: 'es_proveedor_principal',
    label: 'Tipo',
    align: 'center' as const,
    field: 'es_proveedor_principal',
    sortable: true
  },
  {
    name: 'precio_proveedor',
    label: 'Precio',
    align: 'right' as const,
    field: 'precio_proveedor',
    sortable: true
  },
  {
    name: 'tiempo_entrega_dias',
    label: 'Entrega (días)',
    align: 'center' as const,
    field: 'tiempo_entrega_dias',
    sortable: true
  },
  {
    name: 'cantidad_minima',
    label: 'Cant. Mín.',
    align: 'center' as const,
    field: 'cantidad_minima',
    sortable: true
  },
  {
    name: 'activo',
    label: 'Estado',
    align: 'center' as const,
    field: 'activo',
    sortable: true
  },
  {
    name: 'actions',
    label: 'Acciones',
    align: 'center' as const,
    field: 'actions'
  }
]

// Methods
const onRequestProductos = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarProductos()
}

const cargarProductos = async () => {
  try {
    isLoading.value = true
    const params = {
      skip: (paginacion.value.page - 1) * paginacion.value.rowsPerPage,
      limit: paginacion.value.rowsPerPage
    }

    const response = await productoStore.obtenerProductos(params)
    productos.value = response

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar productos',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const cargarDatosRelacionados = async () => {
  try {
    await Promise.all([
      productoStore.obtenerMarcas(),
      productoStore.obtenerTiposProducto(),
      productoStore.obtenerUnidadesMedida()
    ])
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar datos relacionados',
      caption: error.message
    })
  }
}

const buscarProductos = async () => {
  paginacion.value.page = 1
  await cargarProductos()
}

const abrirFormularioProducto = () => {
  resetFormProducto()
  showCreateProductoDialog.value = true
}


const verDetalleProducto = async (producto: Producto) => {
  try {
    productoDetalle.value = await productoStore.obtenerProducto(producto.id_producto)
    showDetalleDialog.value = true
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar detalles del producto',
      caption: error.message
    })
  }
}

const editarDesdeDetalle = () => {
  if (productoDetalle.value) {
    showDetalleDialog.value = false
    editarProducto(productoDetalle.value)
  }
}

const guardarProducto = async () => {
  try {
    isGuardando.value = true

    if (editandoProducto.value && formProducto.value.id_producto) {
      await productoStore.actualizarProducto(formProducto.value.id_producto, formProducto.value)
      $q.notify({
        type: 'positive',
        message: 'Producto actualizado correctamente'
      })
    } else {
      await productoStore.crearProducto(formProducto.value)
      $q.notify({
        type: 'positive',
        message: 'Producto creado correctamente'
      })
    }

    showCreateProductoDialog.value = false
    resetFormProducto()
    await cargarProductos()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar producto',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoProducto = async (producto: Producto) => {
  try {
    if (producto.activo) {
      // Desactivar
      await productoStore.eliminarProducto(producto.id_producto, false)
      $q.notify({
        type: 'positive',
        message: 'Producto desactivado'
      })
    } else {
      // Activar
      await productoStore.activarProducto(producto.id_producto)
      $q.notify({
        type: 'positive',
        message: 'Producto activado'
      })
    }

    await cargarProductos()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado del producto',
      caption: error.message
    })
  }
}

const resetFormProducto = () => {
  editandoProducto.value = false
  tabActivo.value = 'basica'
  formProducto.value = {
    sku: '',
    nombre_producto: '',
    descripcion_corta: '',
    descripcion_detallada: '',
    id_marca: undefined,
    modelo: '',
    numero_parte: '',
    id_tipo_producto: 0,
    id_unidad_medida: 0,

    // Especificaciones técnicas
    peso_kg: undefined,
    dimensiones_largo_cm: undefined,
    dimensiones_ancho_cm: undefined,
    dimensiones_alto_cm: undefined,
    material_principal: '',
    color: '',

    // Información para sistemas contra incendios
    presion_trabajo_bar: undefined,
    presion_maxima_bar: undefined,
    temperatura_min_celsius: undefined,
    temperatura_max_celsius: undefined,
    temperatura_activacion_celsius: undefined,
    factor_k: undefined,
    conexion_entrada: '',
    conexion_salida: '',

    // Certificaciones
    certificacion_ul: '',
    certificacion_fm: '',

    // Control de inventario
    stock_minimo: 0,
    stock_maximo: 0,
    costo_promedio: undefined,
    precio_venta: undefined,

    // Almacenamiento
    condiciones_especiales: '',
    vida_util_meses: undefined,
    requiere_refrigeracion: false,

    activo: true
  }
}

// Helper methods
const getMarcaNombre = (marcaId?: number): string => {
  if (!marcaId) return '-'
  const marca = productoStore.marcas.find(m => m.id_marca === marcaId)
  return marca?.nombre_marca || '-'
}

const getTipoNombre = (tipoId: number): string => {
  const tipo = productoStore.tiposProducto.find(t => t.id_tipo_producto === tipoId)
  return tipo ? `${tipo.codigo_tipo} - ${tipo.nombre_tipo}` : '-'
}

const getStockColor = (producto: Producto): string => {
  const stock = producto.stock_actual || 0
  if (stock <= 0) return 'negative'
  if (stock <= producto.punto_reorden) return 'warning'
  if (stock <= producto.stock_minimo) return 'orange'
  return 'positive'
}

// Product Suppliers Methods
const cargarProveedores = async () => {
  try {
    const response = await proveedorStore.obtenerProveedores({ activo: true })
    proveedoresList.value = response
  } catch (error: any) {
    console.error('Error al cargar proveedores:', error)
  }
}

const cargarProductoProveedores = async (productoId: number) => {
  if (!productoId || productoId <= 0) {
    console.warn('ProductoId inválido para cargar proveedores:', productoId)
    return
  }

  try {
    isLoadingProveedores.value = true
    const response = await productoStore.obtenerProductoProveedores(productoId)
    productoProveedoresList.value = response || []

    // Log informativo
    if (response && response.length > 0) {
      console.log(`Cargados ${response.length} proveedores para el producto ${productoId}`)
    } else {
      console.log(`No se encontraron proveedores para el producto ${productoId}`)
    }
  } catch (error: any) {
    console.error('Error al cargar proveedores del producto:', error)

    // Si es 404, es probable que el endpoint no exista - no mostrar error al usuario
    if (error.response?.status === 404 || error.message?.includes('404')) {
      console.log('Endpoint de producto-proveedores no disponible (404), continuando sin proveedores')
      proveedoresEndpointDisponible.value = false
      productoProveedoresList.value = []
    } else {
      // Solo mostrar notificación para otros errores
      $q.notify({
        type: 'negative',
        message: 'Error al cargar proveedores del producto',
        caption: error.message
      })
      productoProveedoresList.value = []
    }
  } finally {
    isLoadingProveedores.value = false
  }
}

const abrirFormularioProductoProveedor = () => {
  if (!formProducto.value.id_producto || formProducto.value.id_producto <= 0) {
    $q.notify({
      type: 'negative',
      message: 'Error',
      caption: 'Debe crear o seleccionar un producto antes de agregar proveedores'
    })
    return
  }

  resetFormProductoProveedor()
  formProductoProveedor.value.id_producto = formProducto.value.id_producto
  showCreateProductoProveedorDialog.value = true
}

const editarProductoProveedor = (productoProveedor: ProductoProveedor) => {
  editandoProductoProveedor.value = true
  formProductoProveedor.value = { ...productoProveedor }
  showCreateProductoProveedorDialog.value = true
}

const guardarProductoProveedor = async () => {
  try {
    isGuardandoProveedor.value = true

    // Validaciones antes de enviar
    if (!formProductoProveedor.value.id_producto || formProductoProveedor.value.id_producto <= 0) {
      $q.notify({
        type: 'negative',
        message: 'Error de validación',
        caption: 'Debe seleccionar un producto válido'
      })
      return
    }

    if (!formProductoProveedor.value.id_proveedor || formProductoProveedor.value.id_proveedor <= 0) {
      $q.notify({
        type: 'negative',
        message: 'Error de validación',
        caption: 'Debe seleccionar un proveedor'
      })
      return
    }

    // Preparar datos según el esquema real del backend
    const datosLimpios: any = {
      id_producto: formProductoProveedor.value.id_producto,
      id_proveedor: formProductoProveedor.value.id_proveedor,
      es_principal: Boolean(formProductoProveedor.value.es_proveedor_principal), // Backend usa 'es_principal'
      activo: Boolean(formProductoProveedor.value.activo !== false)
    }

    // Solo agregar campos opcionales si tienen valores válidos
    if (formProductoProveedor.value.precio_proveedor !== undefined && formProductoProveedor.value.precio_proveedor !== null && formProductoProveedor.value.precio_proveedor > 0) {
      datosLimpios.costo_actual = formProductoProveedor.value.precio_proveedor // Backend usa 'costo_actual'
    }

    if (formProductoProveedor.value.tiempo_entrega_dias !== undefined && formProductoProveedor.value.tiempo_entrega_dias !== null && formProductoProveedor.value.tiempo_entrega_dias > 0) {
      datosLimpios.tiempo_entrega_dias = formProductoProveedor.value.tiempo_entrega_dias
    }

    if (formProductoProveedor.value.cantidad_minima !== undefined && formProductoProveedor.value.cantidad_minima !== null && formProductoProveedor.value.cantidad_minima > 0) {
      datosLimpios.cantidad_minima_orden = formProductoProveedor.value.cantidad_minima // Backend usa 'cantidad_minima_orden'
    }


    if (formProductoProveedor.value.descuento_volumen !== undefined && formProductoProveedor.value.descuento_volumen !== null && formProductoProveedor.value.descuento_volumen >= 0) {
      datosLimpios.descuento_producto = formProductoProveedor.value.descuento_volumen // Backend usa 'descuento_producto'
    }

    // Nota: El backend no parece tener campo para condiciones_especiales, omitiendo por ahora

    // Validación final de estructura según el esquema real del backend
    const camposRequeridos = ['id_producto', 'id_proveedor', 'es_principal', 'activo']
    for (const campo of camposRequeridos) {
      if (!(campo in datosLimpios)) {
        $q.notify({
          type: 'negative',
          message: 'Error de validación',
          caption: `Falta el campo requerido: ${campo}`
        })
        return
      }
    }

    // Validar tipos de datos
    if (typeof datosLimpios.id_producto !== 'number' || datosLimpios.id_producto <= 0) {
      $q.notify({
        type: 'negative',
        message: 'Error de validación',
        caption: 'id_producto debe ser un número mayor a 0'
      })
      return
    }

    if (typeof datosLimpios.id_proveedor !== 'number' || datosLimpios.id_proveedor <= 0) {
      $q.notify({
        type: 'negative',
        message: 'Error de validación',
        caption: 'id_proveedor debe ser un número mayor a 0'
      })
      return
    }

    console.log('=== PREPARANDO ENVÍO ===')
    console.log('Form original:', JSON.stringify(formProductoProveedor.value, null, 2))
    console.log('Datos limpios:', JSON.stringify(datosLimpios, null, 2))
    console.log('Editando existente:', editandoProductoProveedor.value)
    console.log('ID producto proveedor:', formProductoProveedor.value.id_producto_proveedor)
    console.log('Validación de estructura completada exitosamente')

    if (editandoProductoProveedor.value && formProductoProveedor.value.id_producto_proveedor) {
      await productoStore.actualizarProductoProveedor(formProductoProveedor.value.id_producto_proveedor, datosLimpios)
      $q.notify({
        type: 'positive',
        message: 'Relación proveedor actualizada correctamente'
      })
    } else {
      await productoStore.crearProductoProveedor(datosLimpios)
      $q.notify({
        type: 'positive',
        message: 'Proveedor agregado correctamente'
      })
    }

    showCreateProductoProveedorDialog.value = false
    resetFormProductoProveedor()
    if (formProducto.value.id_producto) {
      await cargarProductoProveedores(formProducto.value.id_producto)
    }

  } catch (error: any) {
    console.error('Error al guardar relación proveedor:', error)
    console.error('Response data:', error.response?.data)
    console.error('Response status:', error.response?.status)

    let errorMessage = 'Error desconocido'
    if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail
    } else if (error.response?.data?.message) {
      errorMessage = error.response.data.message
    } else if (error.message) {
      errorMessage = error.message
    }

    // Si es error 422 o 400, mostrar información más específica
    if (error.response?.status === 422) {
      console.error('Datos enviados que causaron el error 422:', datosLimpios)
      errorMessage = 'Datos inválidos (422): ' + errorMessage
    } else if (error.response?.status === 400) {
      console.error('Datos enviados que causaron el error 400:', datosLimpios)
      console.error('Error 400 response data:', error.response?.data)

      // Verificar si es error de relación duplicada
      const responseText = JSON.stringify(error.response?.data).toLowerCase()
      if (responseText.includes('duplicate') || responseText.includes('exists') || responseText.includes('ya existe')) {
        errorMessage = 'Ya existe una relación entre este producto y proveedor'
      } else {
        errorMessage = 'Petición incorrecta (400): ' + (error.response?.data?.detail || errorMessage)
      }
    }

    $q.notify({
      type: 'negative',
      message: 'Error al guardar relación proveedor',
      caption: errorMessage
    })
  } finally {
    isGuardandoProveedor.value = false
  }
}

const toggleEstadoProductoProveedor = async (productoProveedor: ProductoProveedor) => {
  try {
    if (productoProveedor.activo) {
      await productoStore.eliminarProductoProveedor(productoProveedor.id_producto_proveedor, false)
      $q.notify({
        type: 'positive',
        message: 'Relación proveedor desactivada'
      })
    } else {
      await productoStore.activarProductoProveedor(productoProveedor.id_producto_proveedor)
      $q.notify({
        type: 'positive',
        message: 'Relación proveedor activada'
      })
    }

    if (formProducto.value.id_producto) {
      if (formProducto.value.id_producto) {
        await cargarProductoProveedores(formProducto.value.id_producto)
      }
    }

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de relación proveedor',
      caption: error.message
    })
  }
}

const establecerProveedorPrincipal = async (productoProveedor: ProductoProveedor) => {
  try {
    await productoStore.establecerProveedorPrincipal(productoProveedor.id_producto_proveedor)
    $q.notify({
      type: 'positive',
      message: 'Proveedor establecido como principal'
    })
    if (formProducto.value.id_producto) {
      if (formProducto.value.id_producto) {
        await cargarProductoProveedores(formProducto.value.id_producto)
      }
    }
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al establecer proveedor principal',
      caption: error.message
    })
  }
}

const resetFormProductoProveedor = () => {
  editandoProductoProveedor.value = false
  formProductoProveedor.value = {
    id_producto: formProducto.value.id_producto || 0,
    id_proveedor: 0,
    es_proveedor_principal: false,
    precio_proveedor: undefined,
    moneda: 'CLP',
    tiempo_entrega_dias: undefined,
    cantidad_minima: undefined,
    descuento_volumen: undefined,
    condiciones_especiales: '',
    activo: true
  }
}

// Helper methods for product suppliers
const getProveedorNombre = (proveedorId: number): string => {
  const proveedor = proveedoresList.value.find(p => p.id_proveedor === proveedorId)
  return proveedor ? `${proveedor.codigo_proveedor} - ${proveedor.nombre_proveedor}` : '-'
}

const formatDate = (dateString: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-CL')
}


// Lifecycle
onMounted(async () => {
  await cargarDatosRelacionados()
  await cargarProveedores()
  await cargarProductos()
})

// Watch for product changes to load suppliers
const editarProducto = (producto: Producto) => {
  editandoProducto.value = true
  formProducto.value = { ...producto }
  showCreateProductoDialog.value = true

  // Load suppliers for this product
  if (producto.id_producto) {
    cargarProductoProveedores(producto.id_producto)
  }
}
</script>