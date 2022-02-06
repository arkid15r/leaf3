import { createApp } from "vue";
import { createI18n } from "vue-i18n";
import Person from "./Person.vue";

const mountToId = "#trees";
const mountTo = document.querySelector(mountToId);

const i18n = createI18n({
  locale: document.querySelector("html").getAttribute("lang"),
});

const app = createApp(Person, { ...mountTo.dataset });
app.use(i18n);
app.mount(mountToId);
