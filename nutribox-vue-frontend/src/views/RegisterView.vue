<script setup>
import authService from '@/services/auth.service';
import Swal from 'sweetalert2';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const nombre = ref('');
const email = ref('');
const password = ref('');
const membresia = ref(''); 
const router = useRouter();

const handleRegister = async () => {
  if (!nombre.value || !email.value || !password.value || !membresia.value) {
       Swal.fire('Error', 'Todos los campos son obligatorios', 'warning');
       return;
  }
   if (password.value.length < 6) {
       Swal.fire('Error', 'La contraseña debe tener al menos 6 caracteres', 'warning');
       return;
   }

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
      };
      
      await authService.register(userData);

      Swal.close(); 

      Swal.fire(
        '¡Registro Exitoso!',
        'Tu cuenta ha sido creada. Por favor, inicia sesión.',
        'success'
      );

      // REDIRIGIR A LOGIN (Comportamiento deseado)
      setTimeout(() => {
        router.push('/login');
      }, 1500); 

  } catch (error) {
      Swal.close(); 
      Swal.fire('Error de Registro', error.message || 'No se pudo completar el registro', 'error');
      console.error('Error en registro:', error);
  }
};
</script>

<template>
  <div class="container-fluid min-vh-100 d-flex align-items-center justify-content-center bg-light-nb">
    <div class="row w-100 justify-content-center align-items-stretch login-container">
      
        <div class="col-lg-5 d-none d-lg-flex flex-column justify-content-center p-5 bg-primary-nb text-white login-info-card card-shadow-top">
            <div class="text-center">
                 <h1 class="fw-bold display-4 mb-4"> NutriBox</h1>
                 <p class="lead mb-4">
                    Comienza a crear loncheras saludables. Elige tu plan para desbloquear funciones.
                 </p>
                 <ul class="list-unstyled text-start mx-auto" style="max-width: 300px;">
                     <li class="mb-2"><i class="fas fa-check-circle me-2 text-secondary-nb"></i> Personalización de menús (Premium)</li>
                     <li class="mb-2"><i class="fas fa-ban me-2 text-secondary-nb"></i> Alertas de restricciones (Premium)</li>
                     <li class="mb-2"><i class="fas fa-chart-line me-2 text-secondary-nb"></i> Estadísticas de consumo (Estándar+)</li>
                 </ul>
            </div>
        </div>

        <div class="col-lg-6 col-md-8 d-flex justify-content-center align-items-center p-5 bg-card form-card">
            <div class="w-100" style="max-width: 400px;">
                <div class="text-center mb-4">
                    <h1 class="text-primary-nb fw-bold fs-3"> NutriBox</h1>
                    <h2 class="h5 mt-3 text-dark-nb fw-bold">Crear Cuenta</h2>
                </div>
                <form @submit.prevent="handleRegister">
                    <div class="mb-3">
                        <label for="nombre" class="form-label text-dark-nb">Nombre completo</label>
                        <input type="text" id="nombre" class="form-control" required v-model="nombre">
                    </div>
                    <div class="mb-3">
                        <label for="email" class="form-label text-dark-nb">Correo electrónico</label>
                        <input type="email" id="email" class="form-control" required v-model="email">
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label text-dark-nb">Contraseña (Mínimo 6 caracteres)</label>
                        <input type="password" id="password" class="form-control" required minlength="6" v-model="password">
                    </div>
                    <div class="mb-3">
                        <label for="membresia" class="form-label text-dark-nb">Plan de Membresía</label>
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
                <p class="text-center mt-3 text-dark-nb">
                    ¿Ya tienes cuenta? <router-link to="/login" class="text-primary-nb fw-bold">Inicia sesión</router-link>
                </p>
            </div>
        </div>
    </div>
  </div>
</template>

<style scoped>
/* Estilos específicos para la vista de Registro (Asegurar que sea consistente con Login) */
.login-container {
    border-radius: 1rem;
    overflow: hidden; 
    box-shadow: var(--shadow-lg);
    max-width: 1000px; /* Un poco más ancho para el formulario largo */
}
.login-info-card {
    border-radius: 0; 
    min-height: 600px; /* Más alto para contener la info */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.form-card {
     border-radius: 0;
}
.login-info-card .text-secondary-nb {
    color: var(--secondary) !important;
}
</style>
