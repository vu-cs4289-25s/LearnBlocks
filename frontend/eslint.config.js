import js from "@eslint/js";
import jsdoc from "eslint-plugin-jsdoc";

import react from "eslint-plugin-react";

// ignore this warning, see https://github.com/facebook/react/issues/30119
// I dont know how to disable it for the time being
import reactHooks from "eslint-plugin-react-hooks"; 
import reactRefresh from "eslint-plugin-react-refresh";

import tailwindcss from "eslint-plugin-tailwindcss";

import prettierConfig from "eslint-config-prettier";

export default [
  // These are the recommended configs for each plugin
  js.configs.recommended, 
  jsdoc.configs["flat/recommended"], 
  prettierConfig, 
  react.configs.flat.recommended, 
  react.configs.flat["jsx-runtime"], // for react > v17
  reactRefresh.configs.recommended,
  ...tailwindcss.configs["flat/recommended"], 
  {
    files: ["**/*.{jsx,jsx}"],
    ignores: ["**/*.config.js"],
    languageOptions: {
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    // TODO: This react hooks configuration is neccessary until the issue above is resolved.
    plugins: {
      'react-hooks': reactHooks, 
    },
    rules: {
      // TODO: once its resolved, reactHooks can be configured like the rest of the plugins
      ...reactHooks.configs.recommended.rules,
      'react/prop-types': 'off'
      }
  },
];

