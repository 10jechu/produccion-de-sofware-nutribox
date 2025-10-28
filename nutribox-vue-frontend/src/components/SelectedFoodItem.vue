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
  <div class="d-flex justify-content-between align-items-center p-2 border-bottom">
    <div class="flex-grow-1">
        <strong>{{ food.nombre }}</strong>
        <div class="small text-muted">
            Total: {{ formatCurrency(food.costo * food.cantidad) }} | {{ (food.kcal * food.cantidad).toFixed(0) }} kcal
        </div>
    </div>
    <div class="d-flex align-items-center" style="gap: 8px;">
        <input type="number" min="1" v-model="quantity" 
            class="form-control form-control-sm" style="width: 70px;"
            @change="handleQuantityChange">
        <button class="btn btn-sm btn-outline-danger" @click="removeFood" title="Quitar alimento">
            <i class="fas fa-trash"></i>
        </button>
    </div>
  </div>
</template>
