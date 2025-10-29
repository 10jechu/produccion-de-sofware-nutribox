<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { getUserDetail } from '@/utils/user';
import authService from '@/services/auth.service';
import FoodItemCard from '@/components/FoodItemCard.vue';
import SelectedFoodItem from '@/components/SelectedFoodItem.vue';
import { useRouter, useRoute } from 'vue-router'; // Importa useRoute

// --- 1. Definición de Variables Reactivas ---
const isLoading = ref(true);
const userData = ref(null);
const foods = ref([]); // Catálogo completo
const hijos = ref([]);
const direcciones = ref([]);
const selectedFoods = ref([]); // Alimentos en la lonchera actual
const restricciones = ref([]); // Restricciones del hijo seleccionado

// --- Modelo del formulario ---
const selectedHijoId = ref(null);
const selectedDate = ref(new Date().toISOString().split("T")[0]); // Fecha de hoy por defecto
const selectedDireccionId = ref(null);
const searchTerm = ref(''); // Para buscar alimentos

const router = useRouter();
const route = useRoute(); // Para leer query params

// --- Funciones Auxiliares ---
function formatCurrency(value) {
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(value);
}

// --- Lógica de Carga Inicial ---
const loadInitialData = async () => {
    isLoading.value = true;
    userData.value = getUserDetail();
    if (!userData.value) {
        authService.logout(); // Ya redirige a login
        return;
    }

    try {
        // Carga en paralelo
        const [foodsList, childrenList, addressesList] = await Promise.all([
            apiService.get('/foods?only_active=true'), // Solo activos para crear lonchera
            apiService.get('/children?usuario_id=' + userData.value.id),
            apiService.get('/addresses?usuario_id=' + userData.value.id)
        ]);
        foods.value = foodsList;
        hijos.value = childrenList;
        direcciones.value = addressesList;

        // Preseleccionar hijo si viene en la URL
        const hijoIdFromUrl = route.query.hijoId;
        if (hijoIdFromUrl && hijos.value.some(h => h.id === parseInt(hijoIdFromUrl))) {
          selectedHijoId.value = parseInt(hijoIdFromUrl);
          // Cargar restricciones automáticamente si hay hijo preseleccionado
          await loadChildRestrictions();
        }

        isLoading.value = false;
    } catch (error) {
        isLoading.value = false;
        Swal.fire('Error', error.message || 'No se pudieron cargar los datos iniciales.', 'error');
    }
};

// --- Cargar Restricciones al Cambiar Hijo ---
const loadChildRestrictions = async () => {
    if (!selectedHijoId.value) {
        restricciones.value = [];
        return; // No necesita calcular nutrición si no hay hijo
    }
    try {
        // Usar Swal.showLoading/close aquí si la carga es lenta
        restricciones.value = await apiService.get('/restrictions?hijo_id=' + selectedHijoId.value);
        // Validar restricciones con alimentos ya seleccionados (si los hay)
        updateNutritionAndAlerts();
    } catch (error) {
        restricciones.value = [];
        updateNutritionAndAlerts(); // Aún recalcular por si acaso
        console.error("Error al cargar restricciones:", error);
        // Podrías mostrar un Swal.fire pequeño aquí si prefieres
    }
};

// --- Watcher para cargar restricciones cuando cambia el hijo seleccionado ---
watch(selectedHijoId, loadChildRestrictions);

// --- Lógica para Manejar Alimentos ---
const addFood = (foodId) => {
    const foodToAdd = foods.value.find(f => f.id === foodId);
    if (!foodToAdd) return;

    const existing = selectedFoods.value.find(f => f.id === foodId);
    if (existing) {
        existing.cantidad++;
    } else {
        selectedFoods.value.push({
            id: foodToAdd.id,
            nombre: foodToAdd.nombre,
            kcal: foodToAdd.kcal,
            proteinas: foodToAdd.proteinas,
            carbos: foodToAdd.carbos,
            costo: foodToAdd.costo,
            cantidad: 1
        });
    }
    updateNutritionAndAlerts();
};

const removeFood = (foodId) => {
    selectedFoods.value = selectedFoods.value.filter(f => f.id !== foodId);
    updateNutritionAndAlerts();
};

const updateQuantity = (foodId, newQuantity) => {
    const food = selectedFoods.value.find(f => f.id === foodId);
    if (food) {
        const quantity = parseInt(newQuantity);
        food.cantidad = !isNaN(quantity) && quantity >= 1 ? quantity : 1; // Asegura que sea >= 1
    }
    updateNutritionAndAlerts(); // Recalcula al cambiar cantidad
};

