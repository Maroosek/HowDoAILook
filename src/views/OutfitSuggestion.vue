<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import UploadPanel from '../components/UploadPanel.vue'

const categories = [
  { key: 'shirt', label: 'Koszula/Bluza' },
  { key: 'pants', label: 'Spodnie' },
  { key: 'shoes', label: 'Buty' }
]

const selected = ref({
  shirt: false,
  pants: false,
  shoes: false
})

const files = ref({
  shirt: null,
  pants: null,
  shoes: null
})

const previews = ref({
  shirt: null,
  pants: null,
  shoes: null
})

const isLoading = ref(false)
const generatedImage = ref(null)

const selectedCount = computed(() =>
  Object.values(selected.value).filter(Boolean).length
)

const canSubmit = computed(() =>
  selectedCount.value > 0 &&
  Object.entries(selected.value).every(([key, isChecked]) =>
    !isChecked || files.value[key]
  )
)

// Obsługa pliku z UploadPanel
function handleFileSelected({ category, file, previewUrl }) {
  files.value[category] = file
  previews.value[category] = previewUrl
}

async function generateSuggestion() {
  if (!canSubmit.value) return

  isLoading.value = true
  generatedImage.value = null

  try {
    const formData = new FormData()
    for (const [category, isChecked] of Object.entries(selected.value)) {
      if (isChecked && files.value[category]) {
        formData.append(category, files.value[category])
      }
    }

    const res = await axios.post('http://127.0.0.1:5000/api/generate-outfit', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    generatedImage.value = res.data.img_url
  } catch (err) {
    console.error('API Error:', err)
    alert('Błąd podczas komunikacji z API.')
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <h1 class="text-3xl font-bold text-center mb-6">AI Stylista – Dobierz stylizację</h1>

    <div class="bg-white max-w-2xl mx-auto p-6 rounded shadow space-y-6">
      <UploadPanel
        v-for="category in categories"
        :key="category.key"
        :label="category.label"
        :category="category.key"
        v-model="selected[category.key]"
        :preview-url="previews[category.key]"
        @file-selected="handleFileSelected"
      />

      <div class="text-center">
        <button
          class="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
          :disabled="!canSubmit || isLoading"
          @click="generateSuggestion"
        >
          Generuj stylizację
        </button>

        <div v-if="isLoading" class="mt-3 text-blue-600 animate-pulse">
          Wysyłanie danych do AI... (To może chwilę potrwać)
        </div>
      </div>

      <div v-if="generatedImage" class="mt-6 text-center">
        <h2 class="text-lg font-semibold mb-2">Wygenerowany model:</h2>
        <img :src="generatedImage" class="mx-auto rounded border max-w-xs" />
      </div>
    </div>
  </div>
</template>