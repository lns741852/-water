<template>
  <div class="location">
    <div class="top">
      <div class="left"></div>
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
      <h1>群組管理</h1>

      <div class="locationheader">
        <el-input placeholder="請輸入地點名稱" v-model="seach_no">
          <el-button slot="append" icon="el-icon-search"></el-button>
        </el-input>
        <el-button type="primary" @click="showAddEmpView"> 新增地點名稱 </el-button>
      </div>
    </div>
    <div class="authManaTool"></div>

    <el-table
      height="500"
      :data="locationList"
      style="margin: auto; width: 95%"
    >
      <el-table-column width="150px" prop="no" label="地點名稱">
      </el-table-column>
      <el-table-column prop="txt" label="地址"> </el-table-column>
      <el-table-column
        width="150px"
        prop="location_range"
        label="打卡範圍(公尺)"
      >
      </el-table-column>

      <el-table-column width="150px" prop="note" label="備註">
        <template #default="scope">
          <el-popover
            placement="right-start"
            width="200"
            trigger="hover"
          >
            <span style="font-size: 18px; font-weight: bold">
              {{ scope.row.note }}</span
            >
            <div
              class="el-icon-chat-line-square"
              style="font-size: 24px"
              slot="reference"
            ></div>
          </el-popover>
        </template>
      </el-table-column>

      <el-table-column width="150px" prop="note" label="編制內容">
        <template #default="scope">
          <el-popover
            placement="right-start"
            width="300"
            trigger="hover"
          >
            <div  v-bind:style="empGroupStyleObject"
              v-loading="loading"
              element-loading-text="數據加載中..."
              element-loading-spinner="el-icon-loading"
              element-loading-background="rgba(0, 0, 0, 0.8)"
             >
              <el-tag
                style="margin: 0 5px 5px;font-size: 18px; font-weight:bold;"
                type="warning"
                v-for="item in groups"
                :key="item"
                >{{ item }}</el-tag
              >
              <el-tag
                style="margin: 0 5px 5px;font-size: 18px; font-weight:bold;"
                v-for="item2 in emps"
                :key="item2"
                >{{ item2 }}</el-tag
              >
            </div>

            <div
              v-on:mouseover="getEmpLocation(scope.row)"
              class="el-icon-s-custom"
              style="font-size: 24px"
              slot="reference"
            ></div>
          </el-popover>
        </template>
      </el-table-column>

      <el-table-column label="操作">
        <template #default="scope">
          <el-button class="button" @click="editLocation(scope.row)"
            >人員編制</el-button
          >
          <el-button class="button" @click="showEditLocationView(scope.row)"
            >修改</el-button
          >
          <el-button class="button" @click="deleteLocation(scope.row)"
            >刪除</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :title="title" :visible.sync="dialogVisible" width="50%">
      <div style="margin-bottom: 10px">
        <el-radio v-model="location.inputItem" label="0">地址</el-radio>
        <el-radio v-model="location.inputItem" label="1">GPS</el-radio>
      </div>
      <el-form
        :model="location"
        :rules="rules"
        ref="location"
        class="demo-ruleForm"
      >
        <el-form-item prop="no">
          <el-input v-model="location.no" placeholder="地點名稱"></el-input>
        </el-form-item>
        <el-row v-if="location.inputItem == '0'">
          <el-col :span="11">
            <el-form-item prop="county">
              <el-select v-model="location.county" placeholder="縣市">
                <el-option
                  v-for="item in counties"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item prop="city">
              <el-select v-model="location.city" placeholder="鄉鎮市區">
                <el-option
                  v-for="item in zipcodes"
                  v-show="item.county == location.county"
                  :key="item.id"
                  :label="item.city"
                  :value="item.city"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item prop="address" v-if="location.inputItem == '0'">
          <el-input v-model="location.address" placeholder="地址"></el-input>
        </el-form-item>
        <el-form-item prop="gps" v-if="location.inputItem == '1'">
          <el-input v-model="location.gps" placeholder="GPS地址"></el-input>
        </el-form-item>
        <el-form-item prop="min">
          <el-input
            v-model="location.min"
            placeholder="打卡範圍(公尺)"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-input v-model="location.note" placeholder="備註"></el-input>
        </el-form-item>
      </el-form>

      <el-button type="primary" @click="doAddLocation">確定</el-button>
    </el-dialog>
    <div style="height: 60px"></div>
  </div>
