import Mock from 'mockjs'

Mock.mock('/api/goodslist', 'get', {
    data: [{
            menu_no: "A1",
            menu_name: "出勤管理"
        }, {
            menu_no: "A2",
            menu_name: "出勤狀況管理"
        }, {
            menu_no: "A3",
            menu_name: "出勤狀況查詢"
        }, {
            menu_no: "B1",
            menu_name: "加班管理"
        }, {
            menu_no: "B2",
            menu_name: "加班時數查詢"
        }, {
            menu_no: "C1",
            menu_name: "人事管理"
        },
        {
            menu_no: "C3",
            menu_name: "人員管理"
        },
        {
            menu_no: "C4",
            menu_name: "職位管理"
        }, {
            menu_no: "C5",
            menu_name: "群組管理"
        }, {
            menu_no: "D1",
            menu_name: "權限管理"
        }, {
            menu_no: "D2",
            menu_name: "不知道"
        }, {
            menu_no: "D3",
            menu_name: "不知道222222"
        }
    ],
});

Mock.mock('/api/auth', 'get', {
    data: [{
        auth_no: "A",
        auth_name: "管理員"
    }, {
        auth_no: "B",
        auth_name: "測試人員"
    }, {
        auth_no: "C",
        auth_name: "使用者"
    }, ],
})

Mock.mock('/api/menu', 'get', {
    data: [{
            menu_no: "A1",
            menu_name: "出勤管理",
            children: [{
                menu_no: "A2",
                menu_name: "出勤狀況管理",
            }, {
                menu_no: "A3",
                menu_name: "出勤狀況查詢",
            }, ],
        },
        {
            menu_no: "B1",
            menu_name: "加班管理",
            children: [{
                menu_no: "B2",
                menu_name: "加班時數查詢",
            }],
        }
    ]

})

Mock.mock('/api/auth/menu/A', 'get', {
    data: ["A2", "B2"],
})


//POST
Mock.mock('/api/addgoods', 'post', function(option) {
    console.log(option)

    return {
        status: 200,
        message: '商品添加成功！'
    }
})