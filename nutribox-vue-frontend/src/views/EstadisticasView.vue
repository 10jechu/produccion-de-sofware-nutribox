<script setup>
import { ref, onMounted, watch } from 'vue';
import { hasRequiredMembership, getUserDetail } from '@/utils/user';
import apiService from '@/services/api.service';
import Swal from 'sweetalert2';
import authService from '@/services/auth.service';

const canViewAdvanced = hasRequiredMembership('Premium');
const canViewBasic = hasRequiredMembership('Estandar');

// --- Refs para Plan Premium ---
const hijos = ref([]);
const selectedHijoId = ref(null);
const isLoading = ref(false); // Para los gráficos
const isLoadingData = ref(false); // Para el dropdown de hijos

// --- Refs para Plan Estándar ---
const isLoadingBasic = ref(true);
const basicStats = ref({
    avg_kcal: 0,
    avg_proteinas: 0,
    avg_carbos: 0
});

let caloriesChartInstance = null;
let macrosChartInstance = null;

// --- Colores ---
const colorPrimary = '#4CAF50'; 
const colorSecondary = '#FF9800'; 
const colorAccent = '#2196F3';  
const colorLightGreen = 'rgba(76, 175, 80, 0.2)';

// --- Lógica para Plan Premium ---
async function loadHijos() {
  isLoadingData.value = true;
  const user = getUserDetail();
  if (!user) { authService.logout(); return; }
  
  try {
    hijos.value = await apiService.get('/children?usuario_id=' + user.id);
    isLoadingData.value = false;
  } catch (error) {
    isLoadingData.value = false;
    Swal.fire('Error', 'No se pudieron cargar los hijos', 'error');
  }
}

async function fetchAndRenderStats() {
  if (!selectedHijoId.value || !canViewAdvanced) return;
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

// --- ### INICIO MODIFICACIÓN: Lógica para Plan Estándar ### ---
async function loadBasicStats() {
    isLoadingBasic.value = true;
    const user = getUserDetail();
    if (!user) { authService.logout(); return; }

    try {
        // Refrescar los datos del usuario para obtener los promedios más recientes
        const freshDetail = await apiService.get('/users/' + user.id + '/detail');
        authService.saveUserDetail(freshDetail); // Actualiza localStorage

        if (freshDetail.resumen) {
            basicStats.value = {
                avg_kcal: freshDetail.resumen.avg_kcal,
                avg_proteinas: freshDetail.resumen.avg_proteinas,
                avg_carbos: freshDetail.resumen.avg_carbos
            };
        }
        isLoadingBasic.value = false;
    } catch (error) {
        isLoadingBasic.value = false;
        Swal.fire('Error', 'No se pudieron cargar las estadísticas básicas.', 'error');
    }
}
// --- ### FIN MODIFICACIÓN ### ---

watch(selectedHijoId, fetchAndRenderStats);

onMounted(() => {
    if (canViewAdvanced.value) {
        loadHijos();
    } else if (canViewBasic.value) {
        loadBasicStats(); // Carga las estadísticas básicas si es Estándar
    }
});

const renderCharts = (statsData) => {
    if (typeof Chart === 'undefined' || !statsData) {
        console.error("Chart.js no está definido o no hay datos");
        return;
    }
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
                 plugins: { legend: { position: 'top' }, tooltip: { callbacks: { label: (context) => (context.label || '') + ': ' + (context.parsed || 0) + '%' } } }
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
                        {{ isLoadingData ? 'Cargando hijos...' : 'Selecciona un hijo' }}
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
            <p class="text-muted mb-4">Este es el promedio de todas tus loncheras confirmadas. Para gráficos avanzados, actualiza a Premium.</p>
            
            <div v-if="isLoadingBasic" class="text-center p-5">
                <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
                <p class="mt-2 text-muted">Calculando promedios...</p>
            </div>
            
            <div v-else class="row justify-content-center">
                 <div class="col-md-6">
                    <ul class="list-group list-group-flush">
                         <li class="list-group-item">Promedio Kcal: <strong>{{ basicStats.avg_kcal }} kcal</strong></li>
                         <li class="list-group-item">Promedio Proteínas: <strong>{{ basicStats.avg_proteinas }} g</strong></li>
                         <li class="list-group-item">Promedio Carbohidratos: <strong>{{ basicStats.avg_carbos }} g</strong></li>
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
