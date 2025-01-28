<script setup lang="ts">
import { ref } from "vue";
import type { User, UserListResponse } from "@/types/User.ts";
import { timeStampFormat } from "@/utils/Helper.ts";
import { createUser, getAllUsers, searchUser, updateUser } from "@/services/user";
import { UNAUTH_401 } from "@/services/Axios.ts";
// import { ElMessageBox } from "element-plus";
import type { AxiosError } from "axios";
import type { FormInstance, InputInstance } from "element-plus";

// 创建用户表单接口
interface CreateUserForm {
    first_name: string;
    last_name: string;
    email: string;
    gender: number;
    password: string;
}

const LIMIT = 10;
let curOffset = 0;

const showCreate = ref<boolean>(false);
const search = ref<string>("");
const loading = ref<boolean>(false);
const data = ref<UserListResponse>();
const total = ref<number>(0);
const curPage = ref<number>(1);
const dialogInput = ref<InputInstance>();
const createFormRef = ref<FormInstance>();
const createUserForm = ref<CreateUserForm>({
    first_name: "",
    last_name: "",
    email: "",
    gender: 0,
    password: "",
});
const genderList = [
    { name: "男", value: 1 },
    { name: "女", value: 2 },
    { name: "未设定", value: 0 },
];

// 请求用户列表数据
const requestUserData = async (offset: number) => {
    loading.value = true;
    try {
        const response = await getAllUsers(LIMIT, offset);
        if (response.status === 200) {
            data.value = response.data;
            total.value = response.data.count;
            curPage.value = Math.floor(offset / LIMIT) + 1;
        }
        loading.value = false;
    } catch (error) {
        if ((error as Error).message === UNAUTH_401) {
            ElMessage.error(`用户列表数据请求错误${error}`);
        }
        loading.value = false;
    }
};

// 搜索用户逻辑
const searchUserData = async (q: string, offset: number) => {
    loading.value = true;
    try {
        const response = await searchUser(q, LIMIT, offset);
        if (response.status === 200) {
            data.value = response.data;
            total.value = response.data.count;
            curPage.value = Math.floor(offset / LIMIT) + 1;
        }
        loading.value = false;
    } catch (error) {
        if ((error as Error).message === UNAUTH_401) {
            ElMessage.error(`搜索用户数据请求错误${error}`);
        }
        loading.value = false;
    }
};

// 创建用户方法
const handleCreateUser = async (formEl: FormInstance | undefined) => {
    if (!formEl) {
        return;
    }
    await formEl.validate(async (valid: boolean) => {
        if (valid) {
            try {
                const response = await createUser(createUserForm.value);
                if (response.status === 201) {
                    ElMessage.success("创建用户成功！");
                    showCreate.value = false;
                    await searchUserData(search.value, curOffset);
                    formEl.resetFields();
                } else {
                    ElMessage.error(`创建用户失败[${response.status}]！`);
                }
            } catch (error) {
                ElMessage.error(`创建用户失败[${(error as AxiosError).response?.status}]！`);
            }
        } else {
            ElMessage.error("请仔细检查表单！");
        }
    });
};

// 页面挂载时请求数据
onMounted(async () => {
    await requestUserData(0);
});

// 显示用户创建方法
const showCreateWindow = () => {
    showCreate.value = true;
};

// 搜索用户方法
const handleSearch = async () => {
    curOffset = 0;
    await searchUserData(search.value, curOffset);
};

// 清空搜索方法
const clearSearch = async () => {
    search.value = "";
    curOffset = 0;
    await requestUserData(curOffset);
};

// 性别显示方法
const displayGender = (gender: number) => {
    if (gender === 1) {
        return "男";
    } else if (gender === 2) {
        return "女";
    } else {
        return "未设定";
    }
};

// 时间格式化方法
const displayTime = (time: string) => {
    if (!time) return time;
    return timeStampFormat(time);
};

// 是否允许登录显示方法
const displayActive = (active: boolean) => {
    return active ? "允许" : "不允许";
};

// 是否禁用按钮
const isDisable = (item: User) => {
    return !item.is_active;
};

