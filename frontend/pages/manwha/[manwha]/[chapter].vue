<template>
    <div class="body">
      <div class="container">
        <v-row class="home-card">
          <v-col cols="12" class="py-0">
            <v-row>
              <v-col cols="12" md="3" style="border: 1px solid red;">
                <img :src="manwha.thumbnail" />
              </v-col>
              <v-col cols="12" md="9" style="border: 1px solid red">
                <h1>{{ manwha.name }}</h1>
                <UiAppButtonList :items="manwha.genres" />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "ManwhaDetails",
    data() {
      return {
        manwha: {},
      };
    },
    methods: {
      async getManwhaInfo() {
        const response = await this.$request.get(`v1/manwhas/${this.$route.query.id}`)
        this.manwha = response.data
      },
    },
    mounted() {
      this.getManwhaInfo();
    },
  };
  </script>
  
  <style scoped>
  .body {
    background-color: rgb(10, 10, 10);
    min-height: 100vh;
    font-family: Poppins, sans-serif;
    display: block;
  }
  
  .container {
    width: 70%;
    padding-right: 15px;
    padding-left: 15px;
    margin-right: auto;
    margin-left: auto;
  }
  
  .home-card {
    background-color: rgb(40, 40, 40);
  }
  
  .home-card-text {
    display: flex;
    color: white;
    padding: 10px 10px 0 10px;
  }
  </style>
  