import type { JobCreate } from "@/types/Job.ts";
import type { AxiosResponse } from "axios";
import { axiosInstance } from "@/services/Axios.ts";

// 创建职位接口
const createJob = (form: JobCreate): Promise<AxiosResponse<null>> => {
    return axiosInstance.post("/manage/job/", {
        ...form,
    });
};

export { createJob };
