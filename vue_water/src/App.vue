<template>
  <div id="app">
    <div class="main">
      <div class="menu">
        <table>
          <tbody>
            <tr>
              <td>
                <button id="menu" @click="menuSwitch">
                  <label
                    ><img src="././assets/img/menu.png" alt="Menu"
                  /></label>
                </button>
              </td>
            </tr>
            <tr>
              <td>
                <label for=""> 臺北自來水事業處管理平台 </label>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="functionList" v-show="functionList">
        <li
          :class="{ active: attendSetting.toggle }"
          v-show="authList.includes('A2')||authList.includes('A3')"
        >
          <span @click="attendActive" style="font-weight: bold">上下班管理</span>
          <div ref="EMP" :class="{ in: attendSetting.toggle }">
            <!-- <li @click="toAttendance" v-show="authList.includes('A2')">
              出勤狀況管理
            </li> -->
            <li @click="toAttendanceQuery" v-show="authList.includes('A3')">
              上下班狀況查詢
            </li>
          </div>
        </li>
        <!-- <li class="">薪資管理
            <div class="">
              <li>薪資查詢</li>
              <li class="">薪資專區</li>
            </div>
        </li> -->
        <!-- <li>出差管理
            <div class="">
              <li>出差申請</li>
              <li>出差查詢</li>
            </div>
        </li> -->
        <li
          :class="{ active: overtimeSetting.toggle }"
          v-show="authList.includes('B2')"
        >
          <span @click="overtimeActive" style="font-weight: bold">
            處外簽到退管理</span
          >
          <div ref="Overtime" :class="{ in: overtimeSetting.toggle }">
            <!-- <li>加班申請</li> -->
            <li @click="toOvertimeQuery" v-show="authList.includes('B2')">
              處外加班簽到退狀況查詢
            </li>
          </div>
        </li>

        <li
          :class="{ active: empSetting.toggle }"
          v-show="authList.includes('C2')||authList.includes('C3')||authList.includes('C4')||authList.includes('C5')||authList.includes('C6')||authList.includes('C7')"
        >
          <span @click="empActive" style="font-weight: bold">人事管理</span>
          <div ref="EMP" :class="{ in: empSetting.toggle }">
            <li @click="toSchedule" v-show="authList.includes('C2')">
              員工排班
            </li>
            <li @click="toEmpManage" v-show="authList.includes('C3')">
              人員管理
            </li>
            <li @click="toLocationManage" v-show="authList.includes('C6')">
              群組管理
            </li>
            <li @click="toWorkplaceManage" v-show="authList.includes('C4')">
              職位管理
            </li>
            <li @click="toGroupManage" v-show="authList.includes('C5')">
              組別管理
            </li>
            <li @click="toOwner" v-show="authList.includes('C7')">
              個人資料管理
            </li>
            <!-- <li @click="toDepnoManage" v-show="authList.includes('C5')">
              部門管理
            </li> -->
          </div>
        </li>

        <li
          :class="{ active: systemSetting.toggle }"
          v-show="authList.includes('D2')||authList.includes('D3')"
        >
          <span @click="systemActive" style="font-weight: bold"> 權限管理</span>
          <div ref="system" :class="{ in: systemSetting.toggle }">
            <!-- <li>加班申請</li> -->
            <li @click="toAdmin" v-show="authList.includes('D2')">
              人員權限管理
            </li>
            <li @click="toRole" v-show="authList.includes('D3')">
              權限選單管理
            </li>
            <!-- <li @click="toMenu">選單管理</li> -->
          </div>
        </li>

        <!-- <li>公告管理
            <div class="">
              <li>公告取消</li>
              <li>公告查詢</li>
              <li>公告申請</li>
            </div>
        </li> -->
        <!-- <li>請假管理
            <div class="">
              <li>請假申請</li>
              <li>請假查詢</li>
            </div>
        </li> -->
        <!-- <li>勞檢專區
            <div class="">
              <li>勞檢專區</li>
            </div>
        </li> -->
        <!-- <li>帳號登出</li> -->
      </div>
      <router-view />
      <div class="bottomText">
        <div style="">
          <p>
            公司名稱: 臺北自來水事業處<br />
            地址: 10672臺北市大安區長興街131號 |<br />
            電話:(02)8733-5678 | 傳真:(02)8733-5804
          </p>
        </div>
        <div>
          <p>© 2021 Greatest Idea Strategy Co.,Ltd All rights reserved.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import userService from "./services/user.services";

