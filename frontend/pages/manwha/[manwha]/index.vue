<template>
  <div class="body">
    <Head>
      <Title>Manwha Reader - {{ manwhaName }}</Title>
    </Head>
    <LayoutNavbarHeader />
    <v-container class="container">
      <v-row>
        <v-col class="summary">
          <ManwhaCompleteSummary :manwha="manwha" v-if="manwha" />
        </v-col>
      </v-row>
      <v-row>
        <v-col class="text-center mt-3 chapters">
          <h3>CAPÍTULOS LANÇADOS</h3>
          <ManwhaChapterList :manwha="manwha" v-if="manwha" />
        </v-col>
      </v-row>
    </v-container>
    <LayoutPageFooter />
  </div>
</template>

<script>
export default {
  name: 'ManwhaDetails',
  data() {
    return {
      manwha: null,
      manwhaId: this.$route.query.id,
      manwhaName: '',
    };
  },
  methods: {
    async getManwhaInfo() {
      const response = await this.$request.get(`v1/manwhas/${this.manwhaId}`);
      this.manwha = response.data;
      this.manwhaName = this.manwha.name;
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

.chapters {
  padding-left: 0px;
  padding-right: 0px;
}

.v-container {
  padding-top: 0px !important;
}

.summary {
  padding-top: 0px !important;
}
</style>
