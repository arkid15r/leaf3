<template>
  <div>
    <div v-if="parentsCount > 0">
      <h5>{{ $t("ancestors") }}</h5>
      <simple-tree
        direction="ancestor"
        :person-uid="personUid"
        :tree-uid="treeUid"
      />
    </div>
    <div v-if="childrenCount > 0">
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
import SimpleTree from "./components/SimpleTree/SimpleTree.vue";

export default {
  name: "person",
  components: { SimpleTree },
  props: {
    childrenCount: String,
    parentsCount: String,
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