export default {
  name: "App",
  data() {
    return {
      path: this.$route.path,
      functionList: true,
      empSetting: {
        toggle: false,
      },
      attendSetting: {
        toggle: false,
      },
      overtimeSetting: {
        toggle: false,
      },
      systemSetting: {
        toggle: false,
      },
      auth: false,
      DialogVisible: false,
      authList: [],
    };
  },
  watch: {},
  mounted() {
    this.getMenuList();
  },
  methods: {
    //取MENU
    async getMenuList() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        let tempDepdata = await userService.getMenudata(ck.emp_no);
        tempDepdata = tempDepdata["Response"]["data"];
        this.authList = tempDepdata;
      }
    },

    /** 登入提示 */
    loginAlert() {
      alert("請先登入再使用功能");
      this.reload();
    },
    /** 刷新頁面 */
    reload() {
      this.isRouterAlive = false;
      this.$nextTick(() => {
        this.isRouterAlive = true;
      });
    },
    /** 選單開關 */
    menuSwitch() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          this.functionList = !this.functionList;
        }
      } else {
        this.loginAlert();
      }
    },
    /** 出勤管理開關 */
    attendActive() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        this.attendSetting.toggle = !this.attendSetting.toggle;
        this.overtimeSetting.toggle = false;
        this.systemSetting.toggle = false;
        this.empSetting.toggle = false;
      } else {
        this.loginAlert();
      }
    },
    /** 人事管理開關 */
    empActive() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        this.empSetting.toggle = !this.empSetting.toggle;
        this.overtimeSetting.toggle = false;
        this.systemSetting.toggle = false;
        this.attendSetting.toggle = false;
      } else {
        this.loginAlert();
      }
    },
    /** 加班管理開關 */
    overtimeActive() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        this.overtimeSetting.toggle = !this.overtimeSetting.toggle;
        this.empSetting.toggle = false;
        this.systemSetting.toggle = false;
        this.attendSetting.toggle = false;
      } else {
        this.loginAlert();
      }
    },
    /** 系統管理開關 */
    systemActive() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        this.systemSetting.toggle = !this.systemSetting.toggle;
        this.empSetting.toggle = false;
        this.overtimeSetting.toggle = false;
        this.attendSetting.toggle = false;
      } else {
        this.loginAlert();
      }
    },
    /** 移至出勤頁面 */
    toAttendance() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/Attendance") {
            this.$router.push("/Attendance");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },
    /** 移至出勤查詢頁面 */
    toAttendanceQuery() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/AttendanceQuery") {
            this.$router.push("/AttendanceQuery");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },
    /** 移至排班頁面 */
    toSchedule() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/userSchedule") {
            this.$router.push("/userSchedule");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },
    /** 移至人員管理頁面 */
    toEmpManage() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/EmpManage") {
            this.$router.push("/EmpManage");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },
    toLocationManage() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/Location") {
            this.$router.push("/Location");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },
    /** 移至加班查詢頁面 */
    toOvertimeQuery() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/OvertimeQuery") {
            this.$router.push("/OvertimeQuery");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },

    /** 移至部門頁面 */
    toDepnoManage() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/Depno") {
            this.$router.push("/Depno");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },

    /** 移至職位頁面 */
    toWorkplaceManage() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/Workplace") {
            this.$router.push("/Workplace");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },

    /** 移至組別頁面 */
    toGroupManage() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/Group") {
            this.$router.push("/Group");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },
    /** 移至組別頁面 */
    toMenu() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/Menu") {
            this.$router.push("/Menu");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },
    /** 移至組別頁面 */
    toAdmin() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/Admin") {
            this.$router.push("/Admin");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },
    /** 移至組別頁面 */
    toRole() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/Role") {
            this.$router.push("/Role");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },

        /** 移至組別頁面 */
    toOwner() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/Owner") {
            this.$router.push("/Owner");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },
  },
};
</script>

<style>
@import "assets/css/base.css";
</style>
