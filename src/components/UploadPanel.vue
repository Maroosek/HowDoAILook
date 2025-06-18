<script setup>
import { ref, watch } from 'vue'

const emit = defineEmits(['files-selected'])
const previews = ref([])
const selectedFiles = ref([])

function onFileChange(event) {
  const files = Array.from(event.target.files).slice(0, 3)
  selectedFiles.value = files
  emit('files-selected', files)

  previews.value = files.map(file => URL.createObjectURL(file))
}

// Clean up object URLs
watch(previews, (newVal, oldVal) => {
  oldVal.forEach(url => URL.revokeObjectURL(url))
})
</script>

<template>
  <div class="bg-white p-4 rounded shadow-md max-w-xl mx-auto mb-6">
    <h2 class="text-xl font-semibold mb-2">Prześlij zdjęcia ubrań (max 3)</h2>
    <input type="file" accept="image/*" multiple @change="onFileChange" />
    
    <div v-if="previews.length" class="flex gap-4 mt-4">
      <img v-for="(src, index) in previews" :key="index" :src="src" class="w-24 h-24 object-cover rounded border" />
    </div>
  </div>
</template>
