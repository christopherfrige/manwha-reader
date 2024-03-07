<template>
  <div class="select">
    <select @change="navigateToManwhaChapter()" v-model="selectedChapter">
      <option
        v-for="chapter in chapters"
        :value="{ id: chapter.id, number: chapter.chapter_number }"
      >
        Capítulo <span>{{ chapter.chapter_number }}</span>
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: "ChapterSelectButton",
  props: {
    chapters: Array,
    initialSelectedChapter: Object
  },
  data() {
    return {
      selectedChapter: this.initialSelectedChapter,
    };
  },
  methods: {
    async navigateToManwhaChapter() {
      const chapterNumberNormalized = normalizeChapterNumber(
        this.selectedChapter.number
      );
      return navigateTo({
        path: `/manwha/${this.$route.params.manwha}/capitulo-${chapterNumberNormalized}`,
        query: {
          id: this.selectedChapter.id,
        },
      });
    },
  },
};
</script>

<style scoped>
select {
  appearance: none;
  outline: 10px red;
  border: 0;
  box-shadow: none;
  flex: 1;
  padding: 7px 10px;
  color: #fff;
  background-color: #ffffff31;
  background-image: none;
  cursor: pointer;
}

option {
  color: #000;
}

.select {
  position: relative;
  display: flex;
  width: 180px;
  border-radius: 0.25em;
  overflow: hidden;
}

/* Arrow */
.select::after {
  content: "\2B83";
  position: absolute;
  top: 0;
  right: 0;
  padding: 7px 12px;
  background-color: #ffffff31;
  transition: 0.2s all ease;
  pointer-events: none;
}

.select:hover::after {
  color: rgb(231, 212, 105);
}
</style>
