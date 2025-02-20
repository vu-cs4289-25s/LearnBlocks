import flowbite from 'flowbite-react/tailwind';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}', flowbite.content()],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#FFF5F2',
          100: '#FFF1EE',
          200: '#FFE4DE',
          300: '#FFD5CC',
          400: '#FFBCAD',
          500: '#FE795D',
          600: '#EF562F',
          700: '#EB4F27',
          800: '#CC4522',
          900: '#A5371B',
        },

        gray: {
          50: '#e6e6e6',
          100: '#d2d2d2',
          200: '#bebebe',
          300: '#aaaaaa',
          400: '#bebebe',
          500: '#828282',
          600: '#6e6e6e',
          700: '#4a4a4a',
          800: '#2f2f2f',
          900: '#1e1e1e',
        },

        cyan: {
          500: '#ec7018',
          600: '#c26008',
          700: '#d27018',
          800: '#c26008',
        }
      },
    },
  },
  plugins: [flowbite.plugin()],
};
