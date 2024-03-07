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
      <v-col cols="10">
        <h3>{{ manwha.manwha_name }}</h3>
      </v-col>
    </v-row>
   
</template>

<script>
export default {
  name: "ManwhaCard",
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
  border-radius: 15px;
}

.thumbnail:hover {
  filter: brightness(60%);
}


h3 {
  font-size: 14px;
}
</style>
