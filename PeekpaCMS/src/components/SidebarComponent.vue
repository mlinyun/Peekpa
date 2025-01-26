<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import PEEKPA_PERMISSION from "@/stores/modules/PermissionConstants.ts";
import userStore from "@/stores/modules/User.ts";

// 全局路由
const route = useRoute();

// 导航菜单选项接口
interface NavItem {
    icon?: string;
    path: string;
    title: string;
    subgroup?: NavItem[];
    permission?: string;
}

// 导航菜单栏数据列表
// 公司管理员导航菜单
const navList: NavItem[] = [
    {
        icon: "odometer",
        path: "/dashboard",
        title: "首页",
    },
    {
        icon: "document",
        path: "/job",
        title: "职位管理",
        subgroup: [
            {
                path: "/publish",
                title: "职位发布",
            },
            {
                path: "/manage",
                title: "职位管理",
            },
        ],
    },
    {
        icon: "videoCamera",
        path: "/interview/manage",
        title: "面试管理",
    },
    {
        icon: "user",
        path: "/user/manage",
        title: "员工管理",
        permission: PEEKPA_PERMISSION.MANAGE,
    },
    {
        icon: "setting",
        path: "/setting",
        title: "修改资料",
    },
];

// 超级管理员导航菜单
const superuserNavList: NavItem[] = [
    {
        icon: "house",
        path: "/company/manage",
        title: "公司管理",
    },
];

// 菜单图标
enum MenuIcon {
    odometer = IconEpOdometer,
    document = IconEpDocument,
    videoCamera = IconEpVideoCamera,
    user = IconEpUser,
    setting = IconEpSetting,
    house = IconEpHouse,
}

// 获取图标组件
const resolveIcon = (icon: string): MenuIcon | undefined => {
    return MenuIcon[icon as keyof typeof MenuIcon];
};

const navItems = ref<NavItem[]>([]);

// 默认激活菜单的 index
const onRoutes = computed(() => {
    return route.path;
});

const useUserStore = userStore();

watch(
    () => useUserStore.token,
    (newValue) => {
        if (!newValue) {
            navItems.value = [];
        } else if (useUserStore.getUser?.is_superuser) {
            navItems.value = superuserNavList;
        } else {
            navList.forEach((item: NavItem) => {
                if (item.permission) {
                    const userPermission = useUserStore.getUser;
                    if (userPermission && userPermission.is_manager) {
                        const temp: NavItem = {
                            icon: item.icon,
                            path: item.path,
                            title: item.title,
                            subgroup: item.subgroup,
                        };
                        navItems.value.push(temp);
                    }
                } else {
                    navItems.value.push(item);
                }
            });
        }
    },
    { immediate: true, deep: true },
);
</script>

<template>
    <div class="sidebar">
        <el-menu
            class="sidebar-el-menu"
            :default-active="onRoutes"
            background-color="var(--theme-one-color)"
            text-color="var(--theme-four-color)"
            active-text-color="var(--theme-three-color)"
            unique-opened
            router
        >
            <template v-for="item in navItems" :key="item.path">
                <el-sub-menu v-if="item.subgroup" :index="item.path">
                    <template #title>
                        <el-icon v-if="item.icon">
                            <component :is="resolveIcon(item.icon)" />
                        </el-icon>
                        <span>{{ item.title }}</span>
                    </template>
                    <el-menu-item-group v-if="item.subgroup">
                        <el-menu-item
                            v-for="sub in item.subgroup"
                            :key="sub.path"
                            :index="`${item.path}${sub.path}`"
                        >
                            {{ sub.title }}
                        </el-menu-item>
                    </el-menu-item-group>
                </el-sub-menu>
                <el-menu-item v-else :index="item.path">
                    <el-icon v-if="item.icon">
                        <component :is="resolveIcon(item.icon)" />
                    </el-icon>
                    <template #title>{{ item.title }}</template>
                </el-menu-item>
            </template>
        </el-menu>
    </div>
</template>

<style scoped>
.sidebar {
    display: block;
    position: absolute;
    left: 0;
    /* top: 70px; */
    top: 9%;
    right: 0;
    bottom: 0;
    overflow-y: scroll;
}

.sidebar::-webkit-scrollbar {
    width: 0;
}

.sidebar-el-menu:not(.el-menu--collapse) {
    /* width: 250px; */
    width: 18%;
}

.sidebar > ul {
    height: 100%;
}
</style>
