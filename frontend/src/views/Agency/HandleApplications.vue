<!-- <template>
    <div class="application-container">
      <h2>游客报名审批</h2>
      <div v-if="applications.length === 0">暂无报名记录。</div>
      <div v-for="app in applications" :key="app.id" class="application-card">
        <p><strong>游客ID：</strong>{{ app.tourist_id }}</p>
        <p><strong>路线ID：</strong>{{ app.route_id }}</p>
        <p><strong>报名时间：</strong>{{ new Date(app.signup_date).toLocaleString() }}</p>
        <p><strong>状态：</strong>{{ app.status }}</p>
        <div class="actions" v-if="app.status === '待确认'">
          <button @click="approve(app.id)">同意</button>
          <button @click="reject(app.id)">拒绝</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
    import axios from '@/utils/request'
  
  const applications = ref([])
  
  const fetchApplications = async () => {
    const agency_id = parseInt(localStorage.getItem('agency_id') || '0')
    try {
      const res = await axios.get(`/tourist_route/agency/${agency_id}/enrollments`)
      applications.value = res.data
      console.log(applications)
    } catch (err) {
      console.error("获取报名记录失败", err)
    }
  }
  
  const approve = async (id) => {
    try {
      await axios.put(`/tourist_routes/enrollment/${id}/status`, { status: '已确认' })
      applications.value = applications.value.map(app => app.id === id ? { ...app, status: '已确认' } : app)
    } catch (err) {
      console.error("审批失败", err)
    }
  }
  
  const reject = async (id) => {
    try {
      await axios.put(`/tourist_routes/enrollment/${id}/status`, { status: '已取消' })
      applications.value = applications.value.map(app => app.id === id ? { ...app, status: '已取消' } : app)
    } catch (err) {
      console.error("审批失败", err)
    }
  }
  
  onMounted(() => {
    fetchApplications()
  })
  </script>
  
  <style scoped>
  .application-container {
    padding: 20px;
    max-width: 700px;
    margin: auto;
  }
  .application-card {
    background: #f9f9f9;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  }
  .actions {
    margin-top: 10px;
  }
  button {
    padding: 8px 14px;
    margin-right: 10px;
    border: none;
    border-radius: 5px;
    background-color: #1abc9c;
    color: white;
    cursor: pointer;
  }
  button:hover {
    background-color: #16a085;
  }
  </style> -->
  
  <template>
    <div class="application-container">
      <h2>游客报名审批</h2>
      <div v-if="applications.length === 0">暂无报名记录。</div>
      
      <!-- 显示分页后的报名记录 -->
      <div v-for="app in paginatedApplications" :key="app.id" class="application-card">
        <p><strong>游客ID：</strong>{{ app.tourist_id }}</p>
        <p><strong>路线ID：</strong>{{ app.route_id }}</p>
        <p><strong>报名时间：</strong>{{ new Date(app.signup_date).toLocaleString() }}</p>
        <p><strong>状态：</strong>{{ app.status }}</p>
        <div class="actions" v-if="app.status === '待确认'">
          <button @click="approve(app.id)">同意</button>
          <button @click="reject(app.id)">拒绝</button>
        </div>
      </div>
  
      <!-- 分页控制 -->
      <div v-if="totalPages > 1" class="pagination">
        <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">上一页</button>
        <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
        <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">下一页</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import axios from '@/utils/request'
  
  const applications = ref([]) // 存储所有报名记录
  const paginatedApplications = ref([]) // 当前页面需要显示的报名记录
  const currentPage = ref(1) // 当前页数
  const pageSize = 3 // 每页记录数
  const totalPages = ref(1) // 总页数
  
  // 获取报名记录
  const fetchApplications = async () => {
    const agency_id = parseInt(localStorage.getItem('agency_id') || '0')
    try {
      const res = await axios.get(`/tourist_route/agency/${agency_id}/enrollments`)
      applications.value = res.data
      totalPages.value = Math.ceil(applications.value.length / pageSize)
      updatePaginatedApplications()
    } catch (err) {
      console.error("获取报名记录失败", err)
    }
  }
  
  // 分页逻辑：更新当前页的数据
  const updatePaginatedApplications = () => {
    const start = (currentPage.value - 1) * pageSize
    const end = currentPage.value * pageSize
    paginatedApplications.value = applications.value.slice(start, end)
  }
  
  // 同意报名
const approve = async (id) => {
  try {
    // 打印请求数据
    const requestData = { status: '已确认' }
    console.log(`发送请求，ID: ${id}, 数据:`, requestData)

    const response = await axios.put(`/tourist_route/enrollment/${id}/status`, requestData)

    // 打印响应数据
    console.log(`响应数据：`, response.data)

    // 更新申请状态
    applications.value = applications.value.map(app => app.id === id ? { ...app, status: '已确认' } : app)
    updatePaginatedApplications()

  } catch (err) {
    console.error("审批失败", err)
  }
}

// 拒绝报名
const reject = async (id) => {
  try {
    // 打印请求数据
    const requestData = { status: '已取消' }
    console.log(`发送请求，ID: ${id}, 数据:`, requestData)

    const response = await axios.put(`/tourist_route/enrollment/${id}/status`, requestData)

    // 打印响应数据
    console.log(`响应数据：`, response.data)

    // 更新申请状态
    applications.value = applications.value.map(app => app.id === id ? { ...app, status: '已取消' } : app)
    updatePaginatedApplications()

  } catch (err) {
    console.error("审批失败", err)
  }
}

  
  // 切换页面
  const changePage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
      updatePaginatedApplications()
    }
  }
  
  // 初始化时加载数据
  onMounted(() => {
    fetchApplications()
  })
  </script>


 <style scoped>
 .application-container {
   padding: 20px;
   max-width: 700px;
   margin: auto;
   background-color: #f4f4f4; /* 增加整体背景色，避免白色背景 */
   border-radius: 10px;
   box-shadow: 0 2px 10px rgba(0,0,0,0.1);
   height: 75%; /* 限制容器高度为视口的80% */
   overflow-y: auto; /* 添加垂直滚动条 */
 }
 
 .application-container h2 {
   font-size: 24px;
   font-weight: bold;
   color: #333; /* 深灰色字体，确保清晰可见 */
   margin-bottom: 20px; /* 加大标题和内容的间隔 */
   text-align: center; /* 居中显示标题 */
   text-transform: uppercase; /* 将标题转换为大写，提升标题的视觉层次感 */
   letter-spacing: 1px; /* 增加字母间距，使标题更有层次感 */
 }
 
 .application-card {
   background: #ffffff;
   border-radius: 8px;
   padding: 15px;
   margin-bottom: 15px;
   box-shadow: 0 2px 5px rgba(0,0,0,0.05);
   color: #333; /* 增加字体颜色对比度 */
 }
 
 .actions {
   margin-top: 10px;
 }
 
 button {
   padding: 8px 14px;
   margin-right: 10px;
   border: none;
   border-radius: 5px;
   background-color: #1abc9c; /* 更鲜明的按钮颜色 */
   color: white;
   cursor: pointer;
   font-weight: bold;
 }
 
 button:hover {
   background-color: #16a085; /* 鼠标悬停时按钮颜色变化 */
 }
 
 button:disabled {
   background-color: #bdc3c7; /* 禁用按钮的颜色 */
   cursor: not-allowed;
 }
 
 .pagination {
   display: flex;
   justify-content: center;
   margin-top: 20px;
 }
 
 .pagination button {
   padding: 8px 14px;
   border: none;
   border-radius: 5px;
   background-color: #3498db; /* 分页按钮颜色 */
   color: white;
   cursor: pointer;
   font-weight: bold;
 }
 
 .pagination button:hover {
   background-color: #2980b9; /* 鼠标悬停时分页按钮颜色变化 */
 }
 
 .pagination button:disabled {
   background-color: #bdc3c7; /* 禁用分页按钮的颜色 */
   cursor: not-allowed;
 }
 </style>
 
  
  
  