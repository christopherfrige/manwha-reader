<template>
  <div class="navbar-bg">
    <div class="container">
      <v-row class="mb-8 navbar">
        <v-col cols="10" md="3" class="my-4">
          <h1 @click="navigateToHome()">Manwha Reader</h1>
        </v-col>
        <v-col cols="0" md="5" class="mt-2 d-none d-md-flex">
          <ul>
            <li @click="navigateToHome()">INÍCIO</li>
            <li>MANWHAS</li>
          </ul>
        </v-col>
        <v-col cols="2" md="4" class="mt-2">
          <v-row>
            <v-col>
              <UiSearchBar class="d-none d-md-flex" />
              <LayoutMobileMenu class="d-md-none" />
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
  font-size: 34px;
}

h1:hover {
  transform: scale(2);
}

.navbar-bg {
  background: var(--nav-bg-color);
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

.v-row {
  margin: 0;
}

.v-col {
  padding: 0;
}

li {
  position: relative;
  display: inline-block;
  cursor: pointer;
  margin: 0 35px 0 0;
  font-size: 15px;
  transition: color 0.3s ease-in-out;
}
li:after {
  content: '';
  position: absolute;
  left: 50%;
  top: 100%;
  width: 0%;
  height: 3px;
  background-color: rgb(212, 186, 37);
  transition: all 0.3s ease-in-out;
  transform: translateX(-50%);
}
li:hover:after {
  width: 100%;
}
li:hover {
  color: rgb(212, 186, 37);
}
</style>
