<script setup>
import { ref, computed } from 'vue';

//TODO add scaling to prevent too big images and keep aspect ratio
//TODO add remove image button and clear all images button

const imagesTop = ref([null, null, null]);
const imagesBottom = ref([null, null, null]);
const imagesShoes = ref([null, null, null]);
const mergedImage = ref(null);

const canMerge = computed(() => {
  const allImages = [...imagesTop.value, ...imagesBottom.value, ...imagesShoes.value];
  return allImages.filter(img => img !== null).length >= 2;
});

const handleUpload = (index, event, category) => {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      if (category === 1) {
        imagesTop.value[index] = {
          url: e.target.result,
          width: img.width,
          height: img.height
        };
      } else if (category === 2) {
        imagesBottom.value[index] = {
          url: e.target.result,
          width: img.width,
          height: img.height
        };
      } else if (category === 3) {
        imagesShoes.value[index] = {
          url: e.target.result,
          width: img.width,
          height: img.height
        };
      }
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
};
const mergePhotos = () => {
    // Gather all non-null images from all categories in order
    const allImages = [
        ...imagesTop.value,
        ...imagesBottom.value,
        ...imagesShoes.value
    ].filter(img => img !== null);

    if (allImages.length < 2) return;

    // Calculate total width and max height
    //const totalWidth = allImages.reduce((sum, img) => sum + img.width, 0);
    //const maxHeight = Math.max(...allImages.map(img => img.height));
    const maxHeight = Math.max(
        ...imagesTop.value.map(img => img ? img.height : 0),
        ...imagesBottom.value.map(img => img ? img.height : 0),
        ...imagesShoes.value.map(img => img ? img.height : 0)
    );
    const totalWidth = imagesTop.value.reduce((sum, img) => sum + (img ? img.width : 0), 0) +
                       imagesBottom.value.reduce((sum, img) => sum + (img ? img.width : 0), 0) +
                       imagesShoes.value.reduce((sum, img) => sum + (img ? img.width : 0), 0);

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

    // Load all images and draw them in order
    Promise.all([
      ...imagesTop.value.map(img => img ? loadImage(img.url) : null),
      ...imagesBottom.value.map(img => img ? loadImage(img.url) : null),
      ...imagesShoes.value.map(img => img ? loadImage(img.url) : null)
    ]).then(loadedImgs => {
      // Split loadedImgs into rows
      const topImgs = loadedImgs.slice(0, 3).filter(Boolean);
      const bottomImgs = loadedImgs.slice(3, 6).filter(Boolean);
      const shoesImgs = loadedImgs.slice(6, 9).filter(Boolean);

      // Calculate row widths and heights
      const rowWidths = [
        topImgs.reduce((sum, img) => sum + img.width, 0),
        bottomImgs.reduce((sum, img) => sum + img.width, 0),
        shoesImgs.reduce((sum, img) => sum + img.width, 0)
      ];
      const rowHeights = [
        topImgs.length ? Math.max(...topImgs.map(img => img.height)) : 0,
        bottomImgs.length ? Math.max(...bottomImgs.map(img => img.height)) : 0,
        shoesImgs.length ? Math.max(...shoesImgs.map(img => img.height)) : 0
      ];

      // Only include rows that have images
      const rows = [];
      if (topImgs.length) rows.push({ imgs: topImgs, height: rowHeights[0], width: rowWidths[0] });
      if (bottomImgs.length) rows.push({ imgs: bottomImgs, height: rowHeights[1], width: rowWidths[1] });
      if (shoesImgs.length) {
        // Shoes go below bottom if bottom exists, else below top
        if (bottomImgs.length) {
          rows.push({ imgs: shoesImgs, height: rowHeights[2], width: rowWidths[2] });
        } else {
          // Insert shoes after top
          if (rows.length > 0) {
            rows.splice(1, 0, { imgs: shoesImgs, height: rowHeights[2], width: rowWidths[2] });
          } else {
            rows.push({ imgs: shoesImgs, height: rowHeights[2], width: rowWidths[2] });
          }
        }
      }

      // Canvas size
      const canvasWidth = Math.max(...rows.map(r => r.width));
      const canvasHeight = rows.reduce((sum, r) => sum + r.height, 0);

      canvas.width = canvasWidth;
      canvas.height = canvasHeight;

      // Draw each row
      let offsetY = 0;
      rows.forEach(row => {
        let offsetX = 0;
        row.imgs.forEach(img => {
          ctx.drawImage(img, offsetX, offsetY);
          offsetX += img.width;
        });
        offsetY += row.height;
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
                    @change="handleUpload(0, $event, 1)"
                    class="file-input"
                >
                <label for="photo1" class="upload-label">
                    <span v-if="!imagesTop[0]">Wybierz pierwsze zdjęcie</span>
                    <img v-else :src="imagesTop[0].url" class="preview-image">
                </label>
            </div>
            
            <div class="upload-box" v-if="imagesTop[0]">
                <input 
                    type="file" 
                    id="photo2" 
                    accept="image/*" 
                    @change="handleUpload(1, $event, 1)"
                    class="file-input"
                >
                <label for="photo2" class="upload-label">
                    <span v-if="!imagesTop[1]">Wybierz drugie zdjęcie</span>
                    <img v-else :src="imagesTop[1].url" class="preview-image">
                </label>
            </div>
            <div class="upload-box" v-if="imagesTop[1]">
                <input 
                    type="file" 
                    id="photo3" 
                    accept="image/*" 
                    @change="handleUpload(2, $event, 1)"
                    class="file-input"
                >
                <label for="photo3" class="upload-label">
                    <span v-if="!imagesTop[2]">Wybierz trzecie zdjęcie</span>
                    <img v-else :src="imagesTop[2].url" class="preview-image">
                </label>
            </div>
        </div>
        <div class="upload-section">
            <div class="upload-box">
                <input 
                    type="file" 
                    id="photo4" 
                    accept="image/*" 
                    @change="handleUpload(0, $event, 2)"
                    class="file-input"
                >
                <label for="photo4" class="upload-label">
                    <span v-if="!imagesBottom[0]">Wybierz pierwsze zdjęcie</span>
                    <img v-else :src="imagesBottom[0].url" class="preview-image">
                </label>
            </div>
            
            <div class="upload-box" v-if="imagesBottom[0]">
                <input 
                    type="file" 
                    id="photo5" 
                    accept="image/*" 
                    @change="handleUpload(1, $event, 2)"
                    class="file-input"
                >
                <label for="photo5" class="upload-label">
                    <span v-if="!imagesBottom[1]">Wybierz drugie zdjęcie</span>
                    <img v-else :src="imagesBottom[1].url" class="preview-image">
                </label>
            </div>
            <div class="upload-box" v-if="imagesBottom[1]">
                <input 
                    type="file" 
                    id="photo6" 
                    accept="image/*" 
                    @change="handleUpload(2, $event, 2)"
                    class="file-input"
                >
                <label for="photo6" class="upload-label">
                    <span v-if="!imagesBottom[2]">Wybierz trzecie zdjęcie</span>
                    <img v-else :src="imagesBottom[2].url" class="preview-image">
                </label>
            </div>
        </div>
        <div class="upload-section">
            <div class="upload-box">
                <input 
                    type="file" 
                    id="photo7" 
                    accept="image/*" 
                    @change="handleUpload(0, $event, 3)"
                    class="file-input"
                >
                <label for="photo7" class="upload-label">
                    <span v-if="!imagesShoes[0]">Wybierz pierwsze zdjęcie</span>
                    <img v-else :src="imagesShoes[0].url" class="preview-image">
                </label>
            </div>
            
            <div class="upload-box" v-if="imagesShoes[0]">
                <input 
                    type="file" 
                    id="photo8" 
                    accept="image/*" 
                    @change="handleUpload(1, $event, 3)"
                    class="file-input"
                >
                <label for="photo8" class="upload-label">
                    <span v-if="!imagesShoes[1]">Wybierz drugie zdjęcie</span>
                    <img v-else :src="imagesShoes[1].url" class="preview-image">
                </label>
            </div>
            <div class="upload-box" v-if="imagesShoes[1]">
                <input 
                    type="file" 
                    id="photo9" 
                    accept="image/*" 
                    @change="handleUpload(2, $event, 3)"
                    class="file-input"
                >
                <label for="photo9" class="upload-label">
                    <span v-if="!imagesShoes[2]">Wybierz trzecie zdjęcie</span>
                    <img v-else :src="imagesShoes[2].url" class="preview-image">
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