<template>
  <v-row class="mt-1" no-gutters>
    <v-col cols="12 mt-1">
      <span class="chapter">
        <a @click="navigateToManwhaChapter()">Capítulo {{ chapterNumber }}</a>
      </span>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "ChapterButton",
  props: {
    id: Number,
    chapterNumber: Number,
    manwhaName: String
  },
  methods: {
    async navigateToManwhaChapter() {
      const manwhaNameNormalized = normalizeManwhaName(this.manwhaName)
      const chapterNumberNormalized = normalizeChapterNumber(this.chapterNumber)
      return navigateTo({
        path: `/manwha/${manwhaNameNormalized}/capitulo-${chapterNumberNormalized}`,
      })
    }
  }

}
</script>

<style scoped>
.chapter {
  background: rgb(212, 186, 37);
  padding: 4px 10px;
  border-radius: 10px 0 10px 0;
  cursor: pointer;
  color: #000;
  font-size: 14px;
  transition: background 0.5s ease, color 0.3s ease;
}

.chapter:hover {
  background: rgb(231, 212, 105);
}
</style>