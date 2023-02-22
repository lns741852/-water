/* eslint-disable no-use-before-define */
import axios from 'axios'
import API_URL from '../js/API'
import authHeader from './auth-header';
import { downloadRequest } from '../js/download';

// const API = API_URL(API) + '8000/'
const API = API_URL(API) + '/'

class UserServices {
    /** 登入驗證 */
    async tokenCheck() {
        let token = await authHeader();
        const data = await axios.post(API + 'HRCS/RefreshJWTToken', token).then(res => res.data);
        return data;
    }

    /** 取得員工資料 */
    async getEmpdata() {
        const data = await axios.get(API + 'HRCS/getEmpdata', {
            headers: authHeader()
        }).then(res => res.data);
        return data;
    }


    /** 取得地址_員工資料 */
    async getEmplocationdata(id) {
        const data = await axios.get(API + 'HRCS/getEmpLocationdata/' + id, {
            headers: authHeader()
        }).then(res => res.data);

        return data;


    }


    /** 取得地址_單位資料 */
    async getEmpGroupdata(id) {
        const data = await axios.get(API + 'HRCS/getEmpGroupdata/' + id, {
            headers: authHeader()
        }).then(res => res.data);

        return data;
    }

    /** 取得員工資料 */
    async getEmpdata2() {
        const data = await axios.get(API + 'HRCS/getEmpdata2', {
            headers: authHeader()
        }).then(res => res.data);
        return data;
    }

