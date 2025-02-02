// 枚举类，罗列出项目中所有页面的名字，方便在代码中引用
const enum ROUTER_CONSTANTS {
    // 登录页面
    SIGN_IN = "SignIn",
    // 注册页面
    SIGN_UP = "SignUp",
    // 首页
    INDEX = "Index",
    // 职位列表页面
    JOB_LIST = "JobList",
    // 职位详情页面
    JOB_DETAIL = "JobDetail",
    // 公司列表页面
    COMPANY_LIST = "CompanyList",
    // 公司详情页面
    COMPANY_DETAIL = "CompanyDetail",
    // 个人信息页面
    PROFILE = "Profile",
    // 404 页面
    NOTFOUND_404 = "Notfound",
}

export default ROUTER_CONSTANTS;
