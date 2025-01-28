import type { BasePaginationResult } from "@/types/Base.ts";

// 创建职位所需的数据内容
export interface JobCreate {
    title: string; // 职位名称
    status: number; // 职位状态
    city: string; // 职位所在城市
    location: string; // 职位所在具体地点
    salary_min: number; // 月最低薪资
    salary_max: number; // 月最高薪资
    salary_count: number; // 薪资计算方式（一年几薪）
    hire_number: number; // 职位招聘人数
    experience: string; // 职位经验要求
    benefit: string; // 职位福利
    description: string; // 职位具体描述
    education: string; // 职位学历要求
}

// 职位数据内容
export interface Job extends JobCreate {
    id: string; // 职位ID
    pass_number: number; // 职位通过数
    publish_time: string; // 职位通过时间
    resumes: number; // 职位收到简历数
}

// 职位列表返回数据
export interface JobListResponse extends BasePaginationResult {
    results: Job[];
}
