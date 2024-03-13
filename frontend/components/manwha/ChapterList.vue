<template>
  <v-row>
    <v-col v-for="chapter in manwha.chapters" :key="chapter.id" cols="12" sm="6" md="4">
      <v-row class="chapter">
        <ChapterAccessButton
          :chapterId="chapter.id"
          :chapterNumber="chapter.chapter_number"
          :manwhaName="manwha.name"
        />
        <ChapterDatePostedLabel :postedAt="chapter.created_at" />
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'ManwhaChapterList',
  props: {
    manwha: Object,
  },
  data() {
    return {
      manwhaId: this.$route.query.id,
    };
  },
};
</script>

<style scoped>
.chapter {
  display: flex;
  background-color: #ffffff0a;
  align-items: center;
  justify-content: space-between;
  border-radius: 10px;
  padding: 15px;
  margin: 1px;
}
</style>
