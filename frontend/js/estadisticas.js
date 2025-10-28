requireAuth();

function checkMembershipAndRender() {
    const user = getUser();
    const mainContent = document.getElementById("mainContent");

    // Asegúrate de que user y user.membresia existan antes de leer 'tipo'
    if (user && user.membresia && user.membresia.tipo === 'Premium') {
        renderPremiumDashboard();
    } else {
        renderUpgradeMessage();
    }
}

function renderUpgradeMessage() {
    const mainContent = document.getElementById("mainContent");
    mainContent.innerHTML = `
        <div class="dashboard-header mb-4">
            <h1 class="h3">Estadísticas Avanzadas</h1>
            <p class="text-muted">Desbloquea reportes y gráficos detallados con el Plan Premium.</p>
        </div>
        <div class="card p-5 text-center card-shadow">
            <i class="fas fa-lock text-warning mb-3" style="font-size: 48px;"></i>
            <h3 class="h4">Función Premium</h3>
            <p class="text-muted mb-4">Accede a comparativas, tendencias y reportes descargables mejorando tu plan.</p>
            {/* TODO: Implementar lógica de upgrade */}
            <button class="btn btn-warning w-auto mx-auto text-dark">Mejorar a Premium</button>
        </div>
    `;
}

function renderPremiumDashboard() {
    const mainContent = document.getElementById("mainContent");
    mainContent.innerHTML = `
        <div class="dashboard-header mb-4">
            <h1 class="h3">Estadísticas Avanzadas</h1>
            <p class="text-muted">Análisis del consumo nutricional (simulado).</p>
        </div>

        <div class="row g-4 mb-4">
            <div class="col-lg-7">
                <div class="card p-4 h-100 card-shadow">
                     <h5 class="fw-bold mb-3">Calorías Consumidas (Últimos 7 Días)</h5>
                     <canvas id="caloriesChart"></canvas>
                </div>
            </div>
            <div class="col-lg-5">
                 <div class="card p-4 h-100 card-shadow">
                     <h5 class="fw-bold mb-3">Distribución de Macronutrientes (%)</h5>
                     <canvas id="macrosChart"></canvas>
                </div>
            </div>
        </div>

    `;
    // Lógica para renderizar los gráficos (con datos simulados y colores)
    renderCharts();
}

function renderCharts() {
    // --- Colores de la plataforma ---
    const colorPrimary = '#4CAF50'; // Verde principal
    const colorSecondary = '#FF9800'; // Naranja secundario
    const colorAccent = '#2196F3';   // Azul
    const colorLightGreen = 'rgba(76, 175, 80, 0.2)';
    const colorYellow = '#FFCD56'; // Amarillo complementario

    // --- Gráfico de Calorías ---
    const caloriesCtx = document.getElementById('caloriesChart')?.getContext('2d');
    if (caloriesCtx) {
        new Chart(caloriesCtx, {
            type: 'line',
            data: {
                labels: ['Día 1', 'Día 2', 'Día 3', 'Día 4', 'Día 5', 'Día 6', 'Día 7'],
                datasets: [{
                    label: 'Calorías (kcal)',
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

    // --- Gráfico de Macronutrientes ---
    const macrosCtx = document.getElementById('macrosChart')?.getContext('2d');
    if (macrosCtx) {
        new Chart(macrosCtx, {
            type: 'doughnut',
            data: {
                labels: ['Carbohidratos', 'Proteínas', 'Grasas'],
                datasets: [{
                    label: 'Distribución',
                    data: [50, 25, 25],
                    backgroundColor: [
                        colorSecondary, // Naranja
                        colorAccent,    // Azul
                        colorYellow     // Amarillo
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

// Llama a la función principal al cargar la página
checkMembershipAndRender();