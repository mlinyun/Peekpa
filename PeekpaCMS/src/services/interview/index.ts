import type { AxiosResponse } from "axios";
import type { JobNameItem, InterviewListResponse } from "@/types/Interview.ts";
import { axiosInstance } from "@/services/Axios.ts";

// 职位名称接口
const getAllJobName = (): Promise<AxiosResponse<JobNameItem[]>> => {
    return axiosInstance.get("/manage/job/list/");
};

// 面试列表接口
const getAllInterviews = (
    id: string,
    limit: number,
    offset: number,
): Promise<AxiosResponse<InterviewListResponse>> => {
    return axiosInstance.get(`/manage/job/${id}/interviews/`, {
        params: {
            limit,
            offset,
        },
    });
};

// 面试列表搜索接口
const searchInterview = (
    q: string,
    id: string,
    limit: number,
    offset: number,
): Promise<AxiosResponse<InterviewListResponse>> => {
    return axiosInstance.get(`/manage/job/${id}/interviews/`, {
        params: {
            q,
            limit,
            offset,
        },
    });
};

export { getAllJobName, getAllInterviews, searchInterview };
