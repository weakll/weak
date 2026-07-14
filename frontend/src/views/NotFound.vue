<script setup>
import { useRouter } from 'vue-router'
import { Home, Search } from '@lucide/vue'
const router = useRouter()
</script>

<template>
  <div class="notfound-page">
    <div class="nf-content">
      <div class="nf-code">404</div>
      <h1 class="nf-title">页面不存在</h1>
      <p class="nf-desc">您访问的页面可能已被移除或地址输入有误</p>
      <div class="nf-actions">
        <button class="nf-btn primary" @click="router.push('/')"><Home :size="18" /> 返回首页</button>
        <button class="nf-btn" @click="router.push('/food-map')"><Search :size="18" /> 浏览摊位</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.notfound-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }
.nf-content { text-align: center; max-width: 480px; }
.nf-code { font-size: 8em; font-weight: 900; color: #FF6B35; line-height: 1; text-shadow: 0 0 40px rgba(255,107,53,0.3); margin-bottom: 16px; }
.nf-title { font-size: 1.8em; color: #e0d6c8; margin: 0 0 12px; }
.nf-desc { color: #887766; font-size: 1em; margin: 0 0 32px; line-height: 1.6; }
.nf-actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
.nf-btn { display: inline-flex; align-items: center; gap: 8px; padding: 12px 24px; border-radius: 50px; font-size: 0.95em; font-weight: 600; cursor: pointer; transition: all 0.2s; background: rgba(255,255,255,0.06); color: #e0d6c8; border: 1px solid rgba(255,255,255,0.1); }
.nf-btn:hover { background: rgba(255,255,255,0.1); }
.nf-btn.primary { background: linear-gradient(135deg, #FF6B35, #f0932b); color: #fff; border: none; box-shadow: 0 4px 16px rgba(255,107,53,0.3); }
.nf-btn.primary:hover { transform: translateY(-2px); box-shadow: 0 6px 24px rgba(255,107,53,0.5); }
</style>
