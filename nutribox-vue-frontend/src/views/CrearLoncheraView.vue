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
const fecha = ref(new Date().toISOString().split("T")[0]);
const direccionId = ref(null);

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
    
    restricciones.value
        .filter(r => r.tipo === "alergia" && r.alimento_id)
        .forEach(r => {
            if (selectedFoods.value.some(f => f.id === r.alimento_id)) {
                const alimentoAlergico = foods.value.find(f => f.id === r.alimento_id)?.nombre || "Alimento prohibido";
                alerts.push({
                    type: 'danger',
                    message: 'ALERGIA CRITICA: Contiene ' + alimentoAlergico + '.',
                    isCritical: true
                });
            }
        });

    const textosProhibidos = restricciones.value
        .filter(r => r.tipo === "prohibido" && r.texto)
        .map(r => r.texto.toLowerCase());
        
    selectedFoods.value.forEach(f => {
        if (textosProhibidos.some(t => f.nombre.toLowerCase().includes(t))) {
            alerts.push({
                type: 'warning',
                message: 'Advertencia: El alimento ' + f.nombre + ' podria contener ingredientes prohibidos.',
                isCritical: false
            });
        }
    });

    if (totalCalorias.value > 500) {
        alerts.push({
            type: 'info',
            message: 'La lonchera supera las 500 kcal recomendadas.',
            isCritical: false
        });
    } else if (totalCalorias.value < 200 && totalCalorias.value > 0) {
        alerts.push({
            type: 'info',
            message: 'Bajo contenido calorico (menos de 200 kcal).',
            isCritical: false
        });
    }

    return alerts;
});

const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(value);
};

const loadChildRestrictions = async () => {
    if (!hijoId.value) {
        restricciones.value = [];
        return;
    }
    try {
        restricciones.value = await apiService.get('/restrictions?hijo_id=' + hijoId.value);
    } catch (error) {
        restricciones.value = [];
        console.error("Error al cargar restricciones:", error);
    }
};

watch(hijoId, loadChildRestrictions);


const addFood = (foodId) => {
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
    if (!hijoId.value || !fecha.value || selectedFoods.value.length === 0) {
        Swal.fire('Error', 'Debes completar Hijo, Fecha y agregar alimentos', 'warning');
        return;
    }
    
    const tieneAlergiaCritica = alertas.value.some(a => a.isCritical);

    if (tieneAlergiaCritica) {
        const result = await Swal.fire({
            title: "¡ALERTA CRITICA!",
            text: "Esta lonchera contiene un alimento que causa ALERGIA grave al niño. ¿Deseas continuar bajo tu responsabilidad?",
            icon: 'error',
            showCancelButton: true,
            confirmButtonColor: '#4CAF50',
            cancelButtonColor: '#F44336',
            confirmButtonText: 'Si, continuar',
            cancelButtonText: 'Cancelar'
        });
        if (!result.isConfirmed) {
            return;
        }
    }
    
    try {
        Swal.showLoading();
        
        const lunchbox = await apiService.post('/lunchboxes', {
            hijo_id: parseInt(hijoId.value),
            fecha: fecha.value,
            estado: "Borrador",
            direccion_id: direccionId.value ? parseInt(direccionId.value) : null
        });
        
        for (const food of selectedFoods.value) {
            await apiService.post('/lunchboxes/' + lunchbox.id + '/items', {
                alimento_id: food.id,
                cantidad: food.cantidad
            });
        }
        
        Swal.close();
        
        Swal.fire('¡Exito!', 'Lonchera creada correctamente', 'success');
        
        setTimeout(() => {
            router.push('/mis-loncheras');
        }, 2000);
        
    } catch (error) {
        Swal.close();
        Swal.fire('Error', error.message || 'No se pudo completar la creacion de la lonchera', 'error');
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
    }
    
    isLoading.value = false;
  } catch (error) {
    isLoading.value = false;
    Swal.fire('Error', error.message || 'No se pudieron cargar los datos iniciales.', 'error');
  }
};

onMounted(() => {
  // ELIMINAMOS EL BLOQUEO INICIAL. El router ya asegura que sea Estandar/Premium.
  loadData();
});
</script>

