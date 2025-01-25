import type { AxiosResponse } from "axios";
import type { LoginResponse } from "@/types/User.ts";
import { axiosInstance } from "@/services/Axios.ts";

// 登录接口
const login = (email: string, password: string): Promise<AxiosResponse<LoginResponse>> => {
    return axiosInstance.post("/auth/login/", {
        email,
        password,
    });
};

export { login };
