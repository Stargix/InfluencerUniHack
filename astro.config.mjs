import { defineConfig } from 'astro/config';

import tailwind from '@astrojs/tailwind';

export default defineConfig({
  server: {
    port: 8000, // Change the port to 8000
  },

  integrations: [tailwind()],
});