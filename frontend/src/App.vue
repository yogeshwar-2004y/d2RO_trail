<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <RouterView />

</template>

<style scoped>

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

