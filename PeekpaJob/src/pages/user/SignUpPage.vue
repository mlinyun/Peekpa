<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import userStore from "@/stores/modules/User.ts";
import type { InfoForm, SignupForm } from "@/types/User.ts";
import type { FormInstance, FormItemRule } from "element-plus";
import type { InternalRuleItem } from "async-validator";
import type { Arrayable } from "element-plus/es/utils";
import ROUTER_CONSTANTS from "@/router/constants.ts";
import { signup, updateUserInfo, uploadAvatar } from "@/services/user";
import type { AxiosError } from "axios";
import { uploadResume } from "@/services/job";

// 路由对象
const route = useRoute();
// 全局路由
const router = useRouter();
// 用户状态管理
const useUserStore = userStore();
// 注册步骤变量
const step = ref<number>(1);
// 注册表单数据
const signupForm = reactive<SignupForm>({
    email: "",
    first_name: "",
    last_name: "",
    password: "",
});
// 注册信息表单引用
const ruleFormRef = ref<FormInstance>();

const previewInput = ref<HTMLInputElement | null>(null);
const resumeInput = ref<HTMLInputElement | null>(null);
const selectedImage = ref<string>("");
const genderList = [
    {
        name: "请选择性别",
        value: 0,
    },
    {
        name: "男",
        value: 1,
    },
    {
        name: "女",
        value: 2,
    },
];
const experienceList = ["无经验", "2年以内", "2~5年", "5~10年", "10年以上"];
const statusList = ["目前状态", "在职", "已离职", "无业"];
const educationList = ["博士", "研究生", "大学", "高中", "初中", "初中以下"];

// 详细信息表单
const infoForm = reactive<InfoForm>({
    phone: "",
    avatar: "",
    gender: 0,
    position: "",
    education: "",
    school: "",
    major: "",
    experience_year: "",
    status: "",
    city: "",
    company_name: "",
    salary_min: "",
    salary_max: "",
});

// 自定义验证规则，检测姓名
const validateName = (
    _rule: InternalRuleItem,
    _value: string,
    callback: (error?: string | Error) => void,
) => {
    if (signupForm.first_name.length && signupForm.last_name.length) {
        callback();
    } else {
        callback(new Error("请正确输入姓名"));
    }
};

// 自定义验证用户性别
const validateGender = (
    _rule: InternalRuleItem,
    value: number,
    callback: (error?: string | Error) => void,
) => {
    if (value !== 0) {
        callback();
    } else {
        callback(new Error("请选择性别"));
    }
};

// 注册表单验证规则
const registerRules = computed((): Partial<Record<string, Arrayable<FormItemRule>>> => {
    return {
        email: [
            { required: true, message: "请输入用户邮箱", trigger: "blur" },
            { type: "email", message: "请输入正确的邮箱地址", trigger: ["blur", "change"] },
        ],
        name: [{ required: true, validator: validateName, trigger: "submit" }],
        password: [
            { required: true, message: "请输入用户密码", trigger: "blur" },
            { min: 8, max: 20, message: "密码长度在 8 到 20 个字符", trigger: "blur" },
        ],
    };
});

// 详细信息表单验证规则
const infoRules = computed((): Partial<Record<string, Arrayable<FormItemRule>>> => {
    return {
        phone: [
            { required: true, message: "请输入手机号码", trigger: "blur" },
            { pattern: /^1[3456789]\d{9}$/, message: "请输入正确的手机号码", trigger: "blur" },
        ],
        gender: [{ required: true, validator: validateGender, trigger: "blur" }],
        position: [{ required: true, message: "请输入想要应聘的职位", trigger: "blur" }],
        education: [{ required: true, message: "请填写最高学历", trigger: "blur" }],
        school: [{ required: true, message: "请输入学校名称", trigger: "blur" }],
        experience_year: [{ required: true, message: "请选择工作经验", trigger: "blur" }],
        status: [{ required: true, message: "请选择目前状态", trigger: "blur" }],
        city: [{ required: true, message: "请输入所在城市", trigger: "blur" }],
    };
});

// 第一次进入页面，检测是否已经登录
onMounted(async () => {
    if (useUserStore.isLogin()) {
        await router.push({
            name: ROUTER_CONSTANTS.PROFILE,
        });
    }
});