</template>
  
<script>
import userService from "../../services/user.services";
import authService from "../../services/auth.service";
import userData from "../../js/userData";
import twzipcode from "twzipcode-data";

export default {
  data() {
    return {
      empGroupStyleObject:{
        height: '40px',
        overflow: 'auto',
      },
      seach_no: "",
      dialogVisible: false,
      username: "",
      title: "",
      locationList: [],
      locationId: "",
      emps: [],
      groups: [],
      loading:true,
      location: {
        inputItem: "0",
        no: "",
        county: "",
        city: "",
        address: "",
        min: "",
        gps: "",
        note: "",
      },
      counties: [],
      zipcodes: [],

      rules: {
        no: [
          {
            required: true,
            message: "請輸入代號",
            trigger: "blur",
          },
        ],
        county: [
          {
            required: true,
            message: "請選擇縣市",
            trigger: "blur",
          },
        ],
        city: [
          {
            required: true,
            message: "請選擇鄉鎮區",
            trigger: "blur",
          },
        ],
        address: [
          {
            required: true,
            message: "請輸入地址",
            trigger: "blur",
          },
        ],
        gps: [
          {
            required: true,
            message: "請輸入GPS",
            trigger: "blur",
          },
        ],
        min: [
          {
            required: true,
            message: "請輸入範圍",
            trigger: "blur",
          },
          { pattern: /^\d*$/, message: "請輸入數字" },
        ],
      },
    };
  },
  mounted() {
    //token驗證
    this.tokenCheck();
    //地址選單
    this.initZipCode();
    this.Auth();
    //get位置
    this.initLocation();
  },
  methods: {
    initZipCode() {
      // 預設中文
      let data = twzipcode();
      // 所有縣市
      this.counties = data.counties;
      // 所有郵遞區號
      this.zipcodes = data.zipcodes;
    },

    async initLocation() {
      let tempData = await userService.getLocation();
      this.locationList = [];

      let temp = tempData["Response"]["data"];

      temp.forEach((element) => {
        if (element.id !== 0) {
          this.locationList.push(element);
        }
      });

      let l = this.locationList;
      let temp2 = [];
      for (let i of l) {
        if (i.no.indexOf(this.seach_no) >= 0) {
          temp2.push(i);
        }
      }
      this.locationList = temp2;
    },
    showAddEmpView() {
      this.title = "新增地址";
      this.location = {
        inputItem: "0",
        id: null,
        no: "",
        county: "",
        city: "",
        address: "",
        min: "",
        gps: "",
        note:""
      };
      this.dialogVisible = true;
      this.$refs["location"].resetFields();
    },

    showEditLocationView(data) {
      this.title = "修改地址";

      if (data.select === "0") {
        let county = data.txt.substring(0, 3);
        let city = data.txt.substring(3, data.txt.indexOf("區") + 1);
        let address = data.txt.substring(data.txt.indexOf("區") + 1);

        this.location = {
          inputItem: data.select,
          id: data.id,
          no: data.no,
          county: county,
          city: city,
          address: address,
          min: data.location_range,
          gps: "",
          note: data.note,
        };
      } else {
        this.location = {
          inputItem: data.select,
          id: data.id,
          no: data.no,
          county: "",
          city: "",
          address: "",
          min: data.location_range,
          gps: data.txt,
          note: data.note,
        };
      }

      this.dialogVisible = true;
      this.$refs["location"].resetFields();
    },

    //新增或修改地址
    doAddLocation() {
      if (this.location.id) {
        this.$refs["location"].validate(async (valid) => {
          if (!valid) return;
          let location;
          if (this.location.inputItem === "0") {
            location = this.locationHandle();
          } else {
            location = {
              id: this.location.id,
              location_range: this.location.min,
              no: this.location.no,
              txt: this.location.gps,
              select: this.location.inputItem,
              note: this.location.note,
            };
          }

          await userService.updataLocationata(location);
          setTimeout(() => {
            let MSG = JSON.parse(localStorage.getItem("MSG"));
            if (MSG["code"] == 200) {
              if (MSG["msg"] != "Succeed") {
                alert(MSG["msg"]);
              } else {
                alert("成功修改");
                this.initLocation();
                this.dialogVisible = false;
              }
            }
          }, 100);
        });
      } else {
        this.$refs["location"].validate(async (valid) => {
          if (!valid) return;

          let location;
          if (this.location.inputItem === "0") {
            location = this.locationHandle();
          } else {
            location = {
              id: null,
              location_range: this.location.min,
              no: this.location.no,
              txt: this.location.gps,
              select: this.location.inputItem,
              note: this.location.note,
            };
          }

          await userService.addLocationdata(location);
          setTimeout(() => {
            let MSG = JSON.parse(localStorage.getItem("MSG"));
            if (MSG["code"] == 200) {
              if (MSG["msg"] != "Succeed") {
                alert(MSG["msg"]);
              } else {
                alert("成功新增");
                this.initLocation();
                this.dialogVisible = false;
              }
            }
          }, 100);
        });
      }
    },

    async deleteLocation(data) {
      if (confirm("確認是否刪除，" + data.no)) {
        let resData = await userService.deleteLocation(data.id);
        if (resData.Response == "Succeed") {
          alert("刪除成功!");
          this.data_Table = [];
          this.initLocation();
        } else {
          alert("刪除失敗!");
        }
      }
    },

    locationHandle() {
      let addressFirst = this.location.county + this.location.city;

      let checkWord = this.location.city.substring(
        this.location.city.length - 1
      );

      let addressSecond = this.location.address.substring(
        this.location.address.indexOf(checkWord) + 1
      );

      let addLoaction = {
        id: this.location.id,
        no: this.location.no,
        txt: addressFirst + addressSecond,
        location_range: this.location.min,
        select: this.location.inputItem,
        note: this.location.note,
      };

      return addLoaction;
    },

    editLocation(data) {
      this.$router.push({ path: `/location/${data.id}` });
    },

    async getEmpLocation(locationData) {
      if (locationData.id != this.locationId) {
        this.loading=true
        this.locationId = locationData.id;
        this.emps = [];
        this.groups = [];
        let empLocationData = await userService.getEmpGroupdata(
          this.locationId
        );
        let tempData = empLocationData["Response"]["data"];

        this.empGroupStyleObject.height='40px'

        let height =parseInt(this.empGroupStyleObject.height.substring(0, this.empGroupStyleObject.height.length-2));
        for (let e of tempData) {  
          height =  height<300 ? height+10:height;    
          if (e.emp_name) {
            this.emps.push(e.emp_name);
          } else {
            this.groups.push(e.group_name);
          }
        }
        this.empGroupStyleObject.height = height+"px"
        this.loading=false
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
    /** 人員判別 */
    Auth() {
      this.username = userData().emp_name;
    },

    /** 登出 */
    async logout() {
      await authService.logout();
      await this.$router.push("/");
      window.location.reload();
    },
  },
  watch: {
    seach_no: async function () {
      await this.initLocation();
    },
  },
};
</script>
  
  <style>
@import "../../assets/css/location.css";

.location .el-table__header-wrapper :nth-child(n) {
  background: #9cd5e2;
  color: #ffff;
  font-weight: bold;
  font-size: 16px;
}

.location .el-table__row {
  background: #f0f8ff;
  font-weight: bold;
}

.location .el-table__row .button {
  font-weight: bold;
  font-size: 16px;
}

.location .locationheader .el-input {
  width: 450px;
}

.location .locationheader {
  display: flex;
  justify-content: space-between;
  margin: 0px 40px 20px 40px;
}
</style>