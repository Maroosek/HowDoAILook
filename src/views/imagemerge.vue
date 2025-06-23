<script setup>
import { ref, computed } from 'vue';

const images = ref([null, null]);
const mergedImage = ref(null);

const canMerge = computed(() => {
  return images.value.every(img => img !== null);
});

const handleUpload = (index, event) => {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      images.value[index] = {
        url: e.target.result,
        width: img.width,
        height: img.height
      };
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
};

const mergePhotos = () => {
    // Filter out null images (support 2 or 3 images)
    const validImages = images.value.filter(img => img !== null);
    if (validImages.length < 2) return;

    // Calculate total width and max height
    const totalWidth = validImages.reduce((sum, img) => sum + img.width, 0);
    const maxHeight = Math.max(...validImages.map(img => img.height));

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = totalWidth;
    canvas.height = maxHeight;

    // Helper to load all images
    const loadImage = src =>
        new Promise(resolve => {
            const img = new Image();
            img.onload = () => resolve(img);
            img.src = src;
        });

    Promise.all(validImages.map(img => loadImage(img.url))).then(loadedImgs => {
        let offsetX = 0;
        loadedImgs.forEach((img, idx) => {
            ctx.drawImage(img, offsetX, 0);
            offsetX += img.width;
        });
        mergedImage.value = canvas.toDataURL('image/jpeg', 0.9);
    });
};

const downloadImage = () => {
  if (!mergedImage.value) return;
  
  const link = document.createElement('a');
  link.href = mergedImage.value;
  link.download = 'polaczone-zdjecie.jpg';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
</script>

<template>
    <div class="photo-merger">
        <div class="upload-section">
            <div class="upload-box">
                <input 
                    type="file" 
                    id="photo1" 
                    accept="image/*" 
                    @change="handleUpload(0, $event)"
                    class="file-input"
                >
                <label for="photo1" class="upload-label">
                    <span v-if="!images[0]">Wybierz pierwsze zdjęcie</span>
                    <img v-else :src="images[0].url" class="preview-image">
                </label>
            </div>
            
            <div class="upload-box" v-if="images[0]">
                <input 
                    type="file" 
                    id="photo2" 
                    accept="image/*" 
                    @change="handleUpload(1, $event)"
                    class="file-input"
                >
                <label for="photo2" class="upload-label">
                    <span v-if="!images[1]">Wybierz drugie zdjęcie</span>
                    <img v-else :src="images[1].url" class="preview-image">
                </label>
            </div>
            <div class="upload-box" v-if="images[1]">
                <input 
                    type="file" 
                    id="photo3" 
                    accept="image/*" 
                    @change="handleUpload(2, $event)"
                    class="file-input"
                >
                <label for="photo3" class="upload-label">
                    <span v-if="!images[2]">Wybierz trzecie zdjęcie</span>
                    <img v-else :src="images[2].url" class="preview-image">
                </label>
            </div>
        </div>

        <button 
            @click="mergePhotos" 
            :disabled="!canMerge"
            class="merge-button"
        >
            Połącz zdjęcia
        </button>

        <div v-if="mergedImage" class="result-section">
            <h3>Wynik:</h3>
            <img :src="mergedImage" class="merged-image">
            <button @click="downloadImage" class="download-button">
                Pobierz połączone zdjęcie
            </button>
        </div>
    </div>
</template>

<style scoped>
.photo-merger {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.upload-section {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.upload-box {
  flex: 1;
}

.file-input {
  display: none;
}

.upload-label {
  display: block;
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-label:hover {
  border-color: #888;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.merge-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 20px;
}

.merge-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.merge-button:not(:disabled):hover {
  background-color: #45a049;
}

.result-section {
  margin-top: 20px;
  text-align: center;
}

.merged-image {
  max-width: 100%;
  border: 1px solid #ddd;
  margin: 10px 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.download-button {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.download-button:hover {
  background-color: #0b7dda;
}
</style>