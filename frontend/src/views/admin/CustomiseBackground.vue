<template>
  <div class="customise-background-page">
    <button class="back-button" @click="$router.go(-1)">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="M19 12H5"></path>
        <polyline points="12 19 5 12 12 5"></polyline>
      </svg>
    </button>
    <div class="content-container">
      <div class="upload-section">
        <h2>Customise Login Page Gallery Images</h2>
        
        <!-- Main Image Section - Fixed -->
        <div class="image-section">
          <h3>Main Banner Image (Fixed)</h3>
          <div class="fixed-notice">
            <p>This image is fixed and cannot be customized</p>
          </div>
        </div>

        <!-- Gallery Images Section -->
        <div class="gallery-section">
          <h3>Gallery Images (Customizable)</h3>
          <p class="section-description">
            You can customize the 5 gallery images displayed at the bottom of the login page
          </p>

          <div class="gallery-images-grid">
            <!-- Gallery Image 1 -->
            <div class="gallery-image-item">
              <h4>Gallery Image 1</h4>
              <div class="current-image-preview">
                <img 
                  :src="currentGalleryImages.image_1 || defaultImageUrls.image_1" 
                  alt="Gallery Image 1"
                />
                <span class="label">Current</span>
              </div>
              <div class="upload-controls">
                <input
                  :ref="'fileInput1'"
                  type="file"
                  accept="image/png,image/jpg,image/jpeg"
                  @change="handleFileSelect(1, $event)"
                  style="display: none"
                />
                <button @click="triggerFileInput(1)" class="upload-btn">
                  {{ uploadingImage === 1 ? 'Uploading...' : 'Upload New' }}
                </button>
                <button 
                  v-if="selectedFiles[1]" 
                  @click="uploadGalleryImage(1)"
                  :disabled="uploadingImage === 1"
                  class="confirm-btn"
                >
                  Confirm
                </button>
                <div v-if="selectedFiles[1]" class="preview-box">
                  <img :src="previewUrls[1]" alt="Preview" />
                </div>
              </div>
            </div>

            <!-- Gallery Image 2 -->
            <div class="gallery-image-item">
              <h4>Gallery Image 2</h4>
              <div class="current-image-preview">
                <img 
                  :src="currentGalleryImages.image_2 || defaultImageUrls.image_2" 
                  alt="Gallery Image 2"
                />
                <span class="label">Current</span>
              </div>
              <div class="upload-controls">
                <input
                  :ref="'fileInput2'"
                  type="file"
                  accept="image/png,image/jpg,image/jpeg"
                  @change="handleFileSelect(2, $event)"
                  style="display: none"
                />
                <button @click="triggerFileInput(2)" class="upload-btn">
                  {{ uploadingImage === 2 ? 'Uploading...' : 'Upload New' }}
                </button>
                <button 
                  v-if="selectedFiles[2]" 
                  @click="uploadGalleryImage(2)"
                  :disabled="uploadingImage === 2"
                  class="confirm-btn"
                >
                  Confirm
                </button>
                <div v-if="selectedFiles[2]" class="preview-box">
                  <img :src="previewUrls[2]" alt="Preview" />
                </div>
              </div>
            </div>

            <!-- Gallery Image 3 -->
            <div class="gallery-image-item">
              <h4>Gallery Image 3</h4>
              <div class="current-image-preview">
                <img 
                  :src="currentGalleryImages.image_3 || defaultImageUrls.image_3" 
                  alt="Gallery Image 3"
                />
                <span class="label">Current</span>
              </div>
              <div class="upload-controls">
                <input
                  :ref="'fileInput3'"
                  type="file"
                  accept="image/png,image/jpg,image/jpeg"
                  @change="handleFileSelect(3, $event)"
                  style="display: none"
                />
                <button @click="triggerFileInput(3)" class="upload-btn">
                  {{ uploadingImage === 3 ? 'Uploading...' : 'Upload New' }}
                </button>
                <button 
                  v-if="selectedFiles[3]" 
                  @click="uploadGalleryImage(3)"
                  :disabled="uploadingImage === 3"
                  class="confirm-btn"
                >
                  Confirm
                </button>
                <div v-if="selectedFiles[3]" class="preview-box">
                  <img :src="previewUrls[3]" alt="Preview" />
                </div>
              </div>
            </div>

            <!-- Gallery Image 4 -->
            <div class="gallery-image-item">
              <h4>Gallery Image 4</h4>
              <div class="current-image-preview">
                <img 
                  :src="currentGalleryImages.image_4 || defaultImageUrls.image_4" 
                  alt="Gallery Image 4"
                />
                <span class="label">Current</span>
              </div>
              <div class="upload-controls">
                <input
                  :ref="'fileInput4'"
                  type="file"
                  accept="image/png,image/jpg,image/jpeg"
                  @change="handleFileSelect(4, $event)"
                  style="display: none"
                />
                <button @click="triggerFileInput(4)" class="upload-btn">
                  {{ uploadingImage === 4 ? 'Uploading...' : 'Upload New' }}
                </button>
                <button 
                  v-if="selectedFiles[4]" 
                  @click="uploadGalleryImage(4)"
                  :disabled="uploadingImage === 4"
                  class="confirm-btn"
                >
                  Confirm
                </button>
                <div v-if="selectedFiles[4]" class="preview-box">
                  <img :src="previewUrls[4]" alt="Preview" />
                </div>
              </div>
            </div>

            <!-- Gallery Image 5 -->
            <div class="gallery-image-item">
              <h4>Gallery Image 5</h4>
              <div class="current-image-preview">
                <img 
                  :src="currentGalleryImages.image_5 || defaultImageUrls.image_5" 
                  alt="Gallery Image 5"
                />
                <span class="label">Current</span>
              </div>
              <div class="upload-controls">
                <input
                  :ref="'fileInput5'"
                  type="file"
                  accept="image/png,image/jpg,image/jpeg"
                  @change="handleFileSelect(5, $event)"
                  style="display: none"
                />
                <button @click="triggerFileInput(5)" class="upload-btn">
                  {{ uploadingImage === 5 ? 'Uploading...' : 'Upload New' }}
                </button>
                <button 
                  v-if="selectedFiles[5]" 
                  @click="uploadGalleryImage(5)"
                  :disabled="uploadingImage === 5"
                  class="confirm-btn"
                >
                  Confirm
                </button>
                <div v-if="selectedFiles[5]" class="preview-box">
                  <img :src="previewUrls[5]" alt="Preview" />
                </div>
              </div>
            </div>
          </div>

          <div v-if="message" :class="['message', messageType]">
            {{ message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CustomiseBackground",
  data() {
    return {
      selectedFiles: {},
      previewUrls: {},
      uploadingImage: null,
      message: "",
      messageType: "success",
      currentGalleryImages: {},
      defaultImageUrls: {
        image_1: "/src/assets/images/Image3.png",
        image_2: "/src/assets/images/Image5.jpg",
        image_3: "/src/assets/images/Image4.jpg",
        image_4: "/src/assets/images/Image2.png",
        image_5: "/src/assets/images/Image1.png",
      },
    };
  },
  methods: {
    triggerFileInput(imageNumber) {
      this.$refs[`fileInput${imageNumber}`].click();
    },

    handleFileSelect(imageNumber, event) {
      const file = event.target.files[0];
      this.processFile(imageNumber, file);
    },

    processFile(imageNumber, file) {
      if (!file) return;

      // Validate file type
      const allowedTypes = ["image/png", "image/jpg", "image/jpeg"];
      if (!allowedTypes.includes(file.type)) {
        this.showMessage(
          "Please select a PNG, JPG, or JPEG image file.",
          "error"
        );
        return;
      }

      // Validate file size (10MB max)
      const maxSize = 10 * 1024 * 1024;
      if (file.size > maxSize) {
        this.showMessage("File size must be less than 10MB.", "error");
        return;
      }

      this.selectedFiles[imageNumber] = file;
      this.createPreview(imageNumber, file);
    },

    createPreview(imageNumber, file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.$set(this.previewUrls, imageNumber, e.target.result);
      };
      reader.readAsDataURL(file);
    },

    async uploadGalleryImage(imageNumber) {
      if (!this.selectedFiles[imageNumber]) return;

      this.uploadingImage = imageNumber;
      this.message = "";

      const formData = new FormData();
      formData.append("image", this.selectedFiles[imageNumber]);

      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/upload-gallery-image/${imageNumber}`,
          {
            method: "POST",
            body: formData,
          }
        );

        const data = await response.json();

        if (data.success) {
          this.showMessage(
            `Gallery image ${imageNumber} uploaded successfully!`,
            "success"
          );
          // Update current image display
          this.currentGalleryImages[`image_${imageNumber}`] = data.image_url;
          // Clear selection
          this.selectedFiles[imageNumber] = null;
          this.previewUrls[imageNumber] = null;
          this.$refs[`fileInput${imageNumber}`].value = "";
        } else {
          this.showMessage(
            data.message || "Upload failed. Please try again.",
            "error"
          );
        }
      } catch (error) {
        console.error("Upload error:", error);
        this.showMessage("Network error. Please try again.", "error");
      } finally {
        this.uploadingImage = null;
      }
    },

    showMessage(text, type) {
      this.message = text;
      this.messageType = type;
      setTimeout(() => {
        this.message = "";
      }, 5000);
    },
  },

  async mounted() {
    // Load current gallery images on component mount
    try {
      const response = await fetch("http://127.0.0.1:5000/api/get-gallery-images");
      const data = await response.json();
      if (data.success && data.gallery_images) {
        this.currentGalleryImages = data.gallery_images;
      }
    } catch (error) {
      console.error("Error loading current gallery images:", error);
    }
  },
};
</script>

<style scoped>
.customise-background-page {
  background-color: #f0f0f0;
  min-height: calc(100vh - 240px);
  display: flex;
  flex-direction: column;
  padding: 20px;
  margin: 0;
}

.content-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.upload-section {
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.upload-section h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 1.5em;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.image-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.image-section h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 1.1em;
  font-weight: bold;
}

.fixed-notice {
  background-color: #ffe6e6;
  border: 1px solid #ffcccc;
  padding: 15px;
  border-radius: 5px;
  text-align: center;
}

.fixed-notice p {
  margin: 0;
  color: #cc0000;
  font-weight: bold;
}

.gallery-section {
  margin-top: 30px;
}

.gallery-section h3 {
  color: #333;
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 10px;
}

.section-description {
  color: #666;
  margin-bottom: 20px;
  line-height: 1.6;
}

.gallery-images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.gallery-image-item {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 15px;
}

.gallery-image-item h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-weight: bold;
  text-align: center;
}

.current-image-preview {
  position: relative;
  text-align: center;
  margin-bottom: 15px;
}

.current-image-preview img {
  max-width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.current-image-preview .label {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: rgba(0, 123, 255, 0.8);
  color: white;
  padding: 2px 8px;
  border-radius: 3px;
  font-size: 0.75em;
  font-weight: bold;
}

.upload-controls {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.upload-btn,
.confirm-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.9em;
  transition: background-color 0.3s ease;
}

.upload-btn {
  background-color: #007bff;
  color: white;
}

.upload-btn:hover {
  background-color: #0056b3;
}

.upload-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.confirm-btn {
  background-color: #28a745;
  color: white;
}

.confirm-btn:hover:not(:disabled) {
  background-color: #218838;
}

.confirm-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.preview-box {
  margin-top: 10px;
  text-align: center;
}

.preview-box img {
  max-width: 100%;
  max-height: 80px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message {
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  font-weight: bold;
  margin-top: 20px;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  position: absolute;
  left: 90px;
  top: 180px;
}

.back-button:hover {
  color: #0056b3;
  background-color: #e9ecef;
}

@media (max-width: 768px) {
  .gallery-images-grid {
    grid-template-columns: 1fr;
  }
}
</style>
