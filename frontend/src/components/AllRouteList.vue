<template>
    <div class="route-list">
      <h1>所有路线</h1>
  
      <!-- 使用 RouteCard 显示每条路线 -->
      <RouteCard
        v-for="route in paginatedRoutes"
        :key="route.id"
        :route="route"
        :showDelete="false" 
        @view-details="viewDetails"
      />
  
      <!-- 分页控制按钮 -->
      <div class="pagination">
        <button @click="previousPage" :disabled="page === 1">上一页</button>
        <span>第 {{ page }} 页</span>
        <button @click="nextPage" :disabled="endIndex >= allRoutes.length">下一页</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '@/utils/request'
  import RouteCard from '@/components/RouteCard.vue'
  
  export default {
    components: {
      RouteCard,
    },
    data() {
      return {
        allRoutes: [],   // 所有路线
        page: 1,
        limit: 3,        // 每页条数
      }
    },
    computed: {
      startIndex() {
        return (this.page - 1) * this.limit
      },
      endIndex() {
        return this.page * this.limit
      },
      paginatedRoutes() {
        return this.allRoutes.slice(this.startIndex, this.endIndex)
      },
    },
    mounted() {
      this.fetchAllRoutes()
    },
    methods: {
      async fetchAllRoutes() {
        try {
          const response = await axios.get('/routes/all')
          if (Array.isArray(response.data)) {
            this.allRoutes = response.data
          } else {
            console.error('返回数据格式不正确:', response.data)
          }
        } catch (error) {
          console.error('获取路线列表失败', error)
          alert('无法获取路线列表')
        }
      },
  
      // 触发查看详情的事件，传递 routeId
      viewDetails(routeId) {
        this.$emit('view-details', routeId)
      },
  
      nextPage() {
        if (this.endIndex < this.allRoutes.length) {
          this.page += 1
        }
      },
  
      previousPage() {
        if (this.page > 1) {
          this.page -= 1
        }
      },
    },
  }
  </script>
  
  