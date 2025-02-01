export interface DashboardItem {
    // 职位 ID
    id: string;
    // 职位名称
    title: string;
    // 职位创建时间
    publish_time: string;
}

// 首页数据
export interface DashboardResponse {
    // 正在招聘的职位数目
    jobs_open: number;
    // 职位总数
    jobs_total: number;
    // 已经招满的职位数目
    jobs_finish: number;
    // 已关闭的职位数目
    jobs_close: number;
    // 正在面试的人数
    interviewing: number;
    // 收到的简历数目
    resumes: number;
    // 新收到的简历数目
    resumes_new: number;
    // 计划招聘人数
    hired_number: number;
    // 已经招聘人数
    pass_number: number;
    // 公司用户数量
    users_number: number;
    // 面试邀请数量
    invitation_number: number;
    // 新发布的职位列表
    new_jobs: DashboardItem[];
    // 新收到简历列表
    new_interviews: DashboardItem[];
}
