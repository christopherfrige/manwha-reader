<template>
  <v-layout>
    <v-app-bar-nav-icon
      variant="text"
      class="expand-button"
      @click.stop="drawer = !drawer"
    ></v-app-bar-nav-icon>

    <v-navigation-drawer v-model="drawer" class="menu">
      <v-list>
        <v-list-item @click="navigateToHome()">
          <v-list-item-title> <v-icon icon="mdi-home"></v-icon> Início </v-list-item-title>
        </v-list-item>
        <v-divider />
        <v-list-item @click="navigateToAdmin()">
          <v-list-item-title>
            <v-icon icon="mdi-cog"></v-icon> Gerenciar Manwhas
          </v-list-item-title>
        </v-list-item>
        <v-divider />
      </v-list>
    </v-navigation-drawer>
  </v-layout>
</template>
<script>
export default {
  data: () => ({
    drawer: false,
  }),

  watch: {
    group() {
      this.drawer = false;
    },
  },
  methods: {
    async navigateToHome() {
      return navigateTo({
        path: `/`,
      });
    },
    async navigateToAdmin() {
      return navigateTo({
        path: `/admin`,
      });
    },
  },
};
</script>
<style scoped>
.expand-button {
  font-size: 2rem;
}
.menu {
  background-color: #181828;
  color: #ccc;
}
</style>
