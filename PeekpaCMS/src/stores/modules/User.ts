import { defineStore } from "pinia";
import type { LoginResponse, UserAuthorizeInfo } from "@/types/User.ts";
import { jwtDecode } from "jwt-decode";

const PEEKPA_USER = "PeekpaJobCMS";

interface AuthToken {
    token: string;
}

// 定义 User Store
const userStore = defineStore("User", {
    // state 定义
    state: (): AuthToken => {
        return {
            token: localStorage.getItem(PEEKPA_USER) || "",
        };
    },
    // getters 定义
    getters: {
        // 获取用户
        getUser(auth: AuthToken): UserAuthorizeInfo | null {
            if (!auth.token) {
                return null;
            }
            return jwtDecode(auth.token) as UserAuthorizeInfo;
        },
        // 获取用户 JWT 令牌
        getToken(auth: AuthToken): string {
            return auth.token;
        },
    },
    // actions 定义
    actions: {
        // 判断是否有用户登录信息
        isLogin(): boolean {
            if (this.token === "") {
                return false;
            }
            const parsed = jwtDecode(this.token) as UserAuthorizeInfo;
            return parsed.exp * 1000 > Date.now();
        },
        // 存储/更新用户登录信息
        login(auth: LoginResponse): void {
            this.token = auth.token;
            localStorage.setItem(PEEKPA_USER, auth.token);
        },
        // 清除用户登录信息
        logout(): void {
            this.token = "";
            localStorage.removeItem(PEEKPA_USER);
        },
    },
});

export default userStore;
