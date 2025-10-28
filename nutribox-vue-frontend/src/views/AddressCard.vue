<script setup>
// Usamos el API de composicion sin importar defineProps/defineEmits
const props = defineProps({
  direccion: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['delete-address']);

const deleteAddress = () => {
    emit('delete-address', props.direccion.id);
};
</script>

<template>
  <div class="card p-3 card-shadow h-100">
    <div class="d-flex justify-content-between align-items-start">
        <div class="flex-grow-1">
            <h5 class="fw-bold mb-1 text-primary-nb">{{ direccion.etiqueta }}</h5>
            <p class="text-muted mb-1">{{ direccion.direccion }}</p>
            <p class="small text-dark mb-0">{{ direccion.barrio }}, <strong>{{ direccion.ciudad }}</strong></p>
        </div>
        <button 
            class="btn btn-sm btn-outline-danger ms-3" 
            title="Eliminar Direccion"
            @click="deleteAddress(direccion.id)"
        >
            <i class="fas fa-trash"></i>
        </button>
    </div>
  </div>
</template>