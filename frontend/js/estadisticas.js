requireAuth();

function checkMembershipAndRender() {
    const user = getUser();
    const mainContent = document.getElementById("mainContent");

    if (user && user.membresia.tipo === 'Premium') {
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
        <div class="row g-4">
            <div class="col-lg-7">
                <div class="card p-4 h-100 card-shadow">
                     <h5 class="fw-bold">Calorías Consumidas (Últimos 7 Días)</h5>
                     <canvas id="caloriesChart"></canvas>
                </div>
            </div>
            <div class="col-lg-5">
                 <div class="card p-4 h-100 card-shadow">
                     <h5 class="fw-bold">Distribución de Macronutrientes</h5>
                     <canvas id="macrosChart"></canvas>
                </div>
            </div>
        </div>
    `;
    // Lógica para renderizar los gráficos (con datos simulados)
    renderCharts();
}

function renderCharts() {
    // Gráfico de Calorías
    const caloriesCtx = document.getElementById('caloriesChart').getContext('2d');
    new Chart(caloriesCtx, {
        type: 'line',
        data: {
            labels: ['Día 1', 'Día 2', 'Día 3', 'Día 4', 'Día 5', 'Día 6', 'Día 7'],
            datasets: [{
                label: 'Calorías (kcal)',
                data: [350, 420, 380, 500, 450, 470, 410],
                borderColor: 'rgba(76, 175, 80, 1)',
                backgroundColor: 'rgba(76, 175, 80, 0.2)',
                fill: true,
                tension: 0.3
            }]
        }
    });

    // Gráfico de Macronutrientes
    const macrosCtx = document.getElementById('macrosChart').getContext('2d');
    new Chart(macrosCtx, {
        type: 'doughnut',
        data: {
            labels: ['Carbohidratos', 'Proteínas', 'Grasas'],
            datasets: [{
                label: 'Distribución',
                data: [50, 25, 25],
                backgroundColor: [
                    'rgba(255, 159, 64, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(255, 206, 86, 0.8)'
                ]
            }]
        }
    });
}

checkMembershipAndRender();