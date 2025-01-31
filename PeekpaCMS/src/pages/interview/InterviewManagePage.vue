<script setup lang="ts">
import { reactive, ref } from "vue";
import type {
    Interview,
    InterviewInvitation,
    InterviewListResponse,
    JobNameItem,
    UpdateInterviewForm,
} from "@/types/Interview.ts";
import {
    createInvitation,
    getAllInterviews,
    getAllJobName,
    updateInterview,
} from "@/services/interview";
import { UNAUTH_401 } from "@/services/Axios.ts";
import { useRoute } from "vue-router";
import { timeStampFormat } from "@/utils/Helper.ts";
import { ElMessageBox, type FormInstance, type InputInstance } from "element-plus";
import type { MessageForm } from "@/types/Message.ts";
import type { AxiosError } from "axios";

const route = useRoute();

const LIMIT = 10;
let curOffset = 0;
const interviewStatus = ["第1轮", "第2轮", "第3轮", "HR轮", "通过", "不合格", "已拒绝"];
const interviewStatusCN = ["第一轮", "第二轮", "第三轮", "HR轮", "通过", "不合格", "已拒绝"];

const currentJob = ref<string>("all");
const nameList = ref<JobNameItem[]>([]);
const search = ref<string>("");
const loading = ref<boolean>(false);
const data = ref<InterviewListResponse>();
const total = ref<number>(0);
const curPage = ref<number>(1);
const showUpdate = ref<boolean>(false);
const showMessage = ref<boolean>(false);
const dialogInput = ref<InputInstance>();

const messageForm = reactive<MessageForm>({
    jobId: "",
    id: "",
    candidateId: "",
    message: "",
    name: "",
    status: 0,
});

const updateFormRef = ref<FormInstance>();

const updateForm = reactive<UpdateInterviewForm>({
    index: -1,
    id: "",
    iid: "",
    feedback: {} as JSON,
    status: -1,
    nextRound: "",
    nextFeedback: "",
});

// 请求工作名称数据
const requestJobNameData = async () => {
    try {
        const response = await getAllJobName();
        if (response.status === 200) {
            nameList.value = response.data;
            nameList.value.splice(0, 0, {
                id: "all",
                title: "全部",
            });
        }
    } catch (error) {
        if ((error as Error).message === UNAUTH_401) {
            ElMessage.error(`请求工作名称列表错误[${error}]`);
        }
    }
};

// 获取面试信息数据
const requestInterviewData = async (id: string, offset: number) => {
    loading.value = true;
    try {
        const response = await getAllInterviews(id, LIMIT, offset);
        if (response.status === 200) {
            data.value = response.data;
            total.value = response.data.count;
            curPage.value = Math.floor(offset / LIMIT) + 1;
        }
        loading.value = false;
    } catch (error) {
        if ((error as Error).message === UNAUTH_401) {
            ElMessage.error(`面试信息数据请求错误${error}`);
        }
        loading.value = false;
    }
};

// 第一次进入页面，判断请求是否携带职位 ID，如果携带，则直接按照职位 ID 搜索，否则就返回全部面试信息
onMounted(async () => {
    await requestJobNameData();
    if (route.query.job_id) {
        currentJob.value = route.query.job_id as string;
    }
    await requestInterviewData(currentJob.value, 0);
});

// 切换工作名称方法
const changeSelectJob = async (id: string) => {
    currentJob.value = id;
    curOffset = 0;
};

// 搜索职位方法
const handleSearch = async () => {
    curOffset = 0;
};

// 清空搜索方法
const clearSearch = async () => {
    search.value = "";
    curOffset = 0;
};

// TODO: 职位 URL，这里请根据实际情况配置 URL
const getJobURL = (item: Interview) => {
    return `http://localhost:8081/api/job/${item.id}/`;
};

// TODO: 简历 URL，这里请根据实际情况配置 URL
const getResumeURL = (path: string) => {
    return `http://localhost:8081/${path}/`;
};

// 判断状态
const pendingInvitation = (invitation: InterviewInvitation | null) => {
    if (!invitation) return true;
    if (invitation.response === 0) {
        return true;
    }
    return false;
};

// 进度列表内容
const displayStatus = (interview: Interview) => {
    let message = interviewStatus[interview.status];
    if (interview.status < 4 && pendingInvitation(interview.invitation)) {
        message = `${message}前`;
    }
    return message;
};

// 动态生产进度列样式
const displayStatusClass = (interview: Interview) => {
    if ((interview.status = 4)) {
        return "success";
    }
    if (interview.status === 5 || interview.status === 6) {
        return "danger";
    }
    return "default";
};

