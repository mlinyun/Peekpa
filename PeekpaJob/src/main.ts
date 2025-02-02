import "./assets/main.css";
import { createApp } from "vue";
import App from "./App.vue";
import stores from "@/stores";
import router from "./router";

const app = createApp(App);

app.use(stores);
app.use(router);

app.mount("#app");
