<script setup lang="ts">
import { useRouter } from "vue-router";
import userStore from "@/stores/modules/User.ts";
import { ref, reactive, onMounted } from "vue";
import { type FormInstance, type FormItemRule } from "element-plus";
// import { ElMessage } from "element-plus/es";
import ROUTER_CONSTANTS from "@/router/constants.ts";
import type { Arrayable } from "element-plus/es/utils";
import { userLogin } from "@/services/user";
import type { AxiosError } from "axios";

// 全局路由
const router = useRouter();
// 创建用户状态管理
const useUserStore = userStore();
// 登录表单引用
const ruleFormRef = ref<FormInstance>();
const loading = ref<boolean>(false);

// 登录表单接口
interface LoginForm {
    email: string;
    password: string;
}

// 登录表单数据
const param = reactive<LoginForm>({
    email: "",
    password: "",
});
// 表单验证
const rules: Partial<Record<string, Arrayable<FormItemRule>>> = {
    email: [
        { required: true, message: "请输入邮箱", trigger: "blur" },
        { type: "email", message: "请输入正确的邮箱地址", trigger: ["blur", "change"] },
    ],
    password: [{ required: true, message: "请输入密码", trigger: "blur" }],
};
// 提交登录表单
const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) {
        return;
    }
    loading.value = true;
    await formEl.validate(async (valid: boolean) => {
        if (valid) {
            try {
                const response = await userLogin(param.email, param.password);
                if (response.status === 200) {
                    const { data } = response;
                    // 保存用户信息
                    useUserStore.login(data);
                    // 默认跳转到首页
                    loading.value = false;
                    let result = null;
                    if (useUserStore.getUser?.is_superuser) {
                        result = await router.push({
                            name: ROUTER_CONSTANTS.CMS_COMPANY_MANAGE,
                        });
                    } else {
                        result = await router.push({
                            name: ROUTER_CONSTANTS.CMS_DASHBOARD,
                        });
                    }
                    if (!result) {
                        ElMessage.success("登录成功！");
                    }
                }
            } catch (error) {
                ElMessage.error(`登录失败[${(error as AxiosError).message}].`);
                loading.value = false;
            }
        } else {
            ElMessage.error("登录出错！");
            loading.value = false;
        }
    });
};

// 第一次进入页面时，判断用户是否已经登录，如果已经登录，则跳转到首页
onMounted(() => {
    if (useUserStore.isLogin()) {
        if (useUserStore.getUser?.is_superuser) {
            router.push({
                name: ROUTER_CONSTANTS.CMS_COMPANY_MANAGE,
            });
        } else {
            router.push({
                name: ROUTER_CONSTANTS.CMS_DASHBOARD,
            });
        }
    }
});
</script>

<template>
    <div class="login_wrap">
        <div class="ms_login">
            <div class="ms_title">Peekpa 管理系统</div>
            <el-form
                ref="ruleFormRef"
                :model="param"
                :rules="rules"
                label-width="0px"
                size="large"
                class="ms_content"
            >
                <el-form-item prop="email">
                    <el-input v-model="param.email" placeholder="请输入邮箱">
                        <template #prepend>
                            <el-icon>
                                <i-ep-user />
                            </el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input
                        v-model="param.password"
                        type="password"
                        placeholder="请输入密码"
                        @keyup.enter="submitForm(ruleFormRef)"
                    >
                        <template #prepend>
                            <el-icon>
                                <i-ep-lock />
                            </el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item class="login_btn">
                    <el-button type="primary" :loading="loading" @click="submitForm(ruleFormRef)">
                        登录
                    </el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<style scoped>
.login_wrap {
    position: relative;
    width: 100%;
    height: 100%;
    background: linear-gradient(to top, #ffffff, #4b5679);
    background-size: 100%;
}

.ms_login {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 350px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.ms_title {
    width: 100%;
    line-height: 50px;
    text-align: center;
    font-size: 1.2rem;
    color: #ffffff;
    border-bottom: 1px solid #dddddd;
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Roboto,
        Oxygen,
        Ubuntu,
        Cantarell,
        "Fira Sans",
        "Droid Sans",
        "Helvetica Neue",
        sans-serif;
}

.ms_content {
    padding: 30px 30px;
}

.login_btn .el-button {
    width: 100%;
    height: 90%;
}
</style>
