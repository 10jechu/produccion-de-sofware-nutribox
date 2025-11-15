<script setup>
import authService from '@/services/auth.service'; // @ es un alias para la carpeta src/
import Swal from 'sweetalert2'; // Para notificaciones
import { ref } from 'vue';
import { useRouter } from 'vue-router'; // Para redirigir
import { isAdmin } from '@/utils/user'; // <-- AÑADIDO

const email = ref('');
const password = ref('');
const router = useRouter();
const handleLogin = async () => {
  console.log('Intentando iniciar sesión con:', email.value, password.value);
  if (!email.value || !password.value) {
    Swal.fire('Error', 'Debes ingresar correo y contraseña', 'warning');
    return;
  }

  // Mostrar loading (opcional)
  Swal.fire({
    title: 'Iniciando sesión...',
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading();
    }
  });

  try {
    await authService.login(email.value, password.value);
    // El token y el UserDetail ya se guardan en authService.login

    Swal.close(); // Cerrar loading

    // ### INICIO DE LA MODIFICACIÓN ###
    // Redirigir según el rol
    if (isAdmin()) {
      router.push('/admin/foods');
    } else {
      router.push('/dashboard');
    }
    // ### FIN DE LA MODIFICACIÓN ###

  } catch (error) {
    Swal.close(); // Cerrar loading
    Swal.fire('Error de Autenticación', error.message || 'Credenciales inválidas', 'error');
    console.error('Error en login:', error);
  }
};
</script>

<template>
  <div class="container">
    <div class="row min-vh-100 justify-content-center align-items-center">
      <div class="col-md-5 col-lg-4">
        <div class="card p-4 card-shadow">
          <div class="text-center mb-4">
            <h1 class="text-primary-nb fw-bold">🍃 NutriBox</h1>
            <h2 class="h5 mt-3">Inicia Sesión</h2>
          </div>
          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label for="email" class="form-label">Correo electrónico</label>
              <input type="email" id="email" class="form-control" required v-model="email">
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Contraseña</label>
              <input type="password" id="password" class="form-control" required v-model="password">
            </div>
            <button type="submit" class="btn btn-primary-nb w-100 py-2 mt-3">
              Iniciar Sesión
            </button>
          </form>
          <p class="text-center mt-3">
            ¿No tienes cuenta?
            <router-link to="/register" class="text-primary-nb fw-bold">Regístrate</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Puedes añadir estilos específicos para esta vista aquí si es necesario */
</style>
