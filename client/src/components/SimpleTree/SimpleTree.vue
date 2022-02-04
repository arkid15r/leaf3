<template>
  <div :id="elementId"></div>
</template>

<script>
import axios from "axios";
import Tree from "./Tree.js";

export default {
  props: ["direction", "personUid", "treeUid"],
  mounted() {
    axios
      .get(
        `/api/tree/${this.treeUid}/person/${this.personUid}/simple-tree/?direction=${this.direction}`
      )
      .then((response) =>
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
        )
      );
  },
  computed: {
    elementId: function () {
      return this.personUid + "-" + this.direction;
    },
  },
};
</script>