// 提交注册信息表单
const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) {
        return;
    }
    await formEl.validate(async (valid) => {
        if (valid) {
            try {
                const response = await signup(signupForm);
                if (response.status === 201) {
                    const userInfo = response.data;
                    // 保存用户信息
                    useUserStore.login(userInfo);
                    // 重置表单
                    formEl.resetFields();
                    step.value = 2;
                }
            } catch (error) {
                ElMessage.error(`注册失败[${(error as AxiosError).message}].`);
            }
        } else {
            ElMessage.error("请正确填写注册信息！");
        }
    });
};

// 选中上传图片文件
const uploadPreview = () => {
    if (previewInput.value) {
        previewInput.value.click();
    }
};

// 上传头像
const handleFileChange = async (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length) {
        const file = target.files[0];
        try {
            const response = await uploadAvatar(file);
            if (response.status === 201) {
                selectedImage.value = `http://localhost:8081/${response.data.url}`;
                infoForm.avatar = selectedImage.value;
            } else {
                ElMessage.error(`头像上传失败[${response.status}]！`);
            }
        } catch (error) {
            ElMessage.error(`头像上传失败[${(error as AxiosError).message}]！`);
        }
    }
};

// 上传简历
const handleResumeChange = async (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length) {
        const file = target.files[0];
        try {
            const response = await uploadResume(file);
            if (response.status === 201) {
                ElMessage.success("简历上传成功！");
            } else {
                ElMessage.error(`简历上传失败[${response.status}]！`);
            }
        } catch (error) {
            ElMessage.error(`简历上传失败[${(error as AxiosError).message}]！`);
        }
    }
};

// 提交详细信息表单
const submitInfoForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) {
        return;
    }
    await formEl.validate(async (valid) => {
        if (valid) {
            try {
                const response = await updateUserInfo(infoForm);
                if (response.status === 200) {
                    // 重置表单数据
                    formEl.resetFields();
                    ElMessage.success("注册成功，正在跳转...");
                    if (route.query.next) {
                        await router.replace(route.query.next as string);
                    } else {
                        // 默认跳转到首页
                        await router.push({
                            name: ROUTER_CONSTANTS.INDEX,
                        });
                    }
                } else {
                    ElMessage.error(`用户信息填写失败[${response.status}].`);
                }
            } catch (error) {
                ElMessage.error(`注册失败[${(error as AxiosError).message}].`);
            }
        } else {
            ElMessage.error("请正确填写注册信息！");
        }
    });
};
</script>

