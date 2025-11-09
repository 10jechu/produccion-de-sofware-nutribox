<script setup>
import { defineProps, defineEmits } from 'vue';
import { ref, watch } from 'vue';

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

const emit = defineEmits(['update-quantity', 'remove-food']);

const quantity = ref(props.food.cantidad);

const handleQuantityChange = () => {
    const newQuantity = parseInt(quantity.value);
    if (!isNaN(newQuantity) && newQuantity >= 1) {
        emit('update-quantity', props.food.id, newQuantity);
    } else {
        quantity.value = props.food.cantidad;
    }
};

const removeFood = () => {
    emit('remove-food', props.food.id);
};

watch(() => props.food.cantidad, (newVal) => {
    quantity.value = newVal;
});
</script>

<template>
  <div class="d-flex justify-content-between align-items-center p-3 border-bottom selected-food-item">
    <div class="flex-grow-1">
        <strong class="text-dark-nb">{{ food.nombre }} <span class="badge bg-primary-light text-dark-nb ms-2">{{ food.cantidad }}x</span></strong>
        <div class="small text-muted-dark mt-1">
            Total: <span class="fw-bold text-dark-nb">{{ formatCurrency(food.costo * food.cantidad) }}</span> 
            | {{ (food.kcal * food.cantidad).toFixed(0) }} kcal
        </div>
    </div>
    <div class="d-flex align-items-center" style="gap: 8px;">
        <input type="number" min="1" v-model="quantity" 
            class="form-control form-control-sm text-center" style="width: 70px;"
            @change="handleQuantityChange">
        <button class="btn btn-sm btn-outline-danger" @click="removeFood" title="Quitar alimento">
            <i class="fas fa-trash"></i>
        </button>
    </div>
  </div>
</template>

<style scoped>
.selected-food-item {
    background-color: var(--bg-hero); /* Fondo crema para destacar el carrito */
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
    border: 1px solid var(--nb-border-medium) !important;
}
</style>
