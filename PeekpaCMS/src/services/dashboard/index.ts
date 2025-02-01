import type { AxiosResponse } from "axios";
import type { DashboardResponse } from "@/types/Dashboard.ts";
import { axiosInstance } from "@/services/Axios.ts";

// 首页接口
const getDashboard = (): Promise<AxiosResponse<DashboardResponse>> => {
    return axiosInstance.get("/manage/dashboard/");
};

export default getDashboard;