// 判断是否禁用按钮
const isDisabled = (item: Interview) => {
    if (
        item.invitation?.response === 2 ||
        item.status === 4 ||
        item.status === 5 ||
        item.status === 6
    ) {
        return true;
    }
    return false;
};

// 判断面试邀请是否过期
const invitationIsExpired = (dueTime: string) => {
    return new Date(dueTime) < new Date();
};

// 显示面试邀请对话框
const showMessageWindow = (item: Interview) => {
    showMessage.value = true;
    messageForm.jobId = item.job.id;
    messageForm.id = item.id;
    messageForm.candidateId = item.candidate.uid;
    messageForm.name = item.candidate.name;
    messageForm.status = item.status;
};

// 动态生产 HTML 内容
const invitationHTML = (message: string, time: string, update?: string) => {
    const timeString = timeStampFormat(time);
    let html = `<p>${message}</p><p>邀请时间：${timeString}</p>`;
    if (update) {
        const updateString = timeStampFormat(update);
        html += `<p>更新时间：${updateString}</p>`;
    }
    return html;
};

// 展示最小面试反馈
const displayFeedback = (feedback: JSON) => {
    if (Object.keys(feedback).length === 0) {
        return "暂无反馈";
    }
    return `${
        Object.keys(feedback)[Object.keys(feedback).length - 1]
    }: ${Object.values(feedback).pop()}`;
};

// 格式化时间
const displayTime = (time: string) => {
    if (!time) return time;
    return timeStampFormat(time);
};

// 判断面试状态
const isPending = (item: Interview) => {
    return !item.invitation || item.invitation.response === 0;
};

// 判断按钮颜色
const getButtonType = (item: Interview) => {
    return isPending(item) && [1, 2, 3, 0].indexOf(item.status) !== -1 ? "warning" : "primary";
};

// 显示填写反馈对话框
const showUpdateWindow = (index: number, item: Interview) => {
    // console.log("index: ", index, "item:", item);
    showUpdate.value = true;
    updateForm.feedback = item.feedback;
    updateForm.id = item.id;
    updateForm.iid = item.job.id;
    updateForm.index = index;
    updateForm.status = item.status + 1;
    updateForm.nextRound = interviewStatusCN[item.status];
    updateForm.nextFeedback = "";
};

// 拒绝操作
const handleReject = (index: number, item: Interview) => {
    // console.log("index: ", index, "item:", item);
    ElMessageBox.confirm(`确定要拒绝求职者 ${item.candidate.name} 的申请么?`, "警告", {
        confirmButtonText: "拒绝",
        cancelButtonText: "取消",
        type: "error",
    })
        .then(async () => {
            const response = await updateInterview(item.job.id, item.id, { status: 5 });
            if (response.status === 200) {
                ElMessage.success("拒绝求职者成功！");
                if (data.value !== undefined) {
                    data.value.results[index] = response.data;
                }
            } else {
                ElMessage.error(`拒绝求职者失败[${response.status}].`);
            }
        })
        .catch((error) => {
            if ((error as AxiosError).name === "CanceledError" && error === "cancel") {
                ElMessage.error("发生网络错误！");
            }
        });
};

// 页面跳转方法
const handlePageChange = async (page: number) => {
    curOffset = (page - 1) * LIMIT;
    await requestInterviewData(currentJob.value, curOffset);
};

// 处理对话框焦点方法
const handleDialogOpen = () => {
    nextTick(() => {
        if (dialogInput.value) {
            dialogInput.value.focus();
        }
    });
};

// 获取求职者名称
const getCandidateName = () => {
    return `发送邀请给 ${messageForm.name}`;
};

// 创建面试邀请消息
const sendInvitation = async () => {
    try {
        const response = await createInvitation(
            messageForm.jobId,
            messageForm.id,
            messageForm.candidateId,
            messageForm.message,
            messageForm.status,
        );
        if (response.status === 201) {
            ElMessage.success("发送邀请成功！");
            // 重置消息内容
            messageForm.jobId = "";
            messageForm.id = "";
            messageForm.candidateId = "";
            messageForm.message = "";
            messageForm.name = "";
            await requestInterviewData(currentJob.value, curOffset);
        }
        showMessage.value = false;
    } catch (error) {
        ElMessage.error(`发送邀请失败[${(error as Error).message}].`);
        showMessage.value = false;
    }
};

// 显示这一轮面试进度
const displayNextRound = () => {
    return `本次反馈(${updateForm.nextRound})`;
};

