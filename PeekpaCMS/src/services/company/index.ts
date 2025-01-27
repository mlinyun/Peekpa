import type { AxiosResponse } from "axios";
import type { CompanyListResponse } from "@/types/Company.ts";
import type { UpdateForm } from "@/types/Base.ts";
import { axiosInstance } from "@/services/Axios.ts";

// 公司列表接口
const getAllCompanies = (
    limit: number,
    offset: number,
): Promise<AxiosResponse<CompanyListResponse>> => {
    return axiosInstance.get("/manage/company/", {
        params: {
            limit,
            offset,
        },
    });
};

// 搜索公司接口
const searchCompany = (
    q: string,
    limit: number,
    offset: number,
): Promise<AxiosResponse<CompanyListResponse>> => {
    return axiosInstance.get("/manage/company/", {
        params: {
            q,
            limit,
            offset,
        },
    });
};

// 公司创建接口
const createCompany = (form: UpdateForm): Promise<AxiosResponse<null>> => {
    return axiosInstance.post("/manage/company/", form);
};

export { getAllCompanies, searchCompany, createCompany };
