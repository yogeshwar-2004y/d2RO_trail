<script setup>
import { RouterLink, RouterView, useRoute } from "vue-router";
import { computed } from "vue";
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
import NewsTicker from "@/components/NewsTicker.vue";
import BreadcrumbNavigation from "@/components/BreadcrumbNavigation.vue";
import AppSidebar from "@/components/AppSidebar.vue";

const route = useRoute();

// Show sidebar on all pages except login and tech support form
const showSidebar = computed(() => {
  return route.name !== "login" && route.name !== "TechSupport";
});
</script>

<template>
  <div id="app">
    <AppSidebar v-if="showSidebar" />
    <AppHeader />
    <BreadcrumbNavigation />
    <main
      class="main-content"
      :class="{
        'with-sidebar': showSidebar,
        'compact-header-margin': !isLoginOrDashboard,
      }"
    >
      <RouterView />
    </main>
    <NewsTicker
      height="50px"
      backgroundColor="#2c3e50"
      textColor="#ffffff"
      class="app-news-ticker"
    />
    <AppFooter class="app-footer" />
  </div>
</template>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  margin-left: 17px;
}

/* Fixed Header */
.app-header {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 1002 !important; /* Highest z-index */
  width: 100% !important;
}

.main-content {
  flex: 1;
  overflow-y: auto; /* Allow vertical scrolling for other pages */
  overflow-x: hidden;
  min-height: 0; /* Allow flex item to shrink */
  margin-top: 234px; /* Account for header (184px) + breadcrumb (50px) - default for login/dashboard */
  margin-bottom: 90px; /* Height of news ticker + footer */
  transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Compact header margin for non-login and non-dashboard pages */
.main-content.compact-header-margin {
  margin-top: 144px; /* Account for compact header (94px/2.5cm) + breadcrumb (50px) */
}

/* Fixed News Ticker */
.app-news-ticker {
  position: fixed !important;
  bottom: 20px !important; /* Reduced gap from 40px to 20px */
  left: 0 !important;
  right: 0 !important;
  z-index: 1001 !important; /* Higher than footer to ensure it's visible */
  width: 100% !important;
}

/* Override NewsTicker internal positioning */
.app-news-ticker .news-ticker-container {
  position: relative !important;
}

/* Fixed Footer */
.app-footer {
  position: fixed !important;
  bottom: 0 !important; /* Position at very bottom */
  left: 0 !important;
  right: 0 !important;
  z-index: 1000 !important;
  width: 100% !important;
}

/* Special handling for login page - no scrolling */
.login-page {
  overflow: hidden !important;
  height: 100vh !important;
}

.login-page .main-content {
  margin-top: 0;
  margin-bottom: 0;
  overflow: hidden !important; /* Prevent scrolling on login page */
  height: 100vh; /* Full viewport height */
}

/* Ensure no scrolling anywhere within login page */
.login-page * {
  overflow: hidden !important;
}

/* Special handling for tech support page */
.tech-support-page {
  margin-top: 0 !important;
  margin-bottom: 0 !important;
}

/* Special handling for dashboard pages - no scrolling */
.home-page,
.designer-home,
.home-page-container {
  overflow: hidden !important;
  height: calc(
    100vh - 310px
  ) !important; /* Account for header (170px), breadcrumb (50px), and news ticker + footer (90px) */
}

.home-page .main-content,
.designer-home .main-content,
.home-page-container .main-content {
  margin-top: 0;
  margin-bottom: 0;
  overflow: hidden !important; /* Prevent scrolling on dashboard pages */
  height: 100%;
}

/* Ensure no scrolling anywhere within dashboard pages */
.home-page *,
.designer-home *,
.home-page-container * {
  overflow: hidden !important;
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
