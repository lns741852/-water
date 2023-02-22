<template>
  <div class="EmpManage">
    <div class="top">
      <div class="left">
        <div class="leftBar">
        </div>
      </div>
      <div class="right">
        <div class="rightBar">
          <label>歡迎使用本系統，{{ username }}</label>
         <!-- <a href="/#/Download">表格下載</a> -->
          <!-- <a href="">最新消息</a> -->
          <button @click="logout()">帳號登出</button>
          <a href=""> <img src="../../assets/img/Logo.png" alt="" /></a>
        </div>
      </div>
    </div>
    <div class="empManagemain">
      <h1>部門管理</h1>
      <div style="justify-content: flex-start">
        <div>
          <input
            type="text"
            class="textSearch form-control"
            placeholder="新增部門名稱"
            v-model="dep_name"
          />
          <button
            class="btnAdd"
            style="background-color: #ffffff; margin: 3px 10px"
            @click="submitAddDep()"
          >
            新增部門
          </button>
        </div>
      </div>
      <div class="tableBorder">
        <div class="table">
          <div id="theadbg"></div>
          <v-client-table
            ref="attendanceTable"
            id="attendanceTable"
            v-model="data_Table"
            :columns="table_Columns"
            :options="table_Options"
          ></v-client-table>
        </div>
      </div>
    </div>
    <transition name="editWintran">
      <div class="editWindow" v-show="editwindow">
        <div class="editWindow_content">
          <div class="closeParent">
            <button class="btn btnClose" @click="editDEPtoggle()">X</button>
          </div>
          <div>
            <form ref="editForm" @submit.prevent="updataDEPdata()">
              <h3>員工資料編輯</h3>
              <div class="addForm_box">
                <div class="addForm_row">
                  <div class="addForm_lable">部門名稱:</div>
                  <div class="addForm_input">
                    <input type="tel" v-model="editDep.dep_name" />
                  </div>
                </div>
              </div>
              <br />
              <input type="submit" class="btn" value="確認" />
            </form>
          </div>
        </div>
      </div>
    </transition>
    <div style="height:60px"></div>
  </div>
</template>

<script>
import Vue from "vue";
import { ClientTable, Event } from "vue-tables-2";
import userService from "../../services/user.services";
import authService from "../../services/auth.service";
import VTdepnoAction from "../VT/VTdepnoAction.vue";
import userData from "../../js/userData";

let temp;
let selectDEP = "";

Vue.use(ClientTable);

export default {
  data() {
    const vm = this;
    return {
      editDep: {
        dep_name: "",
      },
      editDEPerror: {
        emp_name:""
      },
      editwindow: false,
      dep_name: "",
      username: "",
      data_Table: [],
      table_Columns: ["dep_no", "dep_name", "action"],
      table_Options: {
        headings: {
          dep_no: "部門編號",
          dep_name: "部門姓名",
          action: "操作",
        },
        templates: {
          action: VTdepnoAction,
        },
        uniqueKey: "dep_no",
        perPage: 9999999,
        perPageValues: [],
        pagination: false,
        showChildRowToggler: true,
        filterable: false,
        resizableColumns: false,
        destroyEventBus: true,
      },
    };
  },
  watch: {
  },
  async mounted() {
    let vm = this;
    //token驗證
    this.tokenCheck();
    //權限確認
    this.Auth();
    //讀取資料中
    this.$refs.attendanceTable.setLoadingState(true);
    //取得資料
    this.getDepno();
    //接刪除事件
    Event.$on("vue-tables.dlATTdata", function (data) {
      temp = vm.data_Table.find((x) => x.depno === data.depno);
      selectDEP = temp;
      vm.deleteDep(selectDEP);
    });
    //接收編輯事件
    Event.$on("vue-tables.checkDetails", function (data) {
      vm.editDEPdata(data);
      vm.editDEPtoggle();
    });
  },
  methods: {
    /** token驗證 */
    async tokenCheck() {
      let tc = await userService.tokenCheck();

      if (tc.Response != "Succeed") {
        alert("登入已逾期，請重新登入");
        localStorage.clear();
        await this.$router.push("/");
      }
    },
    /** 權限判別 */
    Auth() {
      this.username = userData().emp_name;
      if (userData().auth == "A") {
        this.Admin = true;
      }
    },
    /** 登出 */
    async logout() {
      await authService.logout();
      await this.$router.push("/");
      window.location.reload();
    },
    /** 登出刷新頁面 */
    reload() {
      window.location.reload();
    },
    async getDepno() {
      let tempDepdata = await userService.getDepdata();
      tempDepdata = tempDepdata["Response"]["data"];
      this.data_Table = tempDepdata;
    },
    /** 新增部門 */
    async submitAddDep() {
      let ck = await this.formCheck(this.dep_name);
      if (ck.ck == true) {
        await userService.addDepdata(this.dep_name);
        setTimeout(() => {
          let MSG = JSON.parse(localStorage.getItem("MSG"));
          if (MSG["code"] == 200) {
            if (MSG["msg"] != "Succeed") {
              alert(MSG["msg"]);
            } else {
              alert("成功新增");
              this.getDepno();
            }
          }
        }, 100);
      } else {
        alert(ck.msg);
      }
    },
    /** 刪除部門 */
    async deleteDep(depno) {
      if (confirm("確認是否刪除，" + depno.dep_name)) {
        let resData = await userService.deleteDep(depno.dep_no);
        if (
          resData.Response == "Update Succeed" ||
          resData.Response == "Delete Succeed"
        ) {
          alert("刪除成功!");
          this.getAttendancedata();
        } else {
          alert("刪除失敗!");
        }
      }
    },
    /** 時段編輯視窗開關 */
    async editTimeswitch() {
      this.timeEditwindow.timeEditwindowswitch =
        !this.timeEditwindow.timeEditwindowswitch;
    },
    /** 編輯員工視窗開關 */
    editDEPtoggle() {
      this.editwindow = !this.editwindow;
    },
    /** 編輯員工資料 */
    editDEPdata(depData) {
      this.editDep = depData;
    },
    /** 更新員工資料 */
    async updataDEPdata() {
      const ck = await this.formCheck(this.editDep);
      if (ck.ck) {
        await userService.updataDepdata(this.editEMP);
        setTimeout(() => {
          let MSG = JSON.parse(localStorage.getItem("MSG"));
          if (MSG["code"] == 200) {
            if (MSG["msg"] != "Succeed") {
              alert(MSG["msg"]);
            } else {
              this.table_Data = [];
              alert("成功修改");
              this.getEmpdata();
            }
          }
        }, 100);
      } else {
        alert(ck.msg);
      }

      this.editDEPtoggle();
    },

    /** 表單驗證 */
    async formCheck(data) {
      let check = { ck: true, msg: "" };
      if (data == null || data.trim().length == 0) {
        check.ck = false;
        check.msg = "請輸入部門名稱";

        return check;
      }

      return check;
    },
  },
  destroyed() {
    window.removeEventListener("keyup", this.handleMessage);
  },
};
</script>

<style scoped>
@import "../../assets/css/empManage.css";
</style>
