<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import UploadPanel from '../components/UploadPanel.vue'
import '../styleSuggestion.css'

const categories = [
  { key: 'shirt', label: 'Koszula/Bluza' },
  { key: 'pants', label: 'Spodnie' },
  // { key: 'shoes', label: 'Buty' }
]

const selected = ref({
  shirt: false,
  pants: false,
  shoes: false
})

const files = ref({
  shirt: [],
  pants: [],
  shoes: []
})

const previews = ref({
  shirt: null,
  pants: null,
  shoes: null
})

const result = ref({
  desc: '',
  best_outfit: '',
  img_url: '',
})

const videoResult = ref({
  isLoading: false,
  error: '',
  video_url: ''
})

const isLoading = ref(false)
const generatedImage = ref(null)
const mergedImages = ref(null)
const progressMessage = ref('')
const sex = ref('male') // Domyślnie mężczyzna
const selectedStyle = ref('casual') // Domyślny styl

const selectedCount = computed(() =>
  Object.values(selected.value).filter(Boolean).length
)

const canSubmit = computed(() =>
  selectedCount.value > 0 &&
  Object.entries(selected.value).every(([key, isChecked]) =>
    !isChecked || files.value[key].length
  )
)

// Obsługa pliku z UploadPanel
function handleFileSelected({ category, base64, previews: pv }) {
  files.value[category] = base64
  previews.value[category] = pv
}

// async function mergeImagesVertically() {
//   const selectedFiles = categories
//     .filter(cat => selected.value[cat.key] && files.value[cat.key])
//     .map(cat => files.value[cat.key]);

//   if (selectedFiles.length === 0) return null;

//   const imageElements = await Promise.all(
//     selectedFiles.map(file => {
//       return new Promise((resolve, reject) => {
//         const reader = new FileReader();
//         reader.onload = e => {
//           const img = new Image();
//           img.onload = () => resolve(img);
//           img.onerror = reject;
//           img.src = e.target.result;
//         };
//         reader.onerror = reject;
//         reader.readAsDataURL(file);
//       });
//     })
//   );

//   const width = Math.max(...imageElements.map(img => img.width));
//   const height = imageElements.reduce((sum, img) => sum + img.height, 0);

//   const canvas = document.createElement('canvas');
//   canvas.width = width;
//   canvas.height = height;
//   const ctx = canvas.getContext('2d');

//   let y = 0;
//   for (const img of imageElements) {
//     ctx.drawImage(img, 0, y, img.width, img.height);
//     y += img.height;
//   }

//   return canvas.toDataURL('image/png');
// }

async function generateVideo() {
  videoResult.value.isLoading = true
  videoResult.value.error = ''
  videoResult.value.video_url = ''
  try {
    const res = await axios.post('http://192.168.3.13:5000/api/generate-outfit-video', {
      picture: result.value.img_url
    })
    videoResult.value.video_url = res.data?.video_url || res.data?.url || ''
    if (!videoResult.value.video_url) throw new Error("Brak url do wideo")
  } catch (e) {
    videoResult.value.error = 'Błąd podczas generowania wideo'
  } finally {
    videoResult.value.isLoading = false
  }
}

async function generateSuggestion() {
  if (!canSubmit.value) return

  isLoading.value = true
  generatedImage.value = null
  mergedImages.value = null

  try {
    //mergedImages.value = await mergeImagesVertically();

    // const res = await axios.post('http://127.0.0.1:5000/api/generate-outfit', {
    //   image_base64: mergedImages.value?.split(',')[1],
    //   mime_type: mergedImages.value?.match(/^data:(.*?);base64/)?.[1] || 'image/png'
    // })
    const payload = {}
    for (const { key } of categories) {
      if (selected.value[key] && files.value[key].length) {
      payload[key] = files.value[key]      // tablica Base-64
      }
    }
    payload.sex = sex.value
    payload.selectedStyle = selectedStyle.value

    
    const res = await axios.post('http://192.168.3.13:5000/api/generate-outfit', payload)
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
  }
}
</script>

