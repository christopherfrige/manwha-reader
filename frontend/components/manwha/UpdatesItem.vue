<template>
  <v-row>
    <v-col cols="12">
      <img
        :title="manwha.manwha_name"
        :src="manwha.thumbnail"
        class="thumbnail"
        @click="navigateToManwha()"
      />
    </v-col>
  </v-row>
  <v-row no-gutters>
    <v-col cols="12">
      <h3>
        <a class="title" @click="navigateToManwha()">{{
          manwha.manwha_name
        }}</a>
      </h3>
      <ChapterAccessButton
        :chapterId="manwha.last_chapter_id"
        :chapterNumber="manwha.last_chapter_number"
        :manwhaName="manwha.manwha_name"
      />
      <ChapterDatePostedLabel :postedAt="manwha.last_chapter_uploaded_at" />
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "ManwhaUpdatesItem",
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
.thumbnail {
  max-width: 100%;
  height: auto;
  object-fit: cover;
  transition: filter 0.3s ease;
  border-radius: 15px;
}

.thumbnail:hover {
  filter: brightness(60%);
  cursor: pointer;
}

.title {
  font-size: 16px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  color: #ccc;
  transition: color 0.3s ease;
}

.title:hover {
  color: rgb(212, 186, 37);
  cursor: pointer;
}
</style>
