<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  label: String,
  modelValue: Boolean,
  previewUrl: String,
  category: String
})

const emit = defineEmits(['update:modelValue', 'file-selected'])

const fileInput = ref(null)
const preview = ref(props.previewUrl || null)

// Emituj checkbox
function updateCheckbox(val) {
  emit('update:modelValue', val)
}

// Obsługa pliku
function onFileChange(event) {
  const file = event.target.files[0]
  if (!file) return

  const previewUrl = URL.createObjectURL(file)
  preview.value = previewUrl
  emit('file-selected', { category: props.category, file, previewUrl })
}

// Oczyszczanie URL
watch(preview, (newVal, oldVal) => {
  if (oldVal) URL.revokeObjectURL(oldVal)
})
</script>

<template>
  <div class="border-b pb-4 mb-4">
    <label class="flex items-center gap-2 font-medium mb-2">
      <input type="checkbox" :checked="modelValue" @change="e => updateCheckbox(e.target.checked)" />
      {{ label }}
    </label>

    <div v-if="modelValue">
      <input type="file" accept="image/*" ref="fileInput" @change="onFileChange" />

      <div v-if="preview" class="mt-2">
        <img
          :src="preview"
          class="max-w-32 max-h-32 rounded border object-cover"
        style="max-width: 16rem; max-height: 16rem;"/>
      </div>
    </div>
  </div>
</template>