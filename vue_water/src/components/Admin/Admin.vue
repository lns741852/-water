<template>
  <div class="EmpManage">
    <div class="top">
      <div class="left">
        <div class="leftBar"></div>
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
      <h1>人員權限管理</h1>
      <div class="tableSearch">
        <input
          class="textSearch"
          type="text"
          ref="keyword"
          placeholder="以員編或姓名(中文)搜尋..."
          v-model="searchText"
        />
        <div class="selectSearch custom-margin">
          <select v-model="selectAuth">
            <option value="none">所屬權限</option>
            <option
              v-for="auth in authList"
              :key="auth.auth_no"
              :value="auth.auth_no"
            >
              {{ auth.auth_name }}
            </option>
          </select>
        </div>
        <button class="btnSearch" @click="search()">
          <span>Search</span>
        </button>
      </div>
      <div class="tableBorder">
        <div class="table">
          <div id="theadbg"></div>
          <v-client-table
            ref="empTable"
            id="empTable"
            v-model="table_Data"
            :columns="table_Columns"
            :options="table_Options"
          >
          </v-client-table>
          <div class="clear"></div>
        </div>
      </div>
    </div>
    <transition name="editWintran">
      <div class="editWindow" v-show="editwindow">
        <div class="editWindow_content" style="margin-top: 150px">
          <div class="closeParent">
            <button class="btn btnClose" @click="editAuthtoggle()">X</button>
          </div>
          <div>
            <form ref="editForm" @submit.prevent="updataAuthdata()">
              <h3>權限資料修改</h3>
              <div class="addForm_box">
                <div class="addForm_row">
                  <div class="addForm_lable">權限:</div>
                  <div class="addForm_input">
                    <select v-model="updateSelectAuth.auth">
                      <option
                        v-for="auth in authList"
                        :key="auth.auth_no"
                        :value="auth.auth_no"
                      >
                        {{ auth.auth_name }}
                      </option>
                    </select>
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
import VTempAction from "../VT/VTempAction.vue";
import userData from "../../js/userData";
import axios from "axios";

const ckEMPno = /^[a-zA-Z0-9]/;

Vue.use(ClientTable); //Client table

export default {
  components: {},
  computed: {},
  data() {
    let vm = this;
    return {
      authList: [],
      updateSelectAuth: {},
      selectAuth: "none",
      editwindow: false,
      searchText: "",
      username: "",
      table_Data: [],
      table_Columns: ["emp_no", "emp_name", "auth", "action"],
      table_Options: {
        headings: {
          emp_no: "員工編號",
          emp_name: "員工姓名",
          auth: "權限",
          action: "操作",
        },
        texts: {
          noResults: "無員工資料",
        },
        templates: {
          auth: function (h, row, index) {
            let authList = [];
            let el = [];

            authList.push(row);


            for (let i = 0; i < authList.length; i++) {
              const element = authList[i].auth_name;
              el.push(
                <i>
                  <span>{element}</span>
                </i>
              );
            }
            return <div class="VTempAuth">{el}</div>;
          },
          action: VTempAction,
        },
        
        orderBy: { column: "" },
        sortable: ["emp_no", "emp_name"],
        uniqueKey: "emp_no",
        perPage: 100,
        perPageValues: [],
        pagination: false,
        showChildRowToggler: false,
        filterByColumn: false,
        filterable: false,
        resizableColumns: false,
        destroyEventBus: true,
        customFilters: [
          {
            name: "customFilter",
            callback: function (row, query) {
              if (ckEMPno.test(query)) {
                return row.emp_no.toLowerCase().includes(query.toLowerCase());
              } else {
                return row.emp_name.toLowerCase().includes(query.toLowerCase());
              }
            },
          },
          {
            name: "authFilter",
            callback: function (row, query) {
              if (query == "none") {
                return row.auth !== query;
              }
              return row.auth == query;
            },
          },
        ],
      },
    };
  },
  created() {},
  watch: {
    searchText: function () {
      this.search();
    },
    selectAuth: function () {
      this.queryAuth();
    },
  },
  async mounted() {
    //權限驗證
    // if (userData().auth != "A") {
    //   alert("權限不足");
    //   this.$router.push("/Attendance");
    // }
    this.username = userData().emp_name;
    //token驗證
    this.tokenCheck();
    const vm = this;
    this.$refs.empTable.setLoadingState(true);
    //取得員工資料
    await this.getEmpdata();
    //取得權限
    await this.getAuthdata();
    //監控enter
    window.addEventListener("keyup", this.enter);
    //接收編輯事件
    Event.$on("vue-tables.checkDetails", function (data) {
      vm.editAuthdata(data);
      vm.editAuthtoggle();
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
    /** 登出 */
    async logout() {
      await authService.logout();
      await this.$router.push("/");
       window.location.reload();
    },
    /**搜尋*/
    search() {
      if (this.searchText != undefined) {
        Event.$emit("vue-tables.filter::customFilter", this.searchText);
      }
    },
    /** 群組篩選 */
    queryAuth() {
      // console.log("queryAuth ", this.selectAuth);
      Event.$emit("vue-tables.filter::authFilter", this.selectAuth);
    },
    /**enter事件*/
    enter(event) {
      if (event.keyCode === 13) {
        this.search();
      }
    },
    /** 編輯權限資料 */
    editAuthdata(authData) {
      this.updateSelectAuth = authData;
    },
    /** 權限視窗開關 */
    editAuthtoggle() {
      this.editwindow = !this.editwindow;
    },

    /** 取得權限資料 */
    async getAuthdata() {
      let tempDepdata = await userService.getAuthdata();
      tempDepdata = tempDepdata["Response"]["data"];

      this.authList = tempDepdata;
    },

    /** 取得員工資料 */
    async getEmpdata() {
      let tempData;
      this.table_Data = [];
      tempData = await userService.getEmpdata2();
      tempData = tempData["Response"]["data"];
      this.table_Data = tempData;

    },
    /** 更新權限資料 */
    async updataAuthdata() {
      await userService.updataAuthdata(this.updateSelectAuth);
      setTimeout(() => {
        let MSG = JSON.parse(localStorage.getItem("MSG"));
        if (MSG["code"] == 200) {
          if (MSG["msg"] != "Succeed") {
            alert(MSG["msg"]);
          } else {
            this.table_Data = [];
            alert("成功修改");
            window.location.reload();
          }
        }
      }, 100);
      this.editAuthtoggle();
    },
  },

  //離開此頁面執行的動作
  beforeDestroy() {
    window.removeEventListener("keyup", this.handleMessage);
    localStorage.removeItem("MSG");
  },
};
</script>

<style>
@import "../../assets/css/empManage.css";
.VuePagination{
  display: none;
} 
</style>
