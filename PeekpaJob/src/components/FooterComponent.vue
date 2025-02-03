<script setup lang="ts">
import { ref } from "vue";

const year = ref<number>(2025);
year.value = new Date().getFullYear();
</script>

<template>
    <div class="footer_container">
        <ul class="footer_list">
            <li class="footer_li">
                <div class="logo"></div>
            </li>
            <li class="footer_li">
                <div>
                    © {{ year }} Copyright:
                    <a href="https://peekpa.com" target="_blank">peekpa.com</a>
                </div>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.footer_container {
    height: 150px;
    width: 100%;
    min-width: 1250px;
    border-top: 1px solid #e8e8e8;
    background-color: var(--theme-primary-color);
    text-align: center;
    clear: both;
    margin-top: 20px;
    position: relative;
    z-index: 110;
}

.footer_list {
    display: inline-block;
    width: 1200px;
    margin: 0 auto;
    padding-top: 40px;
    list-style: none;
}

.footer_list li {
    float: left;
    width: 100%;
    font-size: 14px;
    color: var(--theme-third-color);
    text-align: center;
}

.footer_li + .footer_li {
    margin-top: 16px;
}

.logo {
    margin: 0 auto;
    width: 135px;
    height: 50px;
    background: url("@/assets/images/logo-black.png") no-repeat center;
    background-size: cover;
}
</style>
