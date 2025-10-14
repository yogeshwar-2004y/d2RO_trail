<template>
  <div class="customise-background-page">
    <div class="header">
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
    </div>

    <div class="content-container">
      <div class="upload-section">
        <h2>Customise Login Background</h2>
        <p>
          Upload a new background image for the login page. Supported formats:
          PNG, JPG, JPEG
        </p>

        <div class="current-background">
          <h3>Current Background:</h3>
          <div class="background-preview">
            <img :src="currentBackgroundUrl" alt="Current Background" />
          </div>
        </div>

        <div
          class="upload-area"
          @click="triggerFileInput"
          @dragover.prevent
          @drop.prevent="handleDrop"
        >
          <input
            ref="fileInput"
            type="file"
            accept="image/png,image/jpg,image/jpeg"
            @change="handleFileSelect"
            style="display: none"
          />
          <div class="upload-content">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="48"
              height="48"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <circle cx="9" cy="9" r="2"></circle>
              <path d="M21 15l-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
            </svg>
            <p>Click to select an image or drag and drop</p>
            <span class="file-requirements"
              >Max size: 10MB | PNG, JPG, JPEG</span
            >
          </div>
        </div>

        <div v-if="selectedFile" class="selected-file">
          <h3>Selected File:</h3>
          <div class="file-info">
            <span>{{ selectedFile.name }}</span>
            <span>{{ formatFileSize(selectedFile.size) }}</span>
          </div>
          <div class="preview-container" v-if="previewUrl">
            <img :src="previewUrl" alt="Preview" class="preview-image" />
          </div>
        </div>

        <div class="action-buttons">
          <button
            @click="uploadBackground"
            :disabled="!selectedFile || uploading"
            class="upload-button"
          >
            <span v-if="uploading">Uploading...</span>
            <span v-else>Upload Background</span>
          </button>
          <button @click="resetToDefault" class="reset-button">
            Reset to Default
          </button>
        </div>

        <div v-if="message" :class="['message', messageType]">
          {{ message }}
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
      selectedFile: null,
      previewUrl: null,
      uploading: false,
      message: "",
      messageType: "success",
      currentBackgroundUrl: "/src/assets/images/login-background.png",
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    handleFileSelect(event) {
      const file = event.target.files[0];
      this.processFile(file);
    },

    handleDrop(event) {
      const file = event.dataTransfer.files[0];
      this.processFile(file);
    },

    processFile(file) {
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

      this.selectedFile = file;
      this.createPreview(file);
    },

    createPreview(file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.previewUrl = e.target.result;
      };
      reader.readAsDataURL(file);
    },

    async uploadBackground() {
      if (!this.selectedFile) return;

      this.uploading = true;
      this.message = "";

      const formData = new FormData();
      formData.append("background_image", this.selectedFile);

      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/upload-login-background",
          {
            method: "POST",
            body: formData,
          }
        );

        const data = await response.json();

        if (data.success) {
          this.showMessage("Background uploaded successfully!", "success");
          this.currentBackgroundUrl = data.background_url;
          this.selectedFile = null;
          this.previewUrl = null;
          this.$refs.fileInput.value = "";
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
        this.uploading = false;
      }
    },

    async resetToDefault() {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/reset-login-background",
          {
            method: "POST",
          }
        );

        const data = await response.json();

        if (data.success) {
          this.showMessage(
            "Background reset to default successfully!",
            "success"
          );
          this.currentBackgroundUrl = "/src/assets/images/login-background.png";
        } else {
          this.showMessage(
            data.message || "Reset failed. Please try again.",
            "error"
          );
        }
      } catch (error) {
        console.error("Reset error:", error);
        this.showMessage("Network error. Please try again.", "error");
      }
    },

    formatFileSize(bytes) {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const sizes = ["Bytes", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    },

    showMessage(text, type) {
      this.message = text;
      this.messageType = type;
      setTimeout(() => {
        this.message = "";
      }, 8000);
    },
  },

  async mounted() {
    // Load current background on component mount
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/get-current-background"
      );
      const data = await response.json();
      if (data.success && data.background_url) {
        this.currentBackgroundUrl = data.background_url;
      }
    } catch (error) {
      console.error("Error loading current background:", error);
    }
  },
};
</script>

<style scoped>
.customise-background-page {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f0f0f0;
}

.header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  padding: 20px 30px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 20px;
}
</style>

