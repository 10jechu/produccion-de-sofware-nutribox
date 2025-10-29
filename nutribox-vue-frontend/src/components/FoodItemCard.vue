<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  food: {
    type: Object,
    required: true
  },
  formatCurrency: {
    type: Function,
    required: true
  }
});

const emit = defineEmits(['add-food']);

const addFood = () => {
    // Emite el evento 'add-food' con el ID del alimento cuando se hace clic
    emit('add-food', props.food.id);
};
</script>

<template>
  <div class="d-flex justify-content-between align-items-center p-2 border-bottom">
    <div>
        <strong>{{ food.nombre }}</strong>
        <div class="small text-muted">
            {{ food.kcal?.toFixed(1) ?? 'N/A' }} kcal | {{ formatCurrency(food.costo) }}/u
        </div>
    </div>
    <button class="btn btn-sm btn-primary-nb text-white" @click="addFood" title="Agregar a la lonchera">
        <i class="fas fa-plus"></i>
    </button>
  </div>
</template>

<style scoped>
/* Estilos opcionales para este componente específico */
button {
  transition: background-color 0.2s ease;
}
button:hover {
  background-color: var(--nb-primary-dark, #388E3C) !important; /* Usa variable CSS si existe */
}
</style>