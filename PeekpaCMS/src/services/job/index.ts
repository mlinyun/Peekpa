import type { Job, JobCreate, JobListResponse } from "@/types/Job.ts";
import type { AxiosResponse } from "axios";
import { axiosInstance } from "@/services/Axios.ts";
import type { UpdateForm } from "@/types/Base.ts";

// 创建职位接口
const createJob = (form: JobCreate): Promise<AxiosResponse<null>> => {
    return axiosInstance.post("/manage/job/", {
        ...form,
    });
};

// 获取所有职位接口
const getAllJobs = (limit: number, offset: number): Promise<AxiosResponse<JobListResponse>> => {
    return axiosInstance.get("/manage/job/", {
        params: {
            limit,
            offset,
        },
    });
};

// 搜索职位接口
const searchJob = (
    q: string,
    limit: number,
    offset: number,
): Promise<AxiosResponse<JobListResponse>> => {
    return axiosInstance.get("/manage/job/", {
        params: {
            q,
            limit,
            offset,
        },
    });
};

// 更新职位接口
const updateJob = (id: string, form: UpdateForm): Promise<AxiosResponse<Job>> => {
    return axiosInstance.patch(`/manage/job/${id}/`, form);
};

export { createJob, getAllJobs, searchJob, updateJob };
