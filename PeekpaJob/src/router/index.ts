import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import ROUTER_CONSTANTS from "@/router/constants.ts";

const IndexBasePage = () => import("@/pages/IndexBasePage.vue");
const BasePage = () => import("@/pages/BasePage.vue");
const NotFoundPage = () => import("@/pages/exception/NotFoundPage.vue");

const routes: RouteRecordRaw[] = [
    {
        path: "/",
        name: "Home",
        component: BasePage,
        redirect: "/index",
        children: [
            // 首页
            {
                path: "index",
                name: ROUTER_CONSTANTS.INDEX,
                component: IndexBasePage,
            },
            // 职位列表页
            {
                path: "jobs",
                name: ROUTER_CONSTANTS.JOB_LIST,
                component: IndexBasePage,
            },
            // 职位详情页
            {
                path: "job/:jobId",
                name: ROUTER_CONSTANTS.JOB_DETAIL,
                component: IndexBasePage,
            },
            // 公司列表页
            {
                path: "companies",
                name: ROUTER_CONSTANTS.COMPANY_LIST,
                component: IndexBasePage,
            },
            // 公司详情页
            {
                path: "company/:companyId",
                name: ROUTER_CONSTANTS.COMPANY_DETAIL,
                component: IndexBasePage,
            },
            // 个人信息页
            {
                path: "profile",
                name: ROUTER_CONSTANTS.PROFILE,
                component: IndexBasePage,
            },
            // 登录页
            {
                path: "signin",
                name: ROUTER_CONSTANTS.SIGN_IN,
                component: IndexBasePage,
            },
            // 注册页
            {
                path: "signup",
                name: ROUTER_CONSTANTS.SIGN_UP,
                component: IndexBasePage,
            },
            // 404 页面
            {
                path: "/:pathMatch(.*)*",
                name: ROUTER_CONSTANTS.NOTFOUND_404,
                component: NotFoundPage,
                meta: {
                    title: "网页未找到 PeekpaJob",
                },
            },
        ],
    },
];

// 创建 history 模式的路由
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: routes,
});

export default router;
