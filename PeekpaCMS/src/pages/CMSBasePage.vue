<script setup lang="ts">
// Component 是一个类型，必须使用类型导入语法进行导入
import { type Component, defineAsyncComponent, onBeforeMount, watch } from "vue";
import ROUTER_CONSTANTS from "@/router/constants.ts";

// withDefaults 是一个函数，用于合并默认属性和传入的属性
const props = withDefaults(
    defineProps<{
        page: string;
    }>(),
    {
        page: ROUTER_CONSTANTS.CMS_DASHBOARD,
    },
);
// 通过 props.page 的值来动态加载不同的组件
let currentComponent: Component | null = null;

const baseLoadingComponentConfig = {
    timeout: 10000,
};

const loadPage = () => {
    switch (props.page) {
        case ROUTER_CONSTANTS.CMS_JOB_MANAGE:
            currentComponent = defineAsyncComponent({
                loader: () => import("./job/JobManagePage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
        case ROUTER_CONSTANTS.CMS_JOB_PUBLISH:
            currentComponent = defineAsyncComponent({
                loader: () => import("./job/JobPublishPage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
        case ROUTER_CONSTANTS.CMS_SETTING:
            currentComponent = defineAsyncComponent({
                loader: () => import("./setting/SettingPage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
        case ROUTER_CONSTANTS.CMS_INTERVIEW_MANAGE:
            currentComponent = defineAsyncComponent({
                loader: () => import("./interview/InterviewManagePage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
        case ROUTER_CONSTANTS.CMS_USER_MANAGE:
            currentComponent = defineAsyncComponent({
                loader: () => import("./user/UserManagePage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
        case ROUTER_CONSTANTS.CMS_COMPANY_MANAGE:
            currentComponent = defineAsyncComponent({
                loader: () => import("./company/CompanyManagePage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
        default:
            currentComponent = defineAsyncComponent({
                loader: () => import("./dashboard/DashboardPage.vue"),
                ...baseLoadingComponentConfig,
            });
            break;
    }
};

onBeforeMount(() => {
    loadPage();
});

watch(
    () => props.page,
    () => {
        loadPage();
    },
    {},
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
}
</style>
