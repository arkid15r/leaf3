<template>
  <div>
    <div v-if="person.has_parent">
      <simple-tree
        :person-uid="personUid"
        :tree-uid="treeUid"
        view="ancestors"
      />
    </div>
    <div v-if="person.has_child">
      <simple-tree
        :person-uid="personUid"
        :tree-uid="treeUid"
        direction="rtl"
        view="descendants"
      />
    </div>
    <div v-if="person.has_nephew_or_niece">
      <simple-tree
        :person-uid="personUid"
        :tree-uid="treeUid"
        direction="rtl"
        view="nephews-nieces"
      />
    </div>
    <div v-if="person.has_cousin">
      <simple-tree
        :person-uid="personUid"
        :tree-uid="treeUid"
        direction="rtl"
        view="cousins"
      />
    </div>
    <div v-if="person.has_cousin_nephew_or_niece">
      <simple-tree
        :person-uid="personUid"
        :tree-uid="treeUid"
        direction="rtl"
        view="cousin-nephews-nieces"
      />
    </div>
    <div v-if="person.has_second_cousin">
      <simple-tree
        :person-uid="personUid"
        :tree-uid="treeUid"
        direction="rtl"
        view="second-cousins"
      />
    </div>
    <div v-if="person.has_timeline">
      <timeline :person-uid="personUid" :tree-uid="treeUid" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SimpleTree from "./components/SimpleTree/SimpleTree.vue";
import Timeline from "./components/Timeline/Timeline.vue";

export default {
  name: "person",
  components: { SimpleTree, Timeline },
  data() {
    return {
      person: {},
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
