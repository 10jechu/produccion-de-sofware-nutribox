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
  <div class="d-flex justify-content-between align-items-center p-3 border-bottom food-item-card">
    <div>
        <strong class="text-dark-nb">{{ food.nombre }}</strong>
        <div class="small text-muted-dark mt-1">
            <i class="fas fa-fire me-1 text-secondary-nb"></i> {{ food.kcal?.toFixed(1) ?? 'N/A' }} kcal 
            | <i class="fas fa-dollar-sign me-1 text-primary-nb"></i> {{ formatCurrency(food.costo) }}/u
        </div>
    </div>
    <button class="btn btn-sm btn-primary-nb text-white" @click="addFood" title="Agregar a la lonchera">
        <i class="fas fa-plus"></i>
    </button>
  </div>
</template>

<style scoped>
.food-item-card {
    transition: background-color 0.1s ease;
}
.food-item-card:hover {
    background-color: var(--nb-border-medium);
}
button {
  transition: background-color 0.2s ease;
}
</style>
