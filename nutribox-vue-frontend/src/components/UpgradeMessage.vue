<template>
  <div class="upgrade-message alert alert-info">
    <div class="d-flex align-items-center">
      <i class="fas fa-crown me-3 fs-2 text-warning"></i>
      <div class="flex-grow-1">
        <h5 class="alert-heading mb-2">{{ upgradeInfo.message }}</h5>
        <p class="mb-2" v-if="upgradeInfo.features.length > 0">
          <strong>Incluye:</strong> {{ upgradeInfo.features.join(', ') }}
        </p>
        <button class="btn btn-warning btn-sm" @click="$emit('upgrade')">
          <i class="fas fa-rocket me-1"></i> Ver Planes
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import permissionsService from '@/services/permissions.service';

const props = defineProps({
  featureName: {
    type: String,
    required: true
  }
});

defineEmits(['upgrade']);

const upgradeInfo = computed(() => {
  return permissionsService.getUpgradeMessage(props.featureName);
});
</script>

<style scoped>
.upgrade-message {
  border-left: 4px solid var(--warning);
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}
</style>