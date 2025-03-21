import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  base: '/', // This is the base URL
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      $lib: path.resolve(import.meta.dirname, './src/lib'),
      $pages: path.resolve(import.meta.dirname, './src/pages'),
      $assets: path.resolve(import.meta.dirname, './src/assets'),
    },
  },
});
