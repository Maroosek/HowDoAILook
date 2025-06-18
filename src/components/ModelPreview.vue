<script setup>
defineProps({
  src: String
})
</script>

<template>
  <div class="mt-8 text-center">
    <h2 class="text-xl font-semibold mb-4">Wygenerowany model:</h2>
    <img :src="src" alt="Wygenerowany model" class="max-w-full mx-auto rounded shadow-lg" />
  </div>
</template>