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
            src="@/assets/images/Airforce_1.jpg"
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
              <div class="login-reset-row">
                <button @click="login" class="action-button1">LOGIN</button>
                <button @click="resetPassword" class="action-button2">
                  FORGOT PASSWORD
                </button>
              </div>
              <button @click="techSupport" class="action-button">
                TECH SUPPORT
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Row of Five Images - Full Width -->
      <div class="image-gallery">
        <img
          src="@/assets/images/Image3.png"
          alt="Missile Launch"
          class="gallery-image"
        />
        <!-- Add radar array image path here -->
        <img
          src="@/assets/images/Image5.jpg"
          alt="Radar Array"
          class="gallery-image"
        />
        <!-- Add Tejas fighter image path here -->
        <img
          src="@/assets/images/Image4.jpg"
          alt="Tejas Fighter"
          class="gallery-image"
        />
        <!-- Add Mirage fighter image path here -->
        <img
          src="@/assets/images/Image2.png"
          alt="Mirage Fighter"
          class="gallery-image"
        />
        <!-- Add industrial machinery image path here -->
        <img
          src="@/assets/images/Image1.png"
          alt="Industrial Machinery"
          class="gallery-image"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { setUser } from "@/stores/userStore";

export default {
  name: "LoginPage",
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
      // Navigate to tech support page
      this.$router.push({ name: "TechSupport" });
    },
  },
};
</script>

<style scoped>
.login-page {
  height: calc(
    100vh - 120px
  ); /* Account for header (~60px) and news ticker + footer (~60px) */
  width: 100%; /* Take full width */
  display: flex;
  flex-direction: column;
  font-family: Arial, sans-serif;
  background-color: #f0f8ff; /* Very light blue background */
  margin: 0;
  padding: 0;
  overflow: hidden; /* Prevent scrolling */
}

.main-content {
  flex: 1; /* Take all available space */
  display: flex;
  flex-direction: column;
  padding: 0; /* Remove padding to eliminate white space */
  gap: 0; /* Remove gap */
  margin: 0;
  height: 100%;
}

/* Top Section - Fighter Jet and Login Form Side by Side */
.top-section {
  display: flex;
  gap: 1; /* Remove gap */
  align-items: flex-start;
  margin: 0;
  padding: 0;
}

/* Fighter Jet Image Container */
.main-image-container {
  flex: 2;
  height: 338px; /* Reduced to make room for gallery */
  overflow: hidden;
  border-radius: 0; /* Remove border radius */
  box-shadow: none; /* Remove shadow */
  margin: 0;
  padding: 0;
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
  min-height: 350px; /* Reduced to match image height */
  padding: 10px; /* Add padding only to login section */
}

.login-container {
  width: 100%;
  max-width: 450px; /* Increased from 350px */
  padding: 50px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* Image Gallery - Full Width */
.image-gallery {
  display: flex;
  justify-content: space-between;
  gap: 7px; /* Reduced gap to give more space to images */
  width: 100%;
  height: 170px; /* Adjusted height to ensure all 5 images fit */
  flex-shrink: 2; /* Prevent shrinking */
}

.gallery-image {
  flex: 2;
  height: 100%; /* Use full height of gallery container */
  object-fit: cover; /* Ensures complete image fits within container, crops if necessary */
  object-position: center; /* Centers the image within the container */
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  min-width: 10px; /* Allow images to shrink if needed */
}
/* .gallery-image:hover {
  transform: scale(1.05);
}
 */

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
  border-color: #01050a;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.login-reset-row {
  display: flex;
  gap: 10px; /* Reduced gap for better spacing */
}

.action-button1,
.action-button2,
.action-button {
  flex: 1; /* Make all buttons equal width */
  padding: 12px 20px; /* Increased padding for better size */
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
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
  .login-page {
    height: calc(100vh - 140px); /* Account for larger header on tablet */
  }

  .top-section {
    flex-direction: column;
    gap: 0;
  }

  .main-image-container {
    height: 250px; /* Reduced for tablet */
  }

  .login-section {
    min-height: auto;
    padding: 15px;
  }

  .image-gallery {
    height: 150px; /* Reduced for tablet but still fits all 5 images */
    gap: 4px; /* Smaller gap for tablet */
  }

  .gallery-image {
    flex: 1 1 calc(50% - 4px);
    min-width: 150px;
  }
}

@media (max-width: 768px) {
  .login-page {
    height: calc(100vh - 160px); /* Account for stacked header on mobile */
  }

  .main-content {
    padding: 0;
  }

  .main-image-container {
    height: 200px; /* Reduced for mobile */
  }

  .login-container {
    padding: 20px;
  }

  .image-gallery {
    height: 120px; /* Reduced for mobile but still fits all 5 images */
    gap: 3px; /* Smaller gap for mobile */
  }

  .gallery-image {
    flex: 1 1 100%;
  }
}
</style>
