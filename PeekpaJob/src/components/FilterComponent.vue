<script setup lang="ts">
import type { Filter, FilterItem } from "@/types/Base.ts";
import { type LocationQuery, useRoute } from "vue-router";

// 定义组件的 props
const props = defineProps<{
    dataList: Filter[]; // 过滤器数据列表
}>();

// 路由对象
const router = useRoute();
// 处理过的过滤器数据列表
const displayList = ref<Filter[]>([]);

// 将 URL 中的参数遍历，并将过滤器内对应的元素高亮显示
const processFilterList = (filterList: Filter[], query: LocationQuery) => {
    const result: Filter[] = [];
    filterList.forEach((item: Filter) => {
        const displayItem: Filter = {
            title: item.title,
            param: item.param,
            filters: [],
        };
        item.filters.forEach((filterItem: FilterItem) => {
            let active = false;
            if (query[item.param]) {
                active = query[item.param] === filterItem.param;
            } else {
                active = filterItem.param === "";
            }
            displayItem.filters.push({
                name: filterItem.name,
                param: filterItem.param,
                active,
            } as FilterItem);
        });
        result.push(displayItem);
    });
    return result;
};

// 通过监听来自列表页的过滤器列表数据，处理成带有active的过滤器列表
watch(
    () => props.dataList,
    (newValue) => {
        displayList.value = processFilterList(newValue, router.query);
    },
    { immediate: true, deep: true },
);

// 定义组件 emit 事件
const emit = defineEmits<{
    // 将过滤器的点击事件交由父组件处理
    (eventName: "search", param: string, value: string): void;
}>();
</script>

<template>
    <div v-if="displayList.length" class="filter_container">
        <ul class="selector_list">
            <li v-for="item in displayList" :key="item.title">
                <span class="title">{{ item.title }}:</span>
                <a
                    v-for="subitem in item.filters"
                    :key="subitem.name"
                    :href="subitem.param"
                    :class="{ active: subitem.active }"
                    @click.prevent="emit('search', item.param, subitem.param)"
                >
                    {{ subitem.name }}
                </a>
            </li>
        </ul>
    </div>
</template>

<style scoped>
ul {
    list-style: none;
}

.filter_container {
    margin-top: 20px;
}

.selector_list {
    position: relative;
    padding: 8px 0;
    background-color: rgb(250, 250, 250);
    border: 1px solid rgb(237, 237, 237);
    min-height: 36px;
    overflow: hidden;
}

a {
    color: var(--theme-color);
    text-decoration: none;
    background-color: transparent;
    outline: none;
    cursor: pointer;
    transition: color 0.3s;
}

li {
    margin: 10px 0;
}

li a + a {
    margin: 0 5px;
}

li a {
    padding: 4px 8px;
    cursor: pointer;
    margin-right: 5px;
    height: 24px;
    line-height: 15px;
}

a.active {
    background-color: var(--theme-primary-color);
    color: #fff;
}

.selector_list li {
    padding: 4px 0;
    zoom: 1;
    color: #555;
    border-bottom: 1px dashed transparent;
}

.selector_list > li {
    position: relative;
    z-index: 6;
}

li span {
    font-weight: 600;
    margin-right: 15px;
    margin-left: 15px;
    padding: 4px 8px;
    height: 24px;
    line-height: 15px;
}
</style>
