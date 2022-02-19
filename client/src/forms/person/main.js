import { createApp } from "vue";
import PersonForm from "@/forms/person/PersonForm.vue";

const rootElement = "#person-form-app";

createApp(PersonForm, { ...document.querySelector(rootElement).dataset }).mount(
  rootElement
);
