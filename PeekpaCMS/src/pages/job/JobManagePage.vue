<script setup lang="ts">
import { ref, onMounted } from "vue";
import type { Job, JobListResponse, UpdateJobForm } from "@/types/Job.ts";
import { timeStampFormat } from "@/utils/Helper.ts";
import { getAllJobs, searchJob, updateJob } from "@/services/job";
import ROUTER_CONSTANTS from "@/router/constants.ts";
import { useRouter } from "vue-router";
import { UNAUTH_401 } from "@/services/Axios.ts";
import { ElMessageBox, type FormInstance, type InputInstance } from "element-plus";
import type { AxiosError } from "axios";
import JobPublishForm from "@/pages/job/components/JobPublishForm.vue";

const updateJobForm = reactive<UpdateJobForm>({
    index: -1,
    id: "-1",
    title: "",
    status: -1,
    city: "",
    location: "",
    salary_min: -1,
    salary_max: -1,
    salary_count: -1,
    hire_number: -1,
    pass_number: -1,
    experience: "",
    benefit: "",
    education: "",
    description: "",
    publish_time: "",
    resumes: 0,
});

// 全局路由
const router = useRouter();

const LIMIT = 10;
let curOffset = 0;

const STATUS_LIST_JOB = [
    {
        value: 0,
        label: "已发布",
    },
    {
        value: 1,
        label: "已下线",
    },
    {
        value: 2,
        label: "已结束",
    },
];

const search = ref<string>("");
const loading = ref<boolean>(false);
const data = ref<JobListResponse>();
const curPage = ref<number>(1);
const total = ref<number>(0);
const showUpdate = ref<boolean>(false);
const updateFormRef = ref<FormInstance>();
const dialogInput = ref<InputInstance>();

// 请求职位数据
const requestJobData = async (offset: number) => {
    loading.value = true;
    try {
        const response = await getAllJobs(LIMIT, offset);
        if (response.status === 200) {
            data.value = response.data;
            total.value = response.data.count;
            curPage.value = Math.floor(offset / LIMIT) + 1;
        }
        loading.value = false;
    } catch (error) {
        if ((error as Error).message === UNAUTH_401) {
            ElMessage.error(`职位列表数据请求错误${error}`);
        }
        loading.value = false;
    }
};

// 搜索职位数据
const searchJobData = async (q: string, offset: number) => {
    loading.value = true;
    try {
        const response = await searchJob(q, LIMIT, offset);
        if (response.status === 200) {
            data.value = response.data;
            total.value = response.data.count;
            curPage.value = Math.floor(offset / LIMIT) + 1;
        }
        loading.value = false;
    } catch (error) {
        if ((error as Error).message === UNAUTH_401) {
            ElMessage.error(`搜索职位数据请求错误${error}`);
        }
        loading.value = false;
    }
};

// 页面加载时请求职位数据
onMounted(async () => {
    await requestJobData(curOffset);
});

// 搜索职位方法
const handleSearch = async () => {
    curOffset = 0;
    await searchJobData(search.value, curOffset);
};

// 清空搜索方法
const clearSearch = async () => {
    search.value = "";
    curOffset = 0;
    await requestJobData(curOffset);
};

// 显示薪资
const displaySalary = (item: Job) => {
    const max = Number((item.salary_max / 1000).toFixed(1));
    const min = Number((item.salary_min / 1000).toFixed(1));
    return max === min
        ? `${max}k/月 ${item.salary_count}薪`
        : `${min}k~${max}k/月 ${item.salary_count}薪`;
};

// 显示职位招聘进度
const displayProgress = (item: Job) => {
    return `${item.pass_number} / ${item.hire_number}`;
};

// 时间格式化方法
const displayTime = (time: string) => {
    if (!time) return time;
    return timeStampFormat(time);
};

// 禁止职位修改
const disabledOperation = (item: Job) => {
    return item.status === 1 || item.status === 2;
};

// 修改职位状态
const handleStatusChange = async (status: number, id: string) => {
    try {
        const response = await updateJob(id, { status });
        if (response.status === 200) {
            ElMessage.success("更新成功！");
        } else {
            ElMessage.error("更新失败！");
        }
    } catch (error) {
        ElMessage.error("发生错误！");
    }
};

// 跳转到面试管理页面
const showInterviewMangePage = (id: string) => {
    router.push({
        name: ROUTER_CONSTANTS.CMS_INTERVIEW_MANAGE,
        query: { job_id: id },
    });
};

// 显示修改对话框
const showUpdateWindow = (index: number, item: Job) => {
    // console.log("index", index, "item", item);
    showUpdate.value = true;
    updateJobForm.index = index;
    updateJobForm.id = item.id;
    updateJobForm.title = item.title;
    updateJobForm.status = item.status;
    updateJobForm.city = item.city;
    updateJobForm.location = item.location;
    updateJobForm.salary_count = item.salary_count;
    updateJobForm.salary_min = item.salary_min;
    updateJobForm.salary_max = item.salary_max;
    updateJobForm.hire_number = item.hire_number;
    updateJobForm.pass_number = item.pass_number;
    updateJobForm.education = item.education;
    updateJobForm.experience = item.experience;
    updateJobForm.benefit = item.benefit;
    updateJobForm.description = item.description;
    updateJobForm.publish_time = item.publish_time;
    updateJobForm.resumes = item.resumes;
};

// 职位下线操作
const handleDeleteJob = (index: number, item: Job) => {
    // console.log("index", index, "item", item);
    ElMessageBox.confirm(`确定要下线${item.title}职位么？`, "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "error",
    })
        .then(async () => {
            const response = await updateJob(item.id, { status: STATUS_LIST_JOB[2].value });
            if (response.status === 200) {
                ElMessage.success("下线成功！");
                if (data.value) {
                    data.value.results[index].status = STATUS_LIST_JOB[2].value;
                }
            } else {
                ElMessage.error(`下线失败${response.status}！`);
            }
        })
        .catch((error) => {
            if ((error as AxiosError).name === "CanceledError" && error === "cancel") {
                ElMessage.error("发生网络错误！");
            }
        });
};

