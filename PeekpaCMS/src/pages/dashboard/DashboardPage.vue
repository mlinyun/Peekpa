<script setup lang="ts">
import ClockComponent from "@/components/ClockComponent.vue";
import DashboardCardComponent from "@/components/DashboardCardComponent.vue";
import type { DashboardResponse } from "@/types/Dashboard.ts";
import getDashboard from "@/services/dashboard";
import { UNAUTH_401 } from "@/services/Axios.ts";
import { timeStampFormat } from "@/utils/Helper.ts";

const data = ref<DashboardResponse>();
const loading = ref<boolean>(false);

// 请求首页数据
const requestDashboardData = async () => {
    loading.value = true;
    try {
        const response = await getDashboard();
        if (response.status === 200) {
            data.value = response.data;
        }
        loading.value = false;
    } catch (error) {
        if ((error as Error).message === UNAUTH_401) {
            ElMessage.error(`首页数据请求错误${error}`);
        }
        loading.value = false;
    }
};

// 页面加载时请求首页数据
onMounted(async () => {
    await requestDashboardData();
});

// 定时刷新首页数据
setInterval(
    async () => {
        await requestDashboardData();
    },
    1000 * 60 * 5,
);

// TODO: 以下方法需要根据实际业务逻辑进行修改
const getUrl = (id: string) => {
    return `http://localhost:8081/api/job/${id}`;
};

// 格式化显示时间
const displayTime = (time: string) => {
    return timeStampFormat(time);
};
</script>

<template>
    <div class="dashboard">
        <el-row :gutter="20" class="dashboard_row">
            <el-col :span="6">
                <clock-component />
            </el-col>
            <el-col :span="6">
                <dashboard-card-component
                    title="今日新增简历"
                    :count="data?.resumes_new ?? 0"
                    icon="box"
                />
            </el-col>
            <el-col :span="6">
                <dashboard-card-component
                    title="已经招聘人数"
                    :count="data?.pass_number ?? 0"
                    icon="goldMedal"
                />
            </el-col>
            <el-col :span="6">
                <dashboard-card-component
                    title="预计招聘人数"
                    :count="data?.hired_number ?? 0"
                    icon="medal"
                />
            </el-col>
        </el-row>
        <el-row :gutter="20" class="dashboard_row">
            <el-col :span="6">
                <dashboard-card-component
                    title="职位总数"
                    :count="data?.jobs_total ?? 0"
                    icon="folder"
                />
            </el-col>
            <el-col :span="6">
                <dashboard-card-component
                    title="开放职位"
                    :count="data?.jobs_open ?? 0"
                    icon="folderOpened"
                />
            </el-col>
            <el-col :span="6">
                <dashboard-card-component
                    title="已招满职位"
                    :count="data?.jobs_finish ?? 0"
                    icon="folderChecked"
                />
            </el-col>
            <el-col :span="6">
                <dashboard-card-component
                    title="已下线职位"
                    :count="data?.jobs_close ?? 0"
                    icon="folderDelete"
                />
            </el-col>
        </el-row>
        <el-row :gutter="20" class="dashboard_row">
            <el-col :span="6">
                <dashboard-card-component
                    title="共收到简历"
                    :count="data?.resumes ?? 0"
                    icon="notebook"
                />
            </el-col>
            <el-col :span="6">
                <dashboard-card-component
                    title="面试人数"
                    :count="data?.interviewing ?? 0"
                    icon="dataLine"
                />
            </el-col>
            <el-col :span="6">
                <dashboard-card-component
                    title="发出邀请数"
                    :count="data?.invitation_number ?? 0"
                    icon="stopwatch"
                />
            </el-col>
            <el-col :span="6">
                <dashboard-card-component
                    title="公司总人数"
                    :count="data?.users_number ?? 0"
                    icon="user"
                />
            </el-col>
        </el-row>
        <el-row :gutter="20" class="dashboard_row">
            <el-col :span="12">
                <div class="table-title">最新职位信息</div>
                <el-table border header-cell-class-name="table-header" :data="data?.new_jobs">
                    <el-table-column label="职位名称" prop="title">
                        <template #default="scope">
                            <el-link type="primary" target="_blank" :href="getUrl(scope.row.id)">
                                {{ scope.row.title }}
                            </el-link>
                        </template>
                    </el-table-column>
                    <el-table-column label="发布日期" prop="publish_time" width="200">
                        <template #default="scope">
                            <span>{{ displayTime(scope.row.publish_time) }}</span>
                        </template>
                    </el-table-column>
                </el-table>
            </el-col>
            <el-col :span="12">
                <div class="table-title">最新简历岗位</div>
                <el-table border header-cell-class-name="table-header" :data="data?.new_interviews">
                    <el-table-column label="职位名称" prop="title">
                        <template #default="scope">
                            <el-link type="primary" target="_blank" :href="getUrl(scope.row.id)">
                                {{ scope.row.title }}
                            </el-link>
                        </template>
                    </el-table-column>
                    <el-table-column label="发布日期" prop="publish_time" width="200">
                        <template #default="scope">
                            <span>{{ displayTime(scope.row.publish_time) }}</span>
                        </template>
                    </el-table-column>
                </el-table>
            </el-col>
        </el-row>
    </div>
</template>

<style scoped>
.dashboard {
    padding: 2%;
    background-color: #ffffff;
    border: 1px solid #dddddd;
    border-radius: 5px;
}

.dashboard_row {
    margin-bottom: 20px;
}

.table-title {
    margin-bottom: 15px;
    font-weight: 600;
    font-size: 1.3rem;
}
</style>
