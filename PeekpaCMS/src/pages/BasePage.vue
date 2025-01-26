<script setup lang="ts">
import { onMounted } from "vue";
// import { ElMessage } from "element-plus/es";
import { useRouter } from "vue-router";
import userStore from "@/stores/modules/User.ts";
import ROUTER_CONSTANTS from "@/router/constants.ts";
import HeaderComponent from "@/components/HeaderComponent.vue";
import SidebarComponent from "@/components/SidebarComponent.vue";

// 创建用户状态管理
const useUserStore = userStore();
// 创建全局路由
const router = useRouter();

// 第一次进入页面时，判断用户是否已经登录，如果没有登录，则跳转到登录页面
onMounted(() => {
    if (!useUserStore.isLogin()) {
        ElMessage.error("请先登录");
        router.push({
            name: ROUTER_CONSTANTS.LOGIN,
        });
    }
});
</script>

<template>
    <header-component />
    <sidebar-component />
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
    /* left: 250px; */
    left: 18%;
    right: 0;
    top: 9%;
    /* top: 70px; */
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
