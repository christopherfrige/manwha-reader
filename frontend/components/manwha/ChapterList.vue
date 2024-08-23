<template>
  <v-row no-gutters>
    <v-col v-for="chapter in manwha.chapters" :key="chapter.id" cols="6" sm="4" md="3">
      <v-row class="chapter" no-gutters>
        <ChapterAccessButton
          :chapterId="chapter.id"
          :chapterNumber="chapter.chapter_number"
          :manwhaName="manwha.name"
        />
        <ChapterDatePostedLabel class="date-posted" :postedAt="chapter.created_at" />
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

@media (max-width: 1028px) {
  .date-posted {
    margin-top: 10px;
  }
  .chapter {
    justify-content: center;
  }
}
</style>
