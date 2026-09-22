<template>
    <input v-model="keyword" type="text" placeholder="Search..." v-if="props.filter" />
    <table :style="{ height: props.height }">
        <thead>
            <tr>
                <th v-for="t in columns" :key="t.prop">
                    {{ t.name }}
                </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(row, index) in filteredData" :key="index">
                <td v-for="t in columns" :key="t.prop">
                    <component v-if="t.cell" :is="t.cell(row)" />
                    <template v-else>{{ row[t.prop] }}</template>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
    filter: Boolean,
    height: String,
    columns: {
        type: Array,
        default: () => []
    },
    data: {
        type: Array,
        default: () => []
    }
})

const keyword = ref('')

const filteredData = computed(() => {
    const key = keyword.value.trim().toLowerCase()
    return props.data.filter(row => !key || Object.values(row).some(v => String(v).toLowerCase().includes(key)))
})

</script>