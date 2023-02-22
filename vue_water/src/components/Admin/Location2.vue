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
    <div class="locationHeader">
      <el-row>
        <el-col :span="12" style="margin: 30px 30px">
          <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/location' }"
              >群組管理</el-breadcrumb-item
            >
            <el-breadcrumb-item>人員編制</el-breadcrumb-item>
          </el-breadcrumb>
        </el-col>
        <el-col :span="10">
          <h1>人員編制</h1>
        </el-col>
      </el-row>
    </div>

    <el-card class="locationContext">
      <div>
        <el-radio v-model="radio" label="1">單位</el-radio>
        <el-radio v-model="radio" label="2">人員</el-radio>
      </div>
      <el-divider></el-divider>
      <div v-if="radio === '1'">
        單位:
        <el-input
          class="empLocationInput"
          v-model="query2.name"
          prefix-icon="el-icon-search"
          placeholder="請輸入單位名稱"
        ></el-input>

        <el-divider></el-divider>

        <div class="locationchcheckboxreel">
          <el-checkbox
            class="locationcheckboxAll"
            :indeterminate="isIndeterminate"
            v-model="checkAll"
            @change="handleCheckAllChange"
            >全選</el-checkbox
          >
          <el-checkbox-group
            v-model="checkedGroup"
            @change="handleCheckedCitiesChange"
          >
            <el-checkbox
              class="locationCheckbox"
              v-for="item in groupList"
              :label="item.group_no"
              :key="item.group_no"
              >{{ item.group_name }}</el-checkbox
            >
          </el-checkbox-group>
        </div>
        <!-- <el-button type="primary" style="margin-top: 20px" @click="insertGroup"
            >匯入</el-button
          > -->
      </div>
      <div v-else>
        單位:
        <el-select
          filterable
          @change="queryEmp"
          v-model="query.group"
          clearable
          placeholder="請選擇"
        >
          <el-option
            v-for="item in groupList"
            :key="item.group_no"
            :label="item.group_name"
            :value="item.group_no"
          >
          </el-option>
        </el-select>
        <!-- 職位: 
        <el-select v-model="query.wp" placeholder="請選擇">
            <el-option
            v-for="item in wpList"
            :key="item.wp_code"
            :label="item.wp_name"
            :value="item.wp_code">
            </el-option>
        </el-select> -->
        <el-input
          class="empLocationInput"
          v-model="query.name"
          prefix-icon="el-icon-search"
          placeholder="請輸入人員名稱"
        ></el-input>
        <el-divider></el-divider>

        <div class="locationchcheckboxreel">
          <el-checkbox
            class="locationcheckboxAll"
            :indeterminate="empisIndeterminate"
            v-model="empcheckAll"
            @change="handleCheckAllChange"
            >全選</el-checkbox
          >

          <el-checkbox-group
            v-model="checkEmp"
            @change="handleCheckedCitiesChange"
          >
            <el-checkbox
              class="locationCheckbox"
              v-for="emp in empList"
              :label="emp.emp_no"
              :key="emp.emp_no"
              >{{ emp.emp_name }}</el-checkbox
            >
          </el-checkbox-group>
        </div>

        <!-- <el-button style="margin-top: 20px" type="primary" @click="insertEmp"
          >匯入</el-button
        > -->
      </div>

      <div class="saveBlock">
        <div v-for="item in FullItemList" :key="item.no">
          <el-tag
            v-if="item.no.includes('G_')"
            class="el-icon-circle-close tagStyle"
            type="primary"
            @click="deleteTag(item.no)"
          >
            {{ item.name }}</el-tag
          >
          <el-tag
            v-else
            class="el-icon-circle-close tagStyle"
            type="warning"
            @click="deleteTag(item.no)"
          >
            {{ item.name }}</el-tag
          >
        </div>
      </div>

      <div class="locationSaveButton">
        <el-button icon="el-icon-check" @click="saveLocation" type="primary"
          >確認選取</el-button
        >
        <!-- <el-button icon="el-icon-delete" @click="clearAll">全部清除</el-button> -->
      </div>
    </el-card>
    <div style="height: 100px"></div>
  </div>
</template>
    

<script>
import userService from "../../services/user.services";
import userData from "../../js/userData";
export default {
  data() {
    return {
      id: this.$route.params.id,
      radio: "1",
      query: {
        group: "",
        name: "",
      },
      query2: {
        name: "",
      },
      username: "",
      groupList: [],
      groupNoList: [],
      checkedGroup: [],
      groupForQuery: [],
      empList: [],
      empNoList: [],
      empListForQuery: [],
      checkEmp: [],
      FullItemList: [],
      FullItemListTemp: [],

      checkAll: false,
      isIndeterminate: false,
      empcheckAll: false,
      empisIndeterminate: false,
    };
  },
  mounted() {
    //取得資料
    this.getSettingdata();
    this.Auth();
  },
  methods: {
    /** 人員判別 */
    Auth() {
      this.username = userData().emp_name;
    },
    //全選
    handleCheckAllChange(val) {
      if (this.radio === "1") {
        let temp = this.groupList.map((x) => x.group_no);
        this.checkedGroup = val ? temp : [];
        this.isIndeterminate = false;
        this.insertGroup();
      } else {
        let temp = this.empList.map((x) => x.emp_no);
        this.checkEmp = val ? temp : [];
        this.empisIndeterminate = false;
        this.insertEmp();
      }
    },
    //半選取
    handleCheckedCitiesChange(value) {
      if (this.radio === "1") {
        let checkedCount = value.length;
        this.checkAll = checkedCount === this.groupNoList.length;
        this.isIndeterminate =
          checkedCount > 0 && checkedCount < this.groupNoList.length;
        this.insertGroup();
      } else {
        let checkedCount = value.length;
        this.empcheckAll = checkedCount === this.empNoList.length;
        this.empisIndeterminate =
          checkedCount > 0 && checkedCount < this.empNoList.length;
        this.insertEmp();
      }
    },

    async getSettingdata() {
      let tempGroupdata = await userService.getGroupdata();
      tempGroupdata = tempGroupdata["Response"]["data"];
      this.groupList = tempGroupdata;
      this.groupForQuery = tempGroupdata;
      this.groupList.forEach((i) => {
        this.groupNoList.push(i.group_no);
      });

      let tempData = await userService.getEmpdata();
      tempData = tempData["Response"]["data"];
      this.empList = tempData;
      this.empListForQuery = tempData;
      this.empList.forEach((i) => {
        this.empNoList.push(i.emp_no);
      });

      let empLocationData = await userService.getEmplocationdata(this.id);
      tempData = empLocationData["Response"]["data"];

      if (tempData.length > 0) {
        tempData.forEach((i) => {
          if (i.emp_no == null) {
            this.groupList.forEach((j) => {
              if (j.group_no.toString() === i.group_no) {
                this.FullItemListTemp.push({
                  no: "G_" + i.group_no,
                  name: j.group_name,
                });
              }
            });
            this.checkedGroup.push(i.group_no);
            this.isIndeterminate =
              this.checkedGroup.length > 0 &&
              this.checkedGroup.length < this.groupNoList.length;
            this.checkAll =
              this.checkedGroup.length === this.groupNoList.length;
          } else {
            this.empList.forEach((j) => {
              if (j.emp_no === i.emp_no) {
                this.FullItemListTemp.push({
                  no: "E_" + i.emp_no,
                  name: j.emp_name,
                });
              }
            });
            this.checkEmp.push(i.emp_no);
            this.empisIndeterminate =
              this.checkEmp.length > 0 &&
              this.checkEmp.length < this.empNoList.length;
            this.empcheckAll = this.checkEmp.length === this.empNoList.length;
          }
        });
        this.FullItemList = this.FullItemListTemp;
      }

      //   let tempWPdata = await userService.getWPdata();
      //   tempWPdata = tempWPdata["Response"]["data"];
      //   this.wpList  = tempWPdata;
    },

    //加入選中區域
    insertGroup() {
      let temp = [];

      //所以篩選checkbox
      this.groupList.forEach((i) => {
        //勾選checkbox
        if (this.checkedGroup.includes(i.group_no)) {
          let flag = 0;
          //添加區域
          this.FullItemList.forEach((c) => {
            if (c.no === "G_" + i.group_no) {
              flag = 1;
            }
          });
          if (flag === 0) {
            this.FullItemList.push({
              no: "G_" + i.group_no,
              name: i.group_name,
            });
          }
        } else {
          temp.push("G_" + i.group_no);
        }
      });

      for (let f of this.FullItemList) {
        for (let t of temp) {
          if (f.no === t) {
            this.deleteTag(t);
            break;
          }
        }
      }
    },

    //加入選中區域
    insertEmp() {
      let temp = [];

      this.empList.forEach((i) => {
        if (this.checkEmp.includes(i.emp_no)) {
          let flag = 0;
          this.FullItemList.forEach((c) => {
            if (c.no === "E_" + i.emp_no) {
              flag = 1;
            }
          });
          if (flag === 0) {
            this.FullItemList.push({
              no: "E_" + i.emp_no,
              name: i.emp_name,
            });
          }
        } else {
          temp.push("E_" + i.emp_no);
        }
      });

      for (let f of this.FullItemList) {
        for (let t of temp) {
          if (f.no === t) {
            this.deleteTag(t);
            break;
          }
        }
      }
    },

    clearAll() {
      this.FullItemList = [];
    },

    queryEmp() {
      let tempList = [];
      if (this.query.group != "") {
        this.empListForQuery.forEach((i) => {
          if (this.query.group.toString() === i.group_no) {
            tempList.push(i);
          }
          this.empList = tempList;
        });
      } else {
        this.empList = this.empListForQuery;
      }

      if (this.query.name != "") {
        tempList = [];
        this.empList.forEach((i) => {
          if (i.emp_name.includes(this.query.name)) {
            tempList.push(i);
          }
        });

        this.empList = tempList;
      }

      let i = 0;

      for (let e of this.empList) {
        if (this.checkEmp.includes(e.emp_no)) {
          i++;
        }
      }

      this.empcheckAll = i === this.empList.length;
      this.empisIndeterminate = i > 0 && i < this.empList.length;
    },

    queryGroup() {
      this.groupList = this.groupForQuery;
      let tempList = [];
      this.groupList.forEach((i) => {
        if (i.group_name.includes(this.query2.name)) {
          tempList.push(i);
        }
      });
      this.groupList = tempList;

      let i = 0;

      for (let g of this.groupList) {
        if (this.checkedGroup.includes(g.group_no)) {
          i++;
        }
      }

      this.checkAll = i === this.groupList.length;
      this.isIndeterminate = i > 0 && i < this.groupList.length;
    },

    deleteTag(data) {
      let x = 0;

      if (data.substring(0, 1) === "G") {
        this.checkedGroup = this.checkedGroup.filter(function (value) {
          return value != data.substring(2);
        });
      } else {
        this.checkEmp = this.checkEmp.filter(function (value) {
          return value != data.substring(2);
        });
      }

      x = 0;

      //找刪除資料index
      for (let i in this.FullItemList) {
        x++;
        if (this.FullItemList[i].no === data) {
          break;
        }
      }

      this.FullItemList = this.FullItemList.slice(0, x - 1).concat(
        this.FullItemList.slice(x, this.FullItemList.length + 1)
      );
    },

    saveLocation() {
      this.FullItemListTemp = [];
      if (this.FullItemList.length === 0) {
        this.$confirm("請確認是否清除所有人員資料 !", "警告!", {
          confirmButtonText: "確認",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
            this.saveEmplocation();
          })
          .catch(() => {});
      } else {
        this.saveEmplocation();
      }
    },

    async saveEmplocation() {
      for (let i of this.FullItemList) {
        if (i.no.includes("E_")) {
          this.FullItemListTemp.push({
            emp_no: i.no.substring(2, i.no.length),
            group_no: null,
          });
        } else {
          this.FullItemListTemp.push({
            emp_no: null,
            group_no: i.no.substring(2, i.no.length),
          });
        }
      }

      userService.updataEmpLocationdata(this.id, this.FullItemListTemp);
      setTimeout(() => {
        let MSG = JSON.parse(localStorage.getItem("MSG"));
        if (MSG["code"] == 200) {
          if (MSG["msg"] != "Succeed") {
            alert(MSG["msg"]);
          } else {
            alert("成功修改");
            this.$router.push({ path: `/location` });
          }
        }
      }, 100);
    },
  },
  watch: {
    "query.name": function () {
      this.queryEmp();
    },
    "query2.name": function () {
      this.queryGroup();
    },
  },
};
</script>
<style>
@import "../../assets/css/location.css";

.locationHeader {
  margin-bottom: 10px;
}

.locationContext {
  width: 90%;
  margin: auto;
}

.empLocationInput {
  width: 350px;
  margin: 10px 0 0px 20px;
}

.saveBlock {
  display: flex;
  justify-content: left;
  align-content: flex-start;
  flex-wrap: wrap;
  margin: auto;
  margin-top: 20px;
  margin-bottom: 10px;
  min-height: 150px;
  border: solid 2px rgba(18, 17, 17, 0.2);
  background: #ffffff;
  padding: 20px 20px 20px 20px;
  width: 90%;
  height: 250px;
  overflow: auto;
}

.saveBlock .tagStyle {
  margin: 10px 0 0 10px;
  /* width: 120px; */
  height: 40px;
  text-align: center;
  line-height: 40px;
  font-size: 16px;
  font-weight: bold;
}

.locationcheckboxAll {
  font-weight: bold;
}

.locationchcheckboxreel {
  margin: auto;
  padding: 20px 20px 20px 20px;
  width: 90%;
  height: 265px;
  overflow: auto;
  background: rgba(247, 242, 242, 0.993);
  border: 2px solid rgba(18, 17, 17, 0.2);
}

.locationCheckbox {
  margin-top: 10px;
  padding-left: 10px;
  font-weight: bold;
}

.tagStyle:hover {
  background-color: #fafafa;
  color: gray;
}

.locationSaveButton {
  margin-top: 20px;
  display: flex;
  justify-content: right;
}

.el-card__body {
  background: #f0f8ff;
}
</style>