<template>
  <footer class="app-footer">
    <div class="footer-content">
      <p class="copyright-text">
        AVIATRAX - Designed and Developed by VISTA Engineering Solutions Pvt Ltd © Copy Rights Reserved
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
  padding: 20px 0;
  border-top: 1px solid #e0e0e0;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  text-align: center;
}

.copyright-text {
  font-size: 0.9rem;
  color: #000;
  margin: 0;
  font-family: Arial, sans-serif;
}

/* Responsive design */
@media (max-width: 768px) {
  .copyright-text {
    font-size: 0.8rem;
  }
  
  .app-footer {
    padding: 15px 0;
  }
}
</style>
