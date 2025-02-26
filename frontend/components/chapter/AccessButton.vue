<template>
  <div class="mt-1">
    <span class="chapter">
      <a @click="navigateToManwhaChapter()">Capítulo {{ chapterNumber }}</a>
    </span>
  </div>
</template>

<script>
export default {
  name: 'ChapterButton',
  props: {
    chapterId: Number,
    chapterNumber: Number,
    manwhaName: String,
  },
  methods: {
    async navigateToManwhaChapter() {
      const manwhaNameNormalized = normalizeManwhaName(this.manwhaName);
      const chapterNumberNormalized = normalizeChapterNumber(this.chapterNumber);
      return navigateTo({
        path: `/manwha/${manwhaNameNormalized}/capitulo-${chapterNumberNormalized}`,
        query: {
          id: this.chapterId,
        },
      });
    },
  },
};
</script>

<style scoped>
.chapter {
  background-color: var(--button-bg-color);
  padding: 5px 10px;
  cursor: pointer;
  color: #000;
  font-size: 14px;
  transition: background 0.25s ease;
  white-space: nowrap;
}

.chapter:hover {
  background-color: var(--button-hover-bg-color);
}
</style>
