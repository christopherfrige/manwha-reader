<template>
  <div class="body">
    <Head>
      <Title>Manwha Reader - Ler online Manwhas, Webtoons, Comics e Graphic Novels</Title>
    </Head>
    <LayoutNavbarHeader />
    <div class="container mt-4 pb-8 px-6">
      <v-row class="justify-center">
        <v-col cols="12" class="content">
          <v-row class="section-title">
            <v-col>
              <h2><v-icon icon="mdi-cog"></v-icon> Painel Administrativo</h2>
            </v-col>
          </v-row>
          <v-form v-model="formValid">
            <v-row class="mt-5 mb-2 mx-2">
              <v-select
                v-model="selectedReader"
                label="Leitor"
                :items="readers"
                :rules="selectedReaderRules"
                required
              ></v-select>
            </v-row>
            <v-row class="mb-2 mx-2">
              <v-text-field
                v-model="manwhaUrl"
                label="Manwha URL"
                :rules="manwhaUrlRules"
                required
              ></v-text-field>
            </v-row>
            <v-row class="mx-2">
              <v-text-field
                v-model="chapterStart"
                label="Baixar a partir de qual capítulo"
                type="number"
                :min="0"
                required
              ></v-text-field>
            </v-row>
            <v-row class="justify-center mb-2">
              <button
                type="button"
                class="register-button"
                @click="registerManwha()"
                :disabled="!formValid"
              >
                Cadastrar
              </button>
            </v-row>
          </v-form>
        </v-col>
      </v-row>
    </div>
    <v-snackbar v-model="showSnackBar" :color="colorSnackBar">
      {{ descriptionSnackBar }}
    </v-snackbar>
  </div>
</template>
<script>
export default {
  name: 'AdminPage',
  data() {
    return {
      formValid: false,
      selectedReader: null,
      manwhaUrl: null,
      chapterStart: 0,
      selectedReaderRules: [(value) => !!value || 'Necessário selecionar um leitor'],
      manwhaUrlRules: [
        (value) => !!value || 'Campo obrigatório',
        (value) => this.isURL(value) || 'A URL inserida não é válida',
      ],
      readers: [],
      showSnackBar: false,
      colorSnackBar: null,
      descriptionSnackBar: null,
    };
  },
  methods: {
    async getReaders() {
      const response = await this.$request.get(`v1/readers/`);
      const readers = response.data.records;
      readers.map((reader) => this.readers.push({ title: reader.name, value: reader.id }));
    },
    async registerManwha() {
      const registerPayload = {
        reader_id: this.selectedReader,
        url: this.manwhaUrl,
        chapter_start: Number(this.chapterStart),
      };
      this.$request
        .post(`v1/manwhas`, registerPayload)
        .then((response) => {
          const scraperManwhaId = response.data.scraper_manwha_id;
          const scrapePayload = {
            reader_id: this.selectedReader,
            scraper_manwha_id: scraperManwhaId,
          };
          this.$request.post(`v1/scrapers/scrape`, scrapePayload);

          this.selectedReader = null;
          this.manwhaUrl = null;
          this.chapterStart = 0;

          this.showSnackBar = true;
          this.colorSnackBar = 'green';
          this.descriptionSnackBar = 'Manwha cadastrado com sucesso =)';
        })
        .catch((error) => {
          this.showSnackBar = true;
          this.colorSnackBar = 'red';
          this.descriptionSnackBar = `Erro ao cadastrar o manwha: ${error.response.data.message}`;
        });
    },
    isURL(str) {
      let url;

      try {
        url = new URL(str);
      } catch (_) {
        return false;
      }

      return url.protocol === 'http:' || url.protocol === 'https:';
    },
  },
  mounted() {
    this.getReaders();
  },
};
</script>
<style scoped>
.register-button {
  font-size: 16px;
  background-color: var(--button-bg-color);
  padding: 8px 40px;
  color: #000;
  border-radius: 10px;
  transition: background 0.3s ease;
}
.register-button:hover {
  background: var(--button-hover-bg-color);
  cursor: pointer;
}
.register-button:disabled {
  background-color: rgb(105, 95, 39);
  cursor: auto;
  color: #262626;
}

.content {
  background-color: var(--container-bg-color);
  padding: -10px;
}

.section-title {
  font-size: 14px;
  background-color: var(--container-title-bg-color);
}

.more-updates {
  cursor: pointer;
  background-color: #3c3a46;
  transition: all 0.25s ease;
}

.more-updates:hover {
  background-color: #44424d;
}

.container {
  width: 100%;
  margin-right: auto;
  margin-left: auto;
}

@media (max-width: 960px) {
  .container {
    max-width: 960px;
  }
}

@media (max-width: 960px) {
  .container {
    max-width: 100% !important;
    width: 100% !important;
  }
}

@media (min-width: 960px) {
  .container {
    max-width: 960px;
  }
}
</style>