// 页面跳转方法
const handlePageChange = async (page: number) => {
    curOffset = (page - 1) * LIMIT;
    await requestJobData(curOffset);
};

// 处理对话框焦点方法
const handleDialogOpen = () => {
    nextTick(() => {
        if (dialogInput.value) {
            dialogInput.value.focus();
        }
    });
};

// 职位修改功能
const handleUpdateJob = async (formEl: FormInstance | undefined) => {
    if (!formEl) {
        return;
    }
    await formEl.validate(async (valid: boolean) => {
        if (valid) {
            try {
                const updateData: { [key: string]: string | number } = {};
                Object.entries(updateJobForm).forEach(([key, value]) => {
                    if (typeof value === "string" || typeof value === "number") {
                        updateData[key] = value;
                    }
                });
                const response = await updateJob(updateJobForm.id, updateData);
                if (response.status === 200) {
                    ElMessage.success("职位修改成功！");
                    showUpdate.value = false;
                    const { index } = updateJobForm;
                    if (data.value) {
                        // 更新列表数据
                        data.value.results[index] = response.data;
                    }
                    updateData.index = -1;
                    // 清空表单
                    formEl.resetFields();
                } else {
                    ElMessage.error(`职位修改失败[${response.status}]！`);
                }
            } catch (error) {
                ElMessage.error(`职位修改失败[${(error as AxiosError).message}]！`);
            }
        } else {
            ElMessage.error("请仔细检查表单！");
        }
    });
};
</script>

<template>
    <div class="job-manage">
        <el-row class="search_main">
            <el-col :span="6" :offset="18">
                <el-input
                    v-model="search"
                    placeholder="搜索"
                    clearable
                    @keyup.enter="handleSearch()"
                    @clear="clearSearch"
                >
                    <template #prefix>
                        <el-icon class="el-icon__icon">
                            <i-ep-search />
                        </el-icon>
                    </template>
                </el-input>
            </el-col>
        </el-row>
        <el-table
            v-model="loading"
            border
            header-cell-class-name="table-header"
            :data="data?.results"
        >
            <el-table-column label="ID" prop="id" width="60"></el-table-column>
            <el-table-column label="职位名称" prop="name">
                <template #default="scope">
                    <el-link type="primary">{{ scope.row.title }}</el-link>
                </template>
            </el-table-column>
            <el-table-column label="薪资">
                <template #default="scope">
                    {{ displaySalary(scope.row) }}
                </template>
            </el-table-column>
            <el-table-column label="收到简历" prop="resumes" width="100">
                <template #default="scope">{{ scope.row.resumes }} 份</template>
            </el-table-column>
            <el-table-column label="招聘进度" width="100">
                <template #default="scope">
                    {{ displayProgress(scope.row) }}
                </template>
            </el-table-column>
            <el-table-column label="状态" prop="status" width="100">
                <template #default="scope">
                    <el-select
                        v-model="scope.row.status"
                        :disabled="disabledOperation(scope.row)"
                        size="small"
                        @change="handleStatusChange($event, scope.row.id)"
                    >
                        <el-option
                            v-for="item in STATUS_LIST_JOB"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column label="创建时间" prop="publish_time" width="170">
                <template #default="scope">
                    {{ displayTime(scope.row.publish_time) }}
                </template>
            </el-table-column>
            <el-table-column width="270">
                <template #header>
                    <div class="flex-space-between">
                        <div>操作</div>
                    </div>
                </template>
                <template #default="scope">
                    <el-button
                        type="primary"
                        size="small"
                        plain
                        :disabled="disabledOperation(scope.row)"
                        @click="showInterviewMangePage(scope.row.id)"
                    >
                        <el-icon>
                            <i-ep-document />
                        </el-icon>
                        面试管理
                    </el-button>
                    <el-button
                        type="warning"
                        size="small"
                        plain
                        :disabled="disabledOperation(scope.row)"
                        @click="showUpdateWindow(scope.$index, scope.row)"
                    >
                        <el-icon>
                            <i-ep-setting />
                        </el-icon>
                        修改
                    </el-button>
                    <el-button
                        type="danger"
                        size="small"
                        plain
                        :disabled="disabledOperation(scope.row)"
                        @click="handleDeleteJob(scope.$index, scope.row)"
                    >
                        <el-icon>
                            <i-ep-delete />
                        </el-icon>
                        下线
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination
            class="pagination_main"
            background
            layout="prev, pager, next"
            :current-page="curPage"
            :total="total"
            :page-size="LIMIT"
            @current-change="handlePageChange"
        ></el-pagination>
        <el-dialog v-model="showUpdate" title="修改职位信息" width="60%" @open="handleDialogOpen">
            <job-publish-form
                label_position="left"
                :model="updateJobForm"
                @update:model="updateFormRef = $event"
            ></job-publish-form>
            <template #footer>
                <el-button @click="showUpdate = false">取 消</el-button>
                <el-button type="primary" @click="handleUpdateJob(updateFormRef)">
                    提 交
                </el-button>
            </template>
        </el-dialog>
    </div>
</template>

<style scoped>
.job-manage {
    padding: 2%;
    background-color: #ffffff;
    border: 1px solid #dddddd;
    border-radius: 5px;
}

.search_main {
    margin-bottom: 2%;
}

.flex-space-between {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.el-button .el-icon {
    margin-right: 5%;
}

.pagination_main {
    margin-top: 2%;
}
</style>
