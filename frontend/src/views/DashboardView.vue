<template>
  <q-page class="q-pa-md">
    <div class="row q-gutter-md">
      <!-- Welcome Card -->
      <div class="col-12">
        <q-card class="bg-primary text-white">
          <q-card-section>
            <div class="text-h5">¡Bienvenido, {{ authStore.userName }}!</div>
            <div class="text-subtitle1">Panel de control - ERP DAEL</div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Stats Cards -->
      <div class="col-12 col-md-3">
        <q-card>
          <q-card-section class="text-center">
            <q-icon name="inventory" size="3rem" color="primary" />
            <div class="text-h6 q-mt-sm">Productos</div>
            <div class="text-h4 text-primary">1,234</div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-3">
        <q-card>
          <q-card-section class="text-center">
            <q-icon name="people" size="3rem" color="secondary" />
            <div class="text-h6 q-mt-sm">Clientes</div>
            <div class="text-h4 text-secondary">567</div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-3">
        <q-card>
          <q-card-section class="text-center">
            <q-icon name="assignment" size="3rem" color="positive" />
            <div class="text-h6 q-mt-sm">Órdenes</div>
            <div class="text-h4 text-positive">89</div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-3">
        <q-card>
          <q-card-section class="text-center">
            <q-icon name="trending_up" size="3rem" color="orange" />
            <div class="text-h6 q-mt-sm">Ventas</div>
            <div class="text-h4 text-orange">$45,321</div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Quick Actions -->
      <div class="col-12 col-md-6">
        <q-card>
          <q-card-section>
            <div class="text-h6 q-mb-md">Acciones Rápidas</div>
            <div class="row q-gutter-sm">
              <q-btn
                color="primary"
                icon="add"
                label="Nuevo Producto"
                class="col"
              />
              <q-btn
                color="secondary"
                icon="person_add"
                label="Nuevo Cliente"
                class="col"
              />
            </div>
            <div class="row q-gutter-sm q-mt-sm">
              <q-btn
                color="positive"
                icon="receipt"
                label="Nueva Orden"
                class="col"
              />
              <q-btn
                color="info"
                icon="assessment"
                label="Reportes"
                class="col"
              />
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Recent Activity -->
      <div class="col-12 col-md-6">
        <q-card>
          <q-card-section>
            <div class="text-h6 q-mb-md">Actividad Reciente</div>
            <q-list separator>
              <q-item>
                <q-item-section avatar>
                  <q-icon name="shopping_cart" color="primary" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>Nueva orden #1234</q-item-label>
                  <q-item-label caption>Hace 5 minutos</q-item-label>
                </q-item-section>
              </q-item>

              <q-item>
                <q-item-section avatar>
                  <q-icon name="inventory" color="secondary" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>Producto actualizado</q-item-label>
                  <q-item-label caption>Hace 15 minutos</q-item-label>
                </q-item-section>
              </q-item>

              <q-item>
                <q-item-section avatar>
                  <q-icon name="person_add" color="positive" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>Nuevo cliente registrado</q-item-label>
                  <q-item-label caption>Hace 1 hora</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
</script>