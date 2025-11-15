<script setup>
import { useRouter } from 'vue-router';
import { hasRequiredMembership } from '@/utils/user';

const props = defineProps({
  hijo: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['view-detail', 'delete-hijo']);
const router = useRouter();

// ### INICIO DE LA MODIFICACIÓN ###
// Corregido: 'Premium' en lugar de 'Estandar'
const canCreateLunchbox = hasRequiredMembership('Premium');
const canManageRestrictions = hasRequiredMembership('Premium');
// ### FIN DE LA MODIFICACIÓN ###

const viewHijoDetail = () => {
    emit('view-detail', props.hijo.id);
};

const deleteHijo = () => {
    emit('delete-hijo', props.hijo.id);
};

const goToCreateLunchbox = () => {
    // Uso de concatenación para ruta segura
    router.push('/crear-lonchera?hijoId=' + props.hijo.id);
};

const goToManageRestrictions = () => {
    // Uso de concatenación para ruta segura
    router.push('/restricciones?hijoId=' + props.hijo.id);
};
</script>

<template>
  <div class="card p-4 card-shadow h-100">
    <div class="d-flex justify-content-between align-items-start mb-3">
        <h5 class="fw-bold mb-0 text-primary-nb">{{ hijo.nombre }}</h5>
        <button 
            class="btn btn-sm btn-outline-danger" 
            title="Eliminar Hijo"
            @click="deleteHijo"
        >
            <i class="fas fa-trash"></i>
        </button>
    </div>
    <div class="mb-3">
        <p class="mb-1 small text-muted">Loncheras Activas: <span class="badge bg-info">{{ hijo.loncheras_activas }}</span></p>
        <p class="mb-0 small text-muted">Restricciones: 
             <span :class="['badge', hijo.restricciones_count > 0 ? 'bg-danger' : 'bg-success']">
                {{ hijo.restricciones_count }}
             </span>
        </p>
    </div>
    
    <div class="border-top pt-3 mt-auto d-grid gap-2">
        <button class="btn btn-sm btn-outline-primary" @click="viewHijoDetail">
            <i class="fas fa-eye me-1"></i> Ver Detalle/Estadisticas
        </button>
        
        <button 
            :disabled="!canCreateLunchbox"
            :class="['btn', 'btn-sm', canCreateLunchbox ? 'btn-primary-nb' : 'btn-secondary']"
            @click="goToCreateLunchbox"
        >
            <i class="fas fa-plus me-1"></i> {{ canCreateLunchbox ? 'Crear Lonchera' : 'Plan Premium Requerido' }}
        </button>
        <button 
            v-if="canManageRestrictions"
            class="btn btn-sm btn-outline-warning"
            @click="goToManageRestrictions"
        >
            <i class="fas fa-ban me-1"></i> Gestionar Restricciones
        </button>
    </div>
  </div>
</template>
