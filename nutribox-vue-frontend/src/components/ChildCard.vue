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

// Lógica de membresía para habilitar botones
const canCreateLunchbox = hasRequiredMembership('Estandar');
const canManageRestrictions = hasRequiredMembership('Premium');

const viewHijoDetail = () => {
    emit('view-detail', props.hijo.id);
};

const deleteHijo = () => {
    emit('delete-hijo', props.hijo.id);
};

const goToCreateLunchbox = () => {
    // Uso de rutas agrupadas bajo /app
    router.push('/app/crear-lonchera?hijoId=' + props.hijo.id);
};

const goToManageRestrictions = () => {
    // Uso de rutas agrupadas bajo /app
    router.push('/app/restricciones?hijoId=' + props.hijo.id);
};
</script>

<template>
  <div class="card p-4 card-shadow h-100">
    <div class="d-flex justify-content-between align-items-start mb-3">
        <h4 class="fw-bold mb-0 text-dark-nb">{{ hijo.nombre }}</h4>
        <button 
            class="btn btn-sm btn-outline-danger" 
            title="Eliminar Hijo"
            @click="deleteHijo"
        >
            <i class="fas fa-trash"></i>
        </button>
    </div>
    <div class="mb-3 border-bottom pb-3">
        <p class="mb-1 small text-muted-dark">
            Loncheras Activas: 
            <span class="badge bg-primary-light text-white">{{ hijo.loncheras_activas }}</span>
        </p>
        <p class="mb-0 small text-muted-dark">
            Restricciones: 
             <span :class="['badge', hijo.restricciones_count > 0 ? 'bg-danger' : 'bg-primary-dark text-white']">
                {{ hijo.restricciones_count }}
             </span>
        </p>
    </div>
    
    <div class="pt-3 mt-auto d-grid gap-2">
        <button class="btn btn-sm btn-outline-primary-nb py-2" @click="viewHijoDetail">
            <i class="fas fa-eye me-1"></i> Ver Detalle/Estadísticas
        </button>
        
        <button 
            :disabled="!canCreateLunchbox"
            :class="['btn', 'py-2', canCreateLunchbox ? 'btn-primary-nb' : 'btn-secondary']"
            @click="goToCreateLunchbox"
            :title="!canCreateLunchbox ? 'Requiere Plan Estándar o Superior' : 'Crear Lonchera'"
        >
            <i class="fas fa-plus me-1"></i> {{ canCreateLunchbox ? 'Crear Lonchera' : 'Plan Estándar Requerido' }}
        </button>

        <button 
            v-if="canManageRestrictions"
            class="btn py-2 btn-warning-nb text-dark-nb"
            @click="goToManageRestrictions"
        >
            <i class="fas fa-ban me-1"></i> Gestionar Restricciones
        </button>
         <div v-else class="text-center small text-muted-dark mt-2">
            *Gestionar restricciones requiere Plan Premium.
        </div>
    </div>
  </div>
</template>
