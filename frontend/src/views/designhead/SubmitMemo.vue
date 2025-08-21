<template>
  <div class="submit-memo-page">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
      <span class="page-title">SUBMIT NEW MEMO</span>
    </div>
    <div class="content">
      <h2>Memo Submission Form Coming Soon!</h2>
      <p>This page will contain the form for submitting new memos.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SubmitMemo',
};
</script>

<style scoped>
.submit-memo-page {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #f0f0f0;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
}
.header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 20px;
  width: 100%;
  max-width: 900px; /* Adjust as needed */
  margin-bottom: 30px;
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
  flex-grow: 1;
  text-align: center;
}
.content {
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 50px;
  text-align: center;
}
</style>