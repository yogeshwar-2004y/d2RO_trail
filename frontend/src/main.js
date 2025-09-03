import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { initializeUser } from './stores/userStore'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Initialize user state from localStorage
initializeUser()

app.mount('#app')
