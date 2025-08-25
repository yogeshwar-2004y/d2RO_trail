<template>
  <div class="pdf-viewer-container">
    <!-- Static Top Nav Bar -->
    <div class="top-nav">
      <input type="file" accept=".pdf,.docx" @change="handleFileUpload" />

      <template v-if="fileType">
        <button @click="zoomOut">-</button>
        <span>Zoom: {{ (zoom * 100).toFixed(0) }}%</span>
        <button @click="zoomIn">+</button>

        <template v-if="fileType === 'pdf'">
          <button @click="prevPage" :disabled="page <= 1">Prev</button>
          <span>Page</span>
          <input
            type="number"
            v-model.number="page"
            @keyup.enter="goToPage"
            min="1"
            :max="numPages"
            style="width: 60px"
          />
          <span>/ {{ numPages }}</span>
          <button @click="nextPage" :disabled="page >= numPages">Next</button>
        </template>

        <span class="file-name">{{ fileName }}</span>
      </template>
    </div>

    <!-- Content Area -->
    <div class="content">
      <!-- PDF Viewer -->
      <div
        v-if="fileType === 'pdf' && pdfUrl"
        class="doc-container"
        ref="pdfScroll"
        @scroll="onScroll"
      >
        <vue-pdf-embed
          v-for="p in numPages"
          :key="p"
          :source="pdfUrl"
          :page="p"
          :scale="zoom"
          ref="pdfPages"
          class="pdf-page"
        />
      </div>

      <!-- DOCX Viewer -->
      <div
        v-if="fileType === 'docx'"
        v-html="docxHtml"
        class="doc-container docx-content"
        :style="{ fontSize: zoom * 16 + 'px' }"
      ></div>

      <!-- Empty state -->
      <p v-if="!fileType" class="empty-msg">No file loaded.</p>

      <!-- Sidebar -->
      <aside class="sidebar">
        <h3>Comments</h3>
        <ul class="comments">
          <li v-for="(comment, index) in comments" :key="index">
            {{ comment }}
            <button @click="removeComment(index)">✕</button>
          </li>
        </ul>
        <div class="add-comment">
          <input
            type="text"
            v-model="newComment"
            placeholder="Add comment..."
            @keyup.enter="addComment"
          />
          <button @click="addComment">Add</button>
        </div>
      </aside>
    </div>
  </div>
</template>

<script>
import VuePdfEmbed from "vue-pdf-embed"
import * as mammoth from "mammoth/mammoth.browser"
import * as pdfjsLib from "pdfjs-dist/legacy/build/pdf"

// Tell pdf.js where the worker is (local, no CDN!)
import pdfjsWorker from "pdfjs-dist/legacy/build/pdf.worker?url"
pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker

