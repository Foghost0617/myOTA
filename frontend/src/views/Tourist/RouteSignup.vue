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
h2 {
  color: #000000; /* 设置 <h2> 颜色为黑色 */
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 20px; /* 增加下边距 */
}

.route-signup {
  padding: 20px;
  background-color: #f9f9f9; /* 轻微灰色背景，增强可读性 */
  border-radius: 8px;
}

.route-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.route-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  margin: 10px 0;
  background-color: #ffffff;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 增加阴影效果 */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 平滑的交互效果 */
}

.route-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.route-info h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333333; /* 标题颜色稍深 */
  margin-bottom: 8px;
}

.route-info p {
  font-size: 14px;
  color: #666666; /* 描述文字颜色较浅 */
}

.btn-signup {
  padding: 10px 18px;
  background-color: #28a745; /* 使用自然绿 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease, transform 0.2s ease; /* 添加过渡效果 */
}

.btn-signup:hover {
  background-color: #218838;
  transform: scale(1.05); /* 鼠标悬停时轻微放大按钮 */
}

.no-routes {
  text-align: center;
  font-size: 16px;
  color: #888888; /* 灰色文字 */
  margin-top: 30px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  padding: 10px 18px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.pagination button:hover {
  background-color: #0056b3;
  transform: scale(1.05); /* 鼠标悬停时轻微放大按钮 */
}

.pagination button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.pagination span {
  margin: 0 12px;
  line-height: 40px;
  font-size: 14px;
  color: #333333; /* 页码颜色 */
}
</style>