    /** 新增員工資料 */
    async addEmpdata(empData) {
        await axios.post(API + 'HRCS/getEmpdata', empData, {
            headers: authHeader()
        })
            .then(res => {
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.status
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.status
                }
            })
            .catch(function (error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }

    /** 新增部門資料 */
    async addDepdata(dep_name) {
        await axios.post(API + 'HRCS/getDepdata', dep_name, {
            headers: authHeader()
        })
            .then(res => {
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.status
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.status
                }
            })
            .catch(function (error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }
    /** 新增職位資料 */
    // async addWorkdata(wp) {
    //     await axios.post(API + 'HRCS/getWorkpositionList', wp, {
    //         headers: authHeader()
    //     })
    //         .then(res => {
    //             if (res.data) {
    //                 localStorage.setItem('MSG', JSON.stringify({
    //                     code: res.status,
    //                     msg: res.data.status
    //                 }))
    //             }
    //             return {
    //                 code: res.status,
    //                 msg: res.data.status
    //             }
    //         })
    //         .catch(function (error) {
    //             if (error.res.data) {
    //                 localStorage.setItem('MSG', JSON.stringify({
    //                     code: error.res.status,
    //                     msg: error.res.data.status
    //                 }))
    //             }
    //             return {
    //                 code: error.res.status,
    //                 msg: error.res.data.status
    //             }
    //         })
    // }

    /** 新增組別資料 */
    async addGroupdata(group) {
        await axios.post(API + 'HRCS/getGroupdata', group, {
            headers: authHeader()
        })
            .then(res => {
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.status
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.status
                }
            })
            .catch(function (error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }


    /** 新增地址資料 */
    async addLocationdata(location) {
        await axios.post(API + 'HRCS/getLocationdata', location, {
            headers: authHeader()
        })
            .then(res => {
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.Response
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.Response
                }
            })
            .catch(function (error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }

    /** 補打卡 */
    // async addAttendanceData(attendanceData) {
    //     await axios.post(API + 'HRCS/attendanceData', attendanceData, {
    //         headers: authHeader()
    //     })
    //         .then(res => {
    //             if (res.data) {
    //                 localStorage.setItem('MSG', JSON.stringify({
    //                     code: res.status,
    //                     msg: res.data.status
    //                 }))
    //             }
    //             return {
    //                 code: res.status,
    //                 msg: res.data.status
    //             }
    //         })
    //         .catch(function (error) {
    //             if (error.res.data) {
    //                 localStorage.setItem('MSG', JSON.stringify({
    //                     code: error.res.status,
    //                     msg: error.res.data.status
    //                 }))
    //             }
    //             return {
    //                 code: error.res.status,
    //                 msg: error.res.data.status
    //             }
    //         })
    // }

    /** 更新員工資料 */
    async updataEmpdata(empData) {
        await axios.put(API + 'HRCS/getEmpdata', empData, {
            headers: authHeader()
        })
            .then(res => {
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.status
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.status
                }
            })
            .catch(function (error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }

    /** 更新部門資料 */
    // async updataDepdata(depData) {
    //     await axios.put(API + 'HRCS/getDepdata', depData, {
    //         headers: authHeader()
    //     })
    //         .then(res => {
    //             if (res.data) {
    //                 localStorage.setItem('MSG', JSON.stringify({
    //                     code: res.status,
    //                     msg: res.data.status
    //                 }))
    //             }
    //             return {
    //                 code: res.status,
    //                 msg: res.data.status
    //             }
    //         })
    //         .catch(function (error) {
    //             if (error.res.data) {
    //                 localStorage.setItem('MSG', JSON.stringify({
    //                     code: error.res.status,
    //                     msg: error.res.data.status
    //                 }))
    //             }
    //             return {
    //                 code: error.res.status,
    //                 msg: error.res.data.status
    //             }
    //         })
    // }

    /** 更新職位資料 */
    // async updataWpdata(wpData) {
    //     await axios.put(API + 'HRCS/getWorkpositionList', wpData, {
    //         headers: authHeader()
    //     })
    //         .then(res => {
    //             if (res.data) {
    //                 localStorage.setItem('MSG', JSON.stringify({
    //                     code: res.status,
    //                     msg: res.data.status
    //                 }))
    //             }
    //             return {
    //                 code: res.status,
    //                 msg: res.data.status
    //             }
    //         })
    //         .catch(function (error) {
    //             if (error.res.data) {
    //                 localStorage.setItem('MSG', JSON.stringify({
    //                     code: error.res.status,
    //                     msg: error.res.data.status
    //                 }))
    //             }
    //             return {
    //                 code: error.res.status,
    //                 msg: error.res.data.status
    //             }
    //         })
    // }


    /** 更新組別資料 */
    async updataGroupdata(groupData) {
        await axios.put(API + 'HRCS/getGroupdata', groupData, {
            headers: authHeader()
        })
            .then(res => {
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.status
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.status
                }
            })
            .catch(function (error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }

    /** 更新地址資料 */
    async updataLocationata(location) {
        await axios.put(API + 'HRCS/getLocationdata', location, {
            headers: authHeader()
        })
            .then(res => {
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.Response
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.Response
                }
            })
            .catch(function (error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }

    /** 更新權限資料 */
    async updataAuthdata(authData) {
        await axios.put(API + 'HRCS/getAuthdata', authData, {
            headers: authHeader()
        })
            .then(res => {
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.status
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.status
                }
            })
            .catch(function (error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }


    /** 打卡位置開關 */
    async updatalocationCheck(num, checkList) {
        let empList = []

        checkList.forEach(element => {
            empList.push(element)
        });
        let data = {
            locationCheck: num,
            emp_no: empList
        }

        await axios.put(API + 'HRCS/putLocationdata', data, {
            headers: authHeader()
        })
            .then(res => {
                console.log(res)
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.Response
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.status
                }
            })
            .catch(function (error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }

    /** Line解除 */
    async lineCancel(checkList) {
        let empList = []

        checkList.forEach(element => {
            empList.push(element)
        });
        let data = {
            emp_no: empList
        }

        await axios.put(API + 'HRCS/delLineIddata', data, {
            headers: authHeader()
        }).then(res => {
            if (res.data) {
                localStorage.setItem('MSG', JSON.stringify({
                    code: res.status,
                    msg: res.data.Response
                }))
            }
            return {
                code: res.status,
                msg: res.data.status
            }
        })
            .catch(function (error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }




    /** 取得公司資料 */
    // async getCompanydata() {
    //     const data = await axios.get(API + 'HRCS/getCompanydata', {
    //         headers: authHeader()
    //     }).then(res => res.data)
    //     return data
    // }

    /** 取得人員MENU資料 */
    async getMenudata(emp_no) {
        const data = await axios.get(API + 'HRCS/menu/' + emp_no, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 取得MENU管理資料 */
    async getMenuList() {
        const data = await axios.get(API + 'HRCS/menu', {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }



    /** 取得部門資料 */
    // async getDepdata() {
    //     const data = await axios.get(API + 'HRCS/getDepdata', {
    //         headers: authHeader()
    //     }).then(res => res.data)
    //     return data
    // }

    /** 取得組別資料 */
    async getGroupdata() {
        const data = await axios.get(API + 'HRCS/getGroupdata', {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 取得權限資料 */
    async getAuthdata() {
        const data = await axios.get(API + 'HRCS/getAuthdata', {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 取得權限MENU資料 */
    async getAuthMenudata(auth_no) {
        const data = await axios.get(API + 'HRCS/getAuthMenudata/' + auth_no, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 更新權限MENU資料 */
    async updataAuthMenudata(attr) {
        const data = await axios.put(API + 'HRCS/getAuthMenudata', attr, {
            headers: authHeader()
        }).then(res => {
            if (res.data) {
                localStorage.setItem('MSG', JSON.stringify({
                    code: res.status,
                    msg: res.data.status
                }))
            }
            return {
                code: res.status,
                msg: res.data.status
            }
        })
            .catch(function (error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }


    /** 修改人員地址 */
    async updataEmpLocationdata(id, attr) {
        const data = await axios.put(API + 'HRCS/getEmpLocationdata/' + id, attr, {
            headers: authHeader()
        }).then(res => {
            if (res.data) {
                localStorage.setItem('MSG', JSON.stringify({
                    code: res.status,
                    msg: res.data.Response
                }))
            }
            return {
                code: res.status,
                msg: res.data.status
            }
        })
            .catch(function (error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.Response
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }


    /** 新增權限資料 */
    async addAuthdata(auth) {
        await axios.post(API + 'HRCS/getAuthdata', auth, {
            headers: authHeader()
        })
            .then(res => {
                if (res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: res.status,
                        msg: res.data.Response
                    }))
                }
                return {
                    code: res.status,
                    msg: res.data.status
                }
            })
            .catch(function (error) {
                if (error.res.data) {
                    localStorage.setItem('MSG', JSON.stringify({
                        code: error.res.status,
                        msg: error.res.data.status
                    }))
                }
                return {
                    code: error.res.status,
                    msg: error.res.data.status
                }
            })
    }


    /** 取得職位資料 */
    async getWPdata() {
        const data = await axios.get(API + 'HRCS/getWorkpositionList', {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 取得地址資料 */
    async getLocation() {
        // const data = await axios.get('http://127.0.0.1:3000/location', {
        // }).then(res => res.data)
        // return data
        const data = await axios.get(API + 'HRCS/getLocationdata', {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 取得出勤狀況資料 */
    // async getAttendancedata(attr) {
    //     const data = await axios.get(API + 'HRCS/getAttendanceEmpViewdata' + attr, {
    //         headers: authHeader()
    //     }).then(res => res.data)
    //     return data
    // }

    /** 取消打卡 */
    // async deleteAttendPunch(attend_no) {
    //     const data = await axios.post(API + 'HRCS/deleteAttendPunch', {
    //         attend_no
    //     }, {
    //         headers: authHeader()
    //     }).then(res => res.data)
    //     return data
    // }

    /** 刪除部門 */
    // async deleteDep(dep_no) {
    //     const data = await axios.post(API + 'HRCS/deleteDepno/' + dep_no, {
    //         headers: authHeader()
    //     }).then(res => res.data)
    //     return data
    // }

    /** 刪除職位 */
    // async deleteWP(wp_code) {
    //     const data = await axios.delete(API + 'HRCS/delWorkposition/' + wp_code, {
    //         headers: authHeader()
    //     }).then(res => res.data)
    //     return data
    // }

    /** 刪除組別*/
    async deleteGroup(group_no) {
        const data = await axios.delete(API + 'HRCS/delGroupdata/' + group_no, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 刪除位置*/
    async deleteLocation(no) {
        const data = await axios.delete(API + 'HRCS/delLocationdata/' + no, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 刪除權限*/
    async deleteAuth(auth_no) {
        const data = await axios.delete(API + 'HRCS/delAuthdata/' + auth_no, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 取得排班表資料 */
    // async getShiftdata(attr) {
    //     const data = await axios.get(API + 'HRCS/Shiftdata' + attr, {
    //         headers: authHeader()
    //     }).then(res => res.data)
    //     return data
    // }

    /** 取得時段資料 */
    // async getTimePerioddata() {
    //     const data = await axios.get(API + 'HRCS/getTimePeriod', {
    //         headers: authHeader()
    //     }).then(res => res.data)
    //     return data
    // }

    /** 編輯時段資料 */
    // async editTimePerioddata(attr) {
    //     const data = await axios.put(API + 'HRCS/getTimePeriod', attr, {
    //         headers: authHeader()
    //     }).then(res => res.data)
    //     return data
    // }


    // async resetPassword(attr) {
        // const data = await axios.put(API + 'HRCS/resetPassword', attr, {
        //     headers: authHeader()
        // }).then(res => res.data)
        // return data
    // }

    /** 新增時段資料 */
    // async addTimePerioddata(attr) {
    //     const data = await axios.post(API + 'HRCS/getTimePeriod', attr, {
    //         headers: authHeader()
    //     }).then(res => res.data)
    //     return data
    // }

    /** 新增排班表資料 */
    // async addScheduledata(newSchedule) {
    //     let MSG = ""
    //     await axios.post(API + 'HRCS/Shiftdata', JSON.parse(newSchedule), {
    //         headers: authHeader()
    //     })
    //         .then(res => {
    //             if (res.data) {
    //                 MSG = {
    //                     code: res.status,
    //                     msg: res.data.status
    //                 }
    //                 localStorage.setItem('MSG', JSON.stringify({
    //                     code: res.status,
    //                     msg: res.data.status
    //                 }))
    //             }
    //         })
    //         .catch(function (error) {
    //             // console.log(error);
    //             if (error.res.data) {
    //                 MSG = error.res.data
    //                 localStorage.setItem('MSG', JSON.stringify(error.res.data))
    //             }
    //         })
    //     return MSG
    // }

    /** 修改排班表資料 */
    // async modShiftdata(shift) {
    //     await axios.put(API + 'HRCS/Shiftdata', JSON.stringify(shift), {
    //         headers: authHeader()
    //     })
    //         .then(res => {
    //             // console.log("modShiftdata", res);
    //             if (res.data) {
    //                 localStorage.setItem('MSG', JSON.stringify({
    //                     code: res.status,
    //                     msg: res.data.status
    //                 }))
    //             }
    //             return {
    //                 code: res.status,
    //                 msg: res.data.status
    //             }
    //         })
    //         .catch(function (error) {
    //             if (error.res.data) {
    //                 localStorage.setItem('MSG', JSON.stringify({
    //                     code: error.res.status,
    //                     msg: error.res.data.status
    //                 }))
    //             }
    //             return {
    //                 code: error.res.status,
    //                 msg: error.res.data.status
    //             }
    //         })
    // }

    /** 刪除排班表資料 */
    // async delShiftdata(shiftNo) {
    //     await axios.delete(API + 'HRCS/Shiftdata/' + shiftNo, {
    //         headers: authHeader()
    //     })
    //         .then(res => {
    //             if (res.data) {
    //                 localStorage.setItem('MSG', JSON.stringify({
    //                     code: res.status,
    //                     msg: res.data.status
    //                 }))
    //             }
    //             return {
    //                 code: res.status,
    //                 msg: res.data.status
    //             }
    //         })
    //         .catch(function (error) {
    //             if (error.res.data) {
    //                 localStorage.setItem('MSG', JSON.stringify({
    //                     code: error.res.status,
    //                     msg: error.res.data.status
    //                 }))
    //             }
    //             return {
    //                 code: error.res.status,
    //                 msg: error.res.data.status
    //             }
    //         })
    // }

    /** 出勤資料查詢 */
    // async getAttendanceEmpViewQuery(attr) {
    //     const data = await axios.get(API + 'HRCS/getAttendanceEmpViewQuery' + attr, {
    //         headers: authHeader()
    //     }).then(res => res.data)
    //     return data
    // }

    /** 出勤資料查詢_Jay */
    async getShiftsAttendanceEmpViewQuery(attr) {
        const data = await axios.get(API + 'HRCS/getShiftsAttendanceEmpViewQuery' + attr, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 加班資料查詢 */
    async getWorkOvertimeQuery(attr) {
        const data = await axios.get(API + 'HRCS/getWorkOvertimeQuery' + attr, {
            headers: authHeader()
        }).then(res => res.data)
        return data
    }

    /** 個人月報表匯出 */
    // exportRMPdata(attr) {
    //     downloadRequest('HRCS/exportRMPQuery' + attr);
        // const data = axios.get(API + 'HRCS/exportRMPQuery' + attr, {
        //     headers: authHeader()
        // }).then(res => res.data)
        // return data
    // }


    /** 取得公司資料(TEST) */
    // async TESTgetEmpdata() {
    //     const data = await axios.get(API + 'TEST/getEmpdata', {
    //         headers: authHeader()
    //     }).then(res => res.data)
    //     return data
    // }
}

export default new UserServices()