import type { AxiosResponse } from "axios";
import type { JobNameItem, InterviewListResponse, Interview } from "@/types/Interview.ts";
import { axiosInstance } from "@/services/Axios.ts";
import type { UpdateForm } from "@/types/Base.ts";

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

// 面试更新接口
const updateInterview = (
    id: string,
    iid: string,
    form: UpdateForm,
): Promise<AxiosResponse<Interview>> => {
    return axiosInstance.patch(`/manage/job/${id}/interviews/${iid}/`, form);
};

// 创建面试邀请消息接口
const createInvitation = (
    id: string,
    iid: string,
    uid: string,
    message: string,
    status: number,
): Promise<AxiosResponse<null>> => {
    return axiosInstance.post(`/manage/job/${id}/interviews/${iid}/invitation/`, {
        user_id: uid,
        message,
        status,
    });
};

export { getAllJobName, getAllInterviews, searchInterview, updateInterview, createInvitation };
