<script setup lang="ts">
import { useRouter } from "vue-router";

const router = useRouter();

// 重定向到首页
const redirectToHome = () => {
    router.push("/");
};
</script>

<template>
    <div class="not-found">
        <div class="center-xy">
            <p>404, 页面未找到 ...</p>
            <button @click="redirectToHome" class="home-button">返回首页</button>
        </div>
    </div>
</template>

<style scoped>
.not-found {
    height: 100vh;
    background: radial-gradient(
        ellipse at center,
        var(--theme-two-color) 0%,
        var(--theme-one-color) 70%
    );
    background-size: 100%;
    color: var(--theme-three-color);
}

.center-xy {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
}

p {
    font-size: 24px;
    letter-spacing: 0.2px;
    margin: 0;
}

.home-button {
    margin-top: 20px;
    padding: 10px 20px;
    font-size: 16px;
    color: var(--theme-three-color);
    background-color: var(--theme-one-color);
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition:
        background-color 0.3s,
        transform 0.3s;
}

.home-button:hover {
    background-color: var(--theme-two-color);
    transform: scale(1.05);
}
</style>
