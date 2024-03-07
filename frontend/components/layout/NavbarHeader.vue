<template>
  <div class="navbar-bg">
    <div class="container">
      <v-row class="mb-8 navbar justify-center
      ">
        <v-col cols="3" class="mt-2">
          <h1>Manwha Reader</h1>
        </v-col>
        <v-col cols="4" class="mt-2">
          <v-btn variant="text"> Início </v-btn>
          <v-btn variant="text"> Manwhas </v-btn>
        </v-col>
        <v-col cols="4" class="mt-2">
          <v-row>
            <v-col class="right-nav">
                <UiSearchBar/>
                <span class="search-button">Buscar</span>
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
  data() {
    return {};
  },
};
</script>

<style scoped>
.right-nav {
  display: flex;
  align-items: center;
}

.navbar-bg {
  background-color: #ffffff1a;
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
