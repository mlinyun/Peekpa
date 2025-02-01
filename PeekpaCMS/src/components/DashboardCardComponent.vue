<script setup lang="ts">
// 图标
enum Icon {
    chromeFilled = IconEpChromeFilled,
    box = IconEpBox,
    goldMedal = IconEpGoldMedal,
    medal = IconEpMedal,
    folder = IconEpFolder,
    folderOpened = IconEpFolderOpened,
    folderChecked = IconEpFolderChecked,
    folderDelete = IconEpFolderDelete,
    notebook = IconEpNotebook,
    dataLine = IconEpDataLine,
    stopwatch = IconEpStopwatch,
    user = IconEpUser,
}

const props = withDefaults(
    defineProps<{
        title: string;
        count: number;
        icon: string;
    }>(),
    {
        title: "Title",
        count: 0,
        icon: "chromeFilled",
    },
);

// 获取图标组件
const resolveIcon = (icon: string): Icon | undefined => {
    return Icon[icon as keyof typeof Icon];
};
</script>

<template>
    <div class="small-box card">
        <div class="inner">
            <h2>{{ props.count }}</h2>
            <p>{{ props.title }}</p>
        </div>
        <el-icon class="icon">
            <component :is="resolveIcon(props.icon)" />
        </el-icon>
    </div>
</template>

<style scoped>
.small-box {
    height: 100px;
    box-sizing: border-box;
    position: relative;
    background: radial-gradient(
        ellipse at center,
        var(--theme-two-color) 0%,
        var(--theme-one-color) 70%
    );
    background-size: 100%;
    color: var(--theme-three-color);
    text-shadow:
        0 0 20px var(--theme-four-color),
        0 0 20px var(--theme-one-color);
    border-radius: 4px;
}

.inner {
    padding: 10px;
}

.inner p {
    padding-top: 10px;
}

.inner h2 {
    color: var(--theme-four-color);
    padding-top: 5px;
}

.small-box:hover .icon {
    font-size: 55px;
}

.icon {
    font-size: 45px;
    position: absolute;
    right: 10px;
    top: 10px;
    transition: all 0.2s linear;
}
</style>
