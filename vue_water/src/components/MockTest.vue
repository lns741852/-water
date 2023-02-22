<template>
<div class="">
     <button @click="getGoodsList">获取商品列表</button>
</div>
</template>

<script type="text/ecmascript-6">
import axios from 'axios'

export default {
    methods:{
        async getGoodsList(){
           const {data:res} = await axios.get('/api/goodslist')
           console.log(res)
        }
    }


}
</script>

<style scoped lang='scss'>
</style>
