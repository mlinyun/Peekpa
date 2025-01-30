<script setup lang="ts">
import { ref } from "vue";
import type { FormInstance } from "element-plus";
import type { JobCreate } from "@/types/Job.ts";
import { createJob } from "@/services/job";
import type { AxiosError } from "axios";
import JobPublishForm from "@/pages/job/components/JobPublishForm.vue";

const ruleFormRef = ref<FormInstance>();
const loading = ref<boolean>(false);
const doubleCheck = ref<boolean>(false);

const jobPublishForm = reactive<JobCreate>({
    title: "",
    status: 0,
    city: "",
    location: "",
    salary_min: 0,
    salary_max: 0,
    salary_count: 12,
    hire_number: 1,
    experience: "不需要经验",
    benefit: "",
    description: "",
    education: "",
});

// 跳转到职位发布确认页面
const goToDoubleCheck = async () => {
    if (!ruleFormRef.value) {
        return;
    }
    await ruleFormRef.value.validate(async (valid: boolean) => {
        if (valid) {
            doubleCheck.value = true;
        } else {
            ElMessage.error("请检查表单数据是否填写正确！");
            loading.value = false;
        }
    });
};

// 重置表单数据
const resetForm = () => {
    if (ruleFormRef.value) {
        ruleFormRef.value.resetFields();
    }
};

// 提交表单数据
const submitForm = async () => {
    loading.value = true;
    try {
        const response = await createJob(jobPublishForm);
        if (response.status === 201) {
            ElMessage.success("职位发布成功！");
            doubleCheck.value = false;
            // 重置表单数据
            resetForm();
        } else {
            ElMessage.error(`职位发布失败[${response.status}].`);
        }
        loading.value = false;
    } catch (error) {
        ElMessage.error(`职位发布失败[${(error as AxiosError).message}].`);
        loading.value = false;
    }
};

// 关闭确认发布弹窗
const closeDialog = () => {
    doubleCheck.value = false;
};

// 显示薪资范围
const displaySalary = computed(() => {
    if (jobPublishForm.salary_min === 0 && jobPublishForm.salary_max === 0) {
        return "面议";
    } else if (jobPublishForm.salary_max === jobPublishForm.salary_min) {
        return `${jobPublishForm.salary_min} 元/月 ${jobPublishForm.salary_count}薪`;
    } else {
        return `${jobPublishForm.salary_min} ~ ${jobPublishForm.salary_max} 元/月 ${jobPublishForm.salary_count}薪`;
    }
});
</script>

<template>
    <div class="job-publish">
        <job-publish-form
            label_position="top"
            :model="jobPublishForm"
            @update:model="ruleFormRef = $event"
        >
            <template #submit>
                <el-form-item>
                    <el-button type="primary" @click="goToDoubleCheck">确定</el-button>
                    <el-button @click="resetForm">重置</el-button>
                </el-form-item>
            </template>
        </job-publish-form>
        <el-dialog v-model="doubleCheck" title="确定发布职位么" width="60%">
            <el-form
                v-model="loading"
                :model="jobPublishForm"
                label-width="auto"
                label-position="right"
            >
                <el-form-item label="职位名称">
                    <span>{{ jobPublishForm.title }}</span>
                </el-form-item>
                <el-form-item label="工作城市">
                    <span>{{ jobPublishForm.city }}</span>
                </el-form-item>
                <el-form-item label="详细地址">
                    <span>{{ jobPublishForm.location }}</span>
                </el-form-item>
                <el-form-item label="岗位薪资">
                    <span>{{ displaySalary }}</span>
                </el-form-item>
                <el-form-item label="薪资周期">
                    <span>{{ jobPublishForm.salary_count }} 个月</span>
                </el-form-item>
                <el-form-item label="经验要求">
                    <span>{{ jobPublishForm.experience }}</span>
                </el-form-item>
                <el-form-item label="学历要求">
                    <span>{{ jobPublishForm.education }}</span>
                </el-form-item>
                <el-form-item label="招聘人数">
                    <span>{{ jobPublishForm.hire_number }} 人</span>
                </el-form-item>
                <el-form-item label="福利待遇">
                    <pre>{{ jobPublishForm.benefit }}</pre>
                </el-form-item>
                <el-form-item label="职位描述">
                    <pre>{{ jobPublishForm.description }}</pre>
                </el-form-item>
                <el-row class="flex-end">
                    <el-form-item>
                        <el-button type="primary" @click="submitForm">发 布</el-button>
                        <el-button @click="closeDialog">返 回</el-button>
                    </el-form-item>
                </el-row>
            </el-form>
        </el-dialog>
    </div>
</template>

<style scoped>
.job-publish {
    padding: 2%;
    background-color: #ffffff;
    border: 1px solid #dddddd;
    border-radius: 5px;
}

.flex-end {
    display: flex;
    justify-content: flex-end;
}

pre {
    white-space: pre-line;
}
</style>
