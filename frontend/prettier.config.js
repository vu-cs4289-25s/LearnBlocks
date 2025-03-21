/** @type {import('prettier').Config} */
export default {
  plugins: ['prettier-plugin-tailwindcss'],
  // tailwindcss
  tailwindAttributes: ['theme'],
  tailwindFunctions: ['tw', 'twMerge', 'createTheme'],
  singleQuote: true,
  trailingComma: 'all',
  printWidth: 80,
};