<template>
  <div class="outfit-bg">
    <div class="outfit-glass-container">
      <h1 class="text-3xl font-bold text-center mb-6">AI Stylista – Dobierz stylizację</h1>

      <div>
        <p class="text-center text-gray-600 mb-4">
          Wybierz zdjęcia ubrań, które chcesz wykorzystać do stworzenia stylizacji. Możesz przesłać maksymalnie trzy zdjęcia z każdej kategorii.
          <br>
          <strong>Uwaga:</strong> Upewnij się, że zdjęcia są dobrej jakości i przedstawiają tylko ubrania bez innych elementów.

        </p>
      </div>

      <div class="bg-white max-w-4xl mx-auto p-6 rounded shadow mb-6">
        <p class="text-center mb-4">Zaznacz płeć modela</p>
        <div class="flex justify-center mb-6">
          <label class="inline-flex items-center mr-4">
            <input type="radio" id="man" value="male" v-model="sex" class="form-radio text-blue-600" />
            <span class="ml-2">Mężczyzna</span>
            <input type="radio" id="woman" value="female" v-model="sex" class="form-radio text-blue-600 ml-4" />
            <span class="ml-2">Kobieta</span>
          </label>
        </div>
      </div>
      
      <div class="bg-white max-w-4xl mx-auto p-6 rounded shadow mb-6">
        <p class="text-center mb-4">Wybierz docelowy styl ubioru</p>
        <div class="flex justify-center mb-4">
  <select v-model="selectedStyle" class="border border-gray-300 rounded p-2" style="margin:0; min-width: 180px; text-align:center;">
            <option value="casual">Casual</option>
            <option value="formal">Formalny</option>
            <option value="sport">Sportowy</option>
            <option value="elegant">Elegancki</option>
            <option value="streetwear">Streetwear</option>
            <option value="vintage">Vintage</option>
          </select>
        </div>
      </div>

      <br>

      <div class="bg-white max-w-4xl mx-auto p-6 rounded shadow">
        <div class="flex flex-wrap gap-6 justify-center">
        <UploadPanel v-for="category in categories" :key="category.key" :label="category.label" :category="category.key"
          v-model="selected[category.key]" :preview-url="previews[category.key]" @file-selected="handleFileSelected" />
        </div>
        <div class="text-center mb-4">
          <button class="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50" :disabled="!canSubmit || isLoading"
            @click="generateSuggestion">
            Generuj stylizację
          </button>

          <div v-if="isLoading" class="my-4 flex flex-col items-center">
            <span style="color:#91a0ff;">Wysyłanie danych do AI... (To może chwilę potrwać)</span>
            <div class="loading-bar-container">
              <div class="loading-bar"></div>
            </div>
          </div>
        </div>

        <div v-if="result.img_url" class="mt-8 text-center">
          <h2 class="text-xl font-semibold mb-2">Wynik:</h2>
          <p class="mb-2"><strong>Opis ubrań:</strong> {{ result.desc }}</p>
          <p class="mb-2"><strong>Proponowana stylizacja:</strong> {{ result.best_outfit }}</p>
          <img
            :src="result.img_url"
            class="mx-auto mt-4 rounded border shadow"
            style="max-width: 100%; height: auto; object-fit: contain; background: white;"
          />
          <button
              class="mt-4"
              style="display:block; margin:auto;"
              @click="generateVideo"
            >
              🎬 Wygenerować wideo?
          </button>
          <div v-if="videoResult.isLoading" class="mt-2 text-blue-400">Generuję wideo...</div>
            <div v-if="videoResult.error" class="mt-2 text-red-400">{{ videoResult.error }}</div>
            <video
              v-if="videoResult.video_url"
              :src="videoResult.video_url"
              controls
              class="mx-auto mt-4 rounded border shadow"
              style="max-width: 100%; background: white;"
            ></video>
        </div>
      </div>
    </div>
  </div>

</template>