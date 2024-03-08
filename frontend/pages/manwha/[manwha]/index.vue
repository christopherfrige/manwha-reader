<template>
  <div class="body">
    <LayoutNavbarHeader/>
    <v-container class="container">
      <v-row>
        <v-col>
          <ManwhaCompleteSummary :manwha="manwha" v-if="manwha" />
        </v-col>
      </v-row>
      <v-row>
        <v-col class="text-center">
          <h3>CAPÍTULOS LANÇADOS</h3>
          <ManwhaChapterList :manwha="manwha" v-if="manwha" class="mt-1"/>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "ManwhaDetails",
  data() {
    return {
      manwha: null,
      manwhaId: this.$route.query.id,
    };
  },
  methods: {
    async getManwhaInfo() {
      const response = await this.$request.get(`v1/manwhas/${this.manwhaId}`);
      this.manwha = response.data;
    },
  },
  mounted() {
    this.getManwhaInfo();
  },
};
</script>

<style scoped>
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
