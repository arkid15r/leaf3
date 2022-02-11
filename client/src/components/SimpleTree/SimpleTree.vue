<template>
  <div v-show="loaded">
    <h5 v-if="view == 'ancestors'">{{ $t("ancestors") }}</h5>
    <h5 v-if="view == 'cousins'">{{ $t("cousins") }}</h5>
    <h5 v-if="view == 'descendants'">{{ $t("descendants") }}</h5>
    <h5 v-if="view == 'nephews-nieces'">{{ $t("nephews-nieces") }}</h5>
    <div :id="elementId"></div>
  </div>
</template>

<script>
import axios from "axios";
import Tree from "./Tree.js";

export default {
  computed: {
    elementId: function () {
      return this.personUid + "-" + this.view;
    },
  },
  data() {
    return {
      loaded: false,
    };
  },
  props: ["direction", "personUid", "treeUid", "view"],
  mounted() {
    axios
      .get(
        `/api/tree/${this.treeUid}/person/${this.personUid}/simple-tree/?view=${this.view}`
      )
      .then((response) => {
        document.getElementById(this.elementId).appendChild(
          Tree(response.data, {
            direction: this.direction,
            label: (d) => {
              if (d.birth_year) {
                return `${d.name}, ${d.birth_year}`;
              }

              return d.name;
            },
            title: (d) => `${d.name} ${d.birth_year}`,
            link: (d) => `/tree/${this.treeUid}/person/${d.uid}/view/`,
            width: 1100,
          })
        );
        this.loaded = true;
      });
  },
};
</script>

<i18n>
{
  "en": {
    "ancestors": "Ancestor tree",
    "cousins": "Cousins",
    "descendants": "Descendant tree",
    "nephews-nieces": "Nephews and nieces",
  },
  "ru": {
    "ancestors": "Дерево предков",
    "cousins": "Двоюродные братья и сёстры",
    "descendants": "Дерево потомков",
    "nephews-nieces": "Племянники и племянницы",
  }
}
</i18n>
