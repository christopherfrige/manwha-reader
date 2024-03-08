<template>
  <div class="body">
    <LayoutNavbarHeader/>
    <div class="container" v-if="chapterData && manwhaData">
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
        <v-col  cols="12" md="6" class="text-end">
          <ChapterPaginationButtons
            :chapters="manwhaData.chapters"
            :currentChapterId="Number(this.chapterId)"
            :manwhaId="this.chapterData.manwha_id"
          />
        </v-col>
      </v-row>
      <v-row v-for="page in chapterData.pages" no-gutters class="reading-content  text-center">
        <v-col>
          <img :src="page.url" />
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
export default {
  name: "ChapterPages",
  data() {
    return {
      chapterId: this.$route.query.id,
      chapterData: null,
      manwhaData: null,
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
    },
    async getManwhaInfo() {
      const response = await this.$request.get(
        `v1/manwhas/${this.chapterData.manwha_id}`
      );
      this.manwhaData = response.data;
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


</style>
