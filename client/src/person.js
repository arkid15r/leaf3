import { createApp } from "vue";
import Person from "./Person.vue";

const mountToId = "#trees";
const mountTo = document.querySelector(mountToId);

createApp(Person, { ...mountTo.dataset }).mount(mountToId);
