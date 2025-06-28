<template>
  <div class="app-container">
    <!-- Header -->
    <header class="header">
      <div class="container">
        <div class="logo-container">
          <div class="logo-icon">
            <i class="fa-solid fa-mobile-button"></i>
          </div>
          <h1 class="logo-text">AI Stylista</h1>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <div class="container">
        <!-- Welcome Section -->
        <section class="welcome-section">
            <div class="welcome-logo">
              <i class="fas fa-robot"></i> <!-- Możesz zmienić ikonę -->
            </div>
          <h2 class="welcome-title">How do AI look</h2>
          <p class="welcome-subtitle">
            Odkryj przyszłość mody z naszą aplikacją AI. Wizualizuj outfity i otrzymuj spersonalizowane stylizacje!
          </p>
        </section>

        <!-- Feature Cards -->
        <div class="feature-cards">
          <div class="feature-card" @click="$emit('change-view', 'suggestion')">
            <div class="feature-content">
              <div class="feature-icon styling">
                <i class="fa-solid fa-shirt"></i>
              </div>
              <h3 class="feature-title">Dobieranie ubrań</h3>
              <p class="feature-description">
                Uzyskaj profesjonalną stylizację na podstawie jednego elementu garderoby. AI doradzi Ci idealne dopasowania!
              </p>
            </div>
          </div>

          <div class="feature-card" @click="$emit('change-view', 'authorsview')">
            <div class="feature-content">
              <div class="feature-icon styling">
                <i class="fa-brands fa-linkedin"></i>
              </div>
              <h3 class="feature-title">Autorzy</h3>
              <p class="feature-description">
                Czyli kto stoi za tym pomysłem!
              </p>
            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <p>
          <i class="fas fa-heart text-danger me-1"></i>
          Stworzone z pasją dla mody i technologii
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      selectedFeature: null,
      showNavigation: true,
      uploadedFiles: [],
      processing: false
    }
  },
  methods: {
    selectFeature(feature) {
      this.selectedFeature = feature;
      this.showNavigation = false;
      
      // Smooth scroll to upload section
      this.$nextTick(() => {
        const uploadSection = document.querySelector('.upload-section');
        if (uploadSection) {
          uploadSection.scrollIntoView({ 
            behavior: 'smooth',
            block: 'center'
          });
        }
      });
    },
    
    startVisualization() {
      this.selectFeature('visualize');
    },
    
    startStyling() {
      this.selectFeature('styling');
    },
    
    handleFileUpload(event) {
      const files = Array.from(event.target.files);
      
      files.forEach(file => {
        if (file.type.startsWith('image/')) {
          const reader = new FileReader();
          reader.onload = (e) => {
            this.uploadedFiles.push({
              name: file.name,
              url: e.target.result,
              file: file
            });
          };
          reader.readAsDataURL(file);
        }
      });
    },
    
    removeFile(index) {
      this.uploadedFiles.splice(index, 1);
    },
    
    async processFiles() {
      this.processing = true;
      
      // Symulacja przetwarzania AI
      setTimeout(() => {
        this.processing = false;
        alert(`Przetwarzanie zakończone! Wygenerowano stylizację dla ${this.uploadedFiles.length} plików.`);
      }, 3000);
    }
  }
}
</script>

<style scoped>
:root {
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  --dark-bg: #0a0a0a;
  --card-bg: rgba(255, 255, 255, 0.05);
  --card-border: rgba(255, 255, 255, 0.1);
  --text-primary: #ffffff;
  --text-secondary: rgba(255, 255, 255, 0.7);
  --glass-bg: rgba(255, 255, 255, 0.08);
  --glass-border: rgba(255, 255, 255, 0.15);
}

.app-container {
  max-width: 450px;
  margin: 0px auto;
  min-height: 100vh;
  background: #0a0a0a;
  background-image: 
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.4) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.4) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.3) 0%, transparent 50%);
  color: #ffffff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  box-shadow: 0 8px 32px #0005;
  border-radius: 24px;
}

.header {
  background: var(--glass-bg);
  backdrop-filter: blur(2px);
  border-bottom: 1px solid var(--glass-border);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.logo-container {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  gap: 0.5rem;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: var(--primary-gradient);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.main-content {
  padding: 2rem 1rem;
}

.welcome-section {
  text-align: center;
  margin-bottom: 3rem;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #ffffff;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
  line-height: 1.2;
}

.welcome-subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 2rem;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  text-shadow: 0 1px 5px rgba(0, 0, 0, 0.3);
}

.feature-cards {
  display: grid;
  gap: 1.5rem;
  max-width: 600px;
  margin: 0 auto;
}

.feature-card {
  background: var(--glass-bg);
  backdrop-filter: blur(25px);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  padding: 2rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--primary-gradient);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 20px;
}

.feature-card:hover::before {
  opacity: 0.1;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.3);
}

.feature-content {
  position: relative;
  z-index: 2;
}

.feature-icon {
  width: 60px;
  height: 60px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin: 0 auto 1.5rem;
  color: white;
}

.feature-icon.visualize {
  background: var(--primary-gradient);
}

.feature-icon.styling {
  background: var(--secondary-gradient);
}

.feature-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
  text-align: center;
  color: #ffffff;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.feature-description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
  text-align: center;
  font-size: 0.95rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.navigation-menu {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  padding: 1rem;
  margin-top: 2rem;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.nav-button {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #ffffff;
  padding: 0.8rem 1.5rem;
  border-radius: 12px;
  width: 100%;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
  font-weight: 500;
  cursor: pointer;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.nav-button:last-child {
  margin-bottom: 0;
}

.nav-button:hover:not(:disabled) {
  background: var(--primary-gradient);
  border-color: transparent;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.nav-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.upload-section {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 2px dashed var(--glass-border);
  border-radius: 20px;
  padding: 3rem 2rem;
  text-align: center;
  margin: 2rem 0;
  transition: all 0.3s ease;
}

.upload-section:hover {
  border-color: rgba(255, 255, 255, 0.3);
}

.upload-icon {
  font-size: 3rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.uploaded-files {
  margin-top: 2rem;
}

.files-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.file-preview {
  position: relative;
  text-align: center;
}

.preview-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 12px;
  border: 2px solid var(--glass-border);
}

.file-name {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-top: 0.5rem;
  word-break: break-all;
}

.remove-btn {
  position: absolute;
  top: -8px;
  right: 8px;
  background: #ff4757;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
}

.footer {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.pulse-animation {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(102, 126, 234, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(102, 126, 234, 0);
  }
}

@media (max-width: 768px) {
  .welcome-title {
    font-size: 2rem;
  }
  
  .feature-card {
    padding: 1.5rem;
  }
  
  .main-content {
    padding: 1.5rem 1rem;
  }
  
  .files-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }
}

@media (max-width: 480px) {
  .welcome-title {
    font-size: 1.8rem;
  }
  
  .logo-text {
    font-size: 1.3rem;
  }
}
</style>