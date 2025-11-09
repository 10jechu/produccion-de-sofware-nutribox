<script setup>
import authService from '@/services/auth.service';
import Swal from 'sweetalert2'; 
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const router = useRouter();

const handleLogin = async () => {
  if (!email.value || !password.value) {
    Swal.fire('Error', 'Debes ingresar correo y contraseña', 'warning');
    return;
  }

  Swal.fire({
    title: 'Iniciando sesión...',
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading();
    }
  });

  try {
    // La función login en authService ya maneja la obtención del token y los detalles del usuario
    await authService.login(email.value, password.value);
    Swal.close(); 
    
    // Redirigir al dashboard (ya agrupado bajo /app)
    router.push('/app/dashboard');

  } catch (error) {
    Swal.close(); 
    Swal.fire('Error de Autenticación', error.message || 'Credenciales inválidas', 'error');
    console.error('Error en login:', error);
  }
};
</script>

<template>
  <div class="container-fluid min-vh-100 d-flex align-items-center justify-content-center bg-light-nb">
    <div class="row w-100 justify-content-center align-items-stretch">
      
        <div class="col-lg-5 d-none d-lg-flex flex-column justify-content-center p-5 bg-primary-nb text-white login-info-card">
            <div class="text-center">
                 <h1 class="fw-bold display-4 mb-4">🍃 NutriBox</h1>
                 <p class="lead mb-4">
                    Tu aliado para loncheras escolares saludables y sin complicaciones.
                 </p>
                 <ul class="list-unstyled text-start mx-auto" style="max-width: 300px;">
                     <li class="mb-2"><i class="fas fa-check-circle me-2 text-secondary-nb"></i> Validación de restricciones</li>
                     <li class="mb-2"><i class="fas fa-chart-pie me-2 text-secondary-nb"></i> Resumen nutricional al instante</li>
                     <li class="mb-2"><i class="fas fa-truck me-2 text-secondary-nb"></i> Gestión de direcciones de entrega</li>
                 </ul>
            </div>
        </div>

        <div class="col-lg-4 col-md-8 d-flex justify-content-center align-items-center p-5 bg-card">
            <div class="w-100" style="max-width: 350px;">
                <div class="text-center mb-4">
                    <h1 class="text-primary-nb fw-bold fs-3">🍃 NutriBox</h1>
                    <h2 class="h5 mt-3 text-dark-nb fw-bold">Inicia Sesión</h2>
                </div>
                <form @submit.prevent="handleLogin">
                    <div class="mb-3">
                        <label for="email" class="form-label text-dark-nb">Correo electrónico</label>
                        <input type="email" id="email" class="form-control" required v-model="email">
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label text-dark-nb">Contraseña</label>
                        <input type="password" id="password" class="form-control" required v-model="password">
                    </div>
                    <button type="submit" class="btn btn-primary-nb w-100 py-2 mt-3">
                        Iniciar Sesión
                    </button>
                </form>
                <p class="text-center mt-3 text-dark-nb">
                    ¿No tienes cuenta?
                    <router-link to="/register" class="text-primary-nb fw-bold">Regístrate</router-link>
                </p>
            </div>
        </div>
    </div>
  </div>
</template>

<style scoped>
/* Estilos específicos para la vista de Login */
.login-info-card {
    border-radius: 1rem 0 0 1rem; /* Esquinas redondeadas solo a la izquierda */
    min-height: 500px;
}
/* Asegurar que los íconos de info sean visibles (usamos el amarillo de CTA para visibilidad) */
.login-info-card .text-secondary-nb {
    color: var(--secondary) !important;
}
</style>