// --- Cálculo de Nutrición y Alertas ---
const nutritionSummary = computed(() => {
    const summary = {
        totalCalorias: 0,
        totalProteinas: 0,
        totalCarbos: 0,
        totalCosto: 0,
        alertas: [] // Array para mensajes de alerta
    };

    selectedFoods.value.forEach(food => {
        summary.totalCalorias += food.kcal * food.cantidad;
        summary.totalProteinas += food.proteinas * food.cantidad;
        summary.totalCarbos += food.carbos * food.cantidad;
        summary.totalCosto += food.costo * food.cantidad;
    });

    // Validar Restricciones (si hay hijo seleccionado)
    if (selectedHijoId.value && restricciones.value.length > 0) {
        // Alergias
        restricciones.value.filter(r => r.tipo === 'alergia').forEach(r => {
            if (selectedFoods.value.some(f => f.id === r.alimento_id)) {
                const alimentoAlergico = foods.value.find(f => f.id === r.alimento_id)?.nombre || "Alimento prohibido";
                summary.alertas.push({ type: 'danger', message: `ALERGIA CRÍTICA: Contiene ${alimentoAlergico}.` });
            }
        });
        // Prohibidos
        const textosProhibidos = restricciones.value.filter(r => r.tipo === 'prohibido' && r.texto).map(r => r.texto.toLowerCase());
        selectedFoods.value.forEach(f => {
            if (textosProhibidos.some(t => f.nombre.toLowerCase().includes(t))) {
                 summary.alertas.push({ type: 'warning', message: `Advertencia: ${f.nombre} podría contener ${textosProhibidos.join(", ")}.` });
            }
        });
    }

    // Alertas Nutricionales
    if (summary.totalCalorias > 500) {
        summary.alertas.push({ type: 'info', message: 'Supera las 500 kcal recomendadas.' });
    } else if (summary.totalCalorias < 200 && summary.totalCalorias > 0) {
         summary.alertas.push({ type: 'info', message: 'Bajo contenido calórico (< 200 kcal).' });
    }

    return summary;
});

// Función para forzar la actualización (si computed no es suficiente)
const updateNutritionAndAlerts = () => {
  // En Vue 3 Composition API, computed() es generalmente suficiente.
  // Esta función ahora solo llama a loadChildRestrictions si es necesario
  // o simplemente deja que 'computed' haga su trabajo.
};


// --- Filtrar Catálogo de Alimentos ---
const filteredFoods = computed(() => {
    if (!searchTerm.value) {
        return foods.value;
    }
    const lowerSearch = searchTerm.value.toLowerCase();
    return foods.value.filter(food =>
        food.nombre.toLowerCase().includes(lowerSearch)
    );
});

