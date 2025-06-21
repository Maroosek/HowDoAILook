<script setup>
import { ref, computed } from 'vue'
import UploadPanelSingle from '../components/UploadPanelSingle.vue'
import GenerateButton from '../components/GenerateButton.vue'
import ModelPreview from '../components/ModelPreview.vue'
//import axios from 'axios'

const files = ref([])
const generatedImage = ref(null)
const isLoading = ref(false)

const hasFiles = computed(() => files.value.length > 0)

function handleFiles(selectedFiles) {
  files.value = selectedFiles
}

async function generateModel() {
  if (!hasFiles.value) return

  isLoading.value = true
  generatedImage.value = null

  try {
    const formData = new FormData()
    for (const [category, file] of Object.entries(files.value)) {
      formData.append(category, file)
    }

    const res = await axios.post('/api/generate-model', formData)
    generatedImage.value = res.data.imageUrl || `data:image/png;base64,${res.data.image}`
  } catch (err) {
    console.error('API Error:', err)
    alert('Błąd podczas generowania modela.')
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <h1 class="text-3xl font-bold text-center mb-8">AI Stylista – Generuj modela w swoich ubraniach</h1>

    <UploadPanelSingle @files-selected="handleFiles" />

    <GenerateButton :disabled="!hasFiles || isLoading" @generate="generateModel" />

    <div v-if="isLoading" class="text-center mt-4 text-blue-600">Generowanie modela...</div>

    <ModelPreview v-if="generatedImage" :src="generatedImage" />
  </div>
</template>

