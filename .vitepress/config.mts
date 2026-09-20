import { defineConfig } from 'vitepress'
import doc_server_json from '../build/doc-server.json' with { type: 'json' }

// https://vitepress.dev/reference/site-config
export default defineConfig({
  srcDir: 'doc',
  outDir: 'build/doc',
  title: "Doc",
  lastUpdated: true,
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Server', link: '/server/' },
    ],
    sidebar: {
      '/server/': [
        {
          base: '/server/',
          items: doc_server_json
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/czy21/script' }
    ]
  }
})
