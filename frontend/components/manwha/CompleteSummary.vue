<template>
  <div>
    <v-row class="mt-2">
      <v-col cols="12" md="12" class="content text-center">
        <h1>{{ manwha.name }}</h1>
      </v-col>
    </v-row>
    <v-row class="pt-4 description">
      <v-col cols="12" md="3">
        <img :title="manwha.name" :src="manwha.thumbnail" class="thumbnail" />
      </v-col>
      <v-col cols="12" md="8" class="content">
        <div v-for="content in contents">
          <ManwhaSummaryContent
            :contentTitle="content['title']"
            :contentDescription="manwha[content['description']]"
          />
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: 'ManwhaCompleteSummary',
  props: ['manwha'],
  data() {
    return {
      contents: [
        { title: 'Alternativos', description: 'alternative_names' },
        { title: 'Autor(es)', description: 'authors' },
        { title: 'Artista(s)', description: 'artists' },
        { title: 'Gênero(s)', description: 'genres' },
      ],
    };
  },
};
</script>

<style scoped>
.description {
  justify-content: space-between;
}

.thumbnail {
  max-width: 100%;
  height: auto;
  border-radius: 25px;
  padding: 15px;
  background: #ffffff0a;
}

@media (max-width: 960px) {
  .thumbnail {
    margin: 0 auto 16px auto;
    display: inherit;
    width: 270px;
  }
}

.content {
  background-color: #ffffff0a;
  border-radius: 15px;
}

h1 {
  font-weight: 500;
  font-size: 3.5vh !important;
}
</style>
