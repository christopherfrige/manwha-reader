<template>
  <div class="body">
    <v-container class="container">
      <v-row>
        <v-col cols="12" md="7" class="content" >
          <v-row class="section-title">
            <v-col>
              <h2><v-icon icon="mdi-fire"></v-icon>Atualizações</h2>
            </v-col>
          </v-row>
          <v-row>
            <v-col v-for="manwha in manwhas" cols="6" lg="3" md="4">
              <ManwhaListItem :manwha="manwha" />
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="12" md="4" class="content ml-6">
          <v-row class="section-title">
            <v-col>
              <h2><v-icon icon="mdi-fire"></v-icon>Em Alta</h2>
            </v-col>
          </v-row>
          <v-row v-for="manwha in manwhas">
            <ManwhaPopularItem :manwha="manwha" />
          </v-row>
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
      manwhas: {},
    };
  },
  methods: {
    async getManwhaInfo() {
      const response = await this.$request.get(`v1/manwhas`);
      this.manwhas = response.data.records;
    },
  },
  mounted() {
    this.getManwhaInfo();
  },
};
</script>

<style scoped>
.body {
  background-color: rgb(20, 20, 20);
  min-height: 100vh;
  font-family: poppins, sans-serif;
}

.container {
  display:flex;
  width: 100%;
  margin-right: auto;
  margin-left: auto;
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

@media (max-width: 1200px) {
  .container {
    max-width: 1200px;
  }
}

.content {
  background-color: rgb(40, 40, 40);
}

.section-title {
  color: #fff;
  font-size: 14px;
  background-color: rgb(30, 30, 30);
}
</style>
