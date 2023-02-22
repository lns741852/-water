<template>
  <div class="login">
    <div class="top">
      <div class="left">
        <div class="leftBar"></div>
      </div>
      <div class="right">
        <div class="rightBar">
          <!-- <a href="/#/Download">表格下載</a>
          <a href="">最新消息</a> -->
          <a href=""> <img src="../../assets/img/Logo.png" alt="" /></a>
        </div>
      </div>
    </div>
    <div class="loginMain">
      <img src="../../assets/img/loginBG.png" class="loginImg" alt="" />
      <form class="loginForm" @submit.prevent="login()">
        <div>
          <label for="" class="loginFormtitle">臺北自來水事業處管理系統</label>
        </div>
        <div>
          <input
            type="text"
            placeholder="帳號"
            v-model="user.username"
            required
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="密碼"
            v-model="user.password"
            required
          />
        </div>
        <div>
          <div>
            <!-- <a href="/#/LoginV2" class="fp">員工入口</a>
            <span class="separate_marks">｜</span> -->

            <!-- <router-link to="/Forgetpw">忘記密碼?</router-link> -->
            <!-- <a href="/#/Forgetpw" class="fp">忘記密碼?</a> -->
          </div>
        </div>
        <div class="loginSubmit">
          <input type="submit" value="登入" />
        </div>
      </form>
    </div>
    <el-dialog
      title="帳號初次登入，請自訂新密碼"
      :visible="dialogVisible"
      width="50%"
      :show-close="false"
    >
      <el-form :model="password" :rules="rules" ref="passwd">
        <el-form-item prop="password">
          <el-input v-model="password.password" placeholder="新密碼"></el-input>
        </el-form-item>
        <el-form-item prop="repassword">
          <el-input
            v-model="password.repassword"
            placeholder="重複新密碼"
          ></el-input>
        </el-form-item>
      </el-form>

      <el-button type="primary" @click="submitRepassword">確定</el-button>
    </el-dialog>
    <div style="height:60px"></div>
  </div>
</template>

<script>
import authService from "../../services/auth.service";
import userServices from "../../services/user.services";

const ckEMPno = /^[a-zA-Z0-9]\w+$/;

export default {
  data() {
    var re = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("請重複輸入新密碼"));
      } else if (value !== this.password.password) {
        callback(new Error("密碼不一致"));
      } else {
        callback();
      }
    };
    return {
      user: {
        username: "",
        password: "",
      },

      password: {
        password: "",
        repassword: "",
      },

      dialogVisible: false,

      rules: {
        password: [
          {
            required: true,
            message: "請輸入新密碼",
            trigger: "blur",
            
          },
          { min: 8, max: 16, message: '密碼長度需8-16字', trigger: 'blur' }
        ],
        repassword: [{ validator: re, trigger: "blur" }],
      },
    };
  },
  async mounted() {
    // 驗證既有token是否有效
    await this.tokenCheck();
  },
  methods: {
    /** 移至出勤頁面 */
    toAttendance() {
      this.$router.push("/AttendanceQuery");
    },

    submitRepassword() {
      this.$refs["passwd"].validate(async (valid) => {
        if (!valid) return;
        this.password.emp_no = this.loginMSG.emp_no;

        let repwd = await authService.resetPW(this.password);
        if (repwd.status == "Succeed") {
          alert("密碼修改成功，請重新登入")
          localStorage.clear();
          window.location.reload();
        }
      });
    },

    /** token驗證 */
    async tokenCheck() {

      let tc = await userServices.tokenCheck();

      let user = JSON.parse(localStorage.getItem("user"));
      if (tc.Response === "Succeed") {
        if (user.auth == "A") {
          this.toAttendance();
        } else {
          this.$router.push("/AttendanceQuery");
          // alert("一般員工無法登入本系統，請洽管理部管理人員");
          // localStorage.clear();
        }
      }
    },
    /** 登入 */
    async login() {
      let first =0
      const ck = await this.formCheck(this.user);
      if (ck.ck) {
        let loginMSG = await authService.login(this.user);
        if (loginMSG) {
          this.loginMSG = loginMSG;

          if (loginMSG.token != undefined) {
            alert("登入成功");
            if ("QhrGVE"+this.user.username+"VDdYgdM" === this.user.password) {
              this.dialogVisible = true;
            } else {
              this.toAttendance();
              window.location.reload();
            }
          } else {
            alert(loginMSG);
          }
        }
      }
    },
    /** 表單驗證 */
    async formCheck(data) {
      let check = { ck: true, msg: "" };

      if (!ckEMPno.test(data.username)) {
        check.ck = false;
        check.msg = "員工編號錯誤";

        return check;
      }

      if (data.password == null || data.password.trim().length == 0) {
        check.ck = false;
        check.msg = "請輸入密碼";

        return check;
      }

      return check;
    },
  },
  beforeDestroy() {},
};
</script>

<style scoped>
@import "../../assets/css/login.css";
</style>
