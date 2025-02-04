<script setup lang="ts">
import { type LocationQuery, useRoute, useRouter } from "vue-router";
import { ref } from "vue";
import type { CompanyListResponse } from "@/types/Company.ts";
import { getCompanyList } from "@/services/company";
import type { Filter } from "@/types/Base.ts";
import { companyListFilters, companyListOrder } from "@/constants/Filter.ts";
import ROUTER_CONSTANTS from "@/router/constants.ts";

// 路由对象
const route = useRoute();
// 全局路由
const router = useRouter();

const LIMIT = 12;
let curOffset = 0;
const loading = ref<boolean>(false);
const data = ref<CompanyListResponse>();
const total = ref<number>(0);
const curPage = ref<number>(1);
const initSearchKey = ref<string>("");
const filterData = ref<Filter[]>(companyListFilters);
const filterOrder = ref<Filter[]>(companyListOrder);

// 请求公司列表数据
const requestCompanyData = async (offset: number, query: LocationQuery) => {
    try {
        // 数据复位
        loading.value = true;
        initSearchKey.value = "";
        // 请求公司列表数据
        const response = await getCompanyList(LIMIT, offset, query);
        if (response.status === 200) {
            data.value = response.data;
            total.value = response.data.count;
            curPage.value = Math.floor(offset / LIMIT) + 1;
            if (query.q) {
                initSearchKey.value = query.q as string;
            }
        }
        loading.value = false;
        window.scrollTo(0, 0);
    } catch (error) {
        ElMessage.error(`公司列表数据请求错误${error}`);
        loading.value = false;
    }
};

// 页面加载时请求公司列表数据
onMounted(async () => {
    await requestCompanyData(0, route.query);
});

// 处理搜索，过滤器点击事件。原理就是将搜索参数通过路由传递给
// 列表页面，然后列表页面渲染时根据参数搜索
const search = async (param: string, value: string) => {
    const currentQuery = { ...route.query };
    if (value === "" && currentQuery[param]) {
        delete currentQuery[param];
    } else {
        currentQuery[param] = value;
    }
    await router.push({
        name: ROUTER_CONSTANTS.COMPANY_LIST,
        query: currentQuery,
    });
};

// 页面跳转逻辑
const handlePageChange = async (value: number) => {
    curOffset = (value - 1) * LIMIT;
    await requestCompanyData(curOffset, route.query);
};
</script>

<template>
    <div class="company-list">
        <SearchComponent :init-key="initSearchKey" @search-key="search" />
        <div v-if="data" class="list-container">
            <FilterComponent
                :data-list="filterData"
                :query="route.query"
                @search="search"
            ></FilterComponent>
            <FilterComponent
                :data-list="filterOrder"
                :query="route.query"
                @search="search"
            ></FilterComponent>
            <el-row :gutter="20">
                <CompanyCard v-for="item in data.results" :key="item.id" :company="item" />
            </el-row>
            <el-pagination
                class="pagination"
                background
                layout="prev, pager, next"
                :current-page="curPage"
                :total="total"
                :page-size="LIMIT"
                @current-change="handlePageChange"
            ></el-pagination>
        </div>
        <div v-else-if="!loading && !data" class="failure">没有数据，请稍后再试</div>
    </div>
</template>

<style scoped>
.company-list {
    min-height: calc(100vh - 170px - 60px - 40px);
}

.list-container {
    margin: 100px auto 0 auto;
    width: 1200px;
}

.pagination {
    margin: 20px auto 0 auto;
}

.failure {
    text-align: center;
    margin-top: 250px;
    color: var(--theme-primary-color);
    font-weight: bolder;
}
</style>
