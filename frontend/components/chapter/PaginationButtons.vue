<template>
  <div class="pagination-buttons">
    <a v-if="showPrevious" @click="navigateToManwhaChapter(false)"
      ><v-icon icon="mdi-arrow-left"></v-icon> Anterior</a
    >
    <a v-if="showNext" @click="navigateToManwhaChapter(true)"
      >Próximo <v-icon icon="mdi-arrow-right"></v-icon
    ></a>
    <a v-if="showManwhaInfo" @click="navigateToManwha()"
      ><v-icon icon="mdi-information"></v-icon> Ver Manwha</a
    >
  </div>
</template>

<script>
export default {
  name: 'ChapterPaginationButtons',
  props: {
    chapters: Array,
    currentChapterId: Number,
    manwhaId: Number,
  },
  data() {
    return {
      showNext: false,
      nextChapter: {},
      showPrevious: false,
      previousChapter: {},
      showManwhaInfo: false,
      manwhaNameNormalized: this.$route.params.manwha,
    };
  },
  methods: {
    initializePagination() {
      const chapters = [...this.chapters].reverse();

      const chaptersQuantity = chapters.length;
      const currentChapterIndex = chapters.findIndex(
        (chapter) => chapter.id == this.currentChapterId,
      );

      const hasPreviousChapters = currentChapterIndex > 0;
      if (hasPreviousChapters) {
        this.showPrevious = true;
        this.previousChapter = chapters[currentChapterIndex - 1];
      }

      const hasNextChapters = currentChapterIndex < chaptersQuantity - 1;
      if (hasNextChapters) {
        this.showNext = true;
        this.nextChapter = chapters[currentChapterIndex + 1];
      } else {
        this.showManwhaInfo = true;
      }
    },
    async navigateToManwha() {
      return navigateTo({
        path: `/manwha/${this.manwhaNameNormalized}`,
        query: {
          id: this.manwhaId,
        },
      });
    },
    async navigateToManwhaChapter(isNext) {
      const chapter = isNext ? this.nextChapter : this.previousChapter;

      const chapterNumberNormalized = normalizeChapterNumber(chapter.chapter_number);
      return navigateTo({
        path: `/manwha/${this.manwhaNameNormalized}/capitulo-${chapterNumberNormalized}`,
        query: {
          id: chapter.id,
        },
      });
    },
  },
  mounted() {
    this.initializePagination();
  },
};
</script>

<style scoped>
a {
  background: var(--button-bg-color);
  color: #000;
  padding: 10px;
  border-radius: 5px;
  transition: background 0.25s ease;
}

a:hover {
  cursor: pointer;
  background: var(--button-hover-bg-color);
}

@media (max-width: 576px) {
  a {
    display: inline-block;
    width: 48%;
  }
  .pagination-buttons {
    text-align: center;
  }
}

a:last-of-type {
  margin-left: 7px;
}

.v-icon {
  padding-bottom: 2px;
}
</style>