export default {
  components: { VuePdfEmbed },
  data() {
    return {
      fileType: null,
      pdfUrl: null,
      docxHtml: "",
      page: 1,
      numPages: 0,
      zoom: 1.0,
      comments: [],
      newComment: "",
      fileName: "",
    }
  },
  methods: {
    goToPage() {
      if (this.page >= 1 && this.page <= this.numPages) {
        this.scrollToPage(this.page)
      } else {
        alert(`Enter a page between 1 and ${this.numPages}`)
      }
    },

    handleFileUpload(event) {
      const file = event.target.files?.[0]
      if (!file) return

      this.fileName = file.name
      this.clearDocument()

      const fileType = file.type
      if (fileType === "application/pdf") {
        this.fileType = "pdf"
        this.loadPdf(file)
      } else if (
        fileType ===
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      ) {
        this.fileType = "docx"
        this.loadDocx(file)
      } else {
        alert("Unsupported file type. Please upload a PDF or DOCX file.")
      }
    },

    async loadPdf(file) {
      if (this.pdfUrl) {
        URL.revokeObjectURL(this.pdfUrl)
      }
      this.pdfUrl = URL.createObjectURL(file)
      this.page = 1

      try {
        const loadingTask = pdfjsLib.getDocument(this.pdfUrl)
        const pdf = await loadingTask.promise
        this.numPages = pdf.numPages
      } catch (err) {
        console.error("Failed to load PDF metadata", err)
      }
    },

    async loadDocx(file) {
      try {
        const arrayBuffer = await file.arrayBuffer()
        const result = await mammoth.convertToHtml({ arrayBuffer })
        this.docxHtml = result.value
      } catch (err) {
        alert("Failed to render DOCX file.")
        console.error(err)
      }
    },

    zoomIn() {
      this.zoom += 0.1
    },
    zoomOut() {
      if (this.zoom > 0.3) this.zoom -= 0.1
    },

    nextPage() {
      if (this.page < this.numPages) {
        this.page++
        this.scrollToPage(this.page)
      }
    },
    prevPage() {
      if (this.page > 1) {
        this.page--
        this.scrollToPage(this.page)
      }
    },

    scrollToPage(pageNum) {
      this.$nextTick(() => {
        const pageEl = this.$refs.pdfPages[pageNum - 1]?.$el
        if (pageEl) {
          pageEl.scrollIntoView({ behavior: "smooth", block: "start" })
        }
      })
    },

    onScroll() {
      if (this.fileType !== "pdf") return
      const pages = this.$refs.pdfPages
      if (!pages || !pages.length) return

      let currentPage = 1
      const containerTop = this.$refs.pdfScroll.scrollTop

      pages.forEach((page, idx) => {
        const el = page.$el
        const offset = el.offsetTop - containerTop
        if (offset <= 50) {
          currentPage = idx + 1
        }
      })

      this.page = currentPage
    },

    addComment() {
      if (this.newComment.trim()) {
        this.comments.push(this.newComment.trim())
        this.newComment = ""
      }
    },
    removeComment(index) {
      this.comments.splice(index, 1)
    },

    clearDocument() {
      this.pdfUrl && URL.revokeObjectURL(this.pdfUrl)
      this.pdfUrl = null
      this.docxHtml = ""
      this.page = 1
      this.numPages = 0
      this.zoom = 1.0
      this.fileType = null
    },
  },
  beforeUnmount() {
    if (this.pdfUrl) {
      URL.revokeObjectURL(this.pdfUrl)
    }
  },
}
</script>

<style scoped>
.top-nav {
  position: sticky;
  top: 0;
  z-index: 10;
  background: #f9f9f9;
  border-bottom: 1px solid #ccc;
  padding: 0.75rem;
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.top-nav input[type="file"] {
  margin-right: 1rem;
}

.top-nav .file-name {
  margin-left: auto;
  font-weight: bold;
  color: #555;
}

.pdf-viewer-container {
  font-family: Arial, sans-serif;
  padding: 0;
}

.content {
  display: flex;
  gap: 3rem;
  padding: 1rem;
}

.doc-container {
  flex: 3;
  border: 1px solid #ccc;
  padding: 1rem;
  background: white;
  max-width: 950px;
  max-height: 1000px;
  overflow-y: auto;
}

.pdf-page {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  border: 1px solid #ddd;
  margin-bottom: 1rem;
}

.docx-content {
  white-space: pre-wrap;
  line-height: 1.6;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  color: #222;
}

.docx-content h1,
.docx-content h2,
.docx-content h3 {
  margin: 1rem 0 0.5rem;
  font-weight: bold;
}

.docx-content p {
  margin: 0.5rem 0;
}

/* .empty-msg {
  color: #777;
  font-style: italic;
} */

.empty-msg[data-v-a62cf7c1] {
    color: #888;                      /* Slightly softer gray */
    font-style: italic;
    font-size: 1.1rem;                /* Slightly larger for readability */
    text-align: center;              /* Center align the message */
    padding: 3rem 18rem;              /* More balanced vertical and horizontal padding */
    background-color: #f9f9f9;       /* Light background for better contrast */
    border-radius: 8px;              /* Rounded corners */
    border: 1px dashed #ccc;         /* Optional: visual separation */
    max-width: 600px;                /* Prevent it from stretching too wide */
    margin: 2rem auto;               /* Center horizontally with spacing around */
    line-height: 1.6;                /* Improve readability */
}


.sidebar {
  flex: 1;
  border-left: 1px solid #ccc;
  padding-left: 1rem;
}

.sidebar h3 {
  margin-bottom: 0.5rem;
}

.comments {
  list-style: none;
  padding: 0;
}

.comments li {
  background: #f5f5f5;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  position: relative;
}

.comments li button {
  position: absolute;
  right: 0.5rem;
  top: 0.5rem;
  background: transparent;
  border: none;
  color: red;
  cursor: pointer;
}

.add-comment {
  margin-top: 1rem;
  display: flex;
  gap: 0.5rem;
}

.add-comment input {
  flex: 1;
  padding: 0.3rem;
  border: 1px solid #ccc;
}

.add-comment button {
  padding: 0.3rem 0.6rem;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
