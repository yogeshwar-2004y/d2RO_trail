<script setup>
import { RouterLink, RouterView } from "vue-router";
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
import NewsTicker from "@/components/NewsTicker.vue";
import BreadcrumbNavigation from "@/components/BreadcrumbNavigation.vue";
</script>

<template>
  <div id="app">
    <AppHeader />
    <BreadcrumbNavigation />
    <main class="main-content">
      <RouterView />
    </main>
    <NewsTicker
      height="50px"
      backgroundColor="#2c3e50"
      textColor="#ffffff"
      class="app-news-ticker"
    />
    <AppFooter />
  </div>
</template>

<style>
#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Prevent body scroll */
  margin: 0;
  padding: 0;
}

.main-content {
  flex: 1;
  overflow: hidden; /* Prevent scrolling */
  display: flex;
  flex-direction: column;
}

.app-news-ticker {
  flex-shrink: 0; /* Prevent shrinking */
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
    axios.get('http://127.0.0.1:5000/api')
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
