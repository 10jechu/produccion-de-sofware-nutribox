<script setup>
import { ref, onMounted } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { getUserDetail } from '@/utils/user';
import authService from '@/services/auth.service';
import LunchboxRow from '@/components/LunchboxRow.vue'; 

const lunchboxes = ref([]);
const hijos = ref([]);
const isLoading = ref(true);

function getBadgeClass(estado) {
    if (estado === "Confirmada") return "bg-primary-nb text-white";
    if (estado === "Borrador") return "bg-secondary text-dark-nb";
    return "bg-muted-dark text-white";
}

function formatCurrency(value) {
    // Usamos 'es-CO' pero sin simbolos de tilde en el resto del codigo
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(value);
}

function getHijoName(hijoId) {
    const hijo = hijos.value.find(h => h.id === hijoId);
    return hijo ? hijo.nombre : 'Hijo #' + hijoId; 
}

function formatDate(dateString) {
    const parts = dateString.split('-');
    const date = new Date(Date.UTC(parts[0], parts[1] - 1, parts[2]));
    // Usamos 'es-CO' pero sin tildes en los meses
    return date.toLocaleDateString('es-CO', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' });
}

async function loadLunchboxes() {
    isLoading.value = true;
    const user = getUserDetail();
    if (!user) {
        authService.logout();
        return;
    }

    try {
        // Obtenemos todas las loncheras del usuario actual (no solo las del admin/menus)
        const [baseLunchboxes, childrenList] = await Promise.all([
            apiService.get('/lunchboxes?usuario_id=' + user.id),
            apiService.get('/children?usuario_id=' + user.id)
        ]);
        hijos.value = childrenList;
        
        // Obtenemos el detalle completo de cada lonchera (nutrición, items, costo)
        const detailedLunchboxesPromises = baseLunchboxes.map(lb => 
            apiService.get('/lunchboxes/' + lb.id + '/detail')
        );
        
        const detailedLunchboxes = await Promise.all(detailedLunchboxesPromises);

        lunchboxes.value = detailedLunchboxes.map(detail => ({
            ...detail,
            hijo_nombre: getHijoName(detail.hijo.id), 
            items_count: detail.items.length,
            total_calorias: detail.nutricion_total.calorias.toFixed(0), 
            total_costo: detail.nutricion_total.costo_total 
        }));
        
        isLoading.value = false;
    } catch (error) {
        isLoading.value = false;
        Swal.fire('Error', error.message || 'No se pudieron cargar los detalles de las loncheras.', 'error');
    }
}

async function viewDetail(id) {
    try {
        const detail = lunchboxes.value.find(lb => lb.id === id); 
        if (!detail) throw new Error("Detalle de lonchera no encontrado.");

        const itemsList = detail.items.map(item => 
            '<li class="list-group-item d-flex justify-content-between align-items-center">' +
                '<span>' + item.nombre + '</span>' + 
                '<span class="badge bg-primary-light text-dark-nb">' + item.cantidad + 'x - ' + item.kcal.toFixed(0) + ' kcal / ' + formatCurrency(item.costo) + '</span>' + 
             '</li>'
        ).join("");
        
        const alertasHtml = detail.alertas.map(a => 
            '<div class="alert ' + (a.includes("ALERGIA") ? "alert-danger" : "alert-warning") + ' p-2 mt-2 mb-0 fw-bold" role="alert">' +
                '<i class="fas fa-exclamation-triangle me-1"></i> ' + a + 
            '</div>'
        ).join("");

        const swalHtml = 
             alertasHtml +
             '<div class="text-start mt-3">' +
                 '<h5 class="mb-3 border-bottom pb-2 text-dark-nb">Información General</h5>' +
                 '<div class="row text-dark-nb">' +
                     '<div class="col-6 mb-2"><strong>Fecha:</strong> ' + formatDate(detail.fecha) + '</div>' +
                     '<div class="col-6 mb-2"><strong>Estado:</strong> <span class="badge ' + getBadgeClass(detail.estado) + '">' + detail.estado + '</span></div>' +
                     '<div class="col-12 mb-2"><strong>Entrega:</strong> ' + (detail.direccion ? detail.direccion.etiqueta + " - " + detail.direccion.direccion : "Sin dirección de envío") + '</div>' +
                 '</div>' +
                 
                 '<h5 class="mt-4 mb-2 border-bottom pb-2 text-dark-nb">Alimentos (' + detail.items.length + ')</h5>' +
                 '<ul class="list-group list-group-flush">' + itemsList + '</ul>' +
                 
                 '<h5 class="mt-4 mb-2 border-bottom pb-2 text-dark-nb">Nutrición y Costo</h5>' +
                 '<ul class="list-group list-group-flush text-dark-nb">' +
                     '<li class="list-group-item d-flex justify-content-between px-0">Calorías: <strong class="text-danger">' + detail.nutricion_total.calorias.toFixed(1) + ' kcal</strong></li>' +
                     '<li class="list-group-item d-flex justify-content-between px-0">Proteínas: <strong>' + detail.nutricion_total.proteinas.toFixed(1) + ' g</strong></li>' +
                     '<li class="list-group-item d-flex justify-content-between px-0">Carbohidratos: <strong>' + detail.nutricion_total.carbohidratos.toFixed(1) + ' g</strong></li>' +
                     '<li class="list-group-item d-flex justify-content-between px-0">Costo Total: <strong>' + formatCurrency(detail.nutricion_total.costo_total) + '</strong></li>' +
                 '</ul>' +
             '</div>'
            
        Swal.fire({
            title: 'Lonchera para ' + detail.hijo_nombre,
            html: swalHtml,
            width: 600,
            confirmButtonColor: "#1F8D45"
        });
    } catch (error) {
        Swal.fire('Error', 'No se pudo cargar el detalle', 'error');
    }
}

async function deleteLunchbox(id) {
    const result = await Swal.fire({
        title: "¿Eliminar Lonchera?",
        text: "Esta acción eliminará la lonchera y todos sus alimentos asociados de forma permanente.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#1F8D45',
        cancelButtonColor: '#E53935',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    });

    if (result.isConfirmed) {
        try {
            Swal.showLoading();
            await apiService.delete('/lunchboxes/' + id);
            Swal.close();
            Swal.fire('Éxito', 'Lonchera eliminada correctamente', 'success');
            loadLunchboxes(); 
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'Error al eliminar la lonchera', 'error');
        }
    }
}

