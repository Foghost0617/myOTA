<template>
    <div class="route-list">
      <h1>所有路线</h1>
      <div v-for="route in routes" :key="route.id" class="route-item">
        <h2>{{ route.name }}</h2>
        <p>{{ route.description }}</p>
        <button @click="viewDetails(route.id)">查看详情</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '@/utils/request'
  
  const agency_id = parseInt(localStorage.getItem('agency_id') || '0');

    export default {
        computed: {
             agencyId() {
      return agency_id;  // agencyId 直接返回常量 agency_id 的值
    }
    },
    data() {
        return {
        routes: [],
        };
    },

    mounted() {
        this.fetchRoutes();
    },

    // methods: {
    //     async fetchRoutes() {
    //         try {
    //             console.log(`正在请求路径: /routes/agency/${this.agencyId}`);
    //             const response = await axios.get(`/routes/agency/${this.agencyId}`);
    //             console.log('请求成功，返回的数据：', response.data);
                
    //             // 确认返回的数据结构
    //             if (Array.isArray(response.data)) {
    //             this.routes = response.data;
    //             } else {
    //             console.error('返回数据格式不正确:', response.data);
    //             }
    //         } catch (error) {
    //             console.error('获取路线列表失败', error);
    //             alert('无法获取路线列表');
    //         }
    //         },

    methods: {
  async fetchRoutes() {
    try {
        console.log(`正在请求路径: /routes/agency/${this.agencyId}`);
      const response = await axios.get('/routes/agency/' + this.agencyId);
      // 检查返回的数据
      console.log('请求成功，返回的数据：', response.data);
      if (Array.isArray(response.data)) {
        this.routes = response.data;  // 将获取的路由列表赋值给 routes
      } else {
        console.error('返回数据格式不正确:', response.data);
      }
    } catch (error) {
      console.error('获取路线列表失败', error);
      alert('无法获取路线列表');
    }
  },


        viewDetails(routeId) {
        this.$router.push({ name: 'RouteDetails', params: { routeId } });
        },
    },
    };

  </script>
  
  <style scoped>
  /* 设置整体页面的背景和字体 */
  .route-list {
    font-family: Arial, sans-serif;
    background-color: #f9f9f9;
    padding: 20px;
    min-height: 100vh;  /* 使页面至少充满屏幕 */
  }
  
  h1 {
    font-size: 2rem;
    font-weight: bold;
    color: #333;
    text-align: center;
    margin-bottom: 30px;
  }
  
  /* 路线项的容器 */
  .route-item {
    background-color: #fff;
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease;
  }
  
  /* 当鼠标悬停时，增加阴影效果 */
  .route-item:hover {
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  }
  
  /* 路线名称 */
  .route-item h2 {
    font-size: 1.5rem;
    color: #2d87f0;
    margin-bottom: 10px;
    font-weight: 600;
  }
  
  /* 路线描述 */
  .route-item p {
    font-size: 1rem;
    color: #666;
    margin-bottom: 15px;
    line-height: 1.6;
    max-height: 60px;
    overflow: hidden;  /* 限制描述文本的最大高度 */
  }
  
  /* 查看详情按钮 */
  .route-item button {
    background-color: #2d87f0;
    color: white;
    padding: 10px 20px;
    font-size: 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  /* 当按钮悬停时 */
  .route-item button:hover {
    background-color: #1e65b6;
  }
  
  /* 响应式设计：小屏幕设备上的样式 */
  @media (max-width: 600px) {
    h1 {
      font-size: 1.5rem;
    }
  
    .route-item {
      padding: 10px;
    }
  
    .route-item h2 {
      font-size: 1.2rem;
    }
  
    .route-item p {
      font-size: 0.9rem;
    }
  
    .route-item button {
      padding: 8px 16px;
      font-size: 0.9rem;
    }
  }
  </style>
  


  
  
  