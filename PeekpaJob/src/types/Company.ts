import type { BasePaginationResult } from "@/types/Base.ts";

export interface Company {
    // 公司 ID
    id: string;
    // 公司名称
    name: string;
    // 公司标语
    slogan: string;
    // 公司头像
    avatar: string;
    // 公司标签
    tags: string;
    // 公司规模
    size: string;
    // 公司正在招聘的职位数目
    jobs: number;
    // 公司正在面试的人数
    interviews: number;
}

// 公司列表接口返回的内容
export interface CompanyListResponse extends BasePaginationResult {
    results: Company[];
}
