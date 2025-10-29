<script setup>
import { RouterView, useRoute } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue' // <-- IMPORTA EL LAYOUT
import { computed } from 'vue'

const route = useRoute();

// Determina si la ruta actual debe usar el layout (todas excepto login/register)
const useLayout = computed(() => {
  return route.name !== 'login' && route.name !== 'register';
});
</script>

<template>
  <AppLayout v-if="useLayout">
    <RouterView />
  </AppLayout>

  <RouterView v-else />
</template>

<style scoped>
/* Puedes quitar los estilos aquí si ya están en main.css */
</style>