// --- Crear Lonchera ---
const createLunchbox = async () => {
    if (!selectedHijoId.value || !selectedDate.value || selectedFoods.value.length === 0) {
        Swal.fire("Error", "Debes seleccionar Hijo, Fecha y agregar al menos un alimento.", "warning");
        return;
    }

    // Verificar Alergias Críticas
    const tieneAlergiaCritica = nutritionSummary.value.alertas.some(a => a.type === 'danger');
    if (tieneAlergiaCritica) {
        const result = await Swal.fire({
            title: "¡ALERTA CRÍTICA!",
            text: "Esta lonchera contiene un alimento que causa ALERGIA grave al niño. ¿Deseas continuar bajo tu responsabilidad?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#4CAF50',
            cancelButtonColor: '#DC3545',
            confirmButtonText: 'Sí, continuar',
            cancelButtonText: 'Cancelar'
        });
        if (!result.isConfirmed) return;
    }

    try {
        Swal.fire({ title: 'Creando lonchera...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });

        // 1. Crear la lonchera base
        const newLunchbox = await apiService.post('/lunchboxes', {
            hijo_id: selectedHijoId.value,
            fecha: selectedDate.value,
            estado: "Borrador", // Siempre se crea como borrador
            direccion_id: selectedDireccionId.value ? parseInt(selectedDireccionId.value) : null
        });

        // 2. Agregar los items uno por uno
        for (const food of selectedFoods.value) {
            await apiService.post(`/lunchboxes/${newLunchbox.id}/items`, {
                alimento_id: food.id,
                cantidad: food.cantidad
            });
        }

        Swal.close();
        Swal.fire('¡Éxito!', 'Lonchera creada correctamente como Borrador.', 'success');

        // Redirigir a "Mis Loncheras" después de un momento
        setTimeout(() => {
            router.push('/mis-loncheras');
        }, 1500);

    } catch (error) {
        Swal.close();
        Swal.fire('Error', error.message || 'No se pudo crear la lonchera.', 'error');
    }
};

// --- Carga inicial al montar el componente ---
onMounted(() => {
    loadInitialData();
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
              <h5 class="fw-bold mb-3">Información de la Lonchera</h5>
              <form id="lunchboxForm">
                  <div class="mb-3">
                      <label class="form-label">Hijo</label>
                      <select id="hijoSelect" class="form-select" required v-model="selectedHijoId">
                          <option :value="null" disabled>Selecciona un hijo</option>
                          <option v-for="hijo in hijos" :key="hijo.id" :value="hijo.id">{{ hijo.nombre }}</option>
                      </select>
                  </div>
                  <div class="mb-3">
                      <label class="form-label">Fecha</label>
                      <input type="date" id="fechaInput" class="form-control" required v-model="selectedDate" :min="new Date().toISOString().split('T')[0]">
                  </div>
                  <div class="mb-3">
                      <label class="form-label">Dirección de Entrega</label>
                      <select id="direccionSelect" class="form-select" v-model="selectedDireccionId">
                          <option :value="null">Selecciona una dirección (opcional)</option>
                          <option v-for="dir in direcciones" :key="dir.id" :value="dir.id">{{ dir.etiqueta }} - {{ dir.direccion }}</option>
                      </select>
                  </div>
              </form>
          </div>

          <div class="card p-4 card-shadow">
              <h5 class="fw-bold mb-3">Catálogo de Alimentos ({{ filteredFoods.length }})</h5>
              <input type="text" id="searchFood" class="form-control mb-3" placeholder="Buscar alimento..." v-model="searchTerm">
              <div id="foodsContainer" style="max-height: 400px; overflow-y: auto;">
                  <p v-if="filteredFoods.length === 0" class="text-center text-muted">No se encontraron alimentos.</p>
                  <FoodItemCard
                      v-else
                      v-for="food in filteredFoods"
                      :key="food.id"
                      :food="food"
                      :formatCurrency="formatCurrency"
                      @add-food="addFood"
                  />
              </div>
          </div>
      </div>

      <div class="col-lg-6">
          <div class="card p-4 card-shadow mb-4">
              <h5 class="fw-bold mb-3">Alimentos Seleccionados ({{ selectedFoods.length }})</h5>
              <div id="selectedFoodsContainer" style="min-height: 150px; max-height: 400px; overflow-y: auto;">
                  <p v-if="selectedFoods.length === 0" class="text-center text-muted">No hay alimentos seleccionados</p>
                  <SelectedFoodItem
                      v-else
                      v-for="food in selectedFoods"
                      :key="food.id"
                      :food="food"
                      :formatCurrency="formatCurrency"
                      @update-quantity="updateQuantity"
                      @remove-food="removeFood"
                  />
              </div>
          </div>

          <div class="card p-4 card-shadow">
              <h5 class="fw-bold mb-3">Resumen Nutricional y Costos</h5>
              <div class="d-flex justify-content-between mb-2 border-bottom pb-2">
                  <span>Calorías Totales:</span>
                  <strong id="totalCalorias">{{ nutritionSummary.totalCalorias.toFixed(1) }} kcal</strong>
              </div>
              <div class="d-flex justify-content-between mb-2 border-bottom pb-2">
                  <span>Proteínas Totales:</span>
                  <strong id="totalProteinas">{{ nutritionSummary.totalProteinas.toFixed(1) }} g</strong>
              </div>
              <div class="d-flex justify-content-between mb-3 border-bottom pb-2">
                  <span>Carbohidratos Totales:</span>
                  <strong id="totalCarbos">{{ nutritionSummary.totalCarbos.toFixed(1) }} g</strong>
              </div>
               <div class="d-flex justify-content-between mb-4">
                  <span class="fw-bold fs-5">Costo Total Estimado:</span>
                  <strong id="totalCosto" class="fs-5 text-danger">{{ formatCurrency(nutritionSummary.totalCosto) }}</strong>
              </div>

              <div id="alertasRestriccion" class="mb-3">
                  <div v-for="(alerta, index) in nutritionSummary.alertas" :key="index"
                       :class="['alert', `alert-${alerta.type}`, 'p-2', 'mb-2']" role="alert">
                      <i :class="['fas', alerta.type === 'danger' || alerta.type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle', 'me-1']"></i>
                      {{ alerta.message }}
                  </div>
              </div>

              <button class="btn btn-primary-nb w-100 py-2" @click="createLunchbox" :disabled="selectedFoods.length === 0 || !selectedHijoId || !selectedDate">
                  <i class="fas fa-check me-2"></i> Crear Lonchera
              </button>
          </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
/* Estilos específicos si son necesarios */
#foodsContainer::-webkit-scrollbar,
#selectedFoodsContainer::-webkit-scrollbar {
  width: 6px;
}
#foodsContainer::-webkit-scrollbar-thumb,
#selectedFoodsContainer::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 3px;
}
</style>
