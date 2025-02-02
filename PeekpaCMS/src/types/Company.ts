import type { BasePaginationResult } from "@/types/Base.ts";

// 公司管理员信息
export interface CompanyManager {
    // 用户 UID
    uid: string;
    // 用户邮箱
    email: string;
    // 用户密码（可选）
    password?: string;
    // 用户名
    first_name: string;
    // 用户姓
    last_name: string;
    // 用户创建时间
    data_join: string;
}

// 公司信息
export interface Company {
    // 公司 ID
    id: string;
    // 公司名称
    name: string;
    // 公司网站
    website: string;
    // 公司管理员信息
    user: CompanyManager;
}

// 公司列表
export interface CompanyListResponse extends BasePaginationResult {
    results: Company[];
}
