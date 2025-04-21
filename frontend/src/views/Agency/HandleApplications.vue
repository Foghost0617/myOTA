<template>
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
      const res = await axios.get(`/tourist_routes/agency/${agency_id}/enrollments`)
      applications.value = res.data
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
  </style>
  