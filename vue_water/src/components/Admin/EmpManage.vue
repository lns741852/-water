<template>
  <div class="EmpManage">
    <div class="top">
      <div class="left">
        <div class="leftBar">
          <button class="btnAdd" @click="addEMPtoggle()">新增員工</button>
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
      <h1>人員管理</h1>
      <div class="tableSearch">
        <input
          class="textSearch"
          type="text"
          ref="keyword"
          placeholder="以員編或姓名(中文)搜尋"
          v-model="searchText"
        />
        <div class="selectSearch custom-margin">
          <select v-model="workStuts">
            <option value=0>任職狀態篩選</option>
            <option value=1>在職</option>
            <option value=2>離職</option>
            <option value=3>未到職</option>
            <option value=4>留職停薪</option>
          </select>
        </div>
        <div class="selectSearch custom-margin">
          <select v-model="selectGroup">
            <option value="none">所屬組別</option>
            <option
              v-for="group in groupData"
              :key="group.group_no"
              :value="group.group_no"
            >
              {{ group.group_name }}
            </option>
          </select>
        </div>
        <button class="btnSearch" @click="search()">
          <span>Search</span>
        </button>
      </div>
      <div>
        <el-button
          @click="changeLocation('0')"
          style="margin: 5px 10px 10px 0; font-weight: bold"
        >
          關閉打卡範圍
        </el-button>
        <el-button
          @click="changeLocation('1')"
          style="margin: 5px 10px 10px 0; font-weight: bold"
        >
          開啟打卡範圍
        </el-button>
        <el-button
          @click="cancelLine()"
          style="margin: 5px 10px 10px 0; font-weight: bold"
        >
          解除Line綁定
        </el-button>
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
            <template slot="selected" slot-scope="props">
              <input
                v-model="props.row.selected"
                type="checkbox"
                @click="selectOne(props.row)"
              />
            </template>
          </v-client-table>
          <div class="clear"></div>
        </div>
      </div>
    </div>
    <transition name="editWintran">
      <div class="editWindow" v-show="editwindow">
        <div class="editWindow_content">
          <div class="closeParent">
            <button class="btn btnClose" @click="editEMPtoggle()">X</button>
          </div>
          <div>
            <form ref="editForm" @submit.prevent="updataEMPdata()">
              <h3>員工資料編輯</h3>
              <div class="addForm_box">
                <div class="addForm_row">
                  <div class="addForm_lable">員工編號:</div>
                  <div class="addForm_input">{{ editEMP.emp_no }}</div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">員工姓名:</div>
                  <div class="addForm_input">
                    <input type="text" v-model="editEMP.emp_name" required />
                    <div class="addForm_lable_error">
                      {{ editEMPerror.emp_name }}
                    </div>
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">密碼:</div>
                  <div class="addForm_input">
                    <input type="text" v-model="editEMP.user_pwd" />
                  </div>
                </div>
                <!-- <div class="addForm_row">
                  <div class="addForm_lable">所屬公司:</div>
                  <div class="addForm_input">
                    <select v-model="editEMP.comp_no" required>
                      <option value="none">請選擇</option>
                      <option
                        v-for="comp in compData"
                        :key="comp.comp_no"
                        :value="comp.comp_no"
                      >
                        {{ comp.comp_name }}
                      </option>
                    </select>
                    <div class="addForm_lable_error">
                      {{ editEMPerror.comp_no }}
                    </div>
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">所屬部門:</div>
                  <div class="addForm_input">
                    <select v-model="editEMP.dep_no">
                      <option value="none">請選擇</option>
                      <option
                        v-for="dep in depData"
                        :key="dep.dep_no"
                        :value="dep.dep_no"
                      >
                        {{ dep.dep_name }}
                      </option>
                    </select>
                    <div class="addForm_lable_error">
                      {{ editEMPerror.dep_no }}
                    </div>
                  </div>
                </div> -->
                <div class="addForm_row">
                  <div class="addForm_lable">職位:</div>
                  <div class="addForm_input">
                    <select v-model="editEMP.work_position">
                      <option value="none">請選擇</option>
                      <option
                        v-for="wp in wpData"
                        :key="wp.wp_code"
                        :value="wp.wp_code"
                      >
                        {{ wp.wp_name }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">連絡電話:</div>
                  <div class="addForm_input">
                    <input type="tel" v-model="editEMP.tel" />
                    <div class="addForm_lable_error">
                      {{ editEMPerror.tel }}
                    </div>
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">電子信箱:</div>
                  <div class="addForm_input">
                    <input type="email" v-model="editEMP.mail" />
                    <div class="addForm_lable_error">
                      {{ editEMPerror.mail }}
                    </div>
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">所屬組別:</div>
                  <div class="addForm_input">
                    <select v-model="editEMP.group_no">
                      <option value="none">請選擇</option>
                      <option
                        v-for="group in groupData"
                        :key="group.group_no"
                        :value="group.group_no"
                      >
                        {{ group.group_name }}
                      </option>
                    </select>
                  </div>
                </div>
                <!-- <div class="addForm_row">
                  <div class="addForm_lable">打卡地址:</div>
                  <div class="addForm_input">
                    <input style="width: 90%" v-model="editEMP.location" />
                  </div>
                </div> -->
                <div class="addForm_row">
                  <div class="addForm_lable">是否為組長:</div>
                  <div class="addForm_input">
                    <input
                      id="group_leader_edit"
                      class="checkbox_checkbox"
                      type="checkbox"
                      v-model="editEMP.group_leader"
                    />
                    <label for="group_leader_edit" class="checkbox_btn">
                    </label>
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">任職狀態:</div>
                  <div class="addForm_input">
                    <select v-model="editEMP.working">
                      <option
                        v-for="(working, index) in workingData"
                        :key="index"
                        :value="index"
                      >
                        {{ working }}
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
    <transition name="addWintran">
      <div class="addwindow" v-show="addwindow">
        <div class="addwindow_content">
          <div class="closeParent">
            <button class="btn btnClose" @click="addEMPtoggle()">X</button>
          </div>
          <div>
            <form ref="addForm" @submit.prevent="subAddemp">
              <h3>新增員工</h3>
              <div class="addForm_box">
                <div class="addForm_row">
                  <div class="addForm_lable">員工編號</div>
                  <div class="addForm_input">
                    <input type="text" v-model="addEMP.emp_no" required />
                    <div class="addForm_lable_error">
                      {{ addEMPerror.emp_no }}
                    </div>
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">員工姓名:</div>
                  <div class="addForm_input" >
                    <input type="text" v-model="addEMP.emp_name" required />
                    <div class="addForm_lable_error">
                      {{ addEMPerror.emp_name }}
                    </div>
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">員工密碼:</div>
                  <div class="addForm_input">
                    <input type="password" v-model="addEMP.user_pwd" required />
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">密碼確認:</div>
                  <div class="addForm_input">
                    <input
                      type="password"
                      v-model="addEMP.user_pwd_re"
                      required
                    />
                    <div class="addForm_lable_error">
                      {{ addEMPerror.user_pwd_re }}
                    </div>
                  </div>
                </div>
                <!-- <div class="addForm_row">
                  <div class="addForm_lable">所屬公司:</div>
                  <div class="addForm_input">
                    <select v-model="addEMP.comp_no" required>
                      <option value="none">請選擇</option>
                      <option
                        v-for="comp in compData"
                        :key="comp.comp_no"
                        :value="comp.comp_no"
                      >
                        {{ comp.comp_name }}
                      </option>
                    </select>
                    <div class="addForm_lable_error">
                      {{ addEMPerror.comp_no }}
                    </div>
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">所屬部門:</div>
                  <div class="addForm_input">
                    <select v-model="addEMP.dep_no" required>
                      <option value="none">請選擇</option>
                      <option
                        v-for="dep in depData"
                        :key="dep.dep_no"
                        :value="dep.dep_no"
                      >
                        {{ dep.dep_name }}
                      </option>
                    </select>
                    <div class="addForm_lable_error">
                      {{ addEMPerror.dep_no }}
                    </div>
                  </div>
                </div> -->
                <div class="addForm_row">
                  <div class="addForm_lable">所屬組別:</div>
                  <div class="addForm_input">
                    <select v-model="addEMP.group_no" required>
                      <option value="none">請選擇</option>
                      <option
                        v-for="group in groupData"
                        :key="group.group_no"
                        :value="group.group_no"
                      >
                        {{ group.group_name }}
                      </option>
                    </select>
                    <div class="addForm_lable_error">
                      {{ addEMPerror.group_no }}
                    </div>
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">是否為組長:</div>
                  <div class="addForm_input">
                    <input
                      id="group_leader"
                      class="checkbox_checkbox"
                      type="checkbox"
                      v-model="addEMP.group_leader"
                    />
                    <label for="group_leader" class="checkbox_btn"> </label>
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">職位:</div>
                  <div class="addForm_input">
                    <select v-model="addEMP.work_position" required>
                      <option value="none">請選擇</option>
                      <option
                        v-for="wp in wpData"
                        :key="wp.wp_code"
                        :value="wp.wp_code"
                      >
                        {{ wp.wp_name }}
                      </option>
                    </select>
                    <div class="addForm_lable_error">
                      {{ addEMPerror.work_position }}
                    </div>
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">連絡電話:</div>
                  <div class="addForm_input">
                    <input type="tel" v-model="addEMP.tel" />
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">電子信箱:</div>
                  <div class="addForm_input">
                    <input type="email" v-model="addEMP.mail" />
                  </div>
                </div>
                <!-- <div class="addForm_row">
                  <div class="addForm_lable">打卡地址:</div>
                  <div class="addForm_input">
                    <input style="width: 90%" v-model="addEMP.location" />
                  </div>
                </div> -->
                <!-- <div class="addForm_row">
                  <div class="addForm_lable">任職狀態:</div>
                  <div class="addForm_input">
                    <input
                      id="workingnow"
                      class="checkbox_checkbox"
                      type="checkbox"
                      v-model="addEMP.working"
                    />
                    <label for="workingnow" class="checkbox_btn"> </label>
                  </div>
                </div> -->
                <div class="addForm_row">
                  <div class="addForm_lable">任職狀態:</div>
                  <div class="addForm_input">
                    <select v-model="addEMP.working">
                      <option
                        v-for="(working, index) in workingData"
                        :key="index"
                        :value="index"
                      >
                        {{ working }}
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
    <div style="height: 60px"></div>
  </div>
</template>

<script>
import Vue from "vue";
import { ClientTable, Event } from "vue-tables-2";
import userService from "../../services/user.services";
import authService from "../../services/auth.service";
import VTempAction from "../VT/VTempAction.vue";
import userData from "../../js/userData";


const ckEMPno = /^[a-zA-Z0-9]/;

Vue.use(ClientTable); //Client table

export default {
  components: {},
  computed: {},
  data() {
    let vm = this;
    return {
      groupData: [],
      workingData: ["請選擇", "在職", "離職", "未到職", "留職停薪"],

      wpData: [],
      selectGroup: "none",
      editwindow: false,
      addwindow: false,
      searchText: "",
      workStuts: 0,
      Admin: false,
      username: "",
      table_Data: [],
      table_Data_Check: [],
      table_Columns: [
        "selected",
        "emp_no",
        "emp_name",
        //"dep_no",
        // "work_position",
        // "tel",
        "group_no",
        "base",
        // "auth",
        "working",
        "action",
      ],
      table_Options: {
        headings: {
          selected: function (h) {
            return h("input", {
              attrs: {
                type: "checkbox",
                id: "selectAllCheckbox",
              },
              on: {
                click: (e) => {
                  vm.selectAll(e.srcElement.checked);
                },
              },
              ref: "selectAllCheckbox",
            });
          },
          // selected:"",
          emp_no: "員工編號",
          emp_name: "員工姓名",
          //dep_no: "所屬部門",
          // work_position: "職位",
          tel: "連絡電話",
          group_no: "所屬組別",
          // auth: "權限",
          base: "員工基本資料",
          working: "任職狀態",
          action: "操作",
        },
        texts: {
          noResults: "無員工資料",
        },
        templates: {
          // work_position: function (h, row, index) {
          //   let wp = row.work_position;

          //   wp = vm.dataTransform(wp, "wp_code", vm.wpData);
          //   return wp["wp_name"];
          // },

          group_no: function (h, row, index) {
            let groupNo = row.group_no;

            groupNo = vm.dataTransform(groupNo, "group_no", vm.groupData);
            return groupNo["group_name"];
          },
          working: function (h, row, index) {

            let workStuts = row.working;

            if (workStuts == 1) {
              workStuts = "在職";
            } else if (workStuts == 2) {
              workStuts = "離職";
            } else if (workStuts == 3) {
              workStuts = "未到職";
            } else {
              workStuts = "留職停薪";
            }

            return <div>{workStuts}</div>;
          },
          base: function (h, row, index) {
            let wp = row.work_position;
            wp = vm.dataTransform(wp, "wp_code", vm.wpData);
            let base;
            if (row.locationCheck == 1) {
              if (row.line_id != "") {
                base = (
                  <div>
                    <div>連絡電話:{row.tel}</div>
                    {/* <div style="font-weight:bold;">打卡地址:{row.location}</div> */}
                    <div>個人職位:{wp["wp_name"]}</div>
                    <div>
                      打卡範圍:<el-tag>開</el-tag>
                    </div>
                    <div>
                      line綁定:<el-tag>開</el-tag>
                    </div>
                  </div>
                );
              } else {
                base = (
                  <div>
                    <div>連絡電話:{row.tel}</div>
                    {/* <div style="font-weight:bold;">打卡地址:{row.location}</div> */}
                    <div>個人職位:{wp["wp_name"]}</div>
                    <div>
                      打卡範圍:<el-tag>開</el-tag>
                    </div>
                    <div>
                      line綁定: <el-tag type="danger">關</el-tag>
                    </div>
                  </div>
                );
              }
            } else {
              if (row.line_id != "") {
                base = (
                  <div>
                    <div>連絡電話:{row.tel}</div>
                    <div>個人職位:{wp["wp_name"]}</div>
                    <div>
                      打卡範圍: <el-tag type="danger">關</el-tag>
                    </div>
                    <div>
                      line綁定:<el-tag>開</el-tag>
                    </div>
                  </div>
                );
              } else {
                base = (
                  <div>
                    <div>連絡電話:{row.tel}</div>
                    <div>個人職位:{wp["wp_name"]}</div>
                    <div>
                      打卡範圍: <el-tag type="danger">關</el-tag>
                    </div>
                    <div>
                      line綁定: <el-tag type="danger">關</el-tag>
                    </div>
                  </div>
                );
              }
            }

            return base;
          },
          // auth: function (h, row, index) {
          //   let authList = [];
          //   let el = [];

          //   if (row.auth == "A") {
          //     authList.push("管理員");
          //   }
          //   if (row.group_leader == true || row.group_leader == 1) {
          //     authList.push("組長");
          //   }
          //   authList.push("一般員工");

          //   for (let i = 0; i < authList.length; i++) {
          //     const element = authList[i];
          //     el.push(
          //       <i>
          //         <span>{element}</span>
          //       </i>
          //     );
          //   }

          //   return <div class="VTempAuth">{el}</div>;
          // },
          action: VTempAction,
        },
        orderBy: { column: "" },
        sortable: [
          "emp_no",
          "emp_name",
          "dep_no",
          "work_position",
          "group_no",
          "working",
        ],
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
            name: "workstutsFilter",
            callback: function (row, query) {
              // query = toString(query);
              if(query == 1){
                return row.working == query;
              }else if(query == 2){
                return row.working == query;
              }else if(query == 3){
                return row.working == query;
              }else if(query == 4){
                return row.working == query;
              }else{
                return true
              }
              
            },
          },
          {
            name: "groupFilter",
            callback: function (row, query) {
              if (query == "none") {
                return row.group_no !== query;
              }
              return row.group_no == query;
            },
          },
        ],
      },
      editEMP: {
        emp_no: "",
        emp_name: "",
        user_pwd: "",
        user_pwd_re: "",
        comp_no: "none",
        dep_no: "none",
        group_no: "none",
        group_leader: 0,
        work_position: "none",
        tel: "",
        auth: "",
        mail: "",
        location: "",
        working: 0,
        locationCheck: null,
      },
      editEMPerror: {
        emp_name: "",
        comp_no: "",
        dep_no: "",
        group_no: "",
        work_position: "",
        tel: "",
        mail: "",
      },
      addEMP: {
        emp_no: "",
        emp_name: "",
        user_pwd: "",
        user_pwd_re: "",
        comp_no: "none",
        dep_no: "none",
        group_no: "none",
        group_leader: false,
        work_position: "none",
        tel: "",
        mail: "",
        working: 0,
        auth: "",
        location: "",
        locationCheck: null,
      },
      addEMPerror: {
        emp_no: "",
        emp_name: "",
        user_pwd_re: "",
        comp_no: "",
        dep_no: "",
        group_no: "",
        work_position: "",
      },
    };
  },
  created() {},
  watch: {
    searchText: function () {
      this.search();
    },
    workStuts: function () {
      this.selectWorkStuts();
    },
    selectGroup: function () {
      this.queryGroup();
    },
    //新增員工自動驗證區塊
    "addEMP.emp_no": function (val) {
      this.addEMPerror.emp_no =
        ckEMPno.test(val) && val != ""
          ? ""
          : val == ""
          ? "請輸入員工編號"
          : "不符員工編號規則";
    },
    "addEMP.emp_name": function (val) {
      this.addEMPerror.emp_name =
        val == "" || val.trim().length == 0 ? "請輸入員工姓名" : "";
    },
    "addEMP.user_pwd": function (val) {
      this.addEMPerror.user_pwd_re =
        val != this.addEMP.user_pwd_re ? "與輸入密碼不符" : "";
    },
    "addEMP.user_pwd_re": function (val) {
      this.addEMPerror.user_pwd_re =
        val != this.addEMP.user_pwd ? "與輸入密碼不符" : "";
    },
    "addEMP.comp_no": function (val) {
      this.addEMPerror.comp_no = val == "none" ? "請選擇所屬公司" : "";
    },
    "addEMP.dep_no": function (val) {
      this.addEMPerror.dep_no = val == "none" ? "請選擇所屬部門" : "";
    },
    "addEMP.group_no": function (val) {
      this.addEMPerror.group_no = val == "none" ? "請選擇所屬組別" : "";
    },
    "addEMP.work_position": function (val) {
      this.addEMPerror.work_position = val == "none" ? "請選擇所屬職位" : "";
    },
    //編輯員工自動驗證區塊
    "editEMP.emp_name": function (val) {
      this.editEMPerror.emp_name =
        val == "" || val.trim().length == 0 ? "請輸入員工姓名" : "";
    },
    "editEMP.comp_no": function (val) {
      this.editEMPerror.comp_no = val == "none" ? "請選擇所屬公司" : "";
    },
    "editEMP.dep_no": function (val) {
      this.editEMPerror.dep_no = val == "none" ? "請選擇所屬部門" : "";
    },
    "editEMP.group_no": function (val) {
      this.editEMPerror.group_no = val == "none" ? "請選擇所屬組別" : "";
    },
    "editEMP.work_position": function (val) {
      this.editEMPerror.work_position = val == "none" ? "請選擇所屬職位" : "";
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
    // this.$refs.empTable.setLoadingState(true);
    //接收編輯事件
    Event.$on("vue-tables.checkDetails", function (data) {
      vm.editRMPdata(data);
      vm.editEMPtoggle();
    });
    //接收報表匯出事件
    Event.$on("vue-tables.reportDetails", function (data) {
      vm.exportRMPdata(data);
    });
    //取得設定資料
    await this.getSettingdata();
    //取得員工資料
    await this.getEmpdata();
    //監控enter
    window.addEventListener("keyup", this.enter);
  },

  methods: {
    //打卡開關
    async changeLocation(num) {
      this.table_Data_Check = [];
      this.table_Data.forEach((i) => {
        if (i.selected) {
          this.table_Data_Check.push(i.emp_no);
        }
      });

      if (this.table_Data_Check.length > 0) {
        await userService.updatalocationCheck(num, this.table_Data_Check);
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
        alert("修改資料尚未勾選!");
      }
    },

    //Line解綁
    async cancelLine() {
      this.table_Data_Check = [];
      this.table_Data.forEach((i) => {
        if (i.selected) {
          this.table_Data_Check.push(i.emp_no);
        }
      });

      if (this.table_Data_Check.length > 0) {
        await userService.lineCancel(this.table_Data_Check);
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
        alert("修改資料尚未勾選!");
      }
    },

    selectOne(row) {
      for (let i = 0; i <= this.table_Data.length; i++) {
        if (this.table_Data[i].emp_no == row.emp_no) {
          this.table_Data[i].selected = !this.table_Data[i].selected;
          break;
        }
      }
      // let index;
      // if (!row.selected) {
      //   this.table_Data_Check.push(row.emp_no);
      // } else {
      //   index = this.table_Data_Check.indexOf(row.emp_no);
      //   this.table_Data_Check.splice(index,1);
      // }
    },

    selectAll(checked) {
      for (let i = 0; i < this.table_Data.length; i++) {
        if (checked) {
          this.table_Data[i].selected = true;
          //this.table_Data_Check.push(this.table_Data[i].emp_no);
        } else {
          this.table_Data[i].selected = false;
          //this.table_Data_Check=[]
        }
      }
    },
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
    /** 任職狀態篩選 */
    selectWorkStuts() {
      Event.$emit("vue-tables.filter::workstutsFilter", this.workStuts);
    },
    /** 群組篩選 */
    queryGroup() {
      // console.log("queryGroup ", this.selectGroup);
      Event.$emit("vue-tables.filter::groupFilter", this.selectGroup);
    },
    /**enter事件*/
    enter(event) {
      if (event.keyCode === 13) {
        this.search();
      }
    },
    /** 新增員工視窗開關 */
    addEMPtoggle() {
      (this.addEMP = {
        emp_no: "",
        emp_name: "",
        user_pwd: "",
        user_pwd_re: "",
        comp_no: "none",
        dep_no: "none",
        group_no: "none",
        group_leader: false,
        work_position: "none",
        tel: "",
        mail: "",
        working: 0,
        auth: "",
        location: "",
        locationCheck: null,
      }),
        (this.addEMPerror = {
          emp_no: "",
          emp_name: "",
          user_pwd_re: "",
          comp_no: "",
          dep_no: "",
          group_no: "",
          work_position: "",
        }),
        (this.addwindow = !this.addwindow);
    },
    /** 編輯員工視窗開關 */
    editEMPtoggle() {
      this.editwindow = !this.editwindow;
    },
    /** 取得設定資料 */
    async getSettingdata() {

      let tempGroupdata = await userService.getGroupdata();
      tempGroupdata = tempGroupdata["Response"]["data"];
      this.groupData = tempGroupdata;

      let tempWpdata = await userService.getWPdata();

      tempWpdata = tempWpdata["Response"]["data"];
      this.wpData = tempWpdata;

    },
    /** 取得員工資料 */
    async getEmpdata() {
      let tempData;
      this.table_Data = [];
      tempData = await userService.getEmpdata();

      tempData = tempData["Response"]["data"];

      //選擇框
      tempData.forEach((x) => {
        x.selected = false;
      });
      this.table_Data = tempData;
    },
    /** 新增員工 */
    async subAddemp() {
      let ck = await this.formCheck(this.addEMP);

      if (ck.ck == true) {
        if (this.addEMP.user_pwd == this.addEMP.user_pwd_re) {
          //this.addEMP.auth = this.addEMP.group_no == "0" ? "A" : "";
          this.addEMP.group_leader = this.addEMP.group_leader == true ? 1 : 0;
          this.addEMP.locationCheck = this.addEMP.location == "" ? 0 : 1;
          await userService.addEmpdata(this.addEMP);
          setTimeout(() => {
            let MSG = JSON.parse(localStorage.getItem("MSG"));
            if (MSG["code"] == 200) {
              if (MSG["msg"] != "Succeed") {
                alert(MSG["msg"]);
              } else {
                alert("成功新增");
                this.getEmpdata();
                this.addEMPtoggle();
              }
            }
          }, 100);
        } else {
          alert("密碼確認輸入的密碼與員工密碼不符，請確認");
        }
      } else {
        //錯誤訊息
        alert(ck.msg);
        if (ck.msg == "員工姓名未輸入，請輸入姓名") {
          this.addEMP.emp_name = "";
        }
      }
    },
    /** 編輯員工資料 */
    editRMPdata(empData) {
      empData.user_pwd = "";
      this.editEMP = empData;
    },
    /** 匯出員工月報表 */
    async exportRMPdata(empData) {
      await userService.exportRMPdata("?emp_no=" + empData.emp_no);
    },

    /** 更新員工資料 */
    async updataEMPdata() {
      const ck = await this.formCheck(this.editEMP);
      if (ck.ck) {
        this.editEMP.group_leader = this.editEMP.group_leader == true ? 1 : 0;
        this.editEMP.locationCheck = this.editEMP.location == "" ? 0 : 1;
        await userService.updataEmpdata(this.editEMP);
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
        if (ck.msg == "員工姓名未輸入，請輸入姓名") {
          this.addEMP.emp_name = "";
        }
      }

      this.editEMPtoggle();
    },
    /** 資料轉換 */
    dataTransform(item, attr, listData) {
      let getData = item;
      listData.forEach((data) => {
        if (item == data[attr]) {
          getData = data;
        }
      });
      return getData;
    },
    /** 表單驗證 */
    async formCheck(data) {
      let check = { ck: true, msg: "" };

      if (!ckEMPno.test(data.emp_no)) {
        check.ck = false;
        check.msg = "員工編號錯誤，請輸入符合規則的編號";

        return check;
      }

      if (data.emp_name == null || data.emp_name.trim().length == 0) {
        check.ck = false;
        check.msg = "員工姓名未輸入，請輸入姓名";

        return check;
      }

      // if (data.comp_no == "none") {
      //   check.ck = false;
      //   check.msg = "員工所屬公司未選擇，請選擇一個部門";

      //   return check;
      // }

      // if (data.dep_no == "none") {
      //   check.ck = false;
      //   check.msg = "員工所屬部門未選擇，請選擇一個部門";

      //   return check;
      // }

      if (data.group_no == "none") {
        check.ck = false;
        check.msg = "員工所屬組別未選擇，請選擇一個組別";

        return check;
      }

      if (data.work_position == "none") {
        check.ck = false;
        check.msg = "員工職位未選擇，請選擇一個職位";

        return check;
      }

      if (data.working == 0) {
        check.ck = false;
        check.msg = "請選擇任職狀態";

        return check;
      }

      return check;
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
