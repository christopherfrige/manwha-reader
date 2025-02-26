<template>
  <footer>
    <v-row class="footer">
      <v-col class="my-6">
        © {{ currentYear }} Manwha Reader. Todos os direitos reservados.
      </v-col>
    </v-row>
  </footer>
</template>

<script>
export default {
  computed: {
    currentYear() {
      return new Date().getFullYear();
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
