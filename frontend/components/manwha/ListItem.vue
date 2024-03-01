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
        <h3>{{ manwha.manwha_name }}</h3>
        <h4>Último capítulo: {{ manwha.last_chapter }}</h4>
      </v-col>
    </v-row>
</template>

<script>
import normalizeString from "~/composables/utils";

export default {
  name: "ManwhaCard",
  props: {
    manwha: Object,
  },
  data() {
    return {
      count: 0,
    };
  },
  methods: {
    async navigateToManwha() {
      const manwhaNameNormalized = normalizeString(this.manwha.manwha_name);
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
.manwha-card-container {
  background: rgb(20, 20, 20);
  border: solid yellow 1px;
}

.thumbnail {
  max-width: 100%;
  height: auto;
  object-fit: cover;
  transition: filter 0.3s ease;
  border-radius: 15px;
}

.thumbnail:hover {
  filter: brightness(60%);
}

h3 {
  font-size: 14px;
  overflow: hidden;
  width: 100%;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

h4 {
  font-size: 12px;
}

h3,
h4 {
  color: white;
}
</style>
