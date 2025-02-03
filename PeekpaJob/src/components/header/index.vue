<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";

interface NavMenu {
    // 导航显示名称
    name: string;
    // 导航跳转 URL
    url: string;
}

const BasicNavList: NavMenu[] = [
    {
        name: "首页",
        url: "/index",
    },
    {
        name: "职位",
        url: "/jobs",
    },
    {
        name: "公司",
        url: "/companies",
    },
];

// 当前高亮导航的 index
const currentIndex = ref<number>(-1);
// 路由对象
const route = useRoute();

// 根据路由地址变化更新高亮路由 index
const updateIndex = () => {
    const path = route.path;
    const currentItemIndex = BasicNavList.findIndex((item: NavMenu) => path.includes(item.url));
    currentIndex.value = currentItemIndex !== -1 ? currentItemIndex : currentIndex.value;
};

// 初始化时更新高亮路由 index
onMounted(() => {
    updateIndex();
});

// 监听路由地址变化更新高亮路由 index
watch(
    () => route,
    () => {
        updateIndex();
    },
    { deep: true },
);
</script>

<template>
    <div class="header">
        <div class="inner">
            <div class="float-left">
                <a href="/" class="logo"></a>
                <ul class="left-ul">
                    <li
                        v-for="(item, index) in BasicNavList"
                        :key="item.name"
                        class="nav-container"
                    >
                        <router-link
                            class="nav"
                            :class="{ tab_active: index === currentIndex }"
                            :to="item.url"
                            @click="currentIndex = index"
                        >
                            {{ item.name }}
                        </router-link>
                    </li>
                </ul>
            </div>
            <div>
                <HeaderUserInfoComponent></HeaderUserInfoComponent>
            </div>
        </div>
    </div>
</template>

<style scoped>
.header {
    z-index: 120;
    width: 100%;
    height: 100%;
    background-color: var(--theme-primary-color);
    color: white;
    top: var(--vt-banner-height);
    box-shadow: var(--el-box-shadow);
}

.inner {
    width: var(--main-width);
    height: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin: 0 auto;
    cursor: default;
}

.float-left {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}

ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
}

.header .logo {
    text-decoration: none;
    margin: auto;
    width: 135px;
    height: 50px;
    background-image: url("@/assets/images/logo-white.png");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;
}

.left-ul {
    margin-left: 20px;
    list-style: none;
    font-size: var(--el-font-size-extra-large);
}

.nav-container {
    display: inline;
    height: 100%;
    margin-right: 20px;
}

.left-ul .nav {
    display: inline-block;
    padding: 0 20px;
    outline: none;
    cursor: pointer;
    text-decoration: none;
    transition: color 0.3s;
    color: var(--theme-secondary-color);
    line-height: 60px;
    height: 60px;
}

.left-ul .nav:hover {
    color: var(--theme-third-color);
}

.left-ul .tab_active {
    color: var(--theme-primary-color);
}

.left-ul .tab_active:hover {
    color: var(--theme-secondary-color);
}

.tab_active {
    background: var(--theme-third-color);
    cursor: default;
    font-weight: bold;
}
</style>
