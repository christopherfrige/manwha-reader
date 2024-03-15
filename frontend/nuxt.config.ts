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
      apiUrl: 'http://localhost:8000',
      testEnv: process.env.TEST_ENV || 'TEST_DEFAULT',
    },
  },
});
