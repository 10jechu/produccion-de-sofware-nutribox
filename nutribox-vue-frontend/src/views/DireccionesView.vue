<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { getUserDetail } from '@/utils/user';
import AddressCard from '@/components/AddressCard.vue';
import authService from '@/services/auth.service';

const direcciones = ref([]);
const userData = ref(null);
const isLoading = ref(true);

const maxDirecciones = computed(() => {
    return userData.value?.membresia?.max_direcciones || 0;
});

const canAddAddress = computed(() => {
    return direcciones.value.length < maxDirecciones.value || maxDirecciones.value === 0;
});

const fetchAddresses = async () => {
  isLoading.value = true;
  userData.value = getUserDetail();
  if (!userData.value) {
    authService.logout();
    return;
  }
  
  try {
    const freshUserDetail = await apiService.get('/users/' + userData.value.id + '/detail');
    authService.saveUserDetail(freshUserDetail);
    userData.value = freshUserDetail;

    // Se corrige la ruta para evitar el problema de v_en/v_es en la URL
    direcciones.value = await apiService.get('/addresses?usuario_id=' + userData.value.id);
    
    isLoading.value = false;
  } catch (error) {
    isLoading.value = false;
    Swal.fire('Error', error.message || 'No se pudieron cargar las direcciones.', 'error');
  }
};

const showAddAddressModal = async () => {
    if (!canAddAddress.value) {
        Swal.fire({
            icon: 'warning',
            title: 'Limite Alcanzado',
            text: 'Has alcanzado el limite de ' + maxDirecciones.value + ' direccion(es) permitido por tu Plan ' + userData.value.membresia.tipo + '.',
            confirmButtonColor: '#FF9800'
        });
        return;
    }

    const { value: formValues } = await Swal.fire({
        title: "Agregar Direccion",
        html: 
            '<input id="swal-etiqueta" class="swal2-input form-control" placeholder="Etiqueta (Ej: Casa)" required>' +
            '<input id="swal-direccion" class="swal2-input form-control" placeholder="Direccion completa" required>' +
            '<input id="swal-barrio" class="swal2-input form-control" placeholder="Barrio" required>' +
            '<input id="swal-ciudad" class="swal2-input form-control" placeholder="Ciudad" value="Bogota" required>'
        ,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: "#4CAF50",
        cancelButtonColor: "#DC3545",
        confirmButtonText: "Guardar",
        preConfirm: () => {
            const etiqueta = document.getElementById("swal-etiqueta").value;
            const direccion = document.getElementById("swal-direccion").value;
            if (!etiqueta || !direccion) {
                Swal.showValidationMessage("Etiqueta y direccion son requeridas.");
                return false;
            }
            return { 
                etiqueta, 
                direccion, 
                barrio: document.getElementById("swal-barrio").value, 
                ciudad: document.getElementById("swal-ciudad").value 
            };
        }
    });
    
    if (formValues) {
        try {
            Swal.showLoading();
            await apiService.post('/addresses', {
                usuario_id: userData.value.id,
                ...formValues
            });
            Swal.close();
            Swal.fire('Exito', 'Direccion agregada correctamente', 'success');
            await fetchAddresses();
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'Error al agregar direccion', 'error');
        }
    }
};

const deleteAddress = async (id) => {
    const result = await Swal.fire({
        title: "¿Eliminar direccion?",
        text: "Esta acción eliminara la direccion permanentemente.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#4CAF50',
        cancelButtonColor: '#DC3545',
        confirmButtonText: 'Si, eliminar',
        cancelButtonText: 'Cancelar'
    });
    
    if (result.isConfirmed) {
        try {
            Swal.showLoading();
            await apiService.delete('/addresses/' + id);
            Swal.close();
            Swal.fire('Exito', 'Direccion eliminada correctamente', 'success');
            await fetchAddresses();
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'Error al eliminar direccion', 'error');
        }
    }
};

onMounted(() => {
  fetchAddresses();
});
</script>

<template>
  <main class="flex-grow-1 p-4 bg-light">
    <div class="dashboard-header mb-4">
        <h1 class="h3">Mis Direcciones de Entrega</h1>
        <p class="text-muted">
            Gestiona las direcciones asociadas a tu cuenta. 
            <strong v-if="maxDirecciones > 0">
                 (Limite: {{ direcciones.length }}/{{ maxDirecciones }})
            </strong>
            <strong v-else>(Plan Basico: sin direcciones)</strong>
        </p>
    </div>

    <div class="card p-4 card-shadow">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="card-title fw-bold">Direcciones Activas</h5>
            <button 
                :disabled="!canAddAddress"
                :class="['btn', canAddAddress ? 'btn-primary-nb' : 'btn-secondary']"
                @click="showAddAddressModal"
                title="Agregar nueva direccion"
            >
                <i class="fas fa-plus me-1"></i> Agregar Direccion
            </button>
        </div>
        
        <div v-if="isLoading" class="text-center p-5">
            <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
            <p class="mt-2 text-muted">Cargando direcciones...</p>
        </div>
        
        <div v-else-if="direcciones.length === 0" class="row g-3">
             <div class="col-12">
                <div class="card p-5 text-center card-shadow">
                    <i class="fas fa-map-marker-alt text-primary-nb mb-3" style="font-size: 48px;"></i>
                    <h4 class="h5">No tienes direcciones registradas</h4>
                    <p class="text-muted mb-4">Agrega una direccion de entrega</p>
                    <button class="btn btn-primary-nb w-auto mx-auto" :disabled="!canAddAddress" @click="showAddAddressModal">
                        <i class="fas fa-plus me-1"></i> Agregar Direccion
                    </button>
                </div>
            </div>
        </div>

        <div v-else class="row g-3">
            <div v-for="dir in direcciones" :key="dir.id" class="col-lg-6 col-md-12">
                <AddressCard 
                    :direccion="dir"
                    @delete-address="deleteAddress"
                />
            </div>
        </div>
    </div>
  </main>
</template>
