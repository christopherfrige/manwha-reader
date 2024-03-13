<template>
  <span class="label">
    <v-icon class="clock" icon="mdi-clock-outline"></v-icon>
    {{ getPostedLabel(postedAt) }}
  </span>
</template>

<script>
export default {
  name: 'DatePostedLabel',
  props: {
    postedAt: String,
  },
  methods: {
    getPostedLabel(datetimeString) {
      const months = [
        'Janeiro',
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro',
      ];
      const postedDatetime = new Date(datetimeString);

      const postedRecentlyLabel = this.postedRecentlyLabel(postedDatetime);
      if (postedRecentlyLabel) return postedRecentlyLabel;

      const day = postedDatetime.getDate();
      const month = months[postedDatetime.getMonth()];
      const year = postedDatetime.getFullYear();

      return `${day} de ${month} de ${year}`;
    },
    postedRecentlyLabel(postedDatetime) {
      const now = new Date();

      const differenceInTime = now.getTime() - postedDatetime.getTime();
      const differenceInHours = Math.round(differenceInTime / (1000 * 60 * 60));
      const differenceInMinutes = Math.round(differenceInTime / (1000 * 60));

      const postedYesterday = now.getDate() - 1 === postedDatetime.getDate();

      const showNowLabel = differenceInMinutes === 0;
      const showMinutesLabel = differenceInHours < 1;
      const showHoursLabel = differenceInHours < 24;
      const showYesterdayLabel = !showHoursLabel && postedYesterday;

      const singleValueLabelAdditional =
        differenceInMinutes === 1 || differenceInHours === 1 ? '' : 's';

      if (showNowLabel) return 'Agora';
      if (showMinutesLabel)
        return `${differenceInMinutes} minuto${singleValueLabelAdditional} atrás`;
      if (showHoursLabel) return `${differenceInHours} hora${singleValueLabelAdditional} atrás`;
      if (showYesterdayLabel) return 'Ontem';
      return '';
    },
  },
};
</script>

<style scoped>
.label {
  font-size: 11px;
  color: #ccc;
}

.clock {
  padding-bottom: 2px;
  font-size: 12px;
}
</style>
