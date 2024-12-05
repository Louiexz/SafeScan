import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';
export default defineConfig({
  plugins: [react()],
  base: process.env.NODE_ENV === 'production' ? '/static/' : '/',  // Base URL dos assets para produção e desenvolvimento
  build: {
    manifest: true,  // Gera um arquivo de manifesto para o Django usar
    outDir: resolve(__dirname, '../../backend/safescan/static'), // Diretório de saída para os arquivos compilados no Django
    rollupOptions: {
      input: {
        index: resolve(__dirname, './index.html')
      }
    }
  }
});