// 用户 store 信息，用于存储在 JWT 令牌信息解析后的结果
import type { BasePaginationResult } from "@/types/Base.ts";

export interface UserAuthorizeInfo {
    exp: number; // 过期时间
    iat: number; // 签发时间
    uid: string; // 用户 ID
    is_staff: boolean; // 是否是公司人员
    is_manager: boolean; // 是否是公司经理
    is_superuser?: boolean; // 是否是超级管理员
    email: string; // 邮箱
    name: string; // 用户名
}

// 系统登录接口返回的内容
export interface LoginResponse {
    token: string;
}

// 用户信息
export interface User {
    uid: string;
    email: string;
    first_name: string;
    last_name: string;
    gender: number;
    data_join: string;
    last_login: string;
    password?: string;
    is_active: boolean;
}

// 用户列表接口返回的内容
export interface UserListResponse extends BasePaginationResult {
    results: User[];
}
