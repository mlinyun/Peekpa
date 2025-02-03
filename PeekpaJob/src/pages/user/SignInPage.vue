<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import userStore from "@/stores/modules/User.ts";
import type { LoginForm } from "@/types/User.ts";
import type { FormInstance, FormItemRule } from "element-plus";
import ROUTER_CONSTANTS from "@/router/constants.ts";
import { signin } from "@/services/user";
import type { AxiosError } from "axios";
import type { Arrayable } from "element-plus/es/utils";

// 路由对象
const route = useRoute();
// 全局路由
const router = useRouter();
// 用户状态管理
const useUserStore = userStore();

const param = reactive<LoginForm>({
    email: "",
    password: "",
});
// 登录表单引用
const ruleFormRef = ref<FormInstance>();

// 表单验证
const rules = computed((): Partial<Record<string, Arrayable<FormItemRule>>> => {
    return {
        email: [
            { required: true, message: "请输入用户邮箱", trigger: "blur" },
            { type: "email", message: "请输入正确的邮箱地址", trigger: ["blur", "change"] },
        ],
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

// 提交登录表单
const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) {
        return;
    }
    await formEl.validate(async (valid) => {
        if (valid) {
            try {
                const response = await signin(param.email, param.password);
                if (response.status === 200) {
                    const userInfo = response.data;
                    // 保存用户信息
                    useUserStore.login(userInfo);
                    let result = null;
                    if (route.query.next) {
                        result = await router.replace(route.query.next as string);
                    } else {
                        // 默认跳转到首页
                        result = await router.push({
                            name: ROUTER_CONSTANTS.INDEX,
                        });
                    }
                    if (!result) {
                        ElMessage.success("登录成功！");
                    }
                }
            } catch (error) {
                ElMessage.error(`登录失败[${(error as AxiosError).message}].`);
            }
        } else {
            ElMessage.error("登录出错！");
        }
    });
};
</script>

<template>
    <div class="sign-in">
        <div class="login-main">
            <div class="title-main">
                <div class="title">欢迎登录 PeekpaJob</div>
            </div>
            <el-form ref="ruleFormRef" :model="param" :rules="rules" label-width="0px" size="large">
                <el-form-item prop="email">
                    <el-input v-model="param.email" placeholder="请输入邮箱"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input
                        v-model="param.password"
                        type="password"
                        placeholder="请输入密码"
                        @keyup.enter="submitForm(ruleFormRef)"
                    ></el-input>
                </el-form-item>
                <el-form-item class="register-link">
                    还没有账号？
                    <el-link type="primary" href="/signup">立即注册</el-link>
                </el-form-item>
                <el-form-item class="login-btn">
                    <el-button color="var(--theme-primary-color)" @click="submitForm(ruleFormRef)">
                        登录
                    </el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<style scoped>
.sign-in {
    height: calc(100vh - 170px - 60px - 40px);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.login-main {
    width: 300px;
    margin: 0 auto;
    padding: 20px;
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

.register-link {
    padding: 0 4px;
}

.login-btn {
    text-align: center;
}

.login-btn .el-button {
    width: 100%;
}
</style>