onMounted(() => {
    loadLunchboxes();
});

</script>

<template>
    <main class="flex-grow-1 p-4 bg-light-nb">
        <div class="dashboard-header mb-4">
            <h1 class="h3 text-dark-nb">Mis Loncheras</h1>
            <p class="text-muted-dark">Historial de todas tus loncheras</p>
        </div>

        <div class="card p-4 card-shadow">
            <div v-if="isLoading" class="text-center p-5 bg-card">
                <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
                <p class="mt-2 text-muted-dark">Cargando loncheras...</p>
            </div>
            
            <div v-else-if="lunchboxes.length === 0" class="text-center p-5 text-muted-dark bg-card">
                 No hay loncheras registradas
                 <router-link to="/app/crear-lonchera" class="btn btn-primary-nb mt-3">Crear la primera Lonchera</router-link>
            </div>

            <div v-else class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead class="bg-light-nb">
                        <tr>
                            <th>Fecha</th>
                            <th>Hijo</th>
                            <th>Estado</th>
                            <th>Items</th>
                            <th>Calorías</th>
                            <th>Costo</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody id="lunchboxesTableBody">
                        <LunchboxRow
                            v-for="lb in lunchboxes"
                            :key="lb.id"
                            :lunchbox="lb"
                            :formatCurrency="formatCurrency"
                            :formatDate="formatDate"
                            @view-detail="viewDetail"
                            @delete-lunchbox="deleteLunchbox"
                        />
                    </tbody>
                </table>
            </div>
        </div>
    </main>
</template>
