<template>
  <v-layout class="justify-end">
    <v-app-bar-nav-icon
      variant="text"
      class="expand-button"
      @click.stop="drawer = !drawer"
    ></v-app-bar-nav-icon>

    <v-navigation-drawer v-model="drawer" class="menu">
      <v-list>
        <v-list-item @click="this.navigateToHome()">
          <v-list-item-title>
            <v-icon icon="mdi-home"></v-icon> Início
          </v-list-item-title>
        </v-list-item>
        <v-divider />
        <v-list-item>
          <v-list-item-title>
            <v-icon icon="mdi-book"></v-icon> Manwhas
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
  },
};
</script>
<style scoped>
.expand-button {
  font-size: 40px;
}
.menu {
  background-color: #181828;
  color: #ccc;
}
</style>
