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
const previews = ref(props.previewUrl ? [props.previewUrl] : [])

// Emituj checkbox
function updateCheckbox(val) {
  emit('update:modelValue', val)
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

// Obsługa pliku
async function onFileChange(event) {
  const files = Array.from(event.target.files)
  if (!files.length) return

  previews.value.forEach(u => URL.revokeObjectURL(u))

  previews.value = files.map(f => URL.createObjectURL(f))
  const base64 = await Promise.all(files.map(fileToBase64))

  emit('file-selected', {
    category: props.category,
    files,
    previews: previews.value,
    base64
  })
}

// Oczyszczanie URL
watch(previews, (newVal, oldVal) => {
  oldVal.forEach(u => URL.revokeObjectURL(u))
})
</script>

<template>
  <div class="border-b pb-4 mb-4">
    <label class="flex items-center gap-2 font-medium mb-2">
      <input type="checkbox" :checked="modelValue" @change="e => updateCheckbox(e.target.checked)" />
      {{ label }}
    </label>

    <div v-if="modelValue">
      <input type="file" multiple accept="image/*" ref="fileInput" @change="onFileChange" />

      <div v-if="previews.length" class="mt-2 flex gap-2 flex-wrap">
        <img v-for="(p, i) in previews" :key="i" :src="p" class="preview-img" />
      </div>
    </div>
  </div>
</template>