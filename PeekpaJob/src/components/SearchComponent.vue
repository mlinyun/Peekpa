<script setup lang="ts">
import { useRoute } from "vue-router";

// 定义组件的 props
const props = defineProps<{
    initKey?: string; // 搜索内容关键字初始值，可选
}>();

// 定义组件 emit 事件
const emit = defineEmits<{
    // 将搜索内容的点击事件交由父组件处理
    (eventName: "searchKey", param: string, value: string): void;
}>();

// 路由对象
const route = useRoute();
// 搜索框内的文字
const keyWord = ref<string>(props.initKey || "");

// 监听路由的 path 变化，当 path 变化时，意味着切换了页面，需要清空搜索框的内容
watch(
    () => route.path,
    () => {
        keyWord.value = "";
    },
    { deep: true },
);

// 监听搜索内容初始值，如果有值，则更新搜索框的内容
watch(
    () => props.initKey,
    (newValue) => {
        keyWord.value = newValue as string;
    },
    { immediate: true, deep: true },
);
</script>

<template>
    <div class="search">
        <div class="search-container">
            <el-form class="search-form" inline>
                <el-form-item>
                    <el-input
                        class="search-input"
                        size="large"
                        v-model="keyWord"
                        placeholder="请输入搜索内容"
                        clearable
                        @clear="keyWord = ''"
                        @keyup.enter="emit('searchKey', 'q', keyWord)"
                    >
                        <template #append>
                            <el-button
                                size="large"
                                type="primary"
                                @click="emit('searchKey', 'q', keyWord)"
                            >
                                <el-icon>
                                    <i-ep-search />
                                </el-icon>
                                搜索
                            </el-button>
                        </template>
                    </el-input>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<style scoped>
.search {
    position: fixed;
    width: 100%;
    top: 60px;
    left: 0;
    z-index: 110;
    background: rgb(242, 245, 244);
    padding: 20px 0;
}

.search-container {
    position: relative;
    width: 1200px;
    height: 46px;
    margin: 0 auto;
}

.search-input {
    width: 762px;
    height: 46px;
    line-height: 46px;
    font-size: 16px;
    padding: 0 16px;
}

.el-button .el-icon {
    margin-right: 10%;
}
</style>
