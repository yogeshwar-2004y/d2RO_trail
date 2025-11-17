<template>
  <footer class="app-footer">
    <div class="footer-content">
      <p class="copyright-text">
        AVIATRAX™️ - Designed and Developed by VISTA Engg Solutions Private Ltd  © All Rights Reserved  |  www.vistaes.com  |  info@vistaes.com  
      </p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter'
}
</script>

<style scoped>
.app-footer {
  background-color: #ffffff;
  width: 100%;
  padding: 4px 0; /* Reduced from 20px */
  border-top: 0px solid #e0e0e0;
  margin-top: auto;
  flex-shrink: 0; /* Prevent shrinking */
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 10px;
  text-align: center;
}

.copyright-text {
  font-size: 0.7rem; /* Reduced from 0.9rem */
  color: #000;
  margin: 0;
  font-family: Arial, sans-serif;
}

/* Responsive design */
@media (max-width: 768px) {
  .copyright-text {
    font-size: 0.7rem; /* Reduced from 0.8rem */
  }
  
  .app-footer {
    padding: 5px 0; /* Further reduced for mobile */
  }
}
</style>