<template>
  <main class="flex-grow-1 p-4 bg-light">
    <div class="dashboard-header mb-4">
        <h1 class="h3">Crear Nueva Lonchera</h1>
        <p class="text-muted">Selecciona los alimentos y asigna la entrega (Plan: {{ userData?.membresia?.tipo }})</p>
    </div>

    <div v-if="isLoading" class="text-center p-5">
      <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
      <p class="mt-2 text-muted">Cargando datos...</p>
    </div>

    <div v-else class="row g-4">
        <div class="col-lg-6">
            <div class="card p-4 card-shadow mb-4">
                <h5 class="fw-bold mb-3">Informacion de la Lonchera</h5>
                <form @submit.prevent="createLunchbox">
                    <div class="mb-3">
                        <label class="form-label">Hijo</label>
                        <select id="hijoSelect" class="form-select" required v-model="hijoId">
                            <option :value="null" disabled>Selecciona un hijo</option>
                            <option v-for="h in hijos" :key="h.id" :value="h.id">{{ h.nombre }}</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Fecha</label>
                        <input type="date" id="fechaInput" class="form-control" required v-model="fecha" :min="fecha">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Direccion de Entrega</label>
                        <select id="direccionSelect" class="form-select" v-model="direccionId">
                            <option :value="null">Selecciona una direccion (opcional)</option>
                            <option v-for="d in direcciones" :key="d.id" :value="d.id">{{ d.etiqueta }} - {{ d.direccion }}</option>
                        </select>
                    </div>
                </form>
            </div>

            <div v-if="canPersonalize" class="card p-4 card-shadow">
                <h5 class="fw-bold mb-3">Catalogo de Alimentos (Premium)</h5>
                <input type="text" v-model="searchTerm" class="form-control mb-3" placeholder="Buscar alimento...">
                <div id="foodsContainer" style="max-height: 400px; overflow-y: auto;">
                    <FoodItemCard 
                        v-for="food in filteredFoods" 
                        :key="food.id"
                        :food="food"
                        :formatCurrency="formatCurrency"
                        @add-food="addFood"
                    />
                    <p v-if="filteredFoods.length === 0" class="text-center text-muted">No se encontraron alimentos.</p>
                </div>
            </div>
            <div v-else class="card p-4 card-shadow text-center">
                 <i class="fas fa-lock text-warning mb-3" style="font-size: 48px;"></i>
                 <p class="text-muted">La **Seleccion Alimento por Alimento** requiere el Plan Premium. Usa la seccion de Menus Predeterminados.</p>
            </div>
        </div>

        <div class="col-lg-6">
            <div class="card p-4 card-shadow mb-4">
                <h5 class="fw-bold mb-3">Alimentos Seleccionados ({{ selectedFoods.length }})</h5>
                <div id="selectedFoodsContainer" style="min-height: 150px;">
                    <SelectedFoodItem 
                        v-for="food in selectedFoods"
                        :key="food.id"
                        :food="food"
                        :formatCurrency="formatCurrency"
                        @update-quantity="updateQuantity"
                        @remove-food="removeFood"
                    />
                    <p v-if="selectedFoods.length === 0" class="text-center text-muted">No hay alimentos seleccionados</p>
                </div>
            </div>

            <div class="card p-4 card-shadow">
                <h5 class="fw-bold mb-3">Resumen Nutricional y Costos</h5>
                
                <div class="d-flex justify-content-between mb-2 border-bottom">
                    <span>Calorias Totales:</span>
                    <strong id="totalCalorias">{{ totalCalorias.toFixed(1) }} kcal</strong>
                </div>
                <div class="d-flex justify-content-between mb-2 border-bottom">
                    <span>Proteinas Totales:</span>
                    <strong id="totalProteinas">{{ totalProteinas.toFixed(1) }} g</strong>
                </div>
                <div class="d-flex justify-content-between mb-3 border-bottom">
                    <span>Carbohidratos Totales:</span>
                    <strong id="totalCarbos">{{ totalCarbos.toFixed(1) }} g</strong>
                </div>
                 <div class="d-flex justify-content-between mb-4">
                    <span class="fw-bold fs-5">Costo Total Estimado:</span>
                    <strong id="totalCosto" class="fs-5 text-danger">{{ formatCurrency(totalCosto) }}</strong>
                </div>

                <div id="alertasRestriccion" class="mb-3">
                    <div v-for="(alert, index) in alertas" :key="index" :class="'alert alert-' + alert.type + ' p-2 mb-2'" role="alert">
                         <i :class="['fas', alert.isCritical ? 'fa-exclamation-triangle' : 'fa-balance-scale', 'me-1']"></i> 
                         {{ alert.message }}
                    </div>
                </div>

                <button class="btn btn-primary-nb w-100 py-2" @click="createLunchbox" :disabled="selectedFoods.length === 0 || !hijoId">
                    <i class="fas fa-check me-2"></i> Crear Lonchera
                </button>
            </div>
        </div>
    </div>
  </main>
</template>
