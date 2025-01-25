import axios, { AxiosError, type AxiosRequestConfig, type InternalAxiosRequestConfig } from "axios";
// 使用 element-plus 自动导入时，需要将 ElMessage 从 element-plus/es 中导入，而不是从 element-plus 中导入
// import { ElMessage } from "element-plus/es";
import userStore from "@/stores/modules/User.ts";
import router from "@/router";
import ROUTER_CONSTANTS from "@/router/constants.ts";

const UNAUTH_401 = "401: Unauthorized";

// axios 配置
const axiosConfig: AxiosRequestConfig = {
    baseURL: "/api", // api 的 base_url
    timeout: 5000, // 请求超时时间
    withCredentials: true, // 允许跨域携带 cookie
    responseType: "json", // 返回数据类型
    headers: {
        "Content-Type": "application/json;charset=utf-8", // 传输数据类型
    },
};

// 创建 axios 实例
const axiosInstance = axios.create(axiosConfig);

// 获取 CSRF Token 的函数
const getCSRFToken = () => {
    const name = "csrftoken";
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

// 请求拦截器
axiosInstance.interceptors.request.use((config: InternalAxiosRequestConfig) => {
    const newConfig = config;
    // 获取并设置 CSRF Token
    const csrftoken = getCSRFToken();
    if (csrftoken) {
        newConfig.headers["X-CSRFToken"] = csrftoken;
    }
    // 将用户的 JWT 令牌添加到请求头的 Authorization 字段中
    const store = userStore();
    newConfig.headers.authorization = `Bearer ${store.getToken}`;
    return newConfig;
});

// 响应拦截器
axiosInstance.interceptors.response.use(
    (response) => {
        // 处理响应数据
        return response;
    },
    (error) => {
        // 处理响应错误
        if (
            error instanceof AxiosError &&
            error.response?.status === 401 &&
            error.response.data.code === "user_inactive"
        ) {
            const store = userStore();
            store.logout();
            router.replace({
                name: ROUTER_CONSTANTS.LOGIN,
            });
            ElMessage.error("你的身份已经过期！");
            return Promise.reject(Error(UNAUTH_401));
        }
        if (
            error instanceof AxiosError &&
            error.response?.status === 401 &&
            error.response.data.code === "token_not_valid"
        ) {
            const store = userStore();
            store.logout();
            router.replace({
                name: ROUTER_CONSTANTS.LOGIN,
            });
            ElMessage.error("登录状态已过期，请重新登录！");
            return Promise.reject(Error(UNAUTH_401));
        }
        ElMessage.error("请求错误，请稍后重试！");
        return Promise.reject(error);
    },
);

export { axiosInstance, axiosConfig, UNAUTH_401 };
