<script setup lang="ts">
import userStore from "@/stores/modules/User.ts";
import { userLogout } from "@/services/user";
import { useRouter } from "vue-router";
import ROUTER_CONSTANTS from "@/router/constants.ts";

// 创建用户状态管理
const useUserStore = userStore();

// 获取路由
const router = useRouter();

// 判断是否为超级用户
const isSuperUser = () => {
    return useUserStore.getUser?.is_superuser;
};

// 获取用户名
const username: string | undefined = useUserStore.getUser?.name;

// 用户名下拉菜单选择事件
const handleCommand = async (command: string) => {
    if (command === "logout") {
        try {
            await userLogout();
            useUserStore.logout();
            await router.push({
                name: ROUTER_CONSTANTS.LOGIN,
            });
            ElMessage.success("退出登录成功！");
        } catch (error) {
            ElMessage.error("退出登录失败！");
            useUserStore.logout();
        }
    } else if (command === "setting") {
        try {
            await router.push({
                name: ROUTER_CONSTANTS.CMS_SETTING,
            });
        } catch (error) {
            ElMessage.error("发生错误！");
        }
    }
};
</script>

<template>
    <div class="header">
        <a href="/" class="logo"></a>
        <div class="header_right">
            <div class="header_user_con">
                <el-dropdown class="user_name" trigger="click" @command="handleCommand">
                    <span>
                        <span v-if="isSuperUser()" class="name">超级管理员</span>
                        <span v-else class="name">{{ username }}</span>
                        <el-icon><i-ep-caret-bottom /></el-icon>
                    </span>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item v-if="!isSuperUser()" command="setting">
                                修改资料
                            </el-dropdown-item>
                            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </div>
        </div>
    </div>
</template>

<style scoped>
.header {
    box-sizing: border-box;
    width: 100%;
    /* height: 70px; */
    height: 9%;
    font-size: 1rem;
    background-color: var(--theme-one-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header .logo {
    text-decoration: none;
    margin: auto 0 auto 2%;
    /* width: 135px; */
    width: 14%;
    /* height: 40px; */
    height: 54%;
    background-image: url("@/assets/images/logo-w.png");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center center;
}

.header .header_right {
    float: right;
    /* padding-right: 50px; */
    padding-right: 3%;
}

.header .header_right .header_user_con {
    display: flex;
    /* height: 70px; */
    height: 9%;
    align-items: center;
    cursor: pointer;
}

.header .header_right .user_name {
    color: #ffffff;
}

.header .header_right .name {
    /* margin-right: 10px; */
    margin-right: 0.5rem;
}
</style>
