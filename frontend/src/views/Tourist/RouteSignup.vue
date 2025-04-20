<template>
    <div class="route-signup">
      <h2>所有可报名的路线</h2>
  
      <!-- 没有路线时显示 -->
      <div v-if="routes.length === 0" class="no-routes">
        <p>暂无可报名的路线。</p>
      </div>
  
      <!-- 路线列表 -->
      <div v-else>
        <ul class="route-list">
          <li v-for="route in pagedRoutes" :key="route.id" class="route-item">
            <div class="route-info">
              <h3>{{ route.name }}</h3>
              <p>{{ route.description }}</p>
            </div>
            <button @click="signup(route.id)" class="btn-signup">报名</button>
          </li>
        </ul>
  
        <!-- 分页控制按钮 -->
        <div class="pagination">
          <button @click="previousPage" :disabled="page === 1">上一页</button>
          <span>第 {{ page }} 页 / 共 {{ totalPages }} 页</span>
          <button @click="nextPage" :disabled="page === totalPages">下一页</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import axios from '@/utils/request';
  
  const touristId = parseInt(localStorage.getItem('tourist_id') || '0');
  const routes = ref([]);
  const signupStatus = ref('');
  
  // 分页控制
  const page = ref(1);
  const limit = ref(3); // 每页3条数据
  
  // 获取所有可报名的路线
  const fetchRoutes = async () => {
    try {
      console.log(`Fetching routes for page ${page.value}`);  // 调试输出
  
      const response = await axios.get('/routes/all');
  
      // 查看后端响应的数据
      console.log('Fetched routes:', response.data);
  
      routes.value = response.data; // 处理获取到的路线数据
    } catch (error) {
      console.error('获取路线失败:', error);
      signupStatus.value = '获取路线失败，请稍后再试';
    }
  };
  
  // 获取路线数据
  onMounted(() => {
    fetchRoutes();
  });
  
  // 计算分页后的数据
  const pagedRoutes = computed(() => {
    const start = (page.value - 1) * limit.value;
    const end = start + limit.value;
    return routes.value.slice(start, end);
  });
  
  // 总页数
  const totalPages = computed(() => {
    return Math.ceil(routes.value.length / limit.value);
  });
  
  // 报名函数
  const signup = async (routeId) => {
    if (!touristId) {
      signupStatus.value = '游客ID无效，请重新登录';
      return;
    }
  
    try {
      const response = await axios.post('/tourist_route/signup', { 
        tourist_id: touristId, 
        route_id: routeId,
        status: '待确认'  // 默认状态
      });
      alert("报名成功！")
    } catch (error) {
      console.error('报名失败:', error);
      signupStatus.value = '报名失败，请稍后再试';
    }
  };
  
  // 上一页
  const previousPage = () => {
    if (page.value > 1) {
      page.value--;  // 页数减 1
    }
  };
  
  // 下一页
  const nextPage = () => {
    if (page.value < totalPages.value) {
      page.value++;  // 页数加 1
    }
  };
  </script>
  
  
  
  
  <style scoped>
  .route-signup {
    padding: 20px;
  }
  
  .route-list {
    list-style: none;
    padding: 0;
  }
  
  .route-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #ccc;
    border-radius: 8px;
  }
  
  .route-info {
    flex-grow: 1;
  }
  
  .btn-signup {
    padding: 8px 16px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-signup:hover {
    background-color: #218838;
  }
  
  .no-routes {
    text-align: center;
    font-size: 16px;
    color: #888;
  }
  
  .pagination {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
  
  .pagination button {
    padding: 8px 16px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .pagination button:disabled {
    background-color: #cccccc;
  }
  
  .pagination span {
    margin: 0 10px;
    line-height: 32px;
  }
  </style>
  