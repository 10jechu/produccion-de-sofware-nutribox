<script setup>
import { ref, onMounted, watch } from 'vue';
import { hasRequiredMembership, getUserDetail } from '@/utils/user';
import apiService from '@/services/api.service';
import Swal from 'sweetalert2';
import authService from '@/services/auth.service';

const canViewAdvanced = hasRequiredMembership('Premium'); // RF7.2
const canViewBasic = hasRequiredMembership('Estandar'); // RF7.1

const hijos = ref([]);
const selectedHijoId = ref(null);
const isLoading = ref(false); // Para los gráficos
const isLoadingData = ref(false); // Para el dropdown

let caloriesChartInstance = null;
let macrosChartInstance = null;

// --- Colores ---
const colorPrimary = '#4CAF50'; 
const colorSecondary = '#FF9800'; 
const colorAccent = '#2196F3';  
const colorLightGreen = 'rgba(76, 175, 80, 0.2)';

// --- ### INICIO DE LA CORRECCIÓN ### ---
// Esta función ahora lee desde localStorage, no llama a la API
function loadHijosFromStorage() {
  isLoadingData.value = true;
  const user = getUserDetail(); // Carga el usuario completo desde localStorage
  if (!user) { 
      authService.logout(); 
      return; 
  }
  
  // La lista de hijos ya viene en el objeto 'user'
  if (user.hijos && user.hijos.length > 0) {
    hijos.value = user.hijos;
  } else {
    hijos.value = [];
    console.warn("No se encontraron hijos en el UserDetail de localStorage.");
  }
  isLoadingData.value = false;
}
// --- ### FIN DE LA CORRECCIÓN ### ---

// --- Lógica para buscar datos y renderizar gráficos ---
async function fetchAndRenderStats() {
  if (!selectedHijoId.value || !canViewAdvanced) {
    return;
  }
  
  isLoading.value = true;
  try {
    const stats = await apiService.get('/children/' + selectedHijoId.value + '/statistics');
    renderCharts(stats); 
    isLoading.value = false;
  } catch (error) {
    isLoading.value = false;
    Swal.fire('Error de Estadísticas', error.message || 'No se pudieron cargar los datos del gráfico', 'error');
  }
}

// --- Observador ---
watch(selectedHijoId, fetchAndRenderStats);

// --- Montaje inicial ---
onMounted(() => {
    if (canViewAdvanced.value) {
        loadHijosFromStorage(); // Llama a la nueva función corregida
    }
});

