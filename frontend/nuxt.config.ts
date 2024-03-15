export default defineNuxtConfig({
  components: {
    global: true,
    dirs: ['~/components'],
  },
  css: [
    'vuetify/lib/styles/main.sass',
    '@mdi/font/css/materialdesignicons.min.css',
    'assets/css/global.css',
  ],
  build: {
    transpile: ['vuetify'],
  },
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      apiBackendBaseUrl: process.env.API_BACKEND_BASE_URL || 'http://localhost:8000',
    },
  },
});
