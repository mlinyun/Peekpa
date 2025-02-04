// 公司列表接口
import type { AxiosResponse } from "axios";
import type { CompanyListResponse } from "@/types/Company.ts";
import type { LocationQuery } from "vue-router";
import { axiosInstance } from "@/services/Axios.ts";

const getCompanyList = (
    limit: number,
    offset: number,
    params: LocationQuery,
): Promise<AxiosResponse<CompanyListResponse>> => {
    return axiosInstance.get("/company/", {
        params: {
            limit,
            offset,
            ...params,
        },
    });
};

export { getCompanyList };
