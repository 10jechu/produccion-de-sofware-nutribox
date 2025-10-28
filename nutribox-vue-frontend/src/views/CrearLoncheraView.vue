<script setup>
// ... imports existentes ...
import FoodItemCard from '@/components/FoodItemCard.vue';
import SelectedFoodItem from '@/components/SelectedFoodItem.vue';
import AppLayout from '@/components/AppLayout.vue'; // <-- AÑADE ESTO

// ... resto del script ...
</script>

<template>
  <AppLayout>
    <main class="flex-grow-1 p-4 bg-light">
      <div class="dashboard-header mb-4">
          <h1 class="h3">Crear Nueva Lonchera</h1>
          <p class="text-muted">Selecciona los alimentos y asigna la entrega (Plan: {{ userData?.membresia?.tipo }})</p>
      </div>

      <div v-if="isLoading" class="text-center p-5">
        <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
        <p class="mt-2 text-muted">Cargando datos...</p>
      </div>

      <div v-else class="row g-4">
        </div>
    </main>
  </AppLayout> </template>
