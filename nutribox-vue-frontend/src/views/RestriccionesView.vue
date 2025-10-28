<script setup>
import { ref, onMounted, watch } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { getUserDetail, hasRequiredMembership } from '@/utils/user';
import authService from '@/services/auth.service';
import RestrictionItem from '@/components/RestrictionItem.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const userData = ref(null);
const hijos = ref([]);
const foods = ref([]);
const currentRestrictions = ref([]);
const isLoading = ref(true);
const selectedHijoId = ref(null);

const isPremium = hasRequiredMembership('Premium');

const loadInitialData = async () => {
    isLoading.value = true;
    userData.value = getUserDetail();
    if (!userData.value) {
        authService.logout();
        return;
    }

    if (!isPremium) {
        isLoading.value = false;
        return;
    }

    try {
        const [childrenList, foodList] = await Promise.all([
            apiService.get('/children?usuario_id=' + userData.value.id),
            apiService.get('/foods?only_active=all')
        ]);
        
        hijos.value = childrenList;
        foods.value = foodList;
        
        const urlHijoId = router.currentRoute.value.query.hijoId;
        if (urlHijoId) {
            selectedHijoId.value = parseInt(urlHijoId);
        }
        
        isLoading.value = false;
    } catch (error) {
        isLoading.value = false;
        Swal.fire('Error', error.message || 'No se pudieron cargar los datos iniciales.', 'error');
    }
};

const loadRestrictions = async () => {
    if (!selectedHijoId.value) {
        currentRestrictions.value = [];
        return;
    }
    
    try {
        Swal.showLoading();
        currentRestrictions.value = await apiService.get('/restrictions?hijo_id=' + selectedHijoId.value);
        Swal.close();
    } catch (error) {
        Swal.close();
        Swal.fire('Error', error.message || 'Error al cargar restricciones.', 'error');
    }
};

const showAddRestrictionModal = async () => {
    const foodOptions = foods.value.filter(f => f.activo).map(f => 
        '<option value="' + f.id + '">' + f.nombre + '</option>'
    ).join("");

    const swalHtml = 
        '<select id="swal-tipo" class="form-select mb-3">' +
            '<option value="alergia">Alergia (a un alimento especifico)</option>' +
            '<option value="prohibido">Prohibido (match por texto)</option>' +
        '</select>' +
        '<div id="alimento-field" class="mb-3">' +
            '<select id="swal-alimento" class="form-select">' +
                '<option value="">Selecciona Alimento</option>' +
                foodOptions +
            '</select>' +
        '</div>' +
        '<div id="texto-field" class="mb-3" style="display: none;">' +
            '<input id="swal-texto" class="form-control" placeholder="Ej: mani, gluten, colorante rojo">' +
        '</div>';

    const { value: formValues } = await Swal.fire({
        title: "Agregar Restriccion",
        html: swalHtml,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: "#4CAF50",
        cancelButtonColor: "#DC3545",
        confirmButtonText: "Guardar Restriccion",
        preConfirm: () => {
            const tipo = document.getElementById("swal-tipo").value;
            const alimentoId = document.getElementById("swal-alimento").value;
            const texto = document.getElementById("swal-texto").value;
            
            if (tipo === "alergia" && !alimentoId) {
                Swal.showValidationMessage('Debes seleccionar un alimento para la alergia');
                return false;
            }
            if (tipo === "prohibido" && !texto.trim()) {
                Swal.showValidationMessage('El campo de texto es requerido para esta restriccion');
                return false;
            }
            
            return {
                hijo_id: parseInt(selectedHijoId.value),
                tipo,
                alimento_id: tipo === "alergia" ? parseInt(alimentoId) : null,
                texto: tipo === "prohibido" ? texto.trim() : null
            };
        },
        didOpen: () => {
            const tipoSelect = document.getElementById("swal-tipo");
            const alimentoField = document.getElementById("alimento-field");
            const textoField = document.getElementById("texto-field");

            const toggleFields = () => {
                if (tipoSelect.value === "alergia") {
                    alimentoField.style.display = "block";
                    textoField.style.display = "none";
                } else {
                    alimentoField.style.display = "none";
                    textoField.style.display = "block";
                }
            };
            tipoSelect.addEventListener("change", toggleFields);
            toggleFields();
        }
    });
    
    if (formValues) {
        try {
            Swal.showLoading();
            await apiService.post('/restrictions', formValues);
            Swal.close();
            Swal.fire('Exito', 'Restriccion agregada correctamente', 'success');
            await loadRestrictions();
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'Error al agregar restriccion', 'error');
        }
    }
};

const deleteRestriction = async (id) => {
    const result = await Swal.fire({
        title: "Eliminar restriccion?",
        text: "Esta restriccion sera eliminada permanentemente.",
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
            await apiService.delete('/restrictions/' + id);
            Swal.close();
            Swal.fire('Exito', 'Restriccion eliminada', 'success');
            await loadRestrictions();
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'Error al eliminar restriccion', 'error');
        }
    }
};

watch(selectedHijoId, loadRestrictions);

onMounted(() => {
    loadInitialData();
});
</script>

<template>
    <main class="flex-grow-1 p-4 bg-light">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3">Restricciones Alimentarias</h1>
                <p class="text-muted">Gestiona las alergias y alimentos prohibidos por cada hijo.</p>
            </div>
        </div>

        <div v-if="!isPremium" class="card p-5 text-center card-shadow">
            <i class="fas fa-lock text-warning mb-3" style="font-size: 48px;"></i>
            <h3 class="h4">Funcion Premium</h3>
            <p class="text-muted mb-4">La gestion de restricciones alimentarias es exclusiva del Plan Premium.</p>
        </div>

        <div v-else class="row g-4">
            <div class="col-md-4">
                <div class="card card-shadow p-3 mb-4">
                    <h5 class="card-title fw-bold">Hijo a Gestionar</h5>
                    <select id="hijoSelect" class="form-select mb-3" v-model="selectedHijoId" :disabled="isLoading">
                        <option :value="null">Selecciona un hijo</option>
                        <option v-for="h in hijos" :key="h.id" :value="h.id">{{ h.nombre }}</option>
                    </select>
                    <button 
                        class="btn btn-primary-nb w-100" 
                        @click="showAddRestrictionModal" 
                        :disabled="!selectedHijoId || isLoading"
                    >
                        <i class="fas fa-plus me-1"></i> Agregar Restriccion
                    </button>
                </div>
            </div>
            
            <div class="col-md-8">
                <div class="card card-shadow p-4">
                    <h5 class="card-title fw-bold">Restricciones Activas</h5>
                    <div v-if="isLoading" class="text-center py-4">
                        <i class="fas fa-spinner fa-spin text-primary-nb me-2"></i> Cargando...
                    </div>
                    <div v-else-if="!selectedHijoId" class="py-4">
                        <p class="text-center text-muted">Selecciona un hijo para ver sus restricciones.</p>
                    </div>
                    <div v-else-if="currentRestrictions.length === 0" class="py-4">
                        <p class="text-center text-muted">Este hijo no tiene restricciones registradas. Agrega la primera!</p>
                    </div>
                    <ul v-else class="list-group list-group-flush">
                        <RestrictionItem 
                            v-for="r in currentRestrictions"
                            :key="r.id"
                            :restriction="r"
                            @delete-restriction="deleteRestriction"
                        />
                    </ul>
                </div>
            </div>
        </div>
    </main>
</template>

<style scoped>
/* Los estilos de Bootstrap y main.css manejan la apariencia */
.sidebar { height: 100vh; }
.nav-link.router-link-active, .nav-link.active { background-color: var(--primary) !important; color: white !important; }
</style>