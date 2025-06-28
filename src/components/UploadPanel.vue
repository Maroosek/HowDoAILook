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
const files = ref([]) // Store File objects
const editingIndex = ref(null) // Track which image is being edited

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

async function onFileChange(event) {
  const selectedFiles = Array.from(event.target.files)
  if (!selectedFiles.length) return

  // If editing, replace the file at editingIndex
  if (editingIndex.value !== null) {
    // Revoke old preview URL
    URL.revokeObjectURL(previews.value[editingIndex.value])
    previews.value.splice(editingIndex.value, 1, URL.createObjectURL(selectedFiles[0]))
    files.value.splice(editingIndex.value, 1, selectedFiles[0])
    editingIndex.value = null
  } else {
    // Add new files
    selectedFiles.forEach(f => {
      previews.value.push(URL.createObjectURL(f))
      files.value.push(f)
    })
  }

  const base64 = await Promise.all(files.value.map(fileToBase64))

  emit('file-selected', {
    category: props.category,
    files: files.value,
    previews: previews.value,
    base64
  })

  // Reset input value so the same file can be selected again
  event.target.value = ''
}

function triggerFileInput() {
  editingIndex.value = null
  fileInput.value && fileInput.value.click()
}

function editImage(index) {
  editingIndex.value = index
  fileInput.value && fileInput.value.click()
}

async function deleteImage(index) {
  URL.revokeObjectURL(previews.value[index])
  previews.value.splice(index, 1)
  files.value.splice(index, 1)
  emit('file-selected', {
    category: props.category,
    files: files.value,
    previews: previews.value,
    base64: files.value.length ? await Promise.all(files.value.map(fileToBase64)) : []
  })
}

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
      <input
        type="file"
        multiple
        accept="image/*"
        ref="fileInput"
        @change="onFileChange"
        style="display: none"
      />

      <button type="button" class="btn" @click="triggerFileInput">Dodaj ubranie</button>

<div v-if="previews.length" class="mt-2 grid grid-cols-2 gap-2 max-w-xs mx-auto">
  <div v-for="(p, i) in previews" :key="i" class="relative w-32 h-32">
    <img :src="p" class="preview-img w-full h-full object-cover rounded" />
    <div class="absolute top-1 right-1 flex flex-col gap-1">
      <button type="button" class="bg-white rounded shadow p-1" @click="deleteImage(i)">🗑️</button>
      <button type="button" class="bg-white rounded shadow p-1" @click="editImage(i)">✏️</button>
    </div>
  </div>
</div>


    </div>
  </div>
</template>