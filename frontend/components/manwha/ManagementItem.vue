<template>
  <v-expansion-panel-title @click="$emit('loadManwhaContent'), $emit('loadManwhaScraperContent')">
    <v-row no-gutters>
      <v-col cols="2">
        <img :title="manwha.manwha_name" :src="manwha.thumbnail" class="thumbnail" />
      </v-col>
      <v-col cols="10" class="title">
        <span class="manwha-title">{{ manwha.manwha_name }}</span>
      </v-col>
    </v-row>
  </v-expansion-panel-title>
  <v-expansion-panel-text>
    <v-row no-gutters>
      <v-col
        ><span
          ><strong>Quantidade de capítulos baixados:</strong>
          {{ downloadedChaptersQuantity }}</span
        ></v-col
      >
    </v-row>
    <v-row no-gutters>
      <v-col
        ><span><strong>Capítulo inicial cadastrado:</strong> {{ manwhaChapterStart }}</span></v-col
      >
    </v-row>
    <v-row no-gutters>
      <v-col v-if="downloadedChaptersQuantity"
        ><span><strong>Primeiro capítulo baixado:</strong> {{ manwhaFirstChapter }}</span></v-col
      >
    </v-row>
    <v-row no-gutters>
      <v-col v-if="downloadedChaptersQuantity"
        ><span><strong>Ultimo capítulo baixado:</strong> {{ manwhaLastChapter }}</span></v-col
      >
    </v-row>
    <v-row no-gutters>
      <v-col
        ><span
          ><strong>URL de origem:</strong>
          <a :href="manwhaUrl" class="manwha-origin-url" target="_blank">{{ manwhaUrl }}</a></span
        ></v-col
      >
    </v-row>
    <v-row>
      <v-col cols="6">
        <UiAppButton
          class="mb-4"
          type="primary"
          text="Baixar Capítulos"
          @click="$emit('sendManwhaScrapingRequest')"
        />
      </v-col>
      <v-col cols="6" class="text-end">
        <UiAppButton
          class="mb-4"
          type="error"
          text="Limpar Capítulos"
          :disabled="downloadedChaptersQuantity == 0"
          @click="$emit('deleteManwhaChapters')"
        />
      </v-col>
    </v-row>
  </v-expansion-panel-text>
</template>

<script>
export default {
  name: 'ManwhaAdminItem',
  props: {
    manwha: Object,
    manwhaScraperDetails: Object,
    manwhaDetails: Object,
  },
  emits: [
    'loadManwhaContent',
    'loadManwhaScraperContent',
    'deleteManwhaChapters',
    'sendManwhaScrapingRequest',
  ],
  computed: {
    manwhaChapterStart() {
      return this.manwhaScraperDetails ? this.manwhaScraperDetails.chapter_start : '';
    },
    manwhaUrl() {
      return this.manwhaScraperDetails ? this.manwhaScraperDetails.url : '';
    },
    downloadedChaptersQuantity() {
      return this.manwhaDetails ? this.manwhaDetails.chapters.length : '';
    },
    manwhaLastChapter() {
      if (this.manwhaDetails && this.manwhaDetails.chapters.length > 0) {
        return this.manwhaDetails.chapters[0].chapter_number;
      }
      return '';
    },
    manwhaFirstChapter() {
      if (this.manwhaDetails && this.manwhaDetails.chapters.length > 0) {
        return this.manwhaDetails.chapters.at(-1).chapter_number;
      }
      return '';
    },
  },
};
</script>

<style scoped>
.thumbnail {
  max-width: 100%;
  max-height: 70px;
  vertical-align: middle;
}

.title {
  align-items: center;
  display: grid;
}

.manwha-title {
  font-size: 15px;
  margin-left: 8px;
}

.v-expansion-panel-title {
  background-color: var(--container-item-bg-title);
  color: #fff;
  border-radius: 0;
  padding: 8px 12px;
}

.v-expansion-panel-text {
  background-color: var(--container-item-bg-content);
  color: #fff;
}

:deep(.v-expansion-panel-text__wrapper) {
  padding: 8px 12px !important;
}

strong {
  font-size: 14px;
}

span {
  font-size: 13px;
}

.manwha-origin-url {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  color: #fff;
}
</style>
