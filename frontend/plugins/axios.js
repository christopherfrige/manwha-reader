import axios from "axios";

export default defineNuxtPlugin(() => {
  const defaultUrl = "http://localhost:8000";

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
