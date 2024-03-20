<template>
  <v-row class="px-6 py-3" no-gutters>
    <v-col cols="12" sm="4" class="content-title">
      <span>
        {{ contentTitle }}
      </span>
    </v-col>
    <v-col cols="12" sm="8" class="content-description">
      <span>{{ formatContentDescription(contentDescription) }}</span>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'ManwhaSummaryContent',
  props: {
    contentTitle: String,
    contentDescription: Array,
  },
  methods: {
    formatContentDescription(contentDescription) {
      if (!Array.isArray(contentDescription)) return contentDescription;

      const contentNames = contentDescription.map((item) => {
        return item.name;
      });
      return contentNames.join(', ');
    },
  },
};
</script>

<style scoped>
.content-title {
  font-size: 14px !important;
  font-weight: 600;
  max-width: 150px;
  word-break: break-word;
}

.content-description {
  font-size: 14px;
  color: #ccc;
}
</style>