// --- Lógica de Gráficos (AHORA ACEPTA DATOS) ---
const renderCharts = (statsData) => {
    if (typeof Chart === 'undefined' || !statsData) {
        console.error("Chart.js no está definido o no hay datos");
        return;
    }

    // --- Gráfico de Calorías (Datos Reales) ---
    const caloriesCtx = document.getElementById('caloriesChart')?.getContext('2d');
    if (caloriesCtx) {
        if (caloriesChartInstance) caloriesChartInstance.destroy();
        
        caloriesChartInstance = new Chart(caloriesCtx, {
            type: 'line',
            data: {
                labels: statsData.consumo_diario.map(d => d.fecha),
                datasets: [{
                    label: 'Calorías (kcal)',
                    data: statsData.consumo_diario.map(d => d.calorias),
                    borderColor: colorPrimary,
                    backgroundColor: colorLightGreen,
                    fill: true,
                    tension: 0.3
                }]
            },
            options: { scales: { y: { beginAtZero: false } } }
        });
    }

    // --- Gráfico de Macros (Datos Reales) ---
    const macrosCtx = document.getElementById('macrosChart')?.getContext('2d');
    if (macrosCtx) {
        if (macrosChartInstance) macrosChartInstance.destroy();

        const macroData = statsData.macro_porcentajes;
        
        macrosChartInstance = new Chart(macrosCtx, {
            type: 'doughnut',
            data: {
                labels: ['Carbohidratos', 'Proteínas'],
                datasets: [{
                    label: 'Distribución',
                    data: [macroData.carbos_pct, macroData.proteinas_pct],
                    backgroundColor: [colorSecondary, colorAccent],
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                 responsive: true,
                 plugins: {
                     legend: { position: 'top' },
                     tooltip: {
                         callbacks: {
                             label: function(context) {
                                 let label = context.label || '';
                                 if (label) { label += ': '; }
                                 if (context.parsed !== null) { label += context.parsed + '%'; }
                                 return label;
                             }
                         }
                     }
                 }
            }
        });
    }
};
</script>

<template>
    <main class="flex-grow-1 p-4 bg-light">
        <div class="dashboard-header mb-4">
            <h1 class="h3">Estadísticas {{ canViewAdvanced ? 'Avanzadas (Premium)' : (canViewBasic ? 'Básicas (Estandar)' : '') }}</h1>
            <p class="text-muted">Análisis del consumo nutricional y reportes.</p>
        </div>

        <div v-if="canViewAdvanced">
            <div class="card p-3 card-shadow mb-4">
                <label for="hijoSelect" class="form-label fw-bold">Selecciona un Hijo para ver sus estadísticas</label>
                <select id="hijoSelect" class="form-select" v-model="selectedHijoId" :disabled="isLoadingData">
                    <option :value="null" disabled>
                        {{ isLoadingData ? 'Cargando...' : 'Selecciona un hijo' }}
                    </option>
                    <option v-for="h in hijos" :key="h.id" :value="h.id">{{ h.nombre }}</option>
                </select>
            </div>

            <div v-if="isLoading" class="text-center p-5">
                <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
                <p class="mt-2 text-muted">Cargando estadísticas...</p>
            </div>
            <div v-else-if="!selectedHijoId" class="text-center p-5 text-muted">
                Por favor, selecciona un hijo para ver sus gráficos.
            </div>
            <div v-else class="row g-4">
                <div class="col-lg-7">
                    <div class="card p-4 h-100 card-shadow">
                         <h5 class="fw-bold mb-3">Consumo (Últimos 30 días)</h5>
                         <canvas id="caloriesChart"></canvas>
                    </div>
                </div>
                <div class="col-lg-5">
                     <div class="card p-4 h-100 card-shadow">
                          <h5 class="fw-bold mb-3">Distribución de Macros (%)</h5>
                          <canvas id="macrosChart"></canvas>
                     </div>
                </div>
                <div class="col-12 mt-4">
                    <button class="btn btn-primary-nb"><i class="fas fa-download me-2"></i> Descargar Reporte (Próximamente)</button>
                </div>
            </div>
        </div>
        
        <div v-else-if="canViewBasic" class="card p-5 text-center card-shadow">
            <h3 class="h4">Estadísticas Básicas (Promedio por Lonchera)</h3>
            <p class="text-muted mb-4">Esta es la vista de estadísticas básicas para el Plan Estándar. Para gráficos avanzados, actualiza a Premium.</p>
            <div class="row justify-content-center">
                 <div class="col-md-6">
                    <ul class="list-group list-group-flush">
                         <li class="list-group-item">Promedio Kcal: <strong>410 kcal</strong> (Simulado)</li>
                         <li class="list-group-item">Promedio Proteínas: <strong>15 g</strong> (Simulado)</li>
                         <li class="list-group-item">Promedio Carbohidratos: <strong>40 g</strong> (Simulado)</li>
                     </ul>
                 </div>
            </div>
        </div>

        <div v-else class="card p-5 text-center card-shadow">
            <i class="fas fa-lock text-warning mb-3" style="font-size: 48px;"></i>
            <h3 class="h4">Función de Plan Estándar o Premium</h3>
            <p class="text-muted mb-4">Accede a estadísticas de consumo mejorando tu plan.</p>
        </div>
    </main>
</template>
