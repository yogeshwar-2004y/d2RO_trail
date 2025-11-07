<template>
  <header class="app-header" :class="{ 'compact-header': !isLoginOrDashboard() }">
    <img :src="headerImage" alt="header-img" class="header-image" />
  </header>
</template>

<script>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import Header_HomePage from '@/assets/images/Header_HomePage.jpg'
import Header_AllPage from '@/assets/images/Header_AllPages.jpg'

export default {
  name: 'AppHeader',
  setup() {
    const route = useRoute()
    
    // Check if current route is login or dashboard pages
    const isLoginOrDashboard = () => {
      const routeName = route.name
      return routeName === 'login' || 
             routeName === 'HomePageAdmin' || 
             routeName === 'HomePageDesigner' || 
             routeName === 'HomePageQAHead' || 
             routeName === 'HomePageReviewer' || 
             routeName === 'HomePageDesignHead'
    }
    
    // Computed property to determine which header image to show
    const headerImage = computed(() => {
      if (isLoginOrDashboard()) {
        // Login page and all 5 dashboards: use current image (v3)
        return Header_HomePage
      } else {
        // All other pages: use new image (v4)
        return Header_AllPage
      }
    })
    
    return {
      isLoginOrDashboard,
      headerImage
    }
  }
}
</script>

<style scoped>
.app-header {
  background-color: #DDEFFD;
  width: 100%;
  padding: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin: 0;
}

/* Compact header for non-login and non-dashboard pages */
.app-header.compact-header {
  height: 2.5cm;
  padding: 3px 5px;
  display: flex;
  align-items: center;
}

.header-image {
  width: 100%;
  height: auto;
  display: block;
}

/* Compact header image */
.app-header.compact-header .header-image {
  height: 100%;
  width: 100%;
  object-fit: cover;
}

/* Responsive design */
@media (max-width: 768px) {
  .app-header {
    padding: 3px;
  }
  
  .app-header.compact-header {
    padding: 2px 3px;
  }
}
</style>
