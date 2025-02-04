<script setup lang="ts">
import HeaderComponent from "@/components/HeaderComponent/index.vue";
</script>

<template>
    <el-container class="peekpa-container">
        <!-- 此处应该是 HeaderComponent 组件 -->
        <el-header class="peekpa-header">
            <HeaderComponent></HeaderComponent>
        </el-header>
        <el-main class="peekpa-main">
            <router-view></router-view>
        </el-main>
        <!-- 此处应该是 footer 组件 -->
        <el-footer class="peekpa-footer">
            <FooterComponent></FooterComponent>
        </el-footer>
    </el-container>
</template>

<style scoped>
.peekpa-container {
    height: 100%;
}

.peekpa-header {
    padding: 0;
    width: 100%;
    position: fixed;
    z-index: 999;
}

.peekpa-main {
    width: var(--main-width);
    margin: 60px auto 0 auto;
    padding-left: 0;
    padding-right: 0;
    overflow: visible;
}

.peekpa-footer {
    padding: 0;
    height: 170px;
}
</style>
