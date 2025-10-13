<template>
  <div class="login-page">
    <!-- Main Content Area -->
    <div class="main-content">
      <!-- Fighter Jet Image and Login Form Side by Side -->
      <div class="top-section">
        <!-- Fighter Jet Image -->
        <div class="main-image-container">
          <!-- Add main fighter jet image path here -->
          <img 
            src="" 
            alt="Fighter Jet with Indian Flag" 
            class="main-image"
          />
        </div>
        
        <!-- Login Form -->
        <div class="login-section">
          <div class="login-container">
            <div class="input-group">
              <input
                type="text"
                v-model="email"
                placeholder="Username/Email"
                class="input-field"
              />
            </div>

            <div class="input-group">
              <input
                type="password"
                v-model="password"
                placeholder="Password"
                class="input-field"
              />
            </div>

            <div class="button-group">
              <button @click="login" class="action-button">LOGIN</button>
              <button @click="resetPassword" class="action-button">RESET PASSWORD</button>
              <button @click="techSupport" class="action-button">TECH SUPPORT</button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Row of Five Images - Full Width -->
      <div class="image-gallery">
        <!-- Add missile launch image path here -->
        <img 
          src="" 
          alt="Missile Launch" 
          class="gallery-image"
        />
        <!-- Add radar array image path here -->
        <img 
          src="" 
          alt="Radar Array" 
          class="gallery-image"
        />
        <!-- Add Tejas fighter image path here -->
        <img 
          src="" 
          alt="Tejas Fighter" 
          class="gallery-image"
        />
        <!-- Add Mirage fighter image path here -->
        <img 
          src="" 
          alt="Mirage Fighter" 
          class="gallery-image"
        />
        <!-- Add industrial machinery image path here -->
        <img 
          src="" 
          alt="Industrial Machinery" 
          class="gallery-image"
        />
      </div>
    </div>
    
    <!-- News Ticker -->
    <NewsTicker
      height="60px"
      backgroundColor="#2c3e50"
      textColor="#ffffff"
      class="login-news-ticker"
    />
  </div>
</template>

<script>
import { setUser } from "@/stores/userStore";
import NewsTicker from "@/components/NewsTicker.vue";

export default {
  name: "LoginPage",
  components: {
    NewsTicker,
  },
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async login() {
      if (!this.email || !this.password) {
        alert("Please enter your email and password.");
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:8000/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
          mode: "cors", // ✅
        });

        //console.log('avanthika');

        const data = await response.json();

        if (data.success) {
          console.log("Login successful:", data.user);
          alert(`Welcome ${data.user.name} (${data.user.role})`);

          // Store user data in global state
          setUser(data.user);

          // Role-based navigation - handle exact role names from database
          const role = data.user.role.toLowerCase();

          if (role === "admin") {
            this.$router.push({ name: "HomePageAdmin" });
          } else if (role === "qa reviewer") {
            this.$router.push({ name: "HomePageReviewer" });
          } else if (role === "qa head") {
            this.$router.push({ name: "HomePageQAHead" });
          } else if (role === "design head") {
            this.$router.push({ name: "HomePageDesignHead" });
          } else if (role === "designer") {
            this.$router.push({ name: "HomePageDesigner" });
          } else {
            console.error("Unknown role:", data.user.role);
            alert(`Unknown role: ${data.user.role}. Please contact support.`);
          }
        } else {
          alert(data.message);
        }
      } catch (err) {
        console.error("Login error:", err);
        alert("Server error. Please try again later.");
      }
    },

    resetPassword() {
      // Add reset password functionality
      alert("Reset password functionality will be implemented");
    },

    techSupport() {
      // Add tech support functionality
      alert("Tech support functionality will be implemented");
    },
  },
};
</script>

<style scoped>
.login-page {
  flex: 1;
  display: flex;
  flex-direction: column;
  font-family: Arial, sans-serif;
  background-color: #f0f8ff; /* Very light blue background */
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 20px;
}

/* Top Section - Fighter Jet and Login Form Side by Side */
.top-section {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

/* Fighter Jet Image Container */
.main-image-container {
  flex: 2;
  height: 350px;
  overflow: hidden;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Ensures complete image fits within container, crops if necessary */
  object-position: center; /* Centers the image within the container */
}

/* Login Form Section */
.login-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 350px;
}

.login-container {
  width: 100%;
  max-width: 350px;
  padding: 30px;
  background: #fff;
  border-radius: 15px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* Image Gallery - Full Width */
.image-gallery {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  width: 100%;
}

.gallery-image {
  flex: 1;
  height: 120px;
  object-fit: cover; /* Ensures complete image fits within container, crops if necessary */
  object-position: center; /* Centers the image within the container */
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.gallery-image:hover {
  transform: scale(1.05);
}

.login-news-ticker {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

/* Login Form */
.login-container {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  background: #fff;
  border-radius: 15px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 20px;
}

.input-field {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.input-field:focus {
  border-color: #007bff;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.action-button {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  background-color: #162845;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.action-button:hover {
  background-color: #51759a;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .top-section {
    flex-direction: column;
    gap: 20px;
  }
  
  .main-image-container {
    height: 300px;
  }
  
  .login-section {
    min-height: auto;
  }
  
  .image-gallery {
    flex-wrap: wrap;
  }
  
  .gallery-image {
    flex: 1 1 calc(50% - 5px);
    min-width: 150px;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 10px;
  }
  
  .main-image-container {
    height: 250px;
  }
  
  .login-container {
    padding: 20px;
  }
  
  .gallery-image {
    flex: 1 1 100%;
    height: 100px;
  }
}
</style>
