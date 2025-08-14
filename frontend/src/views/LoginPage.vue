<template>
  <div class="login-page">
    <div class="login-left-panel">
      </div>
    <div class="login-right-panel">
      <div class="login-container">
        <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
        <div class="input-group">
          <span class="input-icon">✉</span>
          <input type="text" v-model="email" placeholder="email id" class="input-field">
        </div>
        <div class="input-group">
          <span class="input-icon">🔒</span>
          <input type="password" v-model="password" placeholder="password" class="input-field">
        </div>
        <button @click="login" class="login-button">LOGIN</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    login() {
      // Basic validation
      if (!this.email || !this.password) {
        alert('Please enter your email and password.');
        return;
      }
      
      // Here you will integrate with your Flask backend
      console.log('Attempting to log in with:', this.email, 'and password:', this.password);
      
      // A placeholder for API call
      // this.$http.post('/api/login', { email: this.email, password: this.password })
      //   .then(response => {
      //     const userRole = response.data.role;
      //     // Navigate to the correct home page based on the user's role
      //     this.$router.push({ name: `HomePage${userRole}` });
      //   })
      //   .catch(error => {
      //     alert('Login failed. Please check your credentials.');
      //   });
    },
  },
};
</script>

<style scoped>
.login-page {
  display: flex;
  height: 829px;
  width: 98vw;
  font-family: Arial, sans-serif;
  background-color: #f0f0f0; /* Match background color */
}

.login-left-panel {
  flex: 1;
  background-image: url('@/assets/images/login-background.png');
  background-size: cover;
  background-position: center;
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
  margin: 20px 0 20px 20px;
}

.login-right-panel {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-container {
  width: 350px;
  padding: 40px;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.logo {
  width: 180px; /* Adjust size as needed */
  margin-bottom: 50px;
}

.input-group {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 25px;
  padding: 5px 15px;
  background-color: #f5f5f5;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

.input-icon {
  font-size: 1.2em;
  color: #888;
  margin-right: 10px;
}

.input-field {
  flex: 1;
  border: none;
  background: transparent;
  padding: 10px 0;
  font-size: 1em;
  outline: none;
}

.login-button {
  width: 100%;
  padding: 15px;
  border: none;
  border-radius: 25px;
  font-size: 1.1em;
  color: #fff;
  background: linear-gradient(to right, #ccc, #888);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 20px;
}

.login-button:hover {
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}
</style>