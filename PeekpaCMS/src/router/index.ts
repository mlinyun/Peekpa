import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import ROUTER_CONSTANTS from "@/router/constants.ts";
import PEEKPA_PERMISSION from "@/stores/modules/PermissionConstants";

const LoginPage = () => import("@/pages/user/LoginPage.vue");
const BasePage = () => import("@/pages/BasePage.vue");
const CMSBasePage = () => import("@/pages/CMSBasePage.vue");
const NotFoundPage = () => import("@/pages/exception/NotFoundPage.vue");

const routes: RouteRecordRaw[] = [
    // 登录页面
    {
        path: "/login",
        name: ROUTER_CONSTANTS.LOGIN,
        component: LoginPage,
    },
    {
        path: "/",
        name: "Home",
        component: BasePage,
        redirect: "/dashboard",
        children: [
            // 中控台页面
            {
                path: "dashboard",
                name: ROUTER_CONSTANTS.CMS_DASHBOARD,
                component: CMSBasePage,
                props: {
                    page: ROUTER_CONSTANTS.CMS_DASHBOARD,
                },
            },
            // 职位
            {
                path: "job",
                children: [
                    // 职位发布页面
                    {
                        path: "publish",
                        name: ROUTER_CONSTANTS.CMS_JOB_PUBLISH,
                        component: CMSBasePage,
                        props: {
                            page: ROUTER_CONSTANTS.CMS_JOB_PUBLISH,
                        },
                    },
                    // 职位管理页面
                    {
                        path: "manage",
                        name: ROUTER_CONSTANTS.CMS_JOB_MANAGE,
                        component: CMSBasePage,
                        props: {
                            page: ROUTER_CONSTANTS.CMS_JOB_MANAGE,
                        },
                    },
                ],
            },
            // 面试管理页面
            {
                path: "interview/manage",
                name: ROUTER_CONSTANTS.CMS_INTERVIEW_MANAGE,
                component: CMSBasePage,
                props: {
                    page: ROUTER_CONSTANTS.CMS_INTERVIEW_MANAGE,
                },
            },
            // 人员管理页面
            {
                path: "user",
                children: [
                    {
                        path: "manage",
                        name: ROUTER_CONSTANTS.CMS_USER_MANAGE,
                        component: CMSBasePage,
                        props: {
                            page: ROUTER_CONSTANTS.CMS_USER_MANAGE,
                        },
                    },
                ],
                meta: {
                    requirePermission: [PEEKPA_PERMISSION.MANAGE],
                },
            },
            // 公司管理页面
            {
                path: "company",
                children: [
                    {
                        path: "manage",
                        name: ROUTER_CONSTANTS.CMS_COMPANY_MANAGE,
                        component: CMSBasePage,
                        props: {
                            page: ROUTER_CONSTANTS.CMS_COMPANY_MANAGE,
                        },
                    },
                ],
                meta: {
                    requirePermission: [PEEKPA_PERMISSION.SUPERUSER],
                },
            },
            // 设置页面
            {
                path: "setting",
                name: ROUTER_CONSTANTS.CMS_SETTING,
                component: CMSBasePage,
                props: {
                    page: ROUTER_CONSTANTS.CMS_SETTING,
                },
            },
        ],
    },
    // 404 页面
    {
        path: "/:pathMatch(.*)*",
        name: ROUTER_CONSTANTS.NOTFOUND_404,
        component: NotFoundPage,
        meta: {
            title: "网页未找到 PeekpaCom",
        },
    },
];

// 创建 history 模式的路由
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: routes,
});

export default router;
