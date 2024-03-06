<template>
    <div class="body">
      <v-row class="justify-center">
        <ManwhaCompleteSummary :manwha="manwha"/>
      </v-row>
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
  };
  </script>
  
  <style scoped>
  .body {
    background-color: rgb(20, 20, 20);
    min-height: 100vh;
    font-family: Poppins, sans-serif;
    display: block;
  }
  </style>
  