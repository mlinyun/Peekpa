<script setup lang="ts">
import type { CompanyListResponse } from "@/types/Company.ts";
import { ref, reactive } from "vue";
import type { FormInstance, InputInstance } from "element-plus";
import { createCompany, getAllCompanies, searchCompany } from "@/services/company";
import { UNAUTH_401 } from "@/services/Axios.ts";
import { timeStampFormat } from "@/utils/Helper.ts";
import type { AxiosError } from "axios";

interface CreateCompanyForm {
    first_name: string;
    last_name: string;
    email: string;
    password: string;
    company: string;
    website: string;
    name: string;
}

const LIMIT = 10;
let curOffset = 0;

const data = ref<CompanyListResponse>();
const curPage = ref<number>(1);
const total = ref<number>(0);
const showCreate = ref<boolean>(false);
const createFormRef = ref<FormInstance>();
const loading = ref<boolean>(false);
const search = ref<string>("");
const createCompanyForm = reactive<CreateCompanyForm>({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    company: "",
    website: "",
    name: "",
});
const dialogInput = ref<InputInstance>();

// 请求公司列表数据
const requestCompanyData = async (offset: number) => {
    loading.value = true;
    try {
        const response = await getAllCompanies(LIMIT, offset);
        if (response.status === 200) {
            data.value = response.data;
            total.value = response.data.count;
            curPage.value = Math.floor(offset / LIMIT) + 1;
        }
        loading.value = false;
    } catch (error) {
        if ((error as Error).message === UNAUTH_401) {
            ElMessage.error(`公司列表数据请求错误${error}`);
        }
        loading.value = false;
    }
};

// 搜索公司逻辑
const searchCompanyData = async (q: string, offset: number) => {
    loading.value = true;
    try {
        const response = await searchCompany(q, LIMIT, offset);
        if (response.status === 200) {
            data.value = response.data;
            total.value = response.data.count;
            curPage.value = Math.floor(offset / LIMIT) + 1;
        }
        loading.value = false;
    } catch (error) {
        if ((error as Error).message === UNAUTH_401) {
            ElMessage.error(`搜索公司请求错误${error}`);
        }
        loading.value = false;
    }
};

// 公司创建方法
const handleCreateCompany = async (formEl: FormInstance | undefined) => {
    if (!formEl) {
        return;
    }
    await formEl.validate(async (valid: boolean) => {
        if (valid) {
            try {
                const response = await createCompany(createCompanyForm);
                if (response.status === 201) {
                    ElMessage.success("公司创建成功！");
                    formEl.resetFields();
                    showCreate.value = false;
                    await searchCompanyData(search.value, curOffset);
                }
            } catch (error) {
                ElMessage.error(`公司创建失败[${(error as AxiosError).response?.status}].`);
            }
        } else {
            ElMessage.error("请仔细检查表单！");
        }
    });
};

// 页面加载时请求公司数据
onMounted(async () => {
    await requestCompanyData(0);
});

// 页面跳转方法
const handlePageChange = async (page: number) => {
    curOffset = (page - 1) * LIMIT;
    await requestCompanyData(curOffset);
};

// 处理对话框焦点方法
const handleDialogOpen = () => {
    nextTick(() => {
        if (dialogInput.value) {
            dialogInput.value.focus();
        }
    });
};

// 搜索方法
const handleSearch = async () => {
    curOffset = 0;
    if (search.value) {
        await searchCompanyData(search.value, curOffset);
    } else {
        await requestCompanyData(curOffset);
    }
};

// 清空搜索方法
const clearSearch = async () => {
    search.value = "";
    curOffset = 0;
    await requestCompanyData(curOffset);
};

// 时间格式化方法
const displayTime = (time: string) => {
    if (!time) return time;
    return timeStampFormat(time);
};

// 显示公司创建方法
const showCreateWindow = () => {
    showCreate.value = true;
};
</script>

<template>
    <div class="company-manage">
        <el-row class="search_main">
            <el-col :span="6">
                <el-button type="primary" @click="showCreateWindow()">
                    <el-icon>
                        <i-ep-circle-plus-filled />
                    </el-icon>
                    创建新公司
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
            v-loading="loading"
            border
            header-cell-class-name="table-header"
            :data="data?.results"
        >
            <el-table-column label="公司名称">
                <template #default="scope">
                    <span>{{ scope.row.name }}</span>
                </template>
            </el-table-column>
            <el-table-column label="公司网址" width="300">
                <template #default="scope">
                    <el-link :href="scope.row.website" target="_blank">
                        {{ scope.row.website }}
                    </el-link>
                </template>
            </el-table-column>
            <el-table-column label="联系人姓名" width="100">
                <template #default="scope">
                    <div v-if="scope.row.user">
                        <span>
                            {{ scope.row.user.first_name ?? "" }}{{ scope.row.user.last_name }}
                        </span>
                    </div>
                </template>
            </el-table-column>
            <el-table-column label="联系人邮箱" width="200">
                <template #default="scope">
                    <div v-if="scope.row.user">
                        <span>{{ scope.row.user.email }}</span>
                    </div>
                </template>
            </el-table-column>
            <el-table-column label="创建时间" width="180">
                <template #default="scope">
                    <div v-if="scope.row.user">
                        <span>{{ displayTime(scope.row.user.data_join) }}</span>
                    </div>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination
            class="pagination_main"
            background
            @current-change="handlePageChange"
            :current-page="curPage"
            :page-size="LIMIT"
            :total="total"
            layout="prev, pager, next"
        ></el-pagination>
        <el-dialog v-model="showCreate" title="创建新公司" width="50%" @open="handleDialogOpen">
            <el-form ref="createFormRef" :model="createCompanyForm" label-position="top">
                <el-form-item label="公司名称" prop="name">
                    <el-input v-model="createCompanyForm.name" ref="dialogInput" />
                </el-form-item>
                <el-form-item label="公司网站" prop="website">
                    <el-input v-model="createCompanyForm.website" />
                </el-form-item>
                <el-form-item label="联系人姓氏" prop="first_name">
                    <el-input v-model="createCompanyForm.first_name" />
                </el-form-item>
                <el-form-item label="联系人名字" prop="last_name">
                    <el-input v-model="createCompanyForm.last_name" />
                </el-form-item>
                <el-form-item label="联系人邮箱" prop="email">
                    <el-input v-model="createCompanyForm.email" />
                </el-form-item>
                <el-form-item label="联系人密码" prop="password">
                    <el-input v-model="createCompanyForm.password" type="password" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showCreate = false">取 消</el-button>
                <el-button type="primary" @click="handleCreateCompany(createFormRef)">
                    提 交
                </el-button>
            </template>
        </el-dialog>
    </div>
</template>

<style scoped>
.company-manage {
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
