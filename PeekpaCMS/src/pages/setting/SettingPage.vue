<script setup lang="ts">
import { ref, reactive } from "vue";
import type { FormInstance } from "element-plus";
import type { UserSetting } from "@/types/User.ts";
import { getUserInfo, updateUserInfo } from "@/services/user";
import { UNAUTH_401 } from "@/services/Axios.ts";
import userStore from "@/stores/modules/User.ts";
import type { AxiosError } from "axios";

// 用户状态管理
const useUserStore = userStore();

// 公司标签多选框列表内容
const companyLabelList = [
    "游戏",
    "社交平台",
    "区块链",
    "金融业",
    "影视",
    "电商平台",
    "短视频",
    "直播平台",
];

// 公司规模
const companySize = [
    "10人以下",
    "10~50人",
    "50~100人",
    "100~500人",
    "500~2000人",
    "2000~10000人",
    "10000人以上",
];

const ruleFormRef = ref<FormInstance>();
const loading = ref<boolean>(false);
const form = reactive<UserSetting>({
    avatar: "",
    name: "",
    description: "",
    size: "",
    slogan: "",
    tags: [],
    website: "",
    password: "",
    user: {
        email: "",
        name: "",
        gender: 0,
    },
});
const isManager = ref<boolean>(false);
const previewInput = ref<HTMLInputElement | null>(null);

// 请求用户数据方法
const requestUserData = async () => {
    loading.value = true;
    try {
        const response = await getUserInfo();
        if (response.status === 200) {
            const protocol = import.meta.env.VITE_BASE_PROTOCOL; // 获取协议
            const host = import.meta.env.VITE_BASE_HOST; // 获取主机名和端口号
            const baseUrl = `${protocol}://${host}`;
            form.avatar = `${baseUrl}/${response.data.avatar}`;
            form.name = response.data.name;
            form.description = response.data.description;
            form.size = response.data.size;
            form.slogan = response.data.slogan;
            form.tags = response.data.tags ? (response.data.tags as string).split(",") : [];
            form.website = response.data.website;
            form.user = response.data.user;
        }
        loading.value = false;
    } catch (error) {
        if ((error as Error).message === UNAUTH_401) {
            ElMessage.error(`用户数据请求错误${error}`);
        }
        loading.value = false;
    }
};

// 初始化用户数据
onMounted(async () => {
    await requestUserData();
    const user = useUserStore.getUser;
    if (user) {
        isManager.value = user.is_manager;
    }
});

// 选中上传图片文件
const previewImage = async (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
        const file = target.files[0];
        form.avatar = URL.createObjectURL(file);
        form.avatar_file = file;
    }
};

// 触发 input 组件上传图片文件
const uploadPreview = () => {
    if (previewInput.value) {
        previewInput.value.click();
    }
};

// 用户信息修改逻辑
const handleSubmit = async () => {
    loading.value = true;
    try {
        const updateData = new FormData();
        if (form.password) {
            updateData.append("password", form.password);
        }
        if (isManager.value) {
            updateData.append("slogan", form.slogan);
            updateData.append("size", form.size);
            updateData.append("description", form.description);
            updateData.append("tags", (form.tags as string[]).join(","));
            if (form.avatar_file) {
                updateData.append("avatar_file", form.avatar_file);
            }
        }
        const response = await updateUserInfo(updateData);
        if (response.status === 200) {
            ElMessage.success("用户信息修改成功！");
            // 重置表单数据
            ruleFormRef.value?.resetFields();
        } else {
            ElMessage.error(`用户信息修改失败[${response.status}].`);
        }
        loading.value = false;
    } catch (error) {
        ElMessage.error(`用户信息修改失败[${(error as AxiosError).message}].`);
        loading.value = false;
    }
};
</script>

<template>
    <div class="setting">
        <el-form
            ref="ruleFormRef"
            v-loading="loading"
            :model="form"
            label-width="auto"
            label-position="top"
        >
            <el-row v-if="isManager" :gutter="40">
                <el-col :span="12">
                    <el-form-item label="公司名称" prop="title">
                        <el-input v-model="form.name" disabled />
                    </el-form-item>
                    <el-form-item label="公司口号" prop="title">
                        <el-input v-model="form.slogan" />
                    </el-form-item>
                    <el-form-item label="公司网址" prop="title">
                        <el-input v-model="form.website" disabled />
                    </el-form-item>
                    <el-row :gutter="20">
                        <el-col :span="16">
                            <el-form-item label="公司标签" prop="title">
                                <el-select
                                    v-model="form.tags"
                                    multiple
                                    :multiple-limit="3"
                                    placeholder="请选择（多选，最多三个）"
                                    style="width: 100%"
                                >
                                    <el-option
                                        v-for="item in companyLabelList"
                                        :key="item"
                                        :label="item"
                                        :value="item"
                                    ></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="8">
                            <el-form-item label="公司规模" prop="title">
                                <el-select v-model="form.size">
                                    <el-option
                                        v-for="item in companySize"
                                        :key="item"
                                        :label="item"
                                        :value="item"
                                    ></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="公司头像" prop="title">
                        <input
                            id="avatar"
                            ref="previewInput"
                            name="avatar"
                            type="file"
                            hidden
                            accept=".png, .jpg, .jepg"
                            @click="previewImage"
                        />
                        <div class="preview_container" @click="uploadPreview">
                            <el-image class="preview" :src="form.avatar" fit="fill">
                                <template #error>
                                    <div class="image-error">
                                        <el-icon>
                                            <i-ep-picture />
                                        </el-icon>
                                    </div>
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
            <el-form-item v-if="isManager" label="公司简介" prop="title">
                <el-input
                    type="textarea"
                    v-model="form.description"
                    :autosize="{ minRows: 3 }"
                    placeholder="请输入公司简介"
                />
            </el-form-item>
            <el-form-item label="登录邮箱" prop="title">
                <el-input v-model="form.user.email" disabled />
            </el-form-item>
            <el-form-item label="联系人姓名" prop="title">
                <el-input v-model="form.user.name" disabled />
            </el-form-item>
            <el-form-item label="新密码" prop="title">
                <el-input v-model="form.password" type="password"></el-input>
            </el-form-item>
            <el-row class="flex-end">
                <el-form-item>
                    <el-button type="primary" @click="handleSubmit">修 改</el-button>
                </el-form-item>
            </el-row>
        </el-form>
    </div>
</template>

<style scoped>
.setting {
    padding: 2%;
    background-color: #ffffff;
    border: 1px solid #dddddd;
    border-radius: 5px;
}

.preview_container {
    width: 8rem;
}

.preview {
    width: 100%;
    height: 8rem;
    cursor: pointer;
    background-size: cover;
}

.image-error {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    background-color: #dfdfdf;
    text-align: center;
}

.preview img {
    width: 100%;
    height: 100%;
}

.flex-end {
    display: flex;
    justify-content: flex-end;
    align-items: center;
}
</style>
