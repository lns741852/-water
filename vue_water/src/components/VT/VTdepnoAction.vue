<template>
  <div class="VDepAction">
    <button @click.prevent="checkDetails" title="編輯部門">
      <img src="../../assets/img/setting_emp.png"  alt="" />
    </button>
    <button @click.prevent="dlATTdata" title="刪除部門" >
      <img  src="../../assets/img/delete.png" style="margin-bottom: -5px;"  alt=""/>
    </button>
  </div>
</template>

<script>
import { Event } from "vue-tables-2";

export default {
  name: "VTdepnoAction",
  props: ["data", "index", "column"],
  data() {
    return {};
  },
  created() {},
  mounted() {},
  methods: {
    dlATTdata() {
      Event.$emit("vue-tables.dlATTdata", this.data);
    },
    checkDetails() {
      Event.$emit("vue-tables.checkDetails", this.data);
    },

  },
};
</script>
