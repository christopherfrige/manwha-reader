<template>
  <v-btn :disabled="disabled" class="button" :class="type" :loading="loading">{{ text }}</v-btn>
</template>
<script>
export default {
  props: {
    type: String,
    text: String,
    disabled: Boolean,
    loading: Boolean,
  },
  computed: {
    buttonStyle() {
      return `${this.type}`;
    },
  },
};
</script>
<style scoped>
.button {
  font-size: 16px;
  transition: background 0.3s ease;
}
.button:hover {
  cursor: pointer;
}
.button:disabled {
  cursor: not-allowed;
}

.error {
  background: var(--error-500);
  color: #000;
}
.error:hover {
  background: var(--error-600);
}
.error:disabled {
  background: var(--error-700);
  color: #262626;
}

.primary {
  background: var(--primary-500);
  color: #000;
}
.primary:hover {
  background: var(--primary-600);
}
.primary:disabled {
  background: var(--primary-700);
  color: #262626;
}
</style>
