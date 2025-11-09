<script setup>
import { RouterLink } from 'vue-router';
</script>

<template>
  <div class="landing-page">
    
    <header class="bg-card shadow-sm sticky-top py-3">
        <div class="container">
            <nav class="navbar navbar-expand-lg">
                <router-link to="/" class="navbar-brand text-dark-nb fw-bold fs-4">🍃 NutriBox</router-link>
                <div class="d-flex ms-auto">
                    <router-link to="/login" class="btn btn-outline-primary-nb me-2">Iniciar Sesión</router-link>
                    <router-link to="/register" class="btn btn-primary-nb">Registrarse</router-link>
                </div>
            </nav>
        </div>
    </header>

    <section class="hero-full text-dark-nb"> 
        <div class="container">
            <div class="row align-items-center">
                
                <div class="col-lg-6 mb-4 mb-lg-0">
                    <h1 class="mb-3 display-4 fw-bold">
                        Tu Socio Inteligente
                        <br>para Loncheras <span class="text-secondary-nb">Saludables</span>
                    </h1>
                    <p class="lead mb-4 text-muted-dark fs-5">
                        Planifica, personaliza y controla loncheras más sanas para tus hijos con NutriBox.
                    </p>
                    <router-link to="/register" class="btn btn-warning-nb me-3 shadow-lg text-dark-nb">
                        Comienza Gratis
                    </router-link>
                    <a href="#planes" class="btn btn-outline-primary-nb">
                        Ver Planes
                    </a>
                </div>
                
                <div class="col-lg-6 d-none d-lg-block">
                    <div class="lonchera-visual">
                        <i class="fas fa-box-open"></i>
                    </div>
                </div>

            </div>
        </div>
    </section>
    
    <section class="py-5 bg-bg-hero border-bottom">
        <div class="container">
            <h2 class="text-center mb-5 fw-bold text-dark-nb">¿Por qué elegir NutriBox?</h2>
            <div class="row row-cols-1 row-cols-md-3 g-4">
                <div class="col">
                    <div class="card h-100 feature-card-modern card-shadow">
                        <div class="feature-icon-modern"><i class="fas fa-chart-pie"></i></div>
                        <h3 class="h5 fw-bold text-dark-nb">Análisis Nutricional Detallado</h3>
                        <p class="text-muted-dark small-desc">Evalúa nutrientes esenciales y personaliza loncheras cada día. (RF3.5)</p>
                    </div>
                </div>
                <div class="col">
                    <div class="card h-100 feature-card-modern card-shadow">
                        <div class="feature-icon-modern"><i class="fas fa-exclamation-triangle"></i></div>
                        <h3 class="h5 fw-bold text-dark-nb">Alertas de Restricciones</h3>
                        <p class="text-muted-dark small-desc">Toda la familia puede agregar restricciones específicas para prevenir alergias. (RF4)</p>
                    </div>
                </div>
                <div class="col">
                    <div class="card h-100 feature-card-modern card-shadow">
                        <div class="feature-icon-modern"><i class="fas fa-history"></i></div>
                        <h3 class="h5 fw-bold text-dark-nb">Ahorro y Planificación</h3>
                        <p class="text-muted-dark small-desc">Simplifica la planificación semanal y optimiza el presupuesto familiar. (RF7)</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="planes" class="py-5 bg-light-nb">
        <div class="container">
            <h2 class="text-center mb-5 fw-bold text-dark-nb">Planes y Membresías</h2>
            <div class="row row-cols-1 row-cols-md-3 g-4 justify-content-center">
                <div class="col">
                    <div class="card text-center h-100 plan-card card-shadow">
                        <h3 class="h4 fw-bold text-dark-nb mb-3">Básico (Gratuito)</h3>
                        <p class="text-muted-dark mb-4">Ideal para empezar.</p>
                        <ul class="list-unstyled text-start my-4 flex-grow-1">
                            <li><i class="fas fa-check text-success me-2"></i> Menús predeterminados (solo visualización)</li>
                            <li><i class="fas fa-check text-success me-2"></i> Información nutricional básica</li>
                            <li><i class="fas fa-times text-danger me-2"></i> **NO**: Loncheras personalizadas</li>
                            <li><i class="fas fa-times text-danger me-2"></i> **NO**: Direcciones de entrega</li>
                        </ul>
                        <router-link to="/register" class="btn btn-outline-primary-nb mt-auto w-100">Comenzar Gratis</router-link>
                    </div>
                </div>
                
                <div class="col">
                    <div class="card text-center h-100 plan-card card-shadow">
                        <h3 class="h4 fw-bold text-dark-nb mb-3">Estándar</h3>
                        <p class="text-muted-dark mb-4">El mejor punto de partida.</p>
                        <ul class="list-unstyled text-start my-4 flex-grow-1">
                            <li><i class="fas fa-check text-success me-2"></i> Todo del Básico</li>
                            <li><i class="fas fa-check text-success me-2"></i> Agregar menús predeterminados a perfil</li>
                            <li><i class="fas fa-check text-success me-2"></i> 1 dirección de entrega (RF5.2)</li>
                            <li><i class="fas fa-check text-success me-2"></i> Estadísticas básicas (RF7.1)</li>
                        </ul>
                        <router-link to="/register" class="btn btn-primary-nb mt-auto w-100">Seleccionar Estándar</router-link>
                    </div>
                </div>

                <div class="col">
                    <div class="card text-center h-100 card-shadow premium plan-card">
                        <div class="badge bg-primary-dark text-white position-absolute top-0 start-50 translate-middle rounded-pill px-3 py-2 fw-bold">✨ MÁS POPULAR</div>
                        <h3 class="h4 fw-bold pt-3 text-secondary-nb mb-3">Premium</h3>
                        <p class="text-muted-dark mb-4">Control total y nutrición avanzada.</p>
                        <ul class="list-unstyled text-start my-4 flex-grow-1">
                            <li><i class="fas fa-check text-success me-2"></i> Todo del Estándar</li>
                            <li><i class="fas fa-check text-success me-2"></i> Loncheras personalizadas (alimento por alimento) (RF3.4)</li>
                            <li><i class="fas fa-check text-success me-2"></i> Hasta 3 direcciones (RF5.2)</li>
                            <li><i class="fas fa-check text-success me-2"></i> Estadísticas avanzadas (RF7.2)</li>
                            <li><i class="fas fa-check text-success me-2"></i> Gestión de restricciones (RF4.1)</li>
                        </ul>
                        <router-link to="/register" class="btn btn-primary-nb mt-auto w-100">Seleccionar Premium</router-link>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="py-5 bg-primary-dark cta-final text-white text-center">
        <div class="container">
            <h2 class="fw-bold mb-3">Empieza a planificar la nutrición de tu hijo hoy</h2>
            <router-link to="/register" class="btn btn-lg btn-warning-nb">REGISTRARSE</router-link>
        </div>
    </section>

    <footer class="text-white">
        <div class="container text-center">
            <p class="mb-1">&copy; 2025 🍃 NutriBox. Todos los derechos reservados. | Proyecto de Producción de Software.</p>
             <div class="small">
                 <router-link to="/app/perfil" class="text-white mx-2 text-decoration-none">Ver Planes</router-link> | 
                 <router-link to="/login" class="text-white mx-2 text-decoration-none">Iniciar Sesión</router-link>
             </div>
        </div>
    </footer>
    
  </div>
</template>

<style scoped>
/* Replicamos el fondo base para esta vista fuera del layout */
.landing-page {
    background-color: var(--bg-light, #F4F8F5);
}
/* Forzar el tamaño del título en Hero para hacerlo grande */
.hero-full h1 {
    font-size: 3.5rem !important;
}
/* Estilo para el fondo del hero */
.hero-full {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 60%, var(--bg-hero) 100%);
    min-height: 45vh; 
    padding: 3rem 0; 
}
</style>
