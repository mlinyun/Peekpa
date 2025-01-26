import type { AxiosResponse } from "axios";
import type { LoginResponse } from "@/types/User.ts";
import { axiosInstance } from "@/services/Axios.ts";

// 用户登录接口
const userLogin = (email: string, password: string): Promise<AxiosResponse<LoginResponse>> => {
    return axiosInstance.post("/auth/login/", {
        email,
        password,
    });
};

// 用户登出接口
const userLogout = (): Promise<AxiosResponse<null>> => {
    return axiosInstance.post("/auth/logout/");
};

export { userLogin, userLogout };
