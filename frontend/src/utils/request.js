// src/utils/request.js
import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:8000', // 后端地址
  timeout: 5000
})

export default instance
