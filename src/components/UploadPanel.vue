<script setup>
import { ref, watch, computed } from 'vue'

const emit = defineEmits(['files-selected'])

const categories = [
  { key: 'top', label: 'Koszula / Bluza' },
  { key: 'bottom', label: 'Spodnie' },
  { key: 'shoes', label: 'Buty' },
]

const selectedCategories = ref([])
const files = ref({})
const previews = ref({})

// Obsługa zmiany pliku
function onFileChange(event, categoryKey) {
  const file = event.target.files[0]
  if (!file) return

  files.value[categoryKey] = file
  previews.value[categoryKey] = URL.createObjectURL(file)

  emitSelected()
}

// Emitujemy tylko zaznaczone z plikami
function emitSelected() {
  const filtered = {}
  for (const key of selectedCategories.value) {
    if (files.value[key]) {
      filtered[key] = files.value[key]
    }
  }
  emit('files-selected', filtered)
}

// Reagujemy na zmianę zaznaczenia checkboxów
watch(selectedCategories, () => {
  emitSelected()
})

// Cleanup dla starych URL
watch(previews, (newVal, oldVal) => {
  Object.values(oldVal).forEach(url => URL.revokeObjectURL(url))
})
</script>

<template>
  <div class="bg-white p-4 rounded shadow-md max-w-xl mx-auto mb-6">
    <h2 class="text-xl font-semibold mb-4">Wybierz i prześlij elementy garderoby</h2>

    <div v-for="category in categories" :key="category.key" class="mb-6 border-b pb-4">
      <label class="flex items-center gap-2 font-medium mb-1">
        <input type="checkbox" v-model="selectedCategories" :value="category.key" />
        {{ category.label }}
      </label>

      <div v-if="selectedCategories.includes(category.key)">
        <input type="file" accept="image/*" @change="event => onFileChange(event, category.key)" />

        <div v-if="previews[category.key]" class="mt-2">
          <img
          :src="previews[category.key]"
          class="max-w-24 max-h-24 w-auto h-auto object-cover rounded border"
          style="max-width: 8rem; max-height: 8rem;"
          />
        </div>
      </div>
    </div>
  </div>
</template>
