// 通用数据接口类型定义
export interface UpdateForm {
    [key: string]: number | string | boolean | JSON | UpdateForm;
}
