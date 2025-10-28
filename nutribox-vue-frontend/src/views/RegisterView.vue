<script setup>
import authService from '@/services/auth.service'; // @ es un alias para src/
import Swal from 'sweetalert2';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const nombre = ref('');
const email = ref('');
const password = ref('');
const membresia = ref(''); // Valor inicial vacío
const router = useRouter();

const handleRegister = async () => {
  console.log('Intentando registrar:', nombre.value, email.value, membresia.value);
  if (!nombre.value || !email.value || !password.value || !membresia.value) {
       Swal.fire('Error', 'Todos los campos son obligatorios', 'warning');
       return;
  }
   if (password.value.length < 6) {
       Swal.fire('Error', 'La contraseña debe tener al menos 6 caracteres', 'warning');
       return;
   }

  // Mostrar loading (opcional)
  Swal.fire({
    title: 'Creando cuenta...',
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading();
    }
  });

  try {
      const userData = {
          nombre: nombre.value,
          email: email.value,
          password: password.value,
          membresia: membresia.value
          // rol: 'Usuario' // El backend debería asignar 'Usuario' por defecto
      };
      const response = await authService.register(userData);
      console.log('Registro exitoso:', response);

      Swal.close(); // Cerrar loading

      Swal.fire(
        '¡Registro Exitoso!',
        'Tu cuenta ha sido creada. Ahora puedes iniciar sesión.',
        'success'
      );

      // Redirigir a login después de un momento
      setTimeout(() => {
        router.push('/login');
      }, 2000); // Espera 2 segundos

  } catch (error) {
      Swal.close(); // Cerrar loading
      Swal.fire('Error de Registro', error.message || 'No se pudo completar el registro', 'error');
      console.error('Error en registro:', error);
  }
};
</script>

<template>
  <div class="container">
    <div class="row min-vh-100 justify-content-center align-items-center">
      <div class="col-md-6 col-lg-5">
        <div class="card p-4 card-shadow">
          <div class="text-center mb-4">
            <h1 class="text-primary-nb fw-bold">🍃 NutriBox</h1>
            <h2 class="h5 mt-3">Crear Cuenta</h2>
          </div>
          <form @submit.prevent="handleRegister">
            <div class="mb-3">
              <label for="nombre" class="form-label">Nombre completo</label>
              <input type="text" id="nombre" class="form-control" required v-model="nombre">
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Correo electrónico</label>
              <input type="email" id="email" class="form-control" required v-model="email">
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Contraseña</label>
              <input type="password" id="password" class="form-control" required minlength="6" v-model="password">
            </div>
            <div class="mb-3">
              <label for="membresia" class="form-label">Plan de Membresía</label>
              <select id="membresia" class="form-select" required v-model="membresia">
                <option value="" disabled>Selecciona un plan</option>
                <option value="Free">Básico (Gratuito)</option>
                <option value="Estandar">Estándar</option>
                <option value="Premium">Premium</option>
              </select>
            </div>
            <button type="submit" class="btn btn-primary-nb w-100 py-2 mt-3">
              Crear Cuenta
            </button>
          </form>
          <p class="text-center mt-3">
            ¿Ya tienes cuenta? <router-link to="/login" class="text-primary-nb fw-bold">Inicia sesión</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Estilos específicos para RegisterView */
</style>