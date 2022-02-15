import { createApp } from "vue";
import { createI18n } from "vue-i18n";
import Person from "./Person.vue";

const rootElement = "#person";

const i18n = createI18n({
  locale: document.querySelector("html").getAttribute("lang"),
});

createApp(Person, { ...document.querySelector(rootElement).dataset })
  .use(i18n)
  .mount(rootElement);
