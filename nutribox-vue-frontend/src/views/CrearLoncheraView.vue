<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { getUserDetail, hasRequiredMembership } from '@/utils/user';
import authService from '@/services/auth.service';
import FoodItemCard from '@/components/FoodItemCard.vue';
import SelectedFoodItem from '@/components/SelectedFoodItem.vue';

const route = useRoute();
const router = useRouter();

const userData = ref(null);
const isLoading = ref(true);
const foods = ref([]);
const hijos = ref([]);
const direcciones = ref([]);
const restricciones = ref([]);
const selectedFoods = ref([]);
const searchTerm = ref('');

const hijoId = ref(null);
// Establece la fecha mínima de hoy
const minDate = new Date().toISOString().split("T")[0]; 
const fecha = ref(minDate); 
const direccionId = ref(null);

// Lógica de permisos
const canPersonalize = hasRequiredMembership('Premium'); 
const canCreate = hasRequiredMembership('Estandar'); 

const filteredFoods = computed(() => {
    if (!searchTerm.value) return foods.value;
    const search = searchTerm.value.toLowerCase();
    return foods.value.filter(f => f.nombre.toLowerCase().includes(search));
});

const totalCalorias = computed(() => {
    return selectedFoods.value.reduce((sum, f) => sum + (f.kcal * f.cantidad), 0);
});

const totalProteinas = computed(() => {
    return selectedFoods.value.reduce((sum, f) => sum + (f.proteinas * f.cantidad), 0);
});

const totalCarbos = computed(() => {
    return selectedFoods.value.reduce((sum, f) => sum + (f.carbos * f.cantidad), 0);
});

const totalCosto = computed(() => {
    return selectedFoods.value.reduce((sum, f) => sum + (f.costo * f.cantidad), 0);
});

const alertas = computed(() => {
    const alerts = [];
    
    // 1. Alergias Críticas (ROJO)
    restricciones.value
        .filter(r => r.tipo === "alergia" && r.alimento_id)
        .forEach(r => {
            if (selectedFoods.value.some(f => f.id === r.alimento_id)) {
                const alimentoAlergico = foods.value.find(f => f.id === r.alimento_id)?.nombre || "Alimento prohibido";
                alerts.push({
                    type: 'danger',
                    message: 'ALERGIA CRÍTICA: Contiene ' + alimentoAlergico + '.',
                    isCritical: true
                });
            }
        });

    // 2. Prohibidos por Texto (AMARILLO/NARANJA)
    const textosProhibidos = restricciones.value
        .filter(r => r.tipo === "prohibido" && r.texto)
        .map(r => r.texto.toLowerCase());
        
    selectedFoods.value.forEach(f => {
        if (textosProhibidos.some(t => f.nombre.toLowerCase().includes(t))) {
            alerts.push({
                type: 'warning',
                message: 'ADVERTENCIA: El alimento ' + f.nombre + ' podría contener ingredientes prohibidos (' + textosProhibidos.join(', ') + ').',
                isCritical: false
            });
        }
    });

    // 3. Alertas Nutricionales (INFO)
    if (totalCalorias.value > 500) {
        alerts.push({
            type: 'info',
            message: 'La lonchera supera las 500 kcal recomendadas.',
            isCritical: false
        });
    } else if (totalCalorias.value < 200 && totalCalorias.value > 0) {
        alerts.push({
            type: 'info',
            message: 'Bajo contenido calórico (menos de 200 kcal).',
            isCritical: false
        });
    }

    return alerts;
});

const formatCurrency = (value) => {
    // Usar el estilo local colombiano
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(value);
};

const loadChildRestrictions = async () => {
    if (!hijoId.value) {
        restricciones.value = [];
        return;
    }
    // Si no es premium, no cargamos restricciones
    if (!hasRequiredMembership('Premium')) return;

    try {
        // Obtenemos el detalle del hijo, incluyendo restricciones, para la validación interna
        const detail = await apiService.get('/children/' + hijoId.value + '/detail');
        restricciones.value = detail.restricciones || [];
    } catch (error) {
        restricciones.value = [];
        console.error("Error al cargar restricciones:", error);
    }
};

watch(hijoId, loadChildRestrictions);


const addFood = (foodId) => {
    if (!canPersonalize.value) {
        Swal.fire('Función Premium', 'La adición de alimentos individuales requiere el Plan Premium.', 'warning');
        return;
    }
    const food = foods.value.find(f => f.id === foodId);
    if (!food) return;
    
    const existing = selectedFoods.value.find(f => f.id === foodId);
    if (existing) {
        existing.cantidad++;
    } else {
        selectedFoods.value.push({
            id: food.id,
            nombre: food.nombre,
            kcal: food.kcal,
            proteinas: food.proteinas,
            carbos: food.carbos,
            costo: food.costo, 
            cantidad: 1
        });
    }
};

const removeFood = (foodId) => {
    selectedFoods.value = selectedFoods.value.filter(f => f.id !== foodId);
};

