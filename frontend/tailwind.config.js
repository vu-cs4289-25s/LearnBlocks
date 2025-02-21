import { colors } from './src/lib/utils/tailwindColors.mjs';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  
  darkMode: 'class',

  theme: {
    extend: {
      colors: {
        primary: colors.orange,

        gray: colors.trueGray,

      },
    },
  },
  plugins: [],
};
