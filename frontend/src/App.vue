<script setup>
import { RouterLink, RouterView } from "vue-router";
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
</script>

<template>
  <div id="app">
    <AppHeader />
    <main class="main-content">
      <RouterView />
    </main>
    <AppFooter />
  </div>
</template>

<style>
#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Prevent body scroll */
}

.main-content {
  flex: 1;
  overflow-y: auto; /* Allow scrolling only in main content */
  overflow-x: hidden;
}
</style>

<!-- simple flask connection -->
<!-- <template>
  <div id="app">
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      message: ''
    };
  },
  mounted() {
    axios.get('http://127.0.0.1:8000/api')
      .then(response => {
        this.message = response.data.message;
      })
      .catch(error => {
        console.error("There was an error!", error);
      });
  }
};
</script>

<style>
#app {
  text-align: center;
  color: #5595d4;
}
</style> -->
