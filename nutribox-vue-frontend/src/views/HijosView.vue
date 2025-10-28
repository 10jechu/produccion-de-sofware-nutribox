<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { getUserDetail } from '@/utils/user';
import ChildCard from '@/components/ChildCard.vue';
import authService from '@/services/auth.service';

const hijos = ref([]);
const userData = ref(null);
const isLoading = ref(true);

const fetchHijos = async () => {
  isLoading.value = true;
  userData.value = getUserDetail();
  if (!userData.value) {
    authService.logout();
    return;
  }
  
  try {
    const childrenList = await apiService.get('/children?usuario_id=' + userData.value.id);
    
    const childrenDetailsPromises = childrenList.map(hijo => 
      apiService.get('/children/' + hijo.id + '/detail')
    );
    
    const detailedChildren = await Promise.all(childrenDetailsPromises);
    
    hijos.value = detailedChildren.map(detail => ({
        id: detail.id,
        nombre: detail.nombre,
        restricciones_count: detail.restricciones.length,
        loncheras_activas: detail.loncheras_recientes.filter(l => l.estado !== 'Archivada').length
    }));
    
    isLoading.value = false;
  } catch (error) {
    isLoading.value = false;
    Swal.fire('Error', error.message || 'No se pudieron cargar los hijos.', 'error');
  }
};

const showAddChildModal = async () => {
    const { value: nombre } = await Swal.fire({
        title: "Agregar Hijo",
        input: "text",
        inputLabel: "Nombre del hijo",
        inputPlaceholder: "Ej: Juan Perez",
        showCancelButton: true,
        confirmButtonColor: "#4CAF50",
        cancelButtonColor: "#DC3545",
        confirmButtonText: "Agregar",
        cancelButtonText: "Cancelar",
        inputValidator: (value) => {
            if (!value) {
                return "Debes ingresar un nombre";
            }
        }
    });
    
    if (nombre) {
        try {
            Swal.showLoading();
            await apiService.post('/children', {
                nombre,
                usuario_id: userData.value.id
            });
            Swal.close();
            Swal.fire('Exito', 'Hijo agregado correctamente', 'success');
            await fetchHijos(); 
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'Error al agregar hijo', 'error');
        }
    }
};

const deleteHijo = async (id) => {
    const result = await Swal.fire({
        title: "Eliminar hijo",
        text: "Esta accion eliminara al hijo y todas sus loncheras asociadas.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#4CAF50',
        cancelButtonColor: '#F44336',
        confirmButtonText: 'Si, eliminar',
        cancelButtonText: 'Cancelar'
    });
    
    if (result.isConfirmed) {
        try {
            Swal.showLoading();
            await apiService.delete('/children/' + id);
            Swal.close();
            Swal.fire('Exito', 'Hijo eliminado correctamente', 'success');
            await fetchHijos(); 
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'Error al eliminar hijo', 'error');
        }
    }
};

const viewHijoDetail = async (id) => {
    const hijo = hijos.value.find(h => h.id === id);
    if (!hijo) return;
    
    try {
        Swal.showLoading();
        const detail = await apiService.get('/children/' + id + '/detail');
        Swal.close();
        
        const restriccionesList = detail.restricciones.length > 0
            ? detail.restricciones.map(r => 
                '<li class="list-group-item d-flex justify-content-between align-items-start py-1 px-0">' + r.tipo.toUpperCase() + ': ' + (r.alimento_nombre || r.texto) + '</li>'
              ).join("")
            : '<li class="list-group-item text-muted px-0">Sin restricciones registradas.</li>';
        
        const swalHtml = 
                '<div class="text-start">' +
                    '<h5 class="mt-3">Restricciones (' + detail.restricciones.length + '): ' +
                        '<a href="/restricciones?hijoId=' + detail.id + '" class="small badge bg-primary-nb text-white text-decoration-none">Gestionar Restricciones</a>' +
                    '</h5>' +
                    '<ul class="list-group list-group-flush border-top border-bottom">' + restriccionesList + '</ul>' +
                    
                    '<h5 class="mt-4">Estadisticas:</h5>' +
                    '<ul class="list-unstyled mb-0">' +
                        '<li><strong>Total de Loncheras:</strong> ' + detail.estadisticas.total_loncheras + '</li>' +
                        '<li><strong>Promedio de Calorias:</strong> <span class="badge bg-success">' + detail.estadisticas.promedio_calorias + ' kcal</span></li>' +
                    '</ul>' +
                '</div>';
        
        Swal.fire({
            title: detail.nombre,
            html: swalHtml,
            width: 600,
            confirmButtonColor: "#4CAF50"
        });
    } catch (error) {
        Swal.close();
        Swal.fire('Error', error.message || 'No se pudo cargar el detalle.', 'error');
    }
};

onMounted(() => {
  fetchHijos();
});
</script>

<template>
  <main class="flex-grow-1 p-4 bg-light">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h1 class="h3">Mis Hijos</h1>
            <p class="text-muted">Gestiona la informacion de tus hijos</p>
        </div>
        <button class="btn btn-primary-nb" @click="showAddChildModal">
            <i class="fas fa-plus me-1"></i> Agregar Hijo
        </button>
    </div>

    <div v-if="isLoading" class="text-center p-5">
      <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
      <p class="mt-2 text-muted">Cargando hijos...</p>
    </div>

    <div v-else-if="hijos.length === 0" class="row g-4">
      <div class="col-12">
        <div class="card p-5 text-center card-shadow">
          <i class="fas fa-child text-primary-nb mb-3" style="font-size: 48px;"></i>
          <h3 class="h4">No tienes hijos registrados</h3>
          <p class="text-muted mb-4">Comienza agregando tu primer hijo</p>
          <button class="btn btn-primary-nb w-auto mx-auto" @click="showAddChildModal">
            <i class="fas fa-plus me-1"></i> Agregar Hijo
          </button>
        </div>
      </div>
    </div>

    <div v-else class="row g-4">
      <div v-for="hijo in hijos" :key="hijo.id" class="col-lg-4 col-md-6">
        <ChildCard 
            :hijo="hijo"
            @view-detail="viewHijoDetail"
            @delete-hijo="deleteHijo"
        />
      </div>
    </div>
  </main>
</template>
