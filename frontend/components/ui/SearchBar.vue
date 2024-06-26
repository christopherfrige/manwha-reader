<template>
  <v-layout>
    <ul class="manwhas-suggestion">
      <li
        class="suggestion"
        v-for="manwha in highlightedResults"
        :key="manwha.manwha_id"
        @click="navigateToManwha(manwha.manwha_id, manwha.manwha_name)"
      >
        <div class="px-4 py-1">
          <span v-html="manwha.highlighted_name"></span>
        </div>
      </li>
    </ul>
    <div class="search-bar">
      <v-text-field
        :loading="searchLoading"
        class="search-input"
        density="compact"
        label="Encontrar manwhas..."
        single-line
        hide-details
        v-model="inputSearch"
        @input="searchManwhas()"
        @focus="searchManwhas()"
      >
      </v-text-field>
      <span class="search-button">Buscar</span>
    </div>
  </v-layout>
</template>
<script>
export default {
  data() {
    return {
      manwhas: null,
      inputSearch: '',
      searchLoading: false,
    };
  },
  methods: {
    searchManwhas: debounce(async function () {
      if (!this.inputSearch) return (this.manwhas = null);
      this.searchLoading = true;

      const params = {
        search: this.inputSearch,
        per_page: 5,
      };
      const response = await this.$request.get(`v1/manwhas/`, { params });
      this.manwhas = response.data.records;

      this.searchLoading = false;
    }, 500),

    clearManwhas: debounce(function () {
      this.manwhas = null;
    }, 100),

    async navigateToManwha(manwhaId, manwhaName) {
      const manwhaNameNormalized = normalizeManwhaName(manwhaName);
      return navigateTo({
        path: `/manwha/${manwhaNameNormalized}/`,
        query: {
          id: manwhaId,
        },
      });
    },
  },
  computed: {
    highlightedResults() {
      if (!this.manwhas) return null;

      const manwhas = [...this.manwhas];
      return manwhas.map((manwha) => {
        const inputtedWords = this.inputSearch.split(' ');
        manwha.highlighted_name = manwha.manwha_name;
        inputtedWords.forEach((word) => {
          manwha.highlighted_name = manwha.highlighted_name.replace(
            new RegExp(word, 'gi'),
            '<b>$&</b>',
          );
        });
        return manwha;
      });
    },
  },
};
</script>

<style scoped>
.manwhas-suggestion {
  list-style-type: none;
  min-width: 250px;
  max-width: 400px;
  position: absolute;
  z-index: 10000;
  background-color: #1f2129;
  border-radius: 0 0 10px 10px;
  font-size: 16px;
  margin-top: 41px;
}

.suggestion:hover {
  background-color: var(--button-bg-color);
  color: #000;
}

.suggestion:hover:last-child {
  border-radius: 0 0 10px 10px;
}

.search-bar {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 450px;
}

.search-input {
  background-color: #ffffff0a;
  max-width: 450px;
}

.search-button {
  font-size: 16px;
  background-color: var(--button-bg-color);
  padding: 8px;
  color: #000;
  border-radius: 0 10px 10px 0;
  transition: background 0.3s ease;
  border: 1px solid #000;
}

.search-button:hover {
  background: var(--button-hover-bg-color);
  cursor: pointer;
}
</style>
