<script setup lang="ts">
import { ref, reactive } from "vue";
import type { InternalRuleItem } from "async-validator";
import type { JobCreate, UpdateJobForm } from "@/types/Job.ts";
import type { FormInstance } from "element-plus";

const props = defineProps<{
    label_position: "left" | "right" | "top";
    model: JobCreate | UpdateJobForm;
}>();

const experienceList = ["不需要经验", "经验0-2年", "经验2-5年", "经验5-10年", "经验10年以上"];
const educationList = ["博士", "研究生", "大学", "高中", "初中", "初中以下"];

const ruleFormRef = ref<FormInstance>();
const loading = ref<boolean>(false);
const jobForm = reactive<JobCreate>(props.model);

const emit = defineEmits(["update:model"]);

const updateJob = () => {
    emit("update:model", ruleFormRef.value);
};

// 薪资自定义验证规则
const validateNumber = (
    _rule: InternalRuleItem,
    _value: number,
    callback: (error?: string | Error) => void,
) => {
    if (
        jobForm.salary_max > 0 &&
        jobForm.salary_min > 0 &&
        Number(jobForm.salary_max) >= Number(jobForm.salary_min)
    ) {
        callback();
    } else {
        callback(new Error("最大薪资必须大于最小薪资！"));
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
</script>

<template>
    <el-form
        class="form-box"
        ref="ruleFormRef"
        v-loading="loading"
        :rules="rules"
        :model="props.model"
        label-width="auto"
        :label-position="props.label_position"
    >
        <el-form-item label="职位名称" prop="title">
            <el-input v-model="jobForm.title" placeholder="请输入职位名称" @input="updateJob" />
        </el-form-item>
        <el-row :gutter="20">
            <el-col :span="8">
                <el-form-item label="工作城市" prop="city">
                    <el-input
                        v-model="jobForm.city"
                        placeholder="请输入工作城市"
                        @input="updateJob"
                    />
                </el-form-item>
            </el-col>
            <el-col :span="16">
                <el-form-item label="详细地址" prop="location">
                    <el-input
                        v-model="jobForm.location"
                        placeholder="请输入工作详细地址"
                        @input="updateJob"
                    />
                </el-form-item>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="8">
                <el-form-item label="最低薪资" prop="salary_min">
                    <el-input
                        v-model="jobForm.salary_min"
                        type="number"
                        placeholder="请输入每月最低薪资"
                        @input="updateJob"
                    >
                        <template #append>元/月</template>
                    </el-input>
                </el-form-item>
            </el-col>
            <el-col :span="8">
                <el-form-item label="最高薪资" prop="salary_max">
                    <el-input
                        v-model="jobForm.salary_max"
                        type="number"
                        placeholder="请输入每月最高薪资"
                        @input="updateJob"
                    >
                        <template #append>元/月</template>
                    </el-input>
                </el-form-item>
            </el-col>
            <el-col :span="8">
                <el-form-item label="薪资周期" prop="salary_count">
                    <el-input-number
                        v-model="jobForm.salary_count"
                        :min="12"
                        :max="36"
                        :step="1"
                        @input="updateJob"
                    />
                </el-form-item>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="8">
                <el-form-item label="经验要求" prop="experience" @select="updateJob">
                    <el-select v-model="jobForm.experience" placeholder="请选择经验要求">
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
                    <el-select
                        v-model="jobForm.education"
                        placeholder="请选择学历要求"
                        @select="updateJob"
                    >
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
                <el-form-item label="招聘人数" prop="hire_number">
                    <el-input-number
                        v-model="jobForm.hire_number"
                        :min="1"
                        :max="200"
                        @click="updateJob"
                        @input="updateJob"
                    />
                </el-form-item>
            </el-col>
        </el-row>
        <el-form-item label="福利待遇" prop="benefit">
            <el-input
                type="textarea"
                v-model="jobForm.benefit"
                :autosize="{ minRows: 2 }"
                placeholder="请输入福利待遇"
                @input="updateJob"
            />
        </el-form-item>
        <el-form-item label="职位描述" prop="description">
            <el-input
                type="textarea"
                v-model="jobForm.description"
                :autosize="{ minRows: 4 }"
                placeholder="请输入职位描述"
                @input="updateJob"
            />
        </el-form-item>
        <el-row class="flex-end">
            <el-form-item>
                <slot name="submit"></slot>
            </el-form-item>
        </el-row>
    </el-form>
</template>

<style scoped>
.flex-end {
    display: flex;
    justify-content: flex-end;
    align-items: center;
}
</style>
