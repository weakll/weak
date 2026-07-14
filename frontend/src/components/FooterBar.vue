<script setup>
</script>

<template>
  <footer id="关于我们" class="footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <span class="footer-logo">&#127753; 烟火美食街</span>
        <p class="footer-slogan">越夜越美味 · 人间烟火味</p>
      </div>
      <div class="footer-links">
        <router-link to="/">首页</router-link>
        <router-link to="/food-map">美食地图</router-link>
        <router-link to="/today">今日推荐</router-link>
        <router-link to="/events">活动公告</router-link>
        <router-link to="/reviews">食客点评</router-link>
        <router-link to="/transport">交通指南</router-link>
      </div>
      <p class="footer-copy">&#169; 2026 烟火美食街官网 · 保留所有权利</p>
    </div>
  </footer>
</template>

<style scoped>
.footer { background: #14120e; border-top: 1px solid rgba(255,255,255,0.06); padding: 32px 16px; }
.footer-inner { max-width: 1280px; margin: 0 auto; text-align: center; }
.footer-brand { margin-bottom: 20px; }
.footer-logo { font-size: 1.3em; font-weight: 700; color: #FF6B35; letter-spacing: 2px; }
.footer-slogan { color: #887766; font-size: 0.85em; margin: 6px 0 0; }
.footer-links { display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; }
.footer-links a { color: #a89880; text-decoration: none; font-size: 0.85em; transition: color 0.2s; }
.footer-links a:hover { color: #FF6B35; }
.footer-copy { color: #665544; font-size: 0.75em; margin: 0; }
</style>
