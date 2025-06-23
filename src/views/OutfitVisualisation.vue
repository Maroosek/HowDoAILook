<script setup>
import { ref } from 'vue'
import axios from 'axios'
import UploadPanelSingle from '../components/UploadPanelSingle.vue'

//TODO add sex option, style preference, formal, casual, etc.

const fileData = ref({})
const isLoading = ref(false)
const progressMessage = ref('')
const result = ref({
  desc: '',
  best_outfit: '',
  img_url: '',
})

function handleFiles(selectedFiles) {
  fileData.value = selectedFiles
}

async function generateModel() {
  if (!fileData.value || !fileData.value.base64) {
    alert('Wybierz plik i zaznacz checkbox.')
    return
  }

  isLoading.value = true
  progressMessage.value = 'Wysyłanie danych do AI...'
  result.value = {}

  try {
    const res = await axios.post('http://127.0.0.1:5000/api/generate-outfit', {
      image_base64: fileData.value.base64.split(',')[1],
      mime_type: fileData.value.base64.match(/^data:(.*?);base64/)?.[1] || 'image/png'
    })

    progressMessage.value = 'Odebrano odpowiedź. Przetwarzanie wyników...'

    result.value = {
      desc: res.data.desc,
      best_outfit: res.data.best_outfit,
      img_url: res.data.img_url
    }
  } catch (err) {
    console.error('API Error:', err)
    alert('Błąd podczas komunikacji z API.')
  } finally {
    isLoading.value = false
    progressMessage.value = ''
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <h1 class="text-3xl font-bold text-center mb-8">AI Stylista – Generuj stylizację</h1>

    <UploadPanelSingle @files-selected="handleFiles" />

    <div class="text-center mt-4">
      <button
        class="bg-blue-600 text-white px-6 py-2 rounded disabled:opacity-50"
        :disabled="isLoading || !fileData.base64"
        @click="generateModel"
      >
        Generuj stylizację
      </button>
    </div>

    <div v-if="isLoading" class="mt-4 text-center text-blue-500 font-medium animate-pulse">
      {{ progressMessage }}
    </div>

    <div v-if="result.img_url" class="mt-8 text-center">
      <h2 class="text-xl font-semibold mb-2">Wynik:</h2>
      <p class="mb-2"><strong>Opis ubrań:</strong> {{ result.desc }}</p>
      <p class="mb-2"><strong>Proponowana stylizacja:</strong> {{ result.best_outfit }}</p>
      <img :src="result.img_url" class="max-w-md mx-auto mt-4 rounded border shadow" 
      style="max-width: 32rem; max-height: 32rem;"/>
    </div>
  </div>
</template>