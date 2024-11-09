import { defineConfig } from 'astro/config';

import tailwind from '@astrojs/tailwind';

export default defineConfig({
  server: {
    port: 8080, // Change the port to 8080
  },

  integrations: [tailwind()],
});