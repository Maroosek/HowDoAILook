<script setup>
defineProps({
  disabled: Boolean
})

defineEmits(['generate'])
</script>

<template>
  <div class="text-center mt-4">
    <button
      class="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
      :disabled="disabled"
      @click="$emit('generate')"
    >
      Generuj modela
    </button>
  </div>
</template>