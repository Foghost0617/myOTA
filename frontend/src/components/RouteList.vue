<!-- <template>
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
  </style> -->
  

  <template>
    <div class="route-list">
      <h1>所有路线</h1>
      <!-- 显示路线列表 -->
      <div v-for="route in routes" :key="route.id" class="route-item">
        <h2>{{ route.name }}</h2>
        <p>{{ route.description }}</p>
        <button @click="viewDetails(route.id)">查看详情</button>
      </div>
  
      <!-- 分页控制按钮 -->
      <div class="pagination">
        <button @click="previousPage" :disabled="page === 1">上一页</button>
        <span>第 {{ page }} 页</span>
        <button @click="nextPage" :disabled="routes.length < limit">下一页</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '@/utils/request';
  
  
  const agency_id = parseInt(localStorage.getItem('agency_id') || '0');
  
  export default {
    computed: {
      agencyId() {
        return agency_id;  // agencyId 直接返回常量 agency_id 的值
      }
    },
    data() {
      return {
        routes: [],  // 存储路线列表
        page: 1,     // 当前页码
        limit: 3,    // 每页显示的数量
      };
    },
  
    mounted() {
      this.fetchRoutes();
    },
  
    methods: {
      async fetchRoutes() {
        try {
          // 请求数据并传递分页参数 (skip 和 limit)
          console.log(`正在请求路径: /routes/agency/${this.agencyId}?skip=${(this.page - 1) * this.limit}&limit=${this.limit}`);
          const response = await axios.get(`/routes/agency/${this.agencyId}`, {
            params: {
              skip: (this.page - 1) * this.limit,  // skip = (页码 - 1) * 每页条数
              limit: this.limit  // 每页显示的条数
            }
          });
  
          console.log('请求成功，返回的数据：', response.data);
          // 确认返回的数据格式
          if (Array.isArray(response.data)) {
            this.routes = response.data;
          } else {
            console.error('返回数据格式不正确:', response.data);
          }
        } catch (error) {
          console.error('获取路线列表失败', error);
          alert('无法获取路线列表');
        }
      },
  
       // 点击查看详情按钮，触发事件
       viewDetails(routeId) {
          console.log('触发查看详情，传递的 routeId:', routeId);  // 检查传递的 routeId
          this.$emit('view-details', routeId);
        },
  
      // 下一页
      nextPage() {
        this.page += 1;
        this.fetchRoutes();  // 请求下一页数据
      },
  
      // 上一页
      previousPage() {
        if (this.page > 1) {
          this.page -= 1;
          this.fetchRoutes();  // 请求上一页数据
        }
      }
    },
  };
  </script>
  

  <style scoped>
  /* 设置整体页面的背景和字体 */
  .route-list {
    padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-height: calc(100vh - 60px);  /* 限制最大高度为视窗高度减去顶部区域 */
  overflow-y: auto;  /* 当内容超出最大高度时显示滚动条 */
  margin: 0 auto;
  }

  /* 主标题样式 */
  h1 {
    font-size: 2rem;
    font-weight: bold;
    color: #333;
    text-align: center;
    margin-bottom: 30px;
  }
  
  /* 路线项的容器 */
  .route-item {
    background-color: #ffffff;
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease;
    max-width: 100; /* 确保项不会超出父容器 */
    overflow: hidden; /* 防止内容溢出 */
  }
  
  /* 当鼠标悬停时，增加阴影效果 */
  .route-item:hover {
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  }
  
  /* 路线名称 */
  .route-item h2 {
    font-size: 1.1rem;
    color: #2d87f0;
    margin-bottom: 10px;
    font-weight: 500;
  }
  
  /* 路线描述 */
  .route-item p {
    font-size: 1rem;
    color: #666;
    margin-bottom: 15px;
    line-height: 1.6;
    max-height: 50px;
    overflow: hidden; /* 限制描述文本的最大高度 */
  }
  
  /* 查看详情按钮 */
  .route-item button {
    background-color: #2d87f0;
    color: white;
    padding: 10px 20px;
    font-size: 0.9rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  /* 当按钮悬停时 */
  .route-item button:hover {
    background-color: #1e65b6;
  }
  
  /* 分页按钮 */
  .pagination {
    text-align: center;
    margin-top: 15px;
  }
  
  /* 分页按钮样式 */
  .pagination button {
    background-color: #2d87f0;
    color: white;
    padding: 10px 20px;
    font-size: 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin: 0 10px;
    transition: background-color 0.3s ease;
  }
  
  .pagination button:hover {
    background-color: #1e65b6;
  }
  
  /* 分页信息文字样式 */
  .pagination span {
    font-size: 1.2rem;
    color: #333;
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
  
    .pagination button {
      padding: 8px 16px;
      font-size: 0.9rem;
    }
  }
  
  </style>
  