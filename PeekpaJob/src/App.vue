<script setup lang="ts">
import zhCn from "element-plus/es/locale/lang/zh-cn";
</script>

<template>
    <!-- Element Plus 提供了一个 Vue 组件 ConfigProvider 用于全局配置国际化的设置 -->
    <el-config-provider :locale="zhCn">
        <router-view></router-view>
    </el-config-provider>
</template>

<style scoped></style>