const updateQuantity = (foodId, cantidad) => {
    const food = selectedFoods.value.find(f => f.id === foodId);
    if (food) {
        food.cantidad = Math.max(1, parseInt(cantidad));
    }
};

const createLunchbox = async () => {
    if (!canCreate.value) {
         Swal.fire('Plan Requerido', 'Necesitas el Plan Estándar o Premium para crear una lonchera.', 'warning');
        return;
    }

    if (!hijoId.value || !fecha.value || selectedFoods.value.length === 0) {
        Swal.fire('Error', 'Debes completar Hijo, Fecha y agregar alimentos', 'warning');
        return;
    }
    
    // Alerta crítica de alergia antes de crear
    const tieneAlergiaCritica = alertas.value.some(a => a.isCritical);

    if (tieneAlergiaCritica) {
        const result = await Swal.fire({
            title: "¡ALERTA CRÍTICA!",
            text: "Esta lonchera contiene un alimento que causa ALERGIA grave al niño. ¿Deseas continuar bajo tu responsabilidad?",
            icon: 'error',
            showCancelButton: true,
            confirmButtonColor: '#1F8D45', // primary
            cancelButtonColor: '#E53935', // danger
            confirmButtonText: 'Sí, continuar',
            cancelButtonText: 'Cancelar'
        });
        if (!result.isConfirmed) {
            return;
        }
    }
    
    try {
        Swal.showLoading();
        
        // 1. Crear lonchera
        const lunchbox = await apiService.post('/lunchboxes', {
            hijo_id: parseInt(hijoId.value),
            fecha: fecha.value,
            estado: "Borrador", // RF3.1
            direccion_id: direccionId.value ? parseInt(direccionId.value) : null
        });
        
        // 2. Agregar items
        for (const food of selectedFoods.value) {
            await apiService.post('/lunchboxes/' + lunchbox.id + '/items', {
                alimento_id: food.id,
                cantidad: food.cantidad
            });
        }
        
        Swal.close();
        
        Swal.fire('¡Éxito!', 'Lonchera creada correctamente', 'success');
        
        setTimeout(() => {
            router.push('/app/mis-loncheras');
        }, 2000);
        
    } catch (error) {
        Swal.close();
        Swal.fire('Error', error.message || 'No se pudo completar la creación de la lonchera', 'error');
    }
};


const loadData = async () => {
  isLoading.value = true;
  userData.value = getUserDetail();
  if (!userData.value) {
    authService.logout();
    return;
  }
  
  try {
    const [foodList, childList, addressList] = await Promise.all([
        // Cargamos todos los alimentos activos (true)
        apiService.get('/foods?only_active=true'), 
        apiService.get('/children?usuario_id=' + userData.value.id),
        apiService.get('/addresses?usuario_id=' + userData.value.id)
    ]);
    
    foods.value = foodList;
    hijos.value = childList;
    direcciones.value = addressList;

    const preselectedHijoId = route.query.hijoId;
    if (preselectedHijoId) {
        hijoId.value = parseInt(preselectedHijoId);
        loadChildRestrictions(); // Carga restricciones si hay hijo preseleccionado
    }
    
    isLoading.value = false;
  } catch (error) {
    isLoading.value = false;
    Swal.fire('Error', error.message || 'No se pudieron cargar los datos iniciales.', 'error');
  }
};

onMounted(() => {
  if (canCreate.value) {
    loadData();
  } else {
      isLoading.value = false;
  }
});
</script>

