<template>
  <v-row v-for="manwha in manwhas" :key="manwha.manwha_id">
    <v-col cols="12">
      <ManwhaAdminItem :manwha="manwha" />
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'ManwhaAdminList',
  props: {
    manwhas: Array,
  },
};
</script>
