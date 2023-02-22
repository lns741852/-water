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

    <!--添加-->
    <div>
      <h1>權限選單管理</h1>
      <div class="tableSearch" style="margin-left: 5%">
        <input
          class="textSearch"
          size="small"
          placeholder="請輸入權限代號..."
          v-model="auth.auth_no"
        />
        <input
          class="textSearch"
          size="small"
          v-model="auth.auth_name"
          placeholder="請輸入權限名稱..."
        />
        <button
          class="btnAdd"
          style="background-color: #ffffff; margin: 3px 10px"
          @click="doAddRole"
        >
          新增權限
        </button>
      </div>
    </div>
    <div class="authManaTool">
      <div style="background: #8bd6e3; height: 50px; margin-top: 10px">
        <span class="table-font">權限管理</span>
      </div>

      <div class="collapseTable">
        <el-collapse
          style="margin-bottom: 50px"
          v-model="activeName"
          accordion
          @change="change(activeName)"
        >
          <el-collapse-item
            style="
              margin: 20px 10px;
              box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
            "
            :title="a.auth_name"
            :name="a.auth_no"
            v-for="(a, index) in authList"
            :key="index"
          >
            <el-card class="box-card">
              <div slot="header">
                <span>目錄</span>
                <el-button
                  v-if="a.auth_no !=='A'"  
                  style="float: right; padding: 3px 0; color: #ff0000"
                  icon="el-icon-delete"
                  type="text"
                  @click="doDeleteRole(a)"
                >
                  刪除
                </el-button>
              </div>
              <el-tree
                :data="menuList"
                show-checkbox
                ref="tree"
                node-key="menu_no"
                default-expand-all
                :default-checked-keys="selectedMenus"
              >
                <span class="custom-tree-node" slot-scope="{ data }">
                  <span>{{ data.menu_name }}</span>
                </span>
              </el-tree>
              <div style="display: flex; justify-content: flex-end">
                <el-button @click="cancelUpdate"  v-if="a.auth_no !=='A'"  >取消修改</el-button>
                <el-button type="primary" @click="doUpdate(a.auth_no, index)"
                v-if="a.auth_no !=='A'"  >確認修改
                </el-button>
              </div>
            </el-card>
          </el-collapse-item>
        </el-collapse>
      </div>
    </div>
    <div style="height:60px"></div>
  </div>
</template>




<script>
import axios from "axios";
import userService from "../../services/user.services";
import authService from "../../services/auth.service";
import userData from "../../js/userData";

export default {
  data() {
    return {
      username: "",
      activeName: "2",
      menuList: [],
      authList: [],
      selectedMenus: [],
      auth: {
        auth_no: "",
        auth_name: "",
      },
    };
  },
  mounted() {
    //token驗證
    this.tokenCheck();
    //權限確認
    this.Auth();
    this.initMenuList();
    this.initAuthList();
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
    async initMenuList() {
      let tempDepdata = await userService.getMenuList();
      tempDepdata = tempDepdata["Response"]["data"];
      this.menuList = tempDepdata;

      // const { data: res } = await axios.get("/api/menu");
      // this.menuList = res.data;
    },
    async initAuthList() {
      let tempDepdata = await userService.getAuthdata();
      tempDepdata = tempDepdata["Response"]["data"];
      this.authList = tempDepdata;

    },
    //查詢擁有權限
    async initSelectedMenus(auth_name) {
      let tempDepdata = await userService.getAuthMenudata(auth_name);
      tempDepdata = tempDepdata["Response"]["data"];
      this.selectedMenus = tempDepdata;
      // const { data: res } = await axios.get("/api/auth/menu/A");
      // this.selectedMenus = res.data;
    },

    //摺疊面板切換事件
    async change(activeName) {
        await this.initSelectedMenus(activeName);
        await this.initMenuList();
    },

    //關閉摺疊面板
    cancelUpdate() {
      this.activeName = -1;
    },
    //更新角色
    async doUpdate(auth_no, index) {
      //獲取展開角色
      let tree = this.$refs.tree[index];
      //獲取選中結點，加上true半勾選選項不會被選中
      let selectedKeys = tree.getCheckedKeys();
      // let selecteHalfdKeys = tree.getHalfCheckedKeys();
 
      // selecteHalfdKeys.forEach((key) => {
      //     selectedKeys.push(key)
      // });

      let putData ={
        auth_no: auth_no,
        menuList: selectedKeys
      }

      await userService.updataAuthMenudata(putData);
        setTimeout(() => {
          let MSG = JSON.parse(localStorage.getItem("MSG"));
          if (MSG["code"] == 200) {
            if (MSG["msg"] != "Succeed") {
              alert(MSG["msg"]);
             
            } else {
              alert("成功修改");
              window.location.reload();
            }
          }
        }, 100);
        
    },
    //刪除
    async doDeleteRole(auth) {
      if (confirm("確認是否刪除，" + auth.auth_name)) {
        let resData = await userService.deleteAuth(auth.auth_no);

        if (resData.Response == "Succeed") {
          alert("刪除成功!");
          this.initAuthList();
        } else {
          alert("刪除失敗!");
        }
      }
    },
    //新增
    async doAddRole() {
      let ck = this.formCheck(this.auth.auth_no);
      ck = this.formCheck(this.auth.auth_name);
      if (ck.ck == true) {
        await userService.addAuthdata(this.auth);
        setTimeout(() => {
          let MSG = JSON.parse(localStorage.getItem("MSG"));
          if (MSG["code"] == 200) {
            if (MSG["msg"] != "Succeed") {
              alert(MSG["msg"]);
            } else {
              alert("成功新增");
              this.auth = {
                auth_no: "",
                auth_name: "",
              };
            }
            this.initAuthList();
          }
        }, 100);
      } else {
        alert(ck.msg);
      }
    },

    /** 表單驗證 */
    formCheck(data) {
      let check = { ck: true, msg: "" };
      if (data == null || data.trim().length == 0) {
        check.ck = false;
        check.msg = "請輸入權限名稱";

        return check;
      }

      return check;
    },
  },
};
</script>

<style>
@import "../../assets/css/empManage.css";
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}

.collapseTable {
  background: #f0f8ff;
}

.authManaTool {
  margin: 0 auto;
  width: 90%;
}

.table-font {
  color: #ffffff;
  font-size: 30px;
  display: flex;
  justify-content: center;
}

.el-card {
  margin: 20px;
}

.el-collapse-item__content {
  background: #f0f8ff;
}

.el-collapse-item__header {
  font-size: 18px;
  padding-left: 10px;
  font-weight: bold;
}
.el-collapse-item__content {
  font-size: 18px;
}

.custom-tree-node {
  font-size: 16px;
}
</style>