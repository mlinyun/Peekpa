import type { AxiosResponse } from "axios";
import type { AvatarResponse, LoginResponse } from "@/types/User.ts";
import { axiosInstance } from "@/services/Axios.ts";
import type { UpdateForm } from "@/types/Base.ts";

// 登录接口
const signin = (email: string, password: string): Promise<AxiosResponse<LoginResponse>> => {
    return axiosInstance.post("/auth/signin/", {
        email,
        password,
    });
};

// 注册接口
const signup = (form: UpdateForm): Promise<AxiosResponse<LoginResponse>> => {
    return axiosInstance.post("/auth/signup/", form);
};

// 更新用户信息接口
const updateUserInfo = (form: UpdateForm): Promise<AxiosResponse<null>> => {
    const updateForm: UpdateForm = {};
    updateForm.details = {};
    Object.entries(form).forEach(([key, value]) => {
        Object.assign(updateForm, { [key]: value });
    });
    return axiosInstance.patch("/profile/", updateForm);
};

// 头像上传接口
const uploadAvatar = (file: File): Promise<AxiosResponse<AvatarResponse>> => {
    const formData = new FormData();
    formData.append("avatar", file);
    return axiosInstance.post("/avatar/upload/", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
};

// 登出接口
const userLogout = (): Promise<AxiosResponse<null>> => {
    return axiosInstance.post("/auth/logout/");
};

export { signin, signup, updateUserInfo, uploadAvatar, userLogout };
