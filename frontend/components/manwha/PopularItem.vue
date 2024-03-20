<template>
  <v-row class="item" no-gutters>
    <v-col cols="2">
      <img
        :title="manwha.manwha_name"
        :src="manwha.thumbnail"
        class="thumbnail"
        @click="navigateToManwha()"
      />
    </v-col>
    <v-col cols="9" class="ml-2">
      <a class="title" @click="navigateToManwha()">{{ manwha.manwha_name }}</a>
      <v-row no-gutters>
        <v-col class="d-flex align-baseline">
          <ChapterAccessButton
            :chapterId="manwha.last_chapter_id"
            :chapterNumber="manwha.last_chapter_number"
            :manwhaName="manwha.manwha_name"
            class="mt-2"
          />
          <ChapterDatePostedLabel :postedAt="manwha.last_chapter_uploaded_at" class="ml-2" />
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'ManwhaCard',
  props: {
    manwha: Object,
  },
  methods: {
    async navigateToManwha() {
      const manwhaNameNormalized = normalizeManwhaName(this.manwha.manwha_name);
      return navigateTo({
        path: `/manwha/${manwhaNameNormalized}/`,
        query: {
          id: this.manwha.manwha_id,
        },
      });
    },
  },
};
</script>

<style scoped>
.item {
  padding: 10px 0 10px 10px;
}

.thumbnail {
  max-width: 100%;
  height: auto;
  max-height: 100px;
  transition: filter 0.3s ease;
  border-radius: 10px;
}

.thumbnail:hover {
  filter: brightness(60%);
  cursor: pointer;
}

.title {
  font-size: 14px;
  font-weight: 600;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  color: #ccc;
  transition: color 0.3s ease;
}

.title:hover {
  color: var(--button-bg-color);
  cursor: pointer;
}
</style>
