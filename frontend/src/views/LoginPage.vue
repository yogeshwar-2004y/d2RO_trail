<template>
  <div class="login-page">
    <div
      class="login-left-panel"
      :style="{ backgroundImage: `url(${backgroundImageUrl})` }"
    ></div>
    <div class="login-right-panel">
      <div class="login-container">
        <div class="logos-container">
          <img
            src="@/assets/images/aviatrax-logo.png"
            alt="Aviatrax Logo"
            class="logo"
          />
          <img
            src="@/assets/images/vista_logo.png"
            alt="Vista Logo"
            class="logo vista-logo"
          />
        </div>

        <div class="input-group">
          <span class="input-icon">✉</span>
          <input
            type="text"
            v-model="email"
            placeholder="email id"
            class="input-field"
          />
        </div>

        <div class="input-group">
          <span class="input-icon">🔒</span>
          <input
            type="password"
            v-model="password"
            placeholder="password"
            class="input-field"
          />
        </div>

        <button @click="login" class="login-button">LOGIN</button>
      </div>
    </div>

    <div style="color: white">🚀 This is the news ticker!</div>
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
      backgroundImageUrl: "/src/assets/images/login-background.png",
    };
  },
  methods: {
    async login() {
      if (!this.email || !this.password) {
        alert("Please enter your email and password.");
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:5000/api/login", {
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

    async loadBackgroundImage() {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/get-current-background"
        );
        const data = await response.json();

        if (data.success && data.background_url) {
          this.backgroundImageUrl = data.background_url;
        }
      } catch (error) {
        console.error("Error loading background:", error);
        // Keep default background on error
      }
    },
  },

  async mounted() {
    await this.loadBackgroundImage();
  },
};
</script>

<style scoped>
.login-page {
  display: flex;
  height: 829px;
  width: 98vw;
  font-family: Arial, sans-serif;
  background-color: #f0f0f0;
}

.login-left-panel {
  flex: 1;
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

.logos-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 50px;
}

.logo {
  width: 180px;
}

.vista-logo {
  width: 150px;
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

.login-news-ticker {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}
</style>
