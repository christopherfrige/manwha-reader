<template>
  <div class="body">
    <LayoutNavbarHeader />
    <div class="container">
      <v-row class="justify-center">
        <v-col cols="12" md="7" class="content">
          <v-row class="section-title">
            <v-col>
              <h2><v-icon icon="mdi-fire"></v-icon>Atualizações</h2>
            </v-col>
          </v-row>
          <v-row>
            <v-col v-for="manwha in manwhas" :key="manwha.manwha_id" cols="6" lg="3" md="4">
              <ManwhaUpdatesItem :manwha="manwha" />
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="12" md="4" class="content ml-6">
          <v-row class="section-title">
            <v-col>
              <h2><v-icon icon="mdi-fire"></v-icon>Em Alta</h2>
            </v-col>
          </v-row>
          <v-row v-for="manwha in manwhas" :key="manwha.manwha_id">
            <ManwhaPopularItem :manwha="manwha" />
          </v-row>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ManwhaDetails',
  data() {
    return {
      manwhas: [],
    };
  },
  methods: {
    async getManwhaInfo() {
      const response = await this.$request.get(`v1/manwhas`);
      this.manwhas = response.data.records;
    },
  },
  mounted() {
    console.log(useRuntimeConfig().public.apiUrl);
    console.log(useRuntimeConfig().public.testEnv);
    this.getManwhaInfo();
  },
};
</script>

<style scoped>
.content {
  background-color: #ffffff0a;
  border-radius: 15px;
}

.section-title {
  font-size: 14px;
  background-color: #ffffff0a;
  border-radius: 15px 15px 0 0;
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
