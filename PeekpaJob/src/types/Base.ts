// 通用数据接口类型定义
export interface UpdateForm {
    [key: string]: number | string | boolean | JSON | UpdateForm;
}

// 存储带有分页结果的列表数据
export interface BasePaginationResult {
    count: number;
    next: string | null;
    previous: string | null;
}

// 过滤器单个按钮
export interface FilterItem {
    // 显示内容
    name: string;
    // 搜索参数
    param: string;
    // 是否高亮显示
    active?: boolean;
}

// 过滤器按钮组
export interface Filter {
    // 组标题
    title: string;
    // 组参数
    param: string;
    // 子按钮列表
    filters: FilterItem[];
}
