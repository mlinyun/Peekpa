// 用户 store 信息，用于存储在 JWT 令牌信息解析后的结果
export interface UserAuthorizeInfo {
    // 过期时间
    exp: number;
    // 签发时间
    iat: number;
    // 用户 ID
    uid: string;
    // 是否是公司人员
    is_staff: boolean;
    // 是否是公司经理
    is_manager: boolean;
    // 是否是超级管理员
    is_superuser?: boolean;
    // 邮箱
    email: string;
    // 用户名
    name: string;
}

// 系统登录接口返回的内容
export interface LoginResponse {
    token: string;
}
