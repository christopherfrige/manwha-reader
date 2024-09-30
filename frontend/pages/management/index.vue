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
              <h2><v-icon icon="mdi-plus"></v-icon> Adicionar Manwha</h2>
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
                v-model.number="chapterStart"
                label="Baixar a partir de qual capítulo"
                type="number"
                :min="0"
                required
              ></v-text-field>
            </v-row>
            <v-row class="justify-center mb-2">
              <UiAppButton
                type="primary"
                text="Cadastrar Manwha"
                :disabled="!formValid"
                @click="registerManwha()"
              >
              </UiAppButton>
            </v-row>
          </v-form>
        </v-col>
      </v-row>
    </div>
    <div class="container mt-4 pb-8 px-6">
      <v-row class="justify-center">
        <v-col cols="12" class="content">
          <v-row class="section-title">
            <v-col>
              <h2><v-icon icon="mdi-cog"></v-icon> Gerenciar Manwhas</h2>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-row no-gutters>
                <v-col
                  cols="6"
                  @click="showManwhasWithChapters()"
                  class="tab"
                  :class="{ 'active-tab': manwhasHavingChapters }"
                >
                  BAIXADOS
                </v-col>
                <v-divider vertical></v-divider>
                <v-col
                  cols="6"
                  @click="showManwhasWithoutChapters()"
                  class="tab"
                  :class="{ 'active-tab': !manwhasHavingChapters }"
                >
                  JÁ LIDOS
                </v-col>
              </v-row>
              <v-expansion-panels variant="accordion" class="panel-with-chapters" flat>
                <v-expansion-panel
                  class="row-list"
                  v-for="(manwha, index) in manwhas"
                  :key="manwha.manwha_id"
                >
                  <div v-show="manwha.last_chapter_downloaded === manwhasHavingChapters">
                    <ManwhaManagementItem
                      :manwha="manwha"
                      :manwhaDetails="manwhasDetails[index]"
                      :manwhaScraperDetails="manwhasScraperDetails[index]"
                      :deleteLoading="deleteLoading"
                      :downloadLoading="downloadLoading"
                      @load-manwha-scraper-content="loadManwhaScraperContent(index)"
                      @load-manwha-content="loadManwhaContent(index)"
                      @delete-manwha-chapters="deleteManwhaChapters(index)"
                      @send-manwha-scraping-request="sendManwhaScrapingRequest(index)"
                    />
                  </div>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-col>
          </v-row>
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
      manwhas: [],
      manwhasDetails: {},
      manwhasScraperDetails: {},
      pagination: {},
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
      manwhasHavingChapters: true,
      downloadLoading: false,
      deleteLoading: false,
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
        .post(`v1/scrapers/manwha`, registerPayload)
        .then((response) => {
          const scraperManwhaId = response.data.scraper_manwha_id;
          const scrapePayload = {
            reader_id: this.selectedReader,
            scraper_manwha_id: scraperManwhaId,
          };

          this.selectedReader = null;
          this.manwhaUrl = null;
          this.chapterStart = 0;

          this.$request.post(`v1/scrapers/scrape`, scrapePayload).catch(() => {
            this.showSnackbar(
              'Manwha foi cadastrado com sucesso, porém não foi possível baixar os capítulos, baixe separadamente. (︶︹︺)',
              false,
            );
            return;
          });

          this.showSnackbar(
            'Manwha cadastrado com sucesso, os capítulos devem aparecer em breve (◑‿◐)',
          );
        })
        .catch((error) => {
          this.showSnackbar(`Erro ao cadastrar o manwha: ${error.response.data.message}`, false);
        });
    },
    async getManwhas() {
      const params = {
        page: this.pageCount,
        per_page: 1000,
        order_entity: 'manwha',
        order_by: 'name',
        order: 'ASC',
      };
      const response = await this.$request.get(`v1/manwhas/`, { params });
      const manwhas = response.data.records;

      this.manwhas = manwhas;

      this.pagination = response.data.pagination;
    },
    async loadManwhaScraperContent(index) {
      if (this.manwhasScraperDetails[index]) {
        return;
      }
      const response = await this.$request.get(
        `v1/scrapers/manwha/${this.manwhas[index].manwha_id}`,
      );
      this.manwhasScraperDetails[index] = response.data;
    },
    async loadManwhaContent(index, force = false) {
      if (this.manwhasDetails[index] && !force) {
        return;
      }
      const response = await this.$request.get(`v1/manwhas/${this.manwhas[index].manwha_id}`);
      this.manwhasDetails[index] = response.data;
    },
    async deleteManwhaChapters(index) {
      this.deleteLoading = true;
      this.$request
        .delete(`v1/manwhas/${this.manwhas[index].manwha_id}/chapters`)
        .then(async () => {
          await this.getManwhas();
          await this.loadManwhaContent(index, true);
          this.showSnackbar('Capítulos deletados com sucesso (◕‿‿◕｡)');
        })
        .catch(() => {
          this.showSnackbar(
            'Ocorreu um problema ao deletar os capítulos desse manwha (╥﹏╥)',
            false,
          );
        })
        .finally(() => (this.deleteLoading = false));
    },
    async sendManwhaScrapingRequest(index) {
      this.downloadLoading = true;
      const scrapePayload = {
        reader_id: this.manwhasScraperDetails[index].reader_id,
        scraper_manwha_id: this.manwhasScraperDetails[index].id,
      };
      this.$request
        .post(`v1/scrapers/scrape`, scrapePayload)
        .then(() => {
          this.showSnackbar(
            'Solicitação recebida com sucesso! Os capítulos devem aparecer em breve (◕‿‿◕｡)',
          );
        })
        .catch((error) => {
          if (error.response) {
            console.log(error.response);
            if (error.response.status === 406) {
              this.showSnackbar('Sem novos capítulos para baixar (✖╭╮✖)', false);
              return;
            }
          }
          this.showSnackbar('Erro ao tentar baixar os capítulos do manwha (✖╭╮✖)', false);
        })
        .finally(() => (this.downloadLoading = false));
    },
    showSnackbar(description, success = true) {
      this.showSnackBar = true;
      this.descriptionSnackBar = description;
      this.colorSnackBar = success ? 'green' : 'red';
    },
    showManwhasWithChapters() {
      this.manwhasHavingChapters = true;
    },
    showManwhasWithoutChapters() {
      this.manwhasHavingChapters = false;
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
    this.getManwhas();
  },
};
</script>
<style scoped>
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

@media (max-width: 768px) {
  .container {
    max-width: 100% !important;
    width: 100% !important;
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 768px;
  }
}

.row-list {
  background-color: #44454d !important;
}

.tab {
  text-align: center;
  padding: 10px 0 !important;
  cursor: pointer;
}

.active-tab {
  background-color: #44454d !important;
}
</style>
