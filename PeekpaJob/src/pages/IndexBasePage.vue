<script setup lang="ts">
import { type Component } from "vue";
import { useRoute } from "vue-router";
import ROUTER_CONSTANTS from "@/router/constants.ts";

// 路由对象
const route = useRoute();

let currentComponent: Component;

const baseLoadingComponentConfig = {
    timeout: 10000,
};

// 根据路由名称加载不同的组件
const loadPage = (key: string) => {
    switch (key) {
        case ROUTER_CONSTANTS.JOB_LIST:
            currentComponent = defineAsyncComponent({
                loader: () => import("@/pages/job/JobListPage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
        case ROUTER_CONSTANTS.JOB_DETAIL:
            currentComponent = defineAsyncComponent({
                loader: () => import("@/pages/job/JobDetailPage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
        case ROUTER_CONSTANTS.COMPANY_LIST:
            currentComponent = defineAsyncComponent({
                loader: () => import("@/pages/company/CompanyListPage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
        case ROUTER_CONSTANTS.COMPANY_DETAIL:
            currentComponent = defineAsyncComponent({
                loader: () => import("@/pages/company/CompanyDetailPage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
        case ROUTER_CONSTANTS.SIGN_IN:
            currentComponent = defineAsyncComponent({
                loader: () => import("@/pages/user/SignInPage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
        case ROUTER_CONSTANTS.SIGN_UP:
            currentComponent = defineAsyncComponent({
                loader: () => import("@/pages/user/SignUpPage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
        case ROUTER_CONSTANTS.PROFILE:
            currentComponent = defineAsyncComponent({
                loader: () => import("@/pages/user/ProfilePage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
        default:
            currentComponent = defineAsyncComponent({
                loader: () => import("@/pages/index/IndexPage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
    }
};

onBeforeMount(() => {
    loadPage(route.name as string);
});

onUpdated(() => {
    loadPage(route.name as string);
});

watch(
    () => route.name,
    (newValue) => {
        loadPage(newValue as string);
    },
    { immediate: true, deep: true },
);
</script>

<template>
    <div class="base_container">
        <currentComponent></currentComponent>
    </div>
</template>

<style scoped>
.base_container {
    min-height: calc(100vh - 170px - 60px - 40px);
    display: flex;
    flex-direction: column;
    justify-content: center;
}
</style>
