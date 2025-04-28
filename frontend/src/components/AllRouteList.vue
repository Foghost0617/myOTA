<template>
    <div class="route-list">
      <h2>所有路线</h2>
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
  

  <style scoped>
  /* 标题样式 */
  h2 {
    color: #333333; /* 更深的黑色，增加对比度 */
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 20px;
    text-align: center; /* 居中标题 */
  }
  
  /* 路线列表 */
  .route-list {
    padding: 20px;
    background-color: #f8f9fa; /* 背景颜色改为浅灰色 */
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  }
  
  .route-list .route-card {
    margin-bottom: 20px;
  }
  
  /* 分页按钮 */
  .pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
  }
  
  .pagination button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    margin: 0 10px;
    transition: background-color 0.3s ease, transform 0.2s ease;
  }
  
  .pagination button:hover {
    background-color: #0056b3; /* 鼠标悬停时颜色变化 */
    transform: scale(1.05); /* 鼠标悬停时放大按钮 */
  }
  
  .pagination button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  
  .pagination span {
    font-size: 16px;
    color: #333333;
  }
  </style>