import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,   // listen on 0.0.0.0 so Docker can expose the port
    port: 5173,
    watch: {
      usePolling: true, // required for Docker on Windows — filesystem events don't propagate through volume mounts
    },
  },
})
