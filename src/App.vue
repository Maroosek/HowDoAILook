<script setup>
import { ref, computed } from 'vue'
import Home from './views/Home.vue'
import OutfitSuggestion from './views/OutfitSuggestion.vue'
import AuthorsView from './views/AuthorsView.vue'

const currentView = ref('home')

const views = {
  home: 'Menu',
}

const currentComponent = computed(() => {
  switch (currentView.value) {
    case 'visualization': return OutfitVisualisation
    case 'suggestion': return OutfitSuggestion
    case 'imagemerge': return imagemerge
    case 'authorsview': return AuthorsView
    default: return Home
  }
})
</script>

<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
  <div class="min-h-screen bg-gray-100 p-6">
    <nav class="flex justify-center gap-4 mb-2">
      <button
        v-for="(label, key) in views"
        :key="key"
        @click="currentView = key"
        :class="[
          'menu-btn',
          currentView === key ? 'bg-blue-600 text-white' : 'bg-white text-blue-600 border border-blue-600'
        ]"
      >
        {{ label }}
      </button>
    </nav>

    <component :is="currentComponent" @change-view="currentView = $event" />
  </div>
</template>

<style scoped>
.menu-btn {
  font-size: 0.87rem;
  padding: 3px 14px;
  border-radius: 8px;
  min-width: 64px;
}
</style>