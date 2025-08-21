<template>
  <div class="document-viewer-page">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
      <span class="page-title">DOCUMENT VIEWER</span>
    </div>

    <div class="viewer-container">
      <div class="document-panel">
        <div class="document-content">
          <img src="http://googleusercontent.com/file_content/2" alt="Document Preview" class="document-preview">
        </div>
      </div>

      <div class="comments-panel">
        <span class="panel-title">QA Comments & Design Team Feedback</span>
        <div class="comment-table-wrapper">
          <table>
            <thead>
              <tr>
                <th>BY</th>
                <th>PAGE NO</th>
                <th>PARA NO</th>
                <th>COMMENT</th>
                <th></th>
                <th>JUSTIFICATION</th>
                <th>NEW PAGE</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(comment, index) in comments" :key="index">
                <td>{{ comment.by }}</td>
                <td>{{ comment.pageNo }}</td>
                <td>{{ comment.paraNo }}</td>
                <td>{{ comment.comment }}</td>
                <td>
                  <div class="action-icons">
                    <svg class="accept-icon" @click="updateStatus(index, 'accepted')" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    <svg class="reject-icon" @click="updateStatus(index, 'rejected')" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="18" y1="6" x2="6" y2="18"></line>
                      <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                  </div>
                </td>
                <td>
                  <textarea v-model="comment.justification" :disabled="comment.status === 'accepted'" placeholder="Add justification"></textarea>
                </td>
                <td>
                  <input type="text" v-model="comment.newPage" placeholder="Page #">
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DocumentViewer',
  data() {
    return {
      documentId: this.$route.params.documentId,
      comments: [
        { by: 'Dr. A', pageNo: 2, paraNo: 1, comment: 'LOREM IPSUM DOLOR SIT AMET, CONSECTETU RADIPISCING ELIT', status: null, justification: '', newPage: '' },
        { by: 'Dr. B', pageNo: 5, paraNo: 2, comment: 'Comment on a different section.', status: null, justification: '', newPage: '' },
      ],
    };
  },
  methods: {
    updateStatus(index, status) {
      this.comments[index].status = status;
    },
  },
};
</script>

<style scoped>
.document-viewer-page {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #f0f0f0;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 20px;
  padding: 20px 30px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
}

.logo {
  width: 120px;
}

.page-title {
  font-size: 1.5em;
  font-weight: bold;
}

.viewer-container {
  display: flex;
  flex-grow: 1;
  padding: 30px;
  gap: 30px;
}

.document-panel {
  flex: 2;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: auto;
}

.document-content {
  padding: 20px;
}

.document-preview {
  width: 100%;
  height: auto;
}

.comments-panel {
  flex: 1;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.panel-title {
  font-size: 1.2em;
  font-weight: bold;
}

.comment-table-wrapper {
  width: 100%;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
}

th {
  background-color: #e8e8e8;
  font-weight: bold;
}

td:first-child, td:nth-child(2), td:nth-child(3) {
  text-align: center;
}

.action-icons {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.accept-icon, .reject-icon {
  cursor: pointer;
}

.accept-icon {
  color: #5cb85c;
}

.reject-icon {
  color: #ff4d4f;
}

textarea {
  width: 100%;
  height: 80px;
  resize: vertical;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 5px;
}

input[type="text"] {
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 5px;
}
</style>