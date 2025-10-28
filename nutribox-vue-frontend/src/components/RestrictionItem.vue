<script setup>
import { defineProps, defineEmits, computed } from 'vue';

const props = defineProps({
  restriction: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['delete-restriction']);

const badgeClass = computed(() => {
    return props.restriction.tipo === 'alergia' ? 'bg-danger' : 'bg-warning text-dark';
});

const restrictionText = computed(() => {
    if (props.restriction.tipo === 'alergia') {
        // CORRECCIÓN: Concatenación simple
        return 'Alergia a: ' + (props.restriction.alimento_nombre || 'Alimento desconocido');
    }
    // CORRECCIÓN: Concatenación simple
    return 'Prohibido (contiene): ' + props.restriction.texto;
});
</script>

<template>
    <li class="list-group-item d-flex justify-content-between align-items-center">
        <div>
            <span :class="['badge', 'me-2', badgeClass]">{{ restriction.tipo.toUpperCase() }}</span>
            <strong>{{ restrictionText }}</strong>
        </div>
        <button class="btn btn-sm btn-outline-danger" @click="emit('delete-restriction', restriction.id)" title="Eliminar restricción">
            <i class="fas fa-trash"></i>
        </button>
    </li>
</template>
