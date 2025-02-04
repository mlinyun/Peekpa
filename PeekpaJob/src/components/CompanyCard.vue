<script setup lang="ts">
import type { Company } from "@/types/Company.ts";

// 定义组件的 props
const props = defineProps<{
    company: Company; // 公司信息
}>();

// 格式化显示公司标签
const displayCompanyTags = computed(() => {
    return props.company.tags.replace(new RegExp(",", "g"), "|");
});

// TODO: 公司详情页地址
const getCompanyUrl = computed(() => {
    return `http://localhost:8081/api/company/${props.company.id}`;
});

// TODO: 公司头像地址
const getCompanyAvatar = computed(() => {
    return `http://localhost:8081/${props.company.avatar}`;
});
</script>

<template>
    <el-col :span="6">
        <el-card shadow="hover" :body-style="{ padding: '20px' }" class="card">
            <div class="first-line">
                <el-image class="image" :src="getCompanyAvatar" fit="fill">
                    <template #placeholder>
                        <div class="image-slot">Loading<span class="dot">...</span></div>
                    </template>
                </el-image>
                <div>
                    <el-link class="company-name" :href="getCompanyUrl" target="_blank">
                        {{ company.name }}
                    </el-link>
                </div>
                <div class="company-tag">{{ displayCompanyTags }}</div>
                <div class="company-slogan">{{ company.slogan }}</div>
            </div>
            <div class="second-line">
                <a :href="getCompanyUrl" target="_blank" class="bottom-item">
                    <div>{{ company.jobs }}</div>
                    <div class="bottom-text">招聘岗位</div>
                </a>
                <div class="bottom-line"></div>
                <a :href="getCompanyUrl" target="_blank" class="bottom-item">
                    <div>{{ company.interviews }}</div>
                    <div class="bottom-text">正在面试</div>
                </a>
            </div>
        </el-card>
    </el-col>
</template>

<style scoped>
.card {
    margin-top: 20px;
    width: 100%;
}

.first-line {
    text-align: center;
    border-bottom: 1px dashed rgb(224, 224, 224);
}

.image {
    width: 80px;
    height: 80px;
}

.image-slot {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    background: var(--el-fill-color-light);
    color: var(--el-text-color-secondary);
    font-size: 14px;
}

.company-name {
    font-size: 1.1rem;
    font-weight: bold;
    color: var(--theme-primary-color);
}

.company-tag {
    min-height: 22px;
    margin: 5px 0;
    font-weight: 300;
    color: #6f6f6f;
}

.company-slogan {
    min-height: 22px;
    margin-bottom: 10px;
}

.second-line {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-top: 10px;
    text-align: center;
}

.bottom-item {
    font-size: 1rem;
    text-decoration: none;
}

.bottom-item:hover {
    color: var(--theme-primary-color);
}

.bottom-text {
    color: #6f6f6f;
}

.bottom-text:hover {
    color: var(--theme-primary-color);
}

.bottom-line {
    top: 0;
    right: 0;
    width: 1px;
    background: #ededed;
}
</style>
