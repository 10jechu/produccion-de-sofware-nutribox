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

const emit = defineEmits(['view-detail', 'delete-lunchbox']);

const getBadgeClass = (estado) => {
    if (estado === "Confirmada") return "bg-primary-nb text-white";
    if (estado === "Borrador") return "bg-secondary text-dark-nb";
    if (estado === "Archivada") return "bg-muted-dark text-white";
    return "bg-accent text-white";
}
</script>

<template>
    <tr class="text-dark-nb">
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
            <button class="btn btn-sm btn-outline-primary-nb me-1" @click="emit('view-detail', lunchbox.id)">
                <i class="fas fa-eye"></i>
                <span class="d-none d-md-inline"> Ver Detalle</span>
            </button>

            <button class="btn btn-sm btn-outline-danger" @click="emit('delete-lunchbox', lunchbox.id)">
                <i class="fas fa-trash"></i>
            </button>
        </td>
    </tr>
</template>
