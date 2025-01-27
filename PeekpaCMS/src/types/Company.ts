import type { BasePaginationResult } from "@/types/Base.ts";

// 公司管理员信息
export interface CompanyManager {
    uid: string; // 用户 UID
    email: string; // 用户邮箱
    password?: string; // 用户密码（可选）
    first_name: string; // 用户名
    last_name: string; // 用户姓
    data_join: string; // 用户创建时间
}

// 公司信息
export interface Company {
    id: string; // 公司 ID
    name: string; // 公司名称
    website: string; // 公司网站
    user: CompanyManager; // 公司管理员信息
}

// 公司列表
export interface CompanyListResponse extends BasePaginationResult {
    results: Company[];
}
