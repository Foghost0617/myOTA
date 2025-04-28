<template>
    <div class="complaint-container">
      <h2 class="title">游客投诉列表</h2>
  
      <div v-if="complaints.length === 0" class="empty">暂无投诉记录。</div>
  
      <div v-else class="complaint-list">
        <div
          v-for="complaint in complaints"
          :key="complaint.id"
          class="complaint-card"
        >
          <div class="card-left">
            <div class="created">提交时间：{{ formatDate(complaint.created_at) }}</div>
            <div class="content">投诉内容：{{ complaint.content }}</div>
            <div class="tourist">投诉人 ID：{{ complaint.tourist_id }}</div>
            <div class="status">
              状态：
              <span :class="complaint.status === '未处理' ? 'status-pending' : 'status-done'">
                {{ complaint.status }}
              </span>
            </div>
          </div>
          <div class="card-right">
            <button
              v-if="complaint.status === '未处理'"
              class="btn-handle"
              @click="markAsHandled(complaint)"
            >
              标记为已处理
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from '@/utils/request'
  
  const complaints = ref([])
  
  const fetchComplaints = async () => {
    try {
      const res = await axios.get('/complaints/check')
      complaints.value = res.data
    } catch (err) {
      console.error('获取投诉失败', err)
    }
  }
  
  // 更新投诉状态为“已处理”
  const markAsHandled = async (complaint) => {
    try {
      // 调用后端接口更新状态
      await axios.put(`/complaints/${complaint.id}`, {
        status: '已处理'
      })
  
      // 更新前端列表中的该条投诉状态
      complaint.status = '已处理'
    } catch (err) {
      console.error('更新状态失败', err)
    }
  }
  
  const formatDate = (ts) => new Date(ts).toLocaleString()
  
  onMounted(fetchComplaints)
  </script>
  
  <style scoped>
  .complaint-container {
    padding: 24px;
    background-color: #f9fafb;
    min-height: 100%;
    color: #111827;
    font-family: "Helvetica Neue", Arial, sans-serif;
  }
  
  .title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 16px;
  }
  
  .empty {
    color: #6b7280;
  }
  
  .complaint-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
    max-height: 400px; /* 设置最大高度 */
    overflow-y: auto; /* 允许垂直滚动 */
  }
  
  .complaint-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }
  
  .card-left {
    flex: 1;
  }
  
  .created {
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 4px;
  }
  
  .content {
    font-size: 16px;
    font-weight: 500;
    margin-bottom: 6px;
  }
  
  .tourist {
    font-size: 14px;
    color: #4b5563;
  }
  
  .status {
    margin-top: 4px;
    font-size: 14px;
  }
  
  .status-pending {
    color: #ef4444;
    font-weight: bold;
  }
  
  .status-done {
    color: #10b981;
    font-weight: bold;
  }
  
  .card-right {
    margin-left: 12px;
  }
  
  .btn-handle {
    padding: 6px 12px;
    background-color: #3b82f6;
    color: white;
    border: 2px solid #3b82f6;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  
  .btn-handle:hover {
    background-color: #2563eb;
  }
  
  .btn-handle:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
  }
  </style>
  
  
  