<template>
  <div class="body">
    <Head>
      <Title>Manwha Reader - Ler online Manwhas, Webtoons, Comics e Graphic Novels</Title>
    </Head>
    <LayoutNavbarHeader />
    <div class="container mt-4 pb-8 px-6">
      <v-row class="justify-center">
        <v-col cols="12" md="8" class="content">
          <v-row class="section-title">
            <v-col>
              <h2><v-icon icon="mdi-fire"></v-icon> Atualizações</h2>
            </v-col>
          </v-row>
          <v-row class="mb-2">
            <v-col v-for="manwha in manwhas" :key="manwha.manwha_id" cols="6" lg="3" md="4">
              <ManwhaUpdatesItem :manwha="manwha" />
            </v-col>
          </v-row>
          <v-row
            class="justify-center py-4 more-updates"
            @click="getMoreManwhaInfo()"
            v-if="pagination.next"
          >
            MAIS ATUALIZAÇÕES
          </v-row>
          <v-row class="justify-center py-4 more-updates" v-if="pagination.next === null">
            VER TUDO
          </v-row>
        </v-col>
        <v-divider vertical class="d-none d-md-flex" />
        <v-col cols="12" md="4" class="content">
          <v-row class="section-title">
            <v-col>
              <h2><v-icon icon="mdi-trending-up"></v-icon> Em Alta</h2>
            </v-col>
          </v-row>
          <v-row v-for="manwha in trendingManwhas" :key="manwha.manwha_id">
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
      pagination: {},
      pageCount: 1,
      trendingManwhas: [],
    };
  },
  methods: {
    async getManwhaInfo(showMore = false) {
      const params = {
        page: this.pageCount,
        per_page: 8,
      };
      const response = await this.$request.get(`v1/manwhas`, { params });
      const manwhas = response.data.records;

      if (showMore) {
        manwhas.map((manwha) => this.manwhas.push(manwha));
      } else {
        this.manwhas = manwhas;
        this.trendingManwhas = manwhas;
      }

      this.pagination = response.data.pagination;
    },
    async getMoreManwhaInfo() {
      this.pageCount += 1;
      this.getManwhaInfo(true);
    },
  },
  mounted() {
    this.getManwhaInfo();
  },
};
</script>

<style scoped>
.content {
  background-color: var(--container-bg-color);
  padding: -10px;
}

.section-title {
  font-size: 14px;
  background-color: var(--container-title-bg-color);
}

.more-updates {
  cursor: pointer;
  background-color: #3c3a46;
  transition: all 0.25s ease;
}

.more-updates:hover {
  background-color: #44424d;
}

.container {
  width: 100%;
  margin-right: auto;
  margin-left: auto;
}

@media (max-width: 960px) {
  .content:last-of-type {
    margin-top: 20px;
  }
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