// 更新面试反馈
const handleUpdate = async (formEl: FormInstance | undefined) => {
    if (!formEl) {
        return;
    }
    await formEl.validate(async (valid: boolean) => {
        if (valid) {
            try {
                updateForm.feedback = {
                    ...updateForm.feedback,
                    [updateForm.nextRound]: updateForm.nextFeedback,
                };
                const response = await updateInterview(updateForm.id, updateForm.iid, {
                    status: updateForm.status,
                    feedback: updateForm.feedback,
                });
                if (response.status === 200) {
                    ElMessage.success("更新面试反馈成功！");
                    showUpdate.value = false;
                    if (data.value !== undefined) {
                        data.value.results[updateForm.index] = response.data;
                    }
                    updateForm.index = -1;
                    formEl.resetFields();
                } else {
                    ElMessage.error(`更新面试反馈失败[${response.status}].`);
                }
            } catch (error) {
                ElMessage.error(`更新面试反馈失败[${(error as AxiosError).message}].`);
            }
        } else {
            ElMessage.error("请检查表单数据是否填写正确！");
        }
    });
};
</script>

<template>
    <div class="interview-manage">
        <el-row class="search_main">
            <el-col :span="6">
                <el-select
                    v-model="currentJob"
                    default-first-option
                    placeholder="工作名称"
                    @change="changeSelectJob($event)"
                >
                    <el-option
                        v-for="item in nameList"
                        :key="item.id"
                        :label="item.title"
                        :value="item.id"
                    >
                        <span class="float-left">{{ item.title }}</span>
                        &nbsp;&nbsp;
                        <span class="float-right">#{{ item.id }}</span>
                    </el-option>
                </el-select>
            </el-col>
            <el-col :span="6" :offset="12">
                <el-input
                    v-model="search"
                    placeholder="搜索"
                    clearable
                    @keyup.enter="handleSearch"
                    @clear="clearSearch"
                >
                    <template #prefix>
                        <el-icon class="el-icon__icon">
                            <i-ep-search />
                        </el-icon>
                    </template>
                </el-input>
            </el-col>
        </el-row>
        <el-table
            v-model="loading"
            border
            header-cell-class-name="table-header"
            :data="data?.results"
        >
            <el-table-column label="职位名称">
                <template #default="scope">
                    <el-link type="primary" :href="getJobURL(scope.row)">
                        {{ scope.row.job.title }}
                    </el-link>
                </template>
            </el-table-column>
            <el-table-column label="求职者" width="80">
                <template #default="scope">
                    {{ scope.row.candidate.name }}
                </template>
            </el-table-column>
            <el-table-column label="简历" width="150">
                <template #default="scope">
                    <el-link type="primary" :href="getResumeURL(scope.row.resume.url)">
                        <el-icon>
                            <i-ep-download />
                        </el-icon>
                        {{ scope.row.resume.name }}
                    </el-link>
                </template>
            </el-table-column>
            <el-table-column label="进度" width="90">
                <template #default="scope">
                    <el-text :type="displayStatusClass(scope.row)">
                        {{ displayStatus(scope.row) }}
                    </el-text>
                </template>
            </el-table-column>
            <el-table-column label="状态" width="125">
                <template #default="scope">
                    <el-text
                        v-if="
                            scope.row.status == 4 || scope.row.status == 5 || scope.row.status == 6
                        "
                    >
                        已结束
                    </el-text>
                    <el-button
                        v-else-if="scope.row.invitation === null"
                        type="primary"
                        text
                        bg
                        :disabled="isDisabled(scope.roe)"
                        @click="showMessageWindow(scope.row)"
                    >
                        未发送邀请
                    </el-button>
                    <el-button
                        v-else-if="
                            scope.row.invitation.response === 0 &&
                            invitationIsExpired(scope.row.invalidate.due_time)
                        "
                        type="primary"
                        text
                        bg
                        :disabled="isDisabled(scope.row)"
                        @click="showMessageWindow(scope.row)"
                    >
                        邀请已过期
                    </el-button>
                    <el-tooltip
                        v-else-if="
                            scope.row.initation.response === 0 &&
                            !invitationIsExpired(scope.row.invalidate.due_time)
                        "
                        :content="
                            invitationHTML(
                                scope.row.invitation.message,
                                scope.row.invalidate.public_time,
                            )
                        "
                        raw-content
                    >
                        <el-text type="warning">未回复</el-text>
                    </el-tooltip>
                    <el-tooltip
                        v-else-if="
                            scope.row.invitation.response === 1 &&
                            !invitationIsExpired(scope.row.invalidate.due_time)
                        "
                        :content="
                            invitationHTML(
                                scope.row.invitation.message,
                                scope.row.invalidate.public_time,
                                scope.row.invalidate.update_time,
                            )
                        "
                        raw-content
                    >
                        <el-text class="mx-1" type="success" tag="b">已同意</el-text>
                    </el-tooltip>
                    <el-tooltip
                        v-else-if="scope.row.invitation.response === 2"
                        :content="
                            invitationHTML(
                                scope.row.invitation.message,
                                scope.row.invalidate.public_time,
                                scope.row.invalidate.update_time,
                            )
                        "
                        raw-content
                    >
                        <el-text class="mx-1" type="danger" tag="b">已拒绝</el-text>
                    </el-tooltip>
                    <el-tooltip
                        v-else-if="scope.row.invitation.response === 3"
                        :content="
                            invitationHTML(
                                scope.row.invitation.message,
                                scope.row.invalidate.public_time,
                                scope.row.invalidate.update_time,
                            )
                        "
                        raw-content
                    >
                        <el-text class="mx-1" type="danger" tag="b">已取消</el-text>
                    </el-tooltip>
                </template>
            </el-table-column>
            <el-table-column label="面试反馈" width="200">
                <template #default="scope">
                    {{ displayFeedback(scope.row.feedback) }}
                </template>
            </el-table-column>
            <el-table-column label="创建时间" width="70">
                <template #default="scope">
                    {{ displayTime(scope.row.publish_time) }}
                </template>
            </el-table-column>
            <el-table-column width="200">
                <template #header>
                    <div class="flex">
                        <div>操作</div>
                    </div>
                </template>
                <template #default="scope">
                    <el-button
                        size="small"
                        plain
                        :type="getButtonType(scope.row)"
                        :disabled="isDisabled(scope.row) || isPending(scope.row)"
                        @click="showUpdateWindow(scope.$index, scope.row)"
                    >
                        <el-icon>
                            <i-ep-document />
                        </el-icon>
                        填写反馈
                    </el-button>
                    <el-button
                        size="small"
                        plain
                        type="danger"
                        :disabled="isDisabled(scope.row)"
                        @click="handleReject(scope.$index, scope.row)"
                    >
                        <el-icon>
                            <i-ep-close />
                        </el-icon>
                        拒绝
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination
            class="pagination_main"
            background
            layout="prev, pager, next"
            :current-page="curPage"
            :total="total"
            :page-size="LIMIT"
            @current-change="handlePageChange"
        ></el-pagination>
        <el-dialog
            v-model="showUpdate"
            title="填写面试反馈信息"
            width="50%"
            @open="handleDialogOpen"
        >
            <el-form ref="updateFormRef" :model="updateForm">
                <div v-if="updateForm.feedback && Object.keys(updateForm.feedback).length">
                    <el-form-item label="历史记录">
                        <el-col
                            v-for="(value, key) in updateForm.feedback"
                            :key="key"
                            :offset="2"
                            :span="22"
                        >
                            <el-row>
                                <el-col :span="4">{{ key }}</el-col>
                                <el-col :span="20">{{ value }}</el-col>
                            </el-row>
                        </el-col>
                    </el-form-item>
                </div>
                <el-form-item :label="displayNextRound()" prop="description">
                    <el-input
                        v-model="updateForm.nextFeedback"
                        :autosize="{ minRows: 4 }"
                        type="textarea"
                    ></el-input>
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="showUpdate = false">取 消</el-button>
                    <el-button type="primary" @click="handleUpdate(updateFormRef)">提 交</el-button>
                </div>
            </template>
        </el-dialog>
        <el-dialog v-model="showMessage" :title="getCandidateName()" width="50%">
            <el-form :model="messageForm">
                <el-form-item label="消息内容" prop="description">
                    <el-input
                        v-model="messageForm.message"
                        :autosize="{ minRows: 4 }"
                        type="textarea"
                    ></el-input>
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="showMessage = false">取 消</el-button>
                    <el-button type="primary" @click="sendInvitation()">发送邀请</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<style scoped>
.interview-manage {
    padding: 2%;
    background-color: #ffffff;
    border: 1px solid #dddddd;
    border-radius: 5px;
}

.search_main {
    margin-bottom: 2%;
}

.float-left {
    float: left;
}

.float-right {
    float: right;
    color: var(--el-text-color-secondary);
    font-size: 13px;
}

.flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.pagination_main {
    margin-top: 2%;
}

.dialog-footer {
    display: flex;
    justify-content: flex-end;
    align-items: center;
}
</style>
