import { fileURLToPath, URL } from "node:url";

import { defineConfig, ProxyOptions } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";
import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers";
import Icons from "unplugin-icons/vite";
import IconsResolver from "unplugin-icons/resolver";
import Inspect from "vite-plugin-inspect";

const pathSrc = fileURLToPath(new URL("./src", import.meta.url));

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        vueDevTools(),
        AutoImport({
            // 自动导入 Vue 相关函数，如：ref, reactive, toRef 等
            imports: ["vue"],
            // 自动导入 Element Plus 相关函数，如：ElMessage, ElMessageBox... (带样式)
            resolvers: [
                ElementPlusResolver(),
                // 自动导入图标组件
                IconsResolver({
                    prefix: "icon",
                }),
            ],
            dts: pathSrc + "/auto-imports.d.ts",
        }),
        Components({
            resolvers: [
                // 自动注册图标组件
                IconsResolver({
                    enabledCollections: ["ep"],
                }),
                // 自动导入 Element Plus 组件
                ElementPlusResolver(),
            ],
            dts: pathSrc + "/components.d.ts",
        }),

        Icons({
            autoInstall: true,
        }),

        Inspect(),
    ],
    resolve: {
        alias: {
            "@": pathSrc,
        },
    },
    // 配置服务器的代理设置
    server: {
        port: 5173,
        open: true,
        // 代理设置，将 /api 开头的请求代理到 http://localhost:8081
        proxy: {
            "/api": {
                // 目标服务器地址（不能写 localhost）
                target: "http://127.0.0.1:8081/api",
                // 更改请求头中的 origin 为代理服务器地址
                changeOrigin: true,
                // 重写请求路径，将 /api 开头的路径去掉 /api
                rewrite: (path) => path.replace(/^\/api/, ""),
            } as ProxyOptions,
        },
    },
});
