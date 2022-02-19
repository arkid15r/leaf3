<script>
import $ from "jquery";

export default {
  methods: {
    deathYearChange() {
      let blocks = [
        $("#div_id_burial_date"),
        $("#div_id_burial_place_uid"),
        $("#div_id_death_cause"),
        $("#div_id_death_cause_details"),
        $("#div_id_death_date"),
        $("#div_id_death_place_uid"),
      ];

      if ($("#id_death_year").val()) {
        blocks.forEach((b) => b.show());
      } else {
        blocks.forEach((b) => b.hide());
      }
    },
  },
  created() {
    $("#id_death_year").keyup(this.deathYearChange);
    this.deathYearChange();
  },
};
</script>
