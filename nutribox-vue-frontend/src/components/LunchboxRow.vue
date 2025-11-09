<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  lunchbox: {
    type: Object,
    required: true
  },
  formatCurrency: {
    type: Function,
    required: true
  },
  formatDate: {
    type: Function,
    required: true
  }
});

// MODIFICADO: Añadido 'confirm-lunchbox'
const emit = defineEmits(['view-detail', 'delete-lunchbox', 'confirm-lunchbox']);

const getBadgeClass = (estado) => {
    if (estado === "Confirmada") return "bg-success";
    if (estado === "Borrador") return "bg-warning text-dark";
    if (estado === "Archivada") return "bg-secondary";
    return "bg-info";
}
</script>

<template>
    <tr>
        <td>{{ formatDate(lunchbox.fecha) }}</td>
        <td><strong>{{ lunchbox.hijo_nombre }}</strong></td>
        <td>
            <span :class="['badge', getBadgeClass(lunchbox.estado)]">
                {{ lunchbox.estado }}
            </span>
        </td>
        <td>{{ lunchbox.items_count }} items</td>
        <td>{{ lunchbox.total_calorias }} kcal</td>
        <td>{{ formatCurrency(lunchbox.total_costo) }}</td>
        <td>
            <button class="btn btn-sm btn-outline-primary me-1" @click="emit('view-detail', lunchbox.id)">
                <i class="fas fa-eye"></i>
                <span class="d-none d-md-inline"> Ver Detalle</span>
            </button>

            <button 
                v-if="lunchbox.estado === 'Borrador'"
                class="btn btn-sm btn-success me-1" 
                title="Confirmar Lonchera"
                @click="emit('confirm-lunchbox', lunchbox.id)">
                <i class="fas fa-check"></i>
                <span class="d-none d-md-inline"> Confirmar</span>
            </button>
            <button class="btn btn-sm btn-outline-danger" @click="emit('delete-lunchbox', lunchbox.id)">
                <i class="fas fa-trash"></i>
            </button>
        </td>
    </tr>
</template>
