<template>
  <div class="body">
    <Head>
      <Title>Manwha Reader - {{ manwhaName }} - Capítulo {{ chapterNumber }}</Title>
    </Head>
    <LayoutNavbarHeader />
    <div class="container mt-4">
      <v-row v-if="isLoading">
        <v-col>
          <v-row>
            <v-skeleton-loader type="heading" class="skeleton-title" />
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-row>
                <v-skeleton-loader type="button" width="300px" class="skeleton-button" />
              </v-row>
            </v-col>
            <v-col cols="12" md="6" class="pagination-skeleton">
              <v-row>
                <v-skeleton-loader type="button" width="49%" class="skeleton-button" />
                <v-skeleton-loader type="button" width="50%" class="skeleton-button" />
              </v-row>
            </v-col>
          </v-row>

          <v-row class="reading-content">
            <v-col>
              <v-skeleton-loader type="image" class="skeleton-image" />
            </v-col>
          </v-row>

          <v-row class="justify-end">
            <v-col cols="12" md="6" class="pagination-skeleton">
              <v-row>
                <v-skeleton-loader type="button" width="49%" class="skeleton-button" />
                <v-skeleton-loader type="button" width="50%" class="skeleton-button" />
              </v-row>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <div v-if="!isLoading">
        <v-row>
          <v-col>
            <h2>
              {{ chapterData.manwha_name }} - Capítulo
              {{ chapterData.chapter_number }}
            </h2>
          </v-col>
        </v-row>
        <v-row class="mb-6">
          <v-col cols="12" md="6">
            <ChapterSelectButton
              :chapters="manwhaData.chapters"
              :initialSelectedChapter="{
                id: chapterId,
                number: chapterData.chapter_number,
              }"
            />
          </v-col>
          <v-col cols="12" md="6" class="text-end">
            <ChapterPaginationButtons
              :chapters="manwhaData.chapters"
              :currentChapterId="Number(this.chapterId)"
              :manwhaId="this.chapterData.manwha_id"
            />
          </v-col>
        </v-row>

        <v-row
          v-for="page in chapterData.pages"
          :key="page.url"
          no-gutters
          class="reading-content text-center"
        >
          <v-col>
            <img :src="page.url" />
          </v-col>
        </v-row>

        <v-row>
          <v-col class="my-5 text-end">
            <ChapterPaginationButtons
              :chapters="manwhaData.chapters"
              :currentChapterId="Number(this.chapterId)"
              :manwhaId="this.chapterData.manwha_id"
            />
          </v-col>
        </v-row>
      </div>

      <LayoutPageFooter />
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChapterPages',
  data() {
    return {
      chapterId: this.$route.query.id,
      chapterData: null,
      manwhaData: null,
      manwhaName: '',
      chapterNumber: '',
    };
  },
  methods: {
    async initializeData() {
      await this.getChapter().then(() => {
        this.getManwhaInfo();
      });
    },
    async getChapter() {
      const response = await this.$request.get(`v1/chapters/${this.chapterId}`);
      this.chapterData = response.data;
      this.chapterNumber = this.chapterData.chapter_number;
    },
    async getManwhaInfo() {
      const response = await this.$request.get(`v1/manwhas/${this.chapterData.manwha_id}`);
      this.manwhaData = response.data;
      this.manwhaName = this.manwhaData.name;
    },
  },
  computed: {
    isLoading() {
      return !(this.manwhaData && this.chapterData);
    },
  },
  mounted() {
    this.initializeData();
  },
};
</script>

<style scoped>
.container {
  width: 100%;
  margin-right: auto;
  padding: 0px 15px;
  margin-left: auto;
}

.reading-content {
  margin-left: -16px;
  margin-right: -16px;
  margin-bottom: -7px;
  -webkit-overflow-scrolling: touch;
}

img {
  max-width: 100%;
  height: auto;
}

@media (min-width: 1200px) {
  .container {
    max-width: 1140px;
  }
}

.skeleton-title {
  width: 800px;
}

.skeleton-image {
  width: 100%;
  margin-bottom: 16px;
  margin-left: auto;
  margin-right: auto;
}

@media (min-width: 768px) {
  .skeleton-image {
    width: 768px;
  }
}

::v-deep(.v-skeleton-loader__image) {
  height: 70vh;
}

::v-deep(.v-skeleton-loader__heading) {
  height: 30px;
}

::v-deep(.v-skeleton-loader__button) {
  max-width: 100%;
  height: 45px;
}
</style>
