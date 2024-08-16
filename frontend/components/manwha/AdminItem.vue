<template>
  <v-row>
    <v-col cols="3">
      <img :title="manwha.manwha_name" :src="manwha.thumbnail" class="thumbnail" />
    </v-col>
    <v-col cols="9">
      <span class="title">{{ manwha.manwha_name }}</span>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'ManwhaAdminItem',
  props: {
    manwha: Object,
  },
  methods: {
    async navigateToManwha() {},
  },
};
</script>

<style scoped>
.thumbnail {
  max-width: 100%;
  max-height: 70px;
}

.title {
  font-size: 16px;
}
</style>
