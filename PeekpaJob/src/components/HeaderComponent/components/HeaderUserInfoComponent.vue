<script setup lang="ts">
import userStore from "@/stores/modules/User.ts";
import { userLogout } from "@/services/user";
import type { AxiosError } from "axios";

// 用户状态管理
const useUserStore = userStore();

// username 计算属性，从用户状态管理中获取
const username = computed(() => {
    const user = useUserStore.getUser;
    if (user) {
        return user.name;
    } else {
        return "null";
    }
});

// 用户登出操作
const handleLogout = async () => {
    try {
        await userLogout();
        useUserStore.logout();
    } catch (error) {
        ElMessage.error(`退出登录失败[${(error as AxiosError).message}]！`);
    }
};
</script>

<template>
    <div class="header-user-info">
        <ul v-if="useUserStore.isLogin()" class="account_bar">
            <li>
                <a href="/public/profile" class="username">{{ username }}</a>
            </li>
            <li>
                <a href="/" class="logout" @click.prevent="handleLogout">登出</a>
            </li>
        </ul>
        <ul v-else class="login_register">
            <li>
                <a href="/signin">登录</a>
            </li>
            <li>
                <span class="diver">|</span>
            </li>
            <li>
                <a href="/signup">注册</a>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.account_bar {
    list-style: none;
}

.account_bar li {
    position: relative;
    text-align: center;
    float: left;
}

.account_bar li a {
    display: inline-block;
    height: 40px;
    line-height: 60px;
    padding-left: 20px;
    text-decoration: none;
}

.login_register {
    list-style: none;
}

.login_register li {
    position: relative;
    text-align: center;
    float: left;
}

.diver {
    padding: 0 15px;
    color: #5e6166;
    line-height: 60px;
    text-align: center;
}

.login_register li a {
    display: inline-block;
    height: 60px;
    line-height: 60px;
    color: var(--theme-secondary-color);
    text-decoration: none;
    transition: color 0.3s;
}

.login_register a:hover {
    color: var(--theme-third-color);
}

.username {
    color: var(--theme-third-color);
    font-weight: bolder;
    font-size: 1.1rem;
}

.logout {
    color: var(--theme-secondary-color);
}
</style>
