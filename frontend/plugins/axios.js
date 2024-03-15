import axios from 'axios';

export default defineNuxtPlugin(() => {
  const defaultUrl = useRuntimeConfig().public.apiUrl;

  let request = axios.create({
    baseURL: defaultUrl,
    headers: {
      common: {},
    },
  });

  return {
    provide: {
      request: request,
    },
  };
});
