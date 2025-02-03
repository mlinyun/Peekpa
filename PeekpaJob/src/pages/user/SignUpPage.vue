<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import userStore from "@/stores/modules/User.ts";
import type { SignupForm } from "@/types/User.ts";
import type { FormInstance, FormItemRule } from "element-plus";
import type { InternalRuleItem } from "async-validator";
import type { Arrayable } from "element-plus/es/utils";
import ROUTER_CONSTANTS from "@/router/constants.ts";
import { signup } from "@/services/user";
import type { AxiosError } from "axios";

// 路由对象
const route = useRoute();
// 全局路由
const router = useRouter();
// 用户状态管理
const useUserStore = userStore();
// 注册步骤变量
const step = ref<number>(1);

const signupForm = reactive<SignupForm>({
    email: "",
    first_name: "",
    last_name: "",
    password: "",
});

// 注册信息表单引用
const ruleFormRef = ref<FormInstance>();

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

// 表单验证规则
const rules = computed((): Partial<Record<string, Arrayable<FormItemRule>>> => {
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
                :rules="rules"
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

.register-main {
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
</style>