<template>
  <main class="flex-grow-1 p-4 bg-light-nb">
    <div class="dashboard-header mb-4">
        <h1 class="h3 text-dark-nb">Crear Nueva Lonchera</h1>
        <p class="text-muted-dark">Selecciona los alimentos y asigna la entrega (Plan: {{ userData?.membresia?.tipo }})</p>
    </div>

    <div v-if="!canCreate" class="card p-5 text-center card-shadow">
        <i class="fas fa-lock text-secondary-nb mb-3" style="font-size: 48px;"></i>
        <h3 class="h4 text-dark-nb">Función de Plan Estándar o Premium</h3>
        <p class="text-muted-dark mb-4">La creación de loncheras es exclusiva de los planes Estándar y Premium.</p>
        <router-link to="/app/perfil" class="btn btn-warning-nb w-auto mx-auto text-dark-nb">Ver Planes</router-link>
    </div>

    <div v-else-if="isLoading" class="text-center p-5 bg-light-nb">
      <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
      <p class="mt-2 text-muted-dark">Cargando datos...</p>
    </div>

    <div v-else class="row g-4">
        <div class="col-lg-6">
            <div class="card p-4 card-shadow mb-4">
                <h5 class="fw-bold mb-3 text-dark-nb">Información de la Lonchera</h5>
                <form @submit.prevent="createLunchbox">
                    <div class="mb-3">
                        <label class="form-label text-dark-nb">Hijo</label>
                        <select id="hijoSelect" class="form-select" required v-model="hijoId">
                            <option :value="null" disabled>Selecciona un hijo</option>
                            <option v-for="h in hijos" :key="h.id" :value="h.id">{{ h.nombre }}</option>
                        </select>
                        <p v-if="hijos.length === 0" class="text-danger small mt-2">¡Debes agregar un hijo primero!</p>
                    </div>
                    <div class="mb-3">
                        <label class="form-label text-dark-nb">Fecha</label>
                        <input type="date" id="fechaInput" class="form-control" required v-model="fecha" :min="minDate">
                    </div>
                    <div class="mb-3">
                        <label class="form-label text-dark-nb">Dirección de Entrega</label>
                        <select id="direccionSelect" class="form-select" v-model="direccionId">
                            <option :value="null">Selecciona una dirección (opcional)</option>
                            <option v-for="d in direcciones" :key="d.id" :value="d.id">{{ d.etiqueta }} - {{ d.direccion }}</option>
                        </select>
                        <p v-if="direcciones.length === 0" class="text-muted-dark small mt-2">Agrega direcciones en la sección Direcciones.</p>
                    </div>
                </form>
            </div>

            <div class="card p-4 card-shadow">
                <h5 class="fw-bold mb-3 text-dark-nb">
                    Catálogo de Alimentos 
                    <span v-if="canPersonalize" class="badge bg-primary-light text-dark-nb">Premium</span>
                </h5>
                <input type="text" v-model="searchTerm" class="form-control mb-3" placeholder="Buscar alimento...">
                <div v-if="!canPersonalize" class="text-center p-3 border rounded">
                    <p class="text-muted-dark mb-0 small">Solo puedes agregar alimentos desde "Menús Predeterminados" con tu plan actual.</p>
                </div>
                <div v-else id="foodsContainer" style="max-height: 400px; overflow-y: auto;">
                    <FoodItemCard 
                        v-for="food in filteredFoods" 
                        :key="food.id"
                        :food="food"
                        :formatCurrency="formatCurrency"
                        @add-food="addFood"
                    />
                    <p v-if="filteredFoods.length === 0" class="text-center text-muted-dark">No se encontraron alimentos activos.</p>
                </div>
            </div>
        </div>

        <div class="col-lg-6">
            <div class="card p-4 card-shadow mb-4">
                <h5 class="fw-bold mb-3 text-dark-nb">Alimentos Seleccionados ({{ selectedFoods.length }})</h5>
                <div id="selectedFoodsContainer" style="min-height: 150px;">
                    <SelectedFoodItem 
                        v-for="food in selectedFoods"
                        :key="food.id"
                        :food="food"
                        :formatCurrency="formatCurrency"
                        @update-quantity="updateQuantity"
                        @remove-food="removeFood"
                    />
                    <p v-if="selectedFoods.length === 0" class="text-center text-muted-dark">No hay alimentos seleccionados</p>
                </div>
            </div>

            <div class="card p-4 card-shadow">
                <h5 class="fw-bold mb-3 text-dark-nb">Resumen Nutricional y Alertas</h5>
                
                <div class="d-flex justify-content-between mb-2 border-bottom">
                    <span class="text-dark-nb">Calorías Totales:</span>
                    <strong id="totalCalorias" class="text-primary-nb">{{ totalCalorias.toFixed(1) }} kcal</strong>
                </div>
                <div class="d-flex justify-content-between mb-2 border-bottom">
                    <span class="text-dark-nb">Proteínas Totales:</span>
                    <strong id="totalProteinas" class="text-dark-nb">{{ totalProteinas.toFixed(1) }} g</strong>
                </div>
                <div class="d-flex justify-content-between mb-3 border-bottom">
                    <span class="text-dark-nb">Carbohidratos Totales:</span>
                    <strong id="totalCarbos" class="text-dark-nb">{{ totalCarbos.toFixed(1) }} g</strong>
                </div>
                 <div class="d-flex justify-content-between mb-4">
                    <span class="fw-bold fs-5 text-dark-nb">Costo Total Estimado:</span>
                    <strong id="totalCosto" class="fs-5 text-danger">{{ formatCurrency(totalCosto) }}</strong>
                </div>

                <div id="alertasRestriccion" class="mb-3">
                    <div v-for="(alert, index) in alertas" :key="index" :class="'alert alert-' + alert.type + ' p-2 mb-2 fw-bold'" role="alert">
                         <i :class="['fas', alert.isCritical ? 'fa-exclamation-triangle' : 'fa-balance-scale', 'me-1']"></i> 
                         {{ alert.message }}
                    </div>
                </div>

                <button class="btn btn-primary-nb w-100 py-3" @click="createLunchbox" :disabled="selectedFoods.length === 0 || !hijoId">
                    <i class="fas fa-check me-2"></i> Crear Lonchera (Borrador)
                </button>
            </div>
        </div>
    </div>
  </main>
</template>
