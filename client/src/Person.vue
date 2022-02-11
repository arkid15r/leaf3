<template>
  <div>
    <div v-if="person.has_parents">
      <simple-tree
        :person-uid="personUid"
        :tree-uid="treeUid"
        view="ancestors"
      />
    </div>
    <div v-if="person.has_children">
      <simple-tree
        :person-uid="personUid"
        :tree-uid="treeUid"
        direction="rtl"
        view="descendants"
      />
    </div>
    <div v-if="person.has_nephews_or_nieces">
      <simple-tree
        :person-uid="personUid"
        :tree-uid="treeUid"
        direction="rtl"
        view="nephews-nieces"
      />
    </div>
    <div v-if="person.has_cousins">
      <simple-tree
        :person-uid="personUid"
        :tree-uid="treeUid"
        direction="rtl"
        view="cousins"
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
