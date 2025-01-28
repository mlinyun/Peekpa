<script setup lang="ts">
import { ref } from "vue";
import type { FormInstance } from "element-plus";
import type { JobCreate } from "@/types/Job.ts";
import type { InternalRuleItem } from "async-validator";
import { createJob } from "@/services/job";
import type { AxiosError } from "axios";

const ruleFormRef = ref<FormInstance>();
const loading = ref<boolean>(false);
const doubleCheck = ref<boolean>(false);

const experienceList = ["不需要经验", "经验0-2年", "经验2-5年", "经验5-10年", "经验10年以上"];
const educationList = ["博士", "研究生", "大学", "高中", "初中", "初中以下"];

const jobPublishForm = reactive<JobCreate>({
    title: "",
    status: 0,
    city: "",
    location: "",
    salary_min: 0,
    salary_max: 0,
    salary_count: 12,
    hire_number: 1,
    experience: experienceList[0],
    benefit: "",
    description: "",
    education: "",
});

// 薪资自定义验证规则
const validateNumber = (
    _rule: InternalRuleItem,
    _value: number,
    callback: (error?: string | Error) => void,
) => {
    if (
        jobPublishForm.salary_max > 0 &&
        jobPublishForm.salary_min > 0 &&
        Number(jobPublishForm.salary_max) >= Number(jobPublishForm.salary_min)
    ) {
        callback();
    } else {
        callback(new Error("最大薪资必须大于最小薪资"));
    }
};

// 表单验证规则
const rules = {
    title: [{ required: true, message: "请输入职位名称", trigger: "blur" }],
    city: [{ required: true, message: "请输入工作所在城市", trigger: "blur" }],
    location: [{ required: true, message: "请输入工作详细地址", trigger: "blur" }],
    benefit: [{ required: true, message: "请输入福利待遇", trigger: "blur" }],
    education: [{ required: true, message: "请选择学历要求", trigger: "blur" }],
    description: [{ required: true, message: "请输入职位描述", trigger: "blur" }],
    salary: [{ validator: validateNumber, trigger: "submit" }],
};

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
        <el-form
            class="form-box"
            ref="ruleFormRef"
            v-loading="loading"
            :rules="rules"
            :model="jobPublishForm"
            label-width="auto"
            label-position="top"
        >
            <el-form-item label="职位名称" prop="title">
                <el-input v-model="jobPublishForm.title" placeholder="请输入职位名称" />
            </el-form-item>
            <el-row :gutter="20">
                <el-col :span="8">
                    <el-form-item label="工作城市" prop="city">
                        <el-input v-model="jobPublishForm.city" placeholder="请输入工作城市" />
                    </el-form-item>
                </el-col>
                <el-col :span="16">
                    <el-form-item label="详细地址" prop="location">
                        <el-input
                            v-model="jobPublishForm.location"
                            placeholder="请输入工作详细地址"
                        />
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="16">
                    <el-form-item label="岗位薪资" prop="salary">
                        <div class="flex">
                            <el-input
                                v-model="jobPublishForm.salary_min"
                                type="number"
                                placeholder="最小薪资"
                            >
                                <template #append>元/月</template>
                            </el-input>
                            <div class="text-center"><span>~</span></div>
                            <el-input
                                v-model="jobPublishForm.salary_max"
                                type="number"
                                placeholder="最大薪资"
                            >
                                <template #append>元/月</template>
                            </el-input>
                        </div>
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="薪资周期">
                        <el-input-number
                            v-model="jobPublishForm.salary_count"
                            :min="12"
                            :max="36"
                            :step="1"
                        />
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="8">
                    <el-form-item label="经验要求" prop="experience">
                        <el-select v-model="jobPublishForm.experience" placeholder="请选择经验要求">
                            <el-option
                                v-for="item in experienceList"
                                :key="item"
                                :label="item"
                                :value="item"
                            />
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="学历要求" prop="education">
                        <el-select v-model="jobPublishForm.education" placeholder="请选择学历要求">
                            <el-option
                                v-for="item in educationList"
                                :key="item"
                                :label="item"
                                :value="item"
                            />
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="招聘人数" prop="hire">
                        <el-input-number v-model="jobPublishForm.hire_number" :min="1" :max="200" />
                    </el-form-item>
                </el-col>
            </el-row>
            <el-form-item label="福利待遇" prop="benefit">
                <el-input
                    type="textarea"
                    v-model="jobPublishForm.benefit"
                    :autosize="{ minRows: 2 }"
                    placeholder="请输入福利待遇"
                />
            </el-form-item>
            <el-form-item label="职位描述" prop="description">
                <el-input
                    type="textarea"
                    v-model="jobPublishForm.description"
                    :autosize="{ minRows: 4 }"
                    placeholder="请输入职位描述"
                />
            </el-form-item>
            <el-row class="flex-end">
                <el-form-item>
                    <el-button type="primary" @click="goToDoubleCheck">确定</el-button>
                    <el-button @click="resetForm">重置</el-button>
                </el-form-item>
            </el-row>
        </el-form>
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

.text-center {
    text-align: center;
    margin: 0 1rem;
}

.flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

.flex-end {
    display: flex;
    justify-content: flex-end;
}

pre {
    white-space: pre-line;
}
</style>
