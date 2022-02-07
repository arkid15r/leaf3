<template>
  <div>
    <div v-if="person.has_parents">
      <h5>{{ $t("ancestors") }}</h5>
      <simple-tree
        direction="ancestor"
        :person-uid="personUid"
        :tree-uid="treeUid"
      />
    </div>
    <div v-if="person.has_children">
      <h5 class="mt-2">{{ $t("descendants") }}</h5>
      <simple-tree
        direction="descendant"
        :person-uid="personUid"
        :tree-uid="treeUid"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SimpleTree from "./components/SimpleTree/SimpleTree.vue";

export default {
  name: "person",
  components: { SimpleTree },
  data() {
    return {
      person: null,
    };
  },
  created() {
    axios
      .get(`/api/tree/${this.treeUid}/person/${this.personUid}/`)
      .then((response) => (this.person = response.data));
  },
  props: {
    personUid: String,
    treeUid: String,
  },
};
</script>

<i18n>
{
  "en": {
    "ancestors": "Ancestors",
    "descendants": "Descendants"
  },
  "ru": {
    "ancestors": "Предки",
    "descendants": "Потомки"
  }
}
</i18n>
