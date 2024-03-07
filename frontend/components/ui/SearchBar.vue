<template>
  <v-text-field
    :loading="false"
    class="search-input"
    density="compact"
    label="Encontrar manwhas..."
    single-line
    hide-details
  >
  </v-text-field>
</template>
<script>
export default {
  data() {
    return {};
  },
};
</script>

<style scoped>
.search-bar {
  background-color: transparent;
  width: 350px;
}

.search-input {
  background-color: #ffffff0a;
  color: white;
}

.search-button {
  font-size: 16px;
  background-color: rgb(212, 186, 37);
  padding: 8px;
  color: #000;
  border-radius: 0 10px 10px 0;
  transition: background 0.3s ease;
}

.search-button:hover {
  background: rgb(231, 212, 105);
  cursor: pointer;
}
</style>
