<script setup>
import { ref, watch } from 'vue'

const emit = defineEmits(['files-selected'])

const selected = ref(false)
const file = ref(null)
const preview = ref(null)
const base64 = ref(null)

// Convert image file to Base64
function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

// Obsługa zmiany pliku
async function onFileChange(event) {
  const f = event.target.files[0]
  if (!f) return

  file.value = f
  preview.value = URL.createObjectURL(f)
  base64.value = await fileToBase64(f)

  emitSelected()
}

// Emitujemy tylko jeśli zaznaczone i plik jest
function emitSelected() {
  emit('files-selected', selected.value && file.value ? { file: file.value, base64: base64.value } : {})
}

// Reagujemy na zmianę zaznaczenia checkboxa
watch(selected, () => {
  emitSelected()
})

// Cleanup dla starych URL
watch(preview, (newVal, oldVal) => {
  if (oldVal) URL.revokeObjectURL(oldVal)
})
</script>

<template>
  <div class="bg-white p-4 rounded shadow-md max-w-xl mx-auto mb-6">
    <h2 class="text-xl font-semibold mb-4">Wybierz i prześlij element garderoby</h2>

    <div class="mb-6 border-b pb-4">
      <label class="flex items-center gap-2 font-medium mb-1">
        <input type="checkbox" v-model="selected" />
        Element garderoby
      </label>

      <div v-if="selected">
        <input type="file" accept="image/*" multiple @change="onFileChange" />

        <div v-if="preview" class="mt-2">
          <img
            :src="preview"
            class="max-w-24 max-h-24 w-auto h-auto object-cover rounded border"
            style="max-width: 16rem; max-height: 16rem;"
          />
        </div>
      </div>
    </div>
  </div>
</template>
