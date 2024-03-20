<template>
  <div>
    <a> Mais atualizações</a>
  </div>
</template>

<script>
export default {
  name: 'ManwhaPaginationButtons',
  props: {
    paginationParams: Object,
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
  margin-left: 5px;
}

a:hover {
  cursor: pointer;

  background: var(--button-hover-bg-color);
}
</style>
