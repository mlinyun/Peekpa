import type { BasePaginationResult } from "@/types/Base.ts";

// 求职者信息
export interface InterviewCandidate {
    uid: string; // 求职者 UID
    name: string; // 求职者姓名
    gender: number; // 求职者性别
    email: string; // 求职者邮箱
    details: string; // 求职者具体信息
}

// 面试职位
export interface InterviewJob {
    id: string; // 面试职位 ID
    title: string; // 面试职位名称
    hire_number: number; // 面试职位计划招聘人数
    pass_number: number; // 面试职位已经招聘人数
}

// 面试的简历
export interface InterviewResume {
    name: string; // 简历名称
    url: string; // 简历下载的 URL 地址
}

// 面试消息
export interface InterviewInvitation {
    id: string; // 面试消息 ID
    response: number; // 面试消息回复状态
    message: string; // 面试消息内容
    due_time: string; // 面试消息截止时间
    publish_time: string; // 面试消息创建时间
    update_time: string; // 面试消息更新时间
}

// 面试信息
export interface Interview {
    id: string; // 面试 ID
    interviewer: string; // 面试官
    status: number; // 面试状态
    feedback: JSON; // 面试反馈
    candidate: InterviewCandidate; // 面试求职者
    job: InterviewJob; // 面试职位
    resume: InterviewResume; // 面试简历
    invitation: InterviewInvitation | null; // 面试消息
    publish_time: string; // 面试创建时间
}

// 面试列表返回数据
export interface InterviewListResponse extends BasePaginationResult {
    results: Interview[];
}

// 职位名称接口返回的数据
export interface JobNameItem {
    id: string; // 职位 ID
    title: string; // 职位名称
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
