import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react({
      // This line enables the modern JSX transform
      jsxRuntime: 'automatic'
    })
  ],
  server: {
    port: 5173 // Ensures a consistent port
  }
})
