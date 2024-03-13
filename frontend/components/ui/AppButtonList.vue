<template>
  <ul class="genre-list">
    <li v-for="item in items">
      <a :title="item" @click="navigateToHome()">{{ item }}</a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'UiAppButtonList',
  props: {
    items: Array,
  },
  methods: {
    async navigateToHome() {
      return navigateTo({
        path: `/`,
      });
    },
  },
};
</script>

<style scoped>
.genre-list li a {
  background: rgb(212, 186, 37);
  padding: 4px 10px;
  border-radius: 10px 0 10px 0;
  cursor: pointer;
}

li {
  list-style-type: none;
}
</style>
