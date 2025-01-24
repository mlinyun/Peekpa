<script setup lang="ts">
import { onMounted } from "vue";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import userStore from "@/stores/modules/User.ts";
import ROUTER_CONSTANTS from "@/router/constants.ts";

// 创建用户状态管理
const user = userStore();
// 创建全局路由
const router = useRouter();

// 第一次进入页面时，判断用户是否已经登录，如果没有登录，则跳转到登录页面
onMounted(() => {
    if (!user.isLogin) {
        ElMessage.warning("请先登录");
        router.push({
            name: ROUTER_CONSTANTS.LOGIN,
        });
    }
});
</script>

<template>
    <v-header></v-header>
    <v-sidebar></v-sidebar>
    <div class="content-box">
        <div class="content">
            <router-view v-slot="{ Component }">
                <transition name="move" mode="out-in">
                    <component :is="Component" />
                </transition>
            </router-view>
        </div>
    </div>
</template>

<style scoped>
.content-box {
    position: absolute;
    left: 250px;
    right: 0;
    top: 70px;
    bottom: 0;
    -webkit-transition: left 0.3s ease-in-out;
    transition: left 0.3s ease-in-out;
    background: #f0f0f0;
}

.content {
    width: auto;
    height: 100%;
    padding: 10px;
    overflow-y: scroll;
    box-sizing: border-box;
}
</style>
