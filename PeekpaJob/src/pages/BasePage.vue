<script setup lang="ts"></script>

<template>
    <el-container class="peekpa_container">
        <!-- 此处应该是 header 组件 -->
        <el-main class="peekpa_main">
            <router-view></router-view>
        </el-main>
        <!-- 此处应该是 footer 组件 -->
    </el-container>
</template>

<style scoped>
.peekpa_container {
    height: 100%;
}

.peekpa_main {
    width: var(--main-width);
    margin: 60px auto 0 auto;
    padding-left: 0;
    padding-right: 0;
    overflow: visible;
}
</style>
