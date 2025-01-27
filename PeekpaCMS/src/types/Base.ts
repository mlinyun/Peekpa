// 存储带有分页结果的列表数据
export interface BasePaginationResult {
    count: number;
    next: string | null;
    previous: string | null;
}

// 表单修改数据
export interface UpdateForm {
    [key: string]: number | string | boolean | JSON;
}
