<template>
  <div class="navbar-bg">
    <div class="container">
      <v-row class="mb-8 navbar px-3">
        <v-col cols="3" class="mt-2">
          <h1 @click="navigateToHome()">Manwha Reader</h1>
        </v-col>
        <v-col cols="5" class="mt-2 d-none d-md-flex">
          <v-btn variant="text" @click="navigateToHome()"> Início </v-btn>
          <v-btn variant="text"> Manwhas </v-btn>
        </v-col>
        <v-col cols="4" class="mt-2">
          <v-row>
            <v-col>
              <UiSearchBar class="d-none d-md-flex" />
              <LayoutMobileMenu class="d-md-none" />
              <v-app-bar-nav-icon v-if="false"></v-app-bar-nav-icon>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    async navigateToHome() {
      return navigateTo({
        path: `/`,
      });
    },
  },
};
</script>

<style scoped>
h1 {
  cursor: pointer;
  display: inline;
  font-size: 36px;
}

.navbar-bg {
  background-color: #181828;
}

.navbar {
  justify-content: space-between;
  align-items: center;
}

.container {
  width: 100%;
  margin-right: auto;
  margin-left: auto;
}

@media (max-width: 1200px) {
  .container {
    max-width: 1200px;
  }
}

@media (max-width: 1440px) {
  .container {
    max-width: 100% !important;
    width: 100% !important;
  }
}

@media (min-width: 1440px) {
  .container {
    max-width: 1440px;
  }
}
</style>
