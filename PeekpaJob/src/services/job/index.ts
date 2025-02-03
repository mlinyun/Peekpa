import type { AxiosResponse } from "axios";
import type { ResumeResponse } from "@/types/Job.ts";
import { axiosInstance } from "@/services/Axios.ts";

// 简历上传接口
const uploadResume = (file: File): Promise<AxiosResponse<ResumeResponse>> => {
    const formData = new FormData();
    formData.append("resume", file);
    return axiosInstance.post("/resume/upload/", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
};

export { uploadResume };
