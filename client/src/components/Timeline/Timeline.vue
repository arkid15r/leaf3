<template>
  <div :id="elementId">
    <div v-show="entries.length > 0">
      <h5 class="mt-2">{{ $t("timeline") }}</h5>
      <div class="bg-light">
        <div class="list-feed">
          <div
            v-for="entry in entries"
            :key="entry.text"
            class="list-feed-item border-warning"
          >
            <div class="text-muted font-size-sm mb-1">{{ entry.occurred }}</div>
            <span v-html="entry.text"></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  computed: {
    elementId: function () {
      return `${this.personUid}-timeline`;
    },
  },
  data() {
    return {
      entries: [],
    };
  },
  props: ["personUid", "treeUid"],
  mounted() {
    axios
      .get(`/api/tree/${this.treeUid}/person/${this.personUid}/timeline/`)
      .then((response) => (this.entries = response.data));
  },
};
</script>

<i18n>
{
  "en": {
    "timeline": "Life events",
  },
  "ru": {
    "timeline": "События жизни",
  }
}
</i18n>