<template>
    <div class="sign-up">
        <div v-if="step === 1" class="register-main">
            <div class="title-main">
                <div class="title">注册 PeekpaJob</div>
            </div>
            <el-form
                ref="ruleFormRef"
                :model="signupForm"
                :rules="registerRules"
                label-width="auto"
                size="large"
            >
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="signupForm.email" placeholder="请输入用户邮箱"></el-input>
                </el-form-item>
                <el-form-item label="姓名" prop="name">
                    <el-col :span="11">
                        <el-input v-model="signupForm.first_name" placeholder="姓氏"></el-input>
                    </el-col>
                    <el-col :offset="2" :span="11">
                        <el-input v-model="signupForm.last_name" placeholder="名字"></el-input>
                    </el-col>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input
                        v-model="signupForm.password"
                        placeholder="请输入用户密码"
                        type="password"
                        @keyup.enter="submitForm(ruleFormRef)"
                    ></el-input>
                </el-form-item>
                <el-form-item class="register-btn">
                    <el-button color="var(--theme-primary-color)" @click="submitForm(ruleFormRef)">
                        注册
                    </el-button>
                </el-form-item>
            </el-form>
        </div>
        <div v-else-if="step === 2" class="info-main">
            <div class="title-main">
                <div class="title">注册成功，请补充以下材料</div>
            </div>
            <el-form
                ref="ruleFormRef"
                :model="infoForm"
                :rules="infoRules"
                label-width="auto"
                size="large"
            >
                <el-row>
                    <el-col :span="16">
                        <el-row :gutter="10">
                            <el-col :span="12">
                                <el-form-item label="联系方式" prop="phone">
                                    <el-input
                                        v-model="infoForm.phone"
                                        placeholder="请输入手机号码"
                                    ></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item label="性别" prop="gender">
                                    <el-select
                                        v-model="infoForm.gender"
                                        default-first-option
                                        placeholder="请选择性别"
                                    >
                                        <el-option
                                            v-for="item in genderList"
                                            :key="item.value"
                                            :label="item.name"
                                            :value="item.value"
                                        ></el-option>
                                    </el-select>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row :gutter="10">
                            <el-col :span="12">
                                <el-form-item label="应聘职位" prop="position">
                                    <el-input
                                        v-model="infoForm.position"
                                        placeholder="请输入想要应聘的职位"
                                    ></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item label="目前状态" prop="status">
                                    <el-select
                                        v-model="infoForm.status"
                                        default-first-option
                                        placeholder="目前状态"
                                    >
                                        <el-option
                                            v-for="item in statusList"
                                            :key="item"
                                            :label="item"
                                            :value="item"
                                        ></el-option>
                                    </el-select>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row :gutter="10">
                            <el-col :span="12">
                                <el-form-item label="工作经验" prop="experience_year">
                                    <el-select
                                        v-model="infoForm.experience_year"
                                        default-first-option
                                        placeholder="工作经验"
                                    >
                                        <el-option
                                            v-for="item in experienceList"
                                            :key="item"
                                            :label="item"
                                            :value="item"
                                        ></el-option>
                                    </el-select>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item label="公司名称">
                                    <el-input
                                        v-model="infoForm.company_name"
                                        placeholder="请输入公司名称"
                                    ></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="头像" prop="avatar">
                            <input
                                type="file"
                                ref="previewInput"
                                name="avatar"
                                hidden="hidden"
                                accept=".png, .jpg, .jepg"
                                @change="handleFileChange"
                            />
                            <div class="preview" @click="uploadPreview">
                                <el-image :src="selectedImage" fit="fill" class="image">
                                    <template #error>
                                        <div class="image-error"></div>
                                    </template>
                                    <template #placeholder>
                                        <div class="image-slot">
                                            Loading<span class="dot">...</span>
                                        </div>
                                    </template>
                                </el-image>
                            </div>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :span="8">
                        <el-form-item label="最高学历" prop="education">
                            <el-select
                                v-model="infoForm.education"
                                default-first-option
                                placeholder="最高学历"
                            >
                                <el-option
                                    v-for="item in educationList"
                                    :key="item"
                                    :label="item"
                                    :value="item"
                                ></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="学校名称" prop="school">
                            <el-input
                                v-model="infoForm.school"
                                placeholder="请输入学校名称"
                            ></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="专业名称" prop="major">
                            <el-input
                                v-model="infoForm.major"
                                placeholder="请输入专业名称"
                            ></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :span="8">
                        <el-form-item label="最低薪资" prop="salary_min">
                            <el-input
                                v-model="infoForm.salary_min"
                                type="number"
                                placeholder="最低薪资"
                            >
                                <template #append>元/月</template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="最高薪资" prop="salary_max">
                            <el-input
                                v-model="infoForm.salary_max"
                                type="number"
                                placeholder="最高薪资"
                            >
                                <template #append>元/月</template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="所在城市" prop="city">
                            <el-input
                                v-model="infoForm.city"
                                placeholder="请输入所在城市"
                            ></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-form-item label="简历文件">
                        <input
                            type="file"
                            ref="resumeInput"
                            name="resume"
                            accept=".txt, .pdf, .doc, .docx"
                            @change="handleResumeChange"
                        />
                    </el-form-item>
                </el-row>
                <el-form-item class="register-btn">
                    <el-button
                        color="var(--theme-primary-color)"
                        @click="submitInfoForm(ruleFormRef)"
                    >
                        提 交
                    </el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<style scoped>
.sign-up {
    min-height: calc(100vh - 170px - 60px - 40px);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.register-main,
.info-main {
    width: 400px;
    margin: 0 auto;
    padding: 25px;
    border-radius: 10px;
    background-color: rgb(250, 250, 250);
    border: 1px solid rgb(237, 237, 237);
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.title-main {
    width: 100%;
    text-align: center;
    margin-bottom: 20px;
}

.title {
    font-size: 1.5rem;
    font-weight: 500;
    color: var(--theme-primary-color);
}

.el-input {
    --el-input-focus-border: var(--theme-primary-color);
}

.register-btn {
    padding: 0 10px;
}

.register-btn .el-button {
    width: 100%;
}

.info-main {
    width: 800px;
}

.preview {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 160px;
    width: 80%;
    margin: 0 auto;
    background-image: url("@/assets/images/avatar-placeholder.jpeg");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;
}

.image {
    width: 100%;
    height: 100%;
}

.preview img {
    width: 100%;
    height: 100%;
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
    text-align: center;
}
</style>