// 禁止用户登录方法
const handleDelete = async (index: number, item: User) => {
    ElMessageBox.confirm(`确定要禁止${item.first_name}${item.last_name}登录系统吗？`, "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "error",
    })
        .then(async () => {
            try {
                const response = await updateUser(item.uid, { is_active: false });
                if (response.status === 200) {
                    ElMessage.success("禁止登录成功！");
                    if (data.value?.results) {
                        data.value.results[index].is_active = false;
                    }
                } else {
                    ElMessage.error(`禁止登录失败[${response.status}]！`);
                }
            } catch (error) {
                ElMessage.error("禁止登录失败！");
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
    await requestUserData(curOffset);
};

// 处理对话框焦点方法
const handleDialogOpen = () => {
    nextTick(() => {
        if (dialogInput.value) {
            dialogInput.value.focus();
        }
    });
};
</script>

<template>
    <div class="user-manage">
        <el-row class="search_main">
            <el-col :span="6">
                <el-button type="primary" @click="showCreateWindow()">
                    <el-icon>
                        <i-ep-circle-plus-filled />
                    </el-icon>
                    创建新用户
                </el-button>
            </el-col>
            <el-col :span="6" :offset="12">
                <el-input
                    v-model="search"
                    placeholder="搜索"
                    clearable
                    @keyup.enter="handleSearch"
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
            <el-table-column label="姓名">
                <template #default="scope">
                    <span>{{ scope.row.first_name }}{{ scope.row.last_name }}</span>
                </template>
            </el-table-column>
            <el-table-column label="性别" width="80">
                <template #default="scope">
                    <span>{{ displayGender(scope.row.gender) }}</span>
                </template>
            </el-table-column>
            <el-table-column label="邮箱" width="200">
                <template #default="scope">
                    <span>{{ scope.row.email }}</span>
                </template>
            </el-table-column>
            <el-table-column label="注册时间" width="170">
                <template #default="scope">
                    <span>{{ displayTime(scope.row.data_join) }}</span>
                </template>
            </el-table-column>
            <el-table-column label="最后登录时间" width="170">
                <template #default="scope">
                    <span>{{ displayTime(scope.row.last_login) }}</span>
                </template>
            </el-table-column>
            <el-table-column label="是否允许登录" width="120">
                <template #default="scope">
                    <span>{{ displayActive(scope.row.is_active) }}</span>
                </template>
            </el-table-column>
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button
                        size="small"
                        type="danger"
                        plain
                        :disabled="isDisable(scope.row)"
                        @click="handleDelete(scope.$index, scope.row)"
                    >
                        <el-icon>
                            <i-ep-close />
                        </el-icon>
                        禁止登录
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination
            class="pagination_main"
            background
            layout="prev, pager, next"
            :total="total"
            :page-size="LIMIT"
            @current-change="handlePageChange"
        ></el-pagination>
        <el-dialog v-model="showCreate" title="创建新用户" width="50%" @open="handleDialogOpen">
            <el-form ref="createFormRef" :model="createUserForm" label-position="top">
                <el-form-item label="姓氏" prop="first_name">
                    <el-input v-model="createUserForm.first_name" ref="dialogInput" />
                </el-form-item>
                <el-form-item label="名字" prop="last_name">
                    <el-input v-model="createUserForm.last_name" />
                </el-form-item>
                <el-form-item label="性别" prop="gender">
                    <el-select
                        v-model="createUserForm.gender"
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
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="createUserForm.email" />
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input v-model="createUserForm.password" type="password" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showCreate = false">取 消</el-button>
                <el-button type="primary" @click="handleCreateUser(createFormRef)">
                    提 交
                </el-button>
            </template>
        </el-dialog>
    </div>
</template>

<style scoped>
.user-manage {
    padding: 2%;
    background-color: #ffffff;
    border: 1px solid #dddddd;
    border-radius: 5px;
}

.el-button .el-icon {
    margin-right: 5%;
}

.pagination_main {
    margin-top: 2%;
}

.search_main {
    margin-bottom: 2%;
}
</style>
