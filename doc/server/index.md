<script setup>
import { h, computed} from 'vue'
import { useData } from 'vitepress'
const { site } = useData()

const columns = [
    {
        "cell": row => h('a', { href: row.link.replace('.md','') }, row.link.replace('.md',''))
    },
    {
        cell: row => h('a', { href: row.repository, target: '_blank', }, `${row.name}:${row.version}`)
    },
    {
        "prop": "latest",
        "name": "Latest"
    }
]

function flatten(items = [], key, type) {
  return items.flatMap(t => [...(t[key] ?? []).map(repository => ({...repository,type,link: t.link})),...(t.items ? flatten(t.items, key, type ?? t.text) : [])])
}

const data = computed(() => flatten(site.value.themeConfig.sidebar['/server/']?.[0]?.items, 'repositories') ?? [])
</script>
<Table :columns="columns" :data="data" height="500px" :filter="true" />

# Grafana
![avatar](./static/grafana-dashboard.png)
# Docker
![avatar](./static/docker.png)
# Kubernetes
![avatar](./static/grafana-k8s.png)
# JVM
![avatar](./static/grafana-jvm.png)