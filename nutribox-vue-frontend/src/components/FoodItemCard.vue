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
    emit('add-food', props.food.id);
};
</script>

<template>
  <div class="d-flex justify-content-between align-items-center p-2 border-bottom">
    <div>
        <strong>{{ food.nombre }}</strong>
        <div class="small text-muted">
            {{ food.kcal }} kcal | {{ formatCurrency(food.costo) }}/u
        </div>
    </div>
    <button class="btn btn-sm bg-primary-nb text-white" @click="addFood" title="Agregar a la lonchera">
        <i class="fas fa-plus"></i>
    </button>
  </div>
</template>
