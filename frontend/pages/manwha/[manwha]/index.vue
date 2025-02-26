<template>
  <div class="body">
    <Head>
      <Title>Manwha Reader - {{ manwha ? manwha.name : 'Loading' }}</Title>
    </Head>
    <LayoutNavbarHeader />
    <v-container class="container">
      <div v-if="!manwha">
        <v-row>
          <v-col class="summary mx-0 px-0">
            <v-row>
              <v-skeleton-loader type="heading" class="skeleton-title" />
            </v-row>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <v-row class="mx-0 px-0">
              <v-skeleton-loader type="image" class="skeleton-image" />
            </v-row>
          </v-col>

          <v-col cols="12" md="8">
            <v-row class="mx-0 px-0">
              <v-skeleton-loader type="image" class="skeleton-summary" />
            </v-row>
          </v-col>
        </v-row>

        <v-row class="mt-7 d-flex skeleton-chapters" no-gutters>
          <v-col v-for="n in 8" cols="6" sm="4" md="3" :key="n" class="mx-0 px-0">
            <v-skeleton-loader type="button" class="skeleton-button" />
          </v-col>
        </v-row>
      </div>

      <div v-else>
        <v-row>
          <v-col class="summary">
            <ManwhaCompleteSummary :manwha="manwha" />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="text-center mt-3 chapters">
            <ManwhaChapterList :manwha="manwha" />
          </v-col>
        </v-row>
      </div>
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

@media (max-width: 960px) {
  .skeleton-summary {
    margin-top: 20px;
  }
  .skeleton-chapters {
    margin-top: 200px !important;
  }
  .skeleton-image {
    margin-left: auto;
    margin-right: auto;
  }
}

@media (max-width: 576px) {
  .skeleton-title {
    height: 155px !important;
  }
  ::v-deep(.v-skeleton-loader__heading) {
    height: 120px !important;
    border-radius: 0;
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

.skeleton-title {
  height: 110px;
  width: 100%;
}

.skeleton-image {
  width: 60%;
}

.skeleton-summary {
  height: 180px;
  width: 100%;
  margin-bottom: 16px;
}

.skeleton-button {
  width: 99%;
}

::v-deep(.v-skeleton-loader__heading) {
  height: 75px;
  border-radius: 0;
}

::v-deep(.v-skeleton-loader__text) {
  height: 30px;
  min-width: 200px;
  width: 200px;
}

::v-deep(.v-skeleton-loader__button) {
  height: 70px;
  min-width: 100%;
  margin: 2px;
  border-radius: 0;
}

::v-deep(.v-skeleton-loader__image) {
  height: 370px;
  width: 100%;
}
</style>
