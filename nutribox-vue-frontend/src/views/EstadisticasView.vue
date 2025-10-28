<script setup>
import { ref, onMounted, computed } from 'vue';
import { hasRequiredMembership } from '@/utils/user';
import { useRouter } from 'vue-router';

// Logica de simulacion para Chart.js
const renderCharts = () => {
    // Si Chart.js no se carga globalmente (como se hace en el vanilla JS), 
    // tendrias que importarlo aqui: import Chart from 'chart.js/auto';
    
    // --- Colores de la plataforma ---
    const colorPrimary = '#4CAF50'; 
    const colorSecondary = '#FF9800'; 
    const colorAccent = '#2196F3';  
    const colorLightGreen = 'rgba(76, 175, 80, 0.2)';
    const colorYellow = '#FFCD56'; 

    if (typeof Chart !== 'undefined') {
        const caloriesCtx = document.getElementById('caloriesChart')?.getContext('2d');
        if (caloriesCtx) {
             // Limpiar el grafico anterior si existe
             if (Chart.getChart('caloriesChart')) {
                 Chart.getChart('caloriesChart').destroy();
             }
             new Chart(caloriesCtx, {
                 type: 'line',
                 data: {
                     labels: ['Dia 1', 'Dia 2', 'Dia 3', 'Dia 4', 'Dia 5', 'Dia 6', 'Dia 7'],
                     datasets: [{
                         label: 'Calorias (kcal)',
                         data: [350, 420, 380, 500, 450, 470, 410],
                         borderColor: colorPrimary,
                         backgroundColor: colorLightGreen,
                         fill: true,
                         tension: 0.3
                     }]
                 },
                 options: {
                     scales: { y: { beginAtZero: false } },
                     plugins: { legend: { display: true } }
                 }
             });
        }

        const macrosCtx = document.getElementById('macrosChart')?.getContext('2d');
        if (macrosCtx) {
             // Limpiar el grafico anterior si existe
             if (Chart.getChart('macrosChart')) {
                 Chart.getChart('macrosChart').destroy();
             }
             new Chart(macrosCtx, {
                 type: 'doughnut',
                 data: {
                     labels: ['Carbohidratos', 'Proteinas', 'Grasas'],
                     datasets: [{
                         label: 'Distribucion',
                         data: [50, 25, 25],
                         backgroundColor: [
                             colorSecondary, 
                             colorAccent,    
                             colorYellow     
                         ],
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
    }
};

const router = useRouter();
const canViewAdvanced = hasRequiredMembership('Premium'); // RF7.2
const canViewBasic = hasRequiredMembership('Estandar'); // RF7.1

onMounted(() => {
    // Si tienes Chart.js instalado en Vue, puedes llamarlo aqui.
    if (canViewAdvanced.value) {
        // La logica de renderCharts asume que Chart es global
        setTimeout(renderCharts, 100); 
    }
});
</script>

<template>
    <main class="flex-grow-1 p-4 bg-light">
        <div class="dashboard-header mb-4">
            <h1 class="h3">Estadisticas {{ canViewAdvanced ? 'Avanzadas (Premium)' : (canViewBasic ? 'Basicas (Estandar)' : '') }}</h1>
            <p class="text-muted">Analisis del consumo nutricional y reportes.</p>
        </div>

        <div v-if="canViewAdvanced" class="row g-4">
            <div class="col-lg-7">
                <div class="card p-4 h-100 card-shadow">
                     <h5 class="fw-bold mb-3">Calorias Consumidas (Ultimos 7 Dias - SIMULADO)</h5>
                     <canvas id="caloriesChart"></canvas>
                </div>
            </div>
            <div class="col-lg-5">
                 <div class="card p-4 h-100 card-shadow">
                      <h5 class="fw-bold mb-3">Distribucion de Macronutrientes (%) - SIMULADO</h5>
                      <canvas id="macrosChart"></canvas>
                 </div>
            </div>
            <div class="col-12 mt-4">
                <button class="btn btn-primary-nb"><i class="fas fa-download me-2"></i> Descargar Reporte Completo (CSV/PDF)</button>
            </div>
        </div>
        
        <div v-else-if="canViewBasic" class="card p-5 text-center card-shadow">
            <h3 class="h4">Estadisticas Basicas (Promedio por Lonchera)</h3>
            <p class="text-muted mb-4">Esta es la vista de estadisticas basicas para el Plan Estandar. Para graficos avanzados, actualiza a Premium.</p>
            <div class="row justify-content-center">
                 <div class="col-md-6">
                    <ul class="list-group list-group-flush">
                         <li class="list-group-item">Promedio Kcal: <strong>410 kcal</strong></li>
                         <li class="list-group-item">Promedio Proteinas: <strong>15 g</strong></li>
                         <li class="list-group-item">Promedio Carbohidratos: <strong>40 g</strong></li>
                     </ul>
                 </div>
            </div>
        </div>


        <div v-else class="card p-5 text-center card-shadow">
            <i class="fas fa-lock text-warning mb-3" style="font-size: 48px;"></i>
            <h3 class="h4">Funcion de Plan Estandar o Premium</h3>
            <p class="text-muted mb-4">Accede a estadisticas de consumo mejorando tu plan.</p>
        </div>
    </main>
</template>