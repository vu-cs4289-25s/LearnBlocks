import flowbite from 'flowbite-react/tailwind';
import { colors } from './src/lib/utils/tailwindColors.mjs';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}', flowbite.content()],
  darkMode: 'class',
  // NOTE: To get around setting defualt elements
  theme: {
    extend: {
      colors: {
        primary: colors.orange,

        gray: colors.trueGray,

        // This is because Flowbite-react
        // doesnt use primary for the default color
        // of certain elements
        // NOTE: cyan is remapped to orange
        cyan: colors.orange,
      },
    },
  },
  plugins: [flowbite.plugin()],
};
