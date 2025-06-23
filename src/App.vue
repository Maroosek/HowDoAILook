<script setup>
import { ref, computed } from 'vue'
import Home from './views/Home.vue'
import OutfitVisualisation from './views/OutfitVisualisation.vue'
import OutfitSuggestion from './views/OutfitSuggestion.vue'
import imagemerge from './views/imagemerge.vue'

const currentView = ref('home')

const views = {
  home: 'Strona główna',
  visualization: 'Wizualizacja ubioru',
  suggestion: 'Dobieranie ubrań',
  imagemerge: 'Łączenie zdjęć'
}

const currentComponent = computed(() => {
  switch (currentView.value) {
    case 'visualization': return OutfitVisualisation
    case 'suggestion': return OutfitSuggestion
    case 'imagemerge': return imagemerge
    default: return Home
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <nav class="flex gap-4 mb-6">
      <button
        v-for="(label, key) in views"
        :key="key"
        @click="currentView = key"
        :class="[
          'px-4 py-2 rounded',
          currentView === key ? 'bg-blue-600 text-white' : 'bg-white text-blue-600 border border-blue-600'
        ]"
      >
        {{ label }}
      </button>
    </nav>

    <component :is="currentComponent" />
  </div>
</template>