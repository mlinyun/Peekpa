import type { BasePaginationResult } from "@/types/Base.ts";

// 求职者信息
export interface InterviewCandidate {
    // 求职者 UID
    uid: string;
    // 求职者姓名
    name: string;
    // 求职者性别
    gender: number;
    // 求职者邮箱
    email: string;
    // 求职者具体信息
    details: string;
}

// 面试职位
export interface InterviewJob {
    // 面试职位 ID
    id: string;
    // 面试职位名称
    title: string;
    // 面试职位计划招聘人数
    hire_number: number;
    // 面试职位已经招聘人数
    pass_number: number;
}

// 面试的简历
export interface InterviewResume {
    // 简历名称
    name: string;
    // 简历下载的 URL 地址
    url: string;
}

// 面试消息
export interface InterviewInvitation {
    // 面试消息 ID
    id: string;
    // 面试消息回复状态
    response: number;
    // 面试消息内容
    message: string;
    // 面试消息截止时间
    due_time: string;
    // 面试消息创建时间
    publish_time: string;
    // 面试消息更新时间
    update_time: string;
}

// 面试信息
export interface Interview {
    // 面试 ID
    id: string;
    // 面试官
    interviewer: string;
    // 面试状态
    status: number;
    // 面试反馈
    feedback: JSON;
    // 面试求职者
    candidate: InterviewCandidate;
    // 面试职位
    job: InterviewJob;
    // 面试简历
    resume: InterviewResume;
    // 面试消息
    invitation: InterviewInvitation | null;
    // 面试创建时间
    publish_time: string;
}

// 面试列表返回数据
export interface InterviewListResponse extends BasePaginationResult {
    results: Interview[];
}

// 职位名称接口返回的数据
export interface JobNameItem {
    // 职位 ID
    id: string;
    // 职位名称
    title: string;
}

// 面试更新表单
export interface UpdateInterviewForm {
    index: number;
    id: string;
    iid: string;
    feedback: JSON;
    status: number;
    nextRound: string;
    nextFeedback: string;
}
