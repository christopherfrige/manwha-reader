<template>
  <footer>
    <v-row class="footer">
      <v-col class="my-6"> © 2024 Manwha Reader. Todos os direitos reservados. </v-col>
    </v-row>
  </footer>
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
footer {
  width: 100%;
  margin-right: auto;
  margin-left: auto;
  margin-top: auto;
  bottom: 0;
  background: var(--nav-bg-color);
  text-align: center;
  font-size: 0.8rem;
}

.v-row {
  margin: 0;
}

.v-col {
  padding: 0;
}
</style>
