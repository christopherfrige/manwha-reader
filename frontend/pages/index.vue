<template>
  <div class="body">
    <Head>
      <Title>Manwha Reader - Ler online Manwhas, Webtoons, Comics e Graphic Novels</Title>
    </Head>
    <LayoutNavbarHeader />
    <div class="container mt-4 pb-8 px-6">
      <v-row class="justify-center">
        <v-col class="content">
          <v-row class="section-title">
            <v-col>
              <h2><v-icon icon="mdi-fire"></v-icon> Últimos lançamentos</h2>
            </v-col>
          </v-row>
          <v-row>
            <v-col v-for="i in 6" v-if="loading" cols="6" lg="2" md="3">
              <v-skeleton-loader type="image, list-item-two-line" />
            </v-col>
            <v-col v-for="manwha in manwhas" :key="manwha.manwha_id" cols="6" lg="2" md="3">
              <ManwhaUpdatesItem :manwha="manwha" />
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </div>
    <LayoutPageFooter />
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
      loading: true,
    };
  },
  methods: {
    async getManwhaInfo(showMore = false) {
      this.loading = true;
      const params = {
        page: this.pageCount,
        per_page: 1000,
        with_chapters_downloaded: true,
      };
      const response = await this.$request.get(`v1/manwhas/`, { params });
      this.loading = false;
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
  computed: {
    hasManwhasToLoad() {
      return this.pagination.next !== null;
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

.v-icon {
  padding-bottom: 5px;
}
</style>
