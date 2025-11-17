<script setup>
import { RouterView, useRoute } from "vue-router";
import { computed, ref } from "vue";
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
import NewsTicker from "@/components/NewsTicker.vue";
import BreadcrumbNavigation from "@/components/BreadcrumbNavigation.vue";
import AppSidebar from "@/components/AppSidebar.vue";
import NotificationsOverlay from "@/components/NotificationsOverlay.vue";

const route = useRoute();

// Notifications state
const isNotificationsOpen = ref(false);

// Sidebar state
const isSidebarCollapsed = ref(true); // Default to collapsed

// Show sidebar on all pages except login and tech support form
const showSidebar = computed(() => {
  return route.name !== "login" && route.name !== "TechSupport";
});

// Computed sidebar width based on collapsed state
const sidebarWidth = computed(() => {
  if (!showSidebar.value) return 0;
  return isSidebarCollapsed.value ? 50 : 250;
});

// Handle sidebar state changes
const handleSidebarStateChanged = (collapsed) => {
  isSidebarCollapsed.value = collapsed;
};

// Handle notifications
const handleOpenNotifications = () => {
  isNotificationsOpen.value = true;
};

const closeNotifications = () => {
  isNotificationsOpen.value = false;
};
</script>

<template>
  <div 
    id="app" 
    :style="{ '--sidebar-width': `${sidebarWidth}px` }"
  >
    <AppSidebar 
      v-if="showSidebar" 
      @open-notifications="handleOpenNotifications"
      @sidebar-state-changed="handleSidebarStateChanged"
    />
    <AppHeader class="app-header-responsive" />
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
      height="30px"
      backgroundColor="#2c3e50"
      textColor="#ffffff"
      class="app-news-ticker app-news-ticker-responsive"
    />
    <AppFooter class="app-footer app-footer-responsive" />
    
    <!-- Notifications Overlay - rendered at app level -->
    <NotificationsOverlay 
      :isOpen="isNotificationsOpen"
      @close="closeNotifications"
    />
  </div>
</template>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
}

/* Fixed Header */
.app-header {
  position: fixed !important;
  top: 0 !important;
  left: var(--sidebar-width, 0) !important;
  right: 0 !important;
  z-index: 1002 !important; /* Highest z-index */
  width: calc(100% - var(--sidebar-width, 0)) !important;
}

.app-header-responsive {
  transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1), width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.main-content {
  flex: 1;
  overflow-y: auto; /* Allow vertical scrolling for other pages */
  overflow-x: hidden;
  min-height: 0; /* Allow flex item to shrink */
  margin-top: 234px; /* Account for header (184px) + breadcrumb (50px) - default for login/dashboard */
  margin-bottom: 90px; /* Height of news ticker + footer */
  margin-left: var(--sidebar-width, 0);
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
  left: var(--sidebar-width, 0) !important;
  right: 0 !important;
  z-index: 1001 !important; /* Higher than footer to ensure it's visible */
  width: calc(100% - var(--sidebar-width, 0)) !important;
}

.app-news-ticker-responsive {
  transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1), width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Override NewsTicker internal positioning */
.app-news-ticker .news-ticker-container {
  position: relative !important;
}

/* Fixed Footer */
.app-footer {
  position: fixed !important;
  bottom: 0 !important; /* Position at very bottom */
  left: var(--sidebar-width, 0) !important;
  right: 0 !important;
  z-index: 1000 !important;
  width: calc(100% - var(--sidebar-width, 0)) !important;
}

.app-footer-responsive {
  transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1), width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
