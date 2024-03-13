module.exports = {
    root: true,
    env: {
      browser: true,
      'jest/globals': true,
      node: true,
    },
    parserOptions: {
      parser: '@babel/eslint-parser',
      requireConfigFile: false,
    },
    extends: [
      'prettier',
      'plugin:nuxt/recommended',
      'plugin:vue/vue3-essential',
      'plugin:vue-scoped-css/vue3-recommended',
      'eslint:recommended',
    ],
    plugins: ['jest'],
    rules: {
      'vue/no-static-inline-styles': [
        'warn',
        {
          allowBinding: false,
        },
      ],
    },
    overrides: [
      {
          "files": ["*.js"],
          "rules": {
              "no-undef": "off"
          }
      },
  ]
  }