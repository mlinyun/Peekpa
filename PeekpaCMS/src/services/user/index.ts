import type { AxiosResponse } from "axios";
import type { LoginResponse, UserListResponse, UserSetting } from "@/types/User.ts";
import { axiosInstance } from "@/services/Axios.ts";
import type { UpdateForm } from "@/types/Base.ts";

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

// 用户列表
const getAllUsers = (limit: number, offset: number): Promise<AxiosResponse<UserListResponse>> => {
    return axiosInstance.get("/manage/user/", {
        params: {
            limit,
            offset,
        },
    });
};

// 用户搜索
const searchUser = (
    q: string,
    limit: number,
    offset: number,
): Promise<AxiosResponse<UserListResponse>> => {
    return axiosInstance.get("/manage/user/", {
        params: {
            q,
            limit,
            offset,
        },
    });
};

// 更新用户信息
const updateUser = (uid: string, form: UpdateForm): Promise<AxiosResponse<null>> => {
    return axiosInstance.patch(`/manage/user/${uid}/`, form);
};

// 创建用户
const createUser = (form: UpdateForm): Promise<AxiosResponse<null>> => {
    return axiosInstance.post("/manage/user/", form);
};

// 获取用户信息
const getUserInfo = (): Promise<AxiosResponse<UserSetting>> => {
    return axiosInstance.get("/manage/setting/");
};

// 更新用户信息
const updateUserInfo = (form: FormData): Promise<AxiosResponse<null>> => {
    return axiosInstance.patch("/manage/setting/", form, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
};

export {
    userLogin,
    userLogout,
    getAllUsers,
    searchUser,
    updateUser,
    createUser,
    getUserInfo,
    updateUserInfo,
};
