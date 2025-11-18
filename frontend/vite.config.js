import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    // Disable devtools in test environment to avoid conflicts
    process.env.NODE_ENV !== "test" && vueDevTools(),
  ].filter(Boolean),
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  optimizeDeps: {
    include: ["html2pdf.js"],
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
        secure: false,
      },
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./tests/setup.js"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html", "lcov", "junit"],
      reportsDirectory: "../reports/frontend/coverage",
      exclude: [
        "node_modules/",
        "dist/",
        "**/*.config.js",
        "**/*.config.ts",
        "cypress/",
        "tests/",
        "**/*.test.js",
        "**/*.spec.js",
      ],
      thresholds: {
        global: {
          branches: 70,
          functions: 70,
          lines: 70,
          statements: 70,
        },
      },
    },
    reporters: ["default", "junit"],
    outputFile: {
      junit: "../reports/frontend/junit.xml",
    },
  },
});
