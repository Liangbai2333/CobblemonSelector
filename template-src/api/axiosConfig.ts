import axios from "axios";

const instance = axios.create({
  baseURL: 'http://localhost:8888/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
instance.interceptors.response.use(
  (response) => {
    // 只返回响应数据部分
    return response.data;
  },
  (error) => {
    // 统一处理错误
    if (error.response) {
      // 服务器返回了错误状态码
      console.error('API Error:', error.response.status, error.response.data);
    } else if (error.request) {
      // 请求发送了但没有收到响应
      console.error('API Error: No response received', error.request);
    } else {
      // 设置请求时发生了错误
      console.error('API Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default instance;