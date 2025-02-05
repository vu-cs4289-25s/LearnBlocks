import flowbite from "flowbite-react/tailwind";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}", flowbite.content()],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'nb-black': '#1e1e1e',
        'nb-gray': {
          '100': '#d9d9d9',
          '300': '#2f2f2f',
          '400': '#2b2b2b',
        },
        'nb-white': '#ffffff',
        'nb-orange': '#a65014',
        'nb-yellow': '#a57b1d'
      }
    },
  },
  plugins: [flowbite.plugin()],
};
