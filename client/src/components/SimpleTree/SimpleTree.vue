<template>
  <div v-show="loaded">
    <h5 v-if="direction == 'ancestor'">{{ $t("ancestors") }}</h5>
    <h5 v-if="direction == 'descendant'">{{ $t("descendants") }}</h5>
    <div :id="elementId"></div>
  </div>
</template>

<script>
import axios from "axios";
import Tree from "./Tree.js";

export default {
  computed: {
    elementId: function () {
      return this.personUid + "-" + this.direction;
    },
  },
  data() {
    return {
      loaded: false,
    };
  },
  props: ["direction", "personUid", "treeUid"],
  mounted() {
    axios
      .get(
        `/api/tree/${this.treeUid}/person/${this.personUid}/simple-tree/?direction=${this.direction}`
      )
      .then((response) => {
        document.getElementById(this.elementId).appendChild(
          Tree(response.data, {
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
    "ancestors": "Ancestors",
    "descendants": "Descendants",
  },
  "ru": {
    "ancestors": "Предки",
    "descendants": "Потомки",
  }
}
</i18n>
