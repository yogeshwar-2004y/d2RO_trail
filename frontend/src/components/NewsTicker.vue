<!-- <template>
  <div class="news-ticker-container" v-if="hasNews">
    <div class="news-ticker">
      <div class="news-content" :style="animationStyle">
        <span v-for="(newsItem, index) in displayNews" :key="index" class="news-item">
          📰 {{ newsItem.news_text }}
        </span>
      </div>
    </div>
  </div>
</template> -->

<template>
  <div
    class="news-ticker-container"
    v-if="hasNews || showWhenEmpty"
    :style="{ height, backgroundColor }"
  >
    <div class="news-ticker">
      <div class="news-content" :style="[animationStyle, { color: textColor }]">
        <span
          v-for="(newsItem, index) in displayNews"
          :key="index"
          class="news-item"
        >
          📰 {{ typeof newsItem === "string" ? newsItem : newsItem.news_text }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "NewsTicker",
  props: {
    height: {
      type: String,
      default: "50px",
    },
    speed: {
      type: Number,
      default: 30, // pixels per second
    },
    backgroundColor: {
      type: String,
      default: "#2c3e50",
    },
    textColor: {
      type: String,
      default: "#ffffff",
    },
    showWhenEmpty: {
      type: Boolean,
      default: true,
    },
    fallbackText: {
      type: String,
      default: "Welcome to Aviatrax",
    },
  },
  data() {
    return {
      news: [],
      animationDuration: 30, // seconds
      loading: false,
    };
  },
  computed: {
    hasNews() {
      return this.news.length > 0;
    },
    displayNews() {
      // Repeat news items for continuous scrolling; if empty and allowed, show fallback
      if (this.news.length > 0) {
        return [...this.news, ...this.news, ...this.news];
      }
      return this.showWhenEmpty ? [this.fallbackText, this.fallbackText] : [];
    },
    animationStyle() {
      return {
        animationDuration: `${this.animationDuration}s`,
        animationTimingFunction: "linear",
        animationIterationCount: "infinite",
      };
    },
  },
  async mounted() {
    await this.loadNews();
    // Refresh news every 30 seconds
    setInterval(this.loadNews, 30000);
  },
  methods: {
    async loadNews() {
      if (this.loading) return;

      this.loading = true;
      try {
        const response = await fetch("http://localhost:5000/api/news");
        const data = await response.json();

        if (data.success && data.news.length > 0) {
          this.news = data.news;
          console.log("Debugging News loaded:", this.news);

          this.calculateAnimationDuration();
        }
      } catch (error) {
        console.error("Error loading news:", error);
      } finally {
        this.loading = false;
      }
    },
    calculateAnimationDuration() {
      // Calculate animation duration based on content length and speed
      if (this.news.length > 0) {
        const totalContent = this.displayNews
          .map((item) => item.news_text)
          .join(" 📰 ");
        const contentLength = totalContent.length;
        // Remove character constraints - allow unlimited content length
        // Use speed prop to control animation: slower speed = longer duration
        // Base calculation: 1 second per 30 characters, adjusted by speed factor
        const baseDuration = Math.ceil(contentLength / 30);
        this.animationDuration = Math.max(
          20,
          baseDuration * (100 / this.speed)
        );
      }
    },
  },
};
</script>

<style scoped>
.news-ticker-container {
  width: 100%;
  overflow: hidden;
  position: relative;
  border-top: 0.8px solid #34495e;
  border-bottom: 0.8px solid #34495e;
  margin-left: 10px;
}

.news-ticker {
  height: 100%;
  display: flex;
  align-items: center;
  position: relative;
  padding-left: 50px;
}

.news-content {
  display: flex;
  align-items: center;
  white-space: nowrap;
  font-weight: 300;
  font-size: 16px;
  animation-name: scroll;
  transform: translateX(100%);
  /* Remove any width constraints to allow unlimited content */
  min-width: max-content;
}

.news-item {
  margin-right: 100px;
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

@keyframes scroll {
  0% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(-100%);
  }
}

@keyframes flash {
  0%,
  50% {
    opacity: 1;
  }
  25%,
  75% {
    opacity: 0.7;
  }
}

.news-ticker-container::before {
  content: "📰 NEWS";
  position: absolute;
  left: 33px;
  top: 0;
  height: 100%;
  background: linear-gradient(45deg, #e74c3c, #c0392b);
  color: white;
  padding: 0 15px;
  display: flex;
  align-items: center;
  font-weight: bold;
  font-size: 12px;
  animation: flash 2s infinite;
  z-index: 1;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.3);
}
</style>
