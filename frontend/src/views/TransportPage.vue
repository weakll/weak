<script setup>
import { transport } from '../data/foodData.js'
import TransportGuide from '../components/TransportGuide.vue'
import { MapPin, Navigation, Landmark } from '@lucide/vue'

const nearby = [
  { name: '包百商圈步行街', dist: '步行2分钟', desc: '集购物、餐饮、娱乐为一体的大型商业综合体。' },
  { name: '包头市博物馆', dist: '驾车8分钟', desc: '了解包头历史文化的绝佳去处，免费参观。' },
  { name: '昆都仑河公园', dist: '步行15分钟', desc: '城市中心的绿色氧吧，饭后散步好去处。' },
  { name: '赛罕塔拉生态园', dist: '驾车20分钟', desc: '大型城市生态公园，适合周末全家出游。' },
]
</script>

<template>
  <div class="transport-page">
    <div class="page-top-spacer"></div>
    <section class="page-hero">
      <h1>交通指南</h1>
      <p>如何来到烟火美食街</p>
    </section>
    <TransportGuide />
    <section class="nearby-section">
      <h2 class="section-title"><Landmark :size="22" /> 周边景点</h2>
      <p class="section-desc">吃饱喝足，周边还有这些好去处</p>
      <div class="nearby-grid">
        <div class="nearby-card" v-for="n in nearby" :key="n.name">
          <Navigation :size="18" class="nearby-icon" />
          <div>
            <h3>{{ n.name }}</h3>
            <p class="nearby-dist">{{ n.dist }}</p>
            <p class="nearby-desc">{{ n.desc }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.transport-page { min-height: 100vh; }
.page-top-spacer { height: 80px; }
.page-hero { text-align: center; padding: 40px 20px; background: linear-gradient(135deg, rgba(255,107,53,0.06), transparent); }
.page-hero h1 { font-size: 2.4em; font-weight: 800; color: #FF6B35; margin: 0 0 6px; letter-spacing: 3px; }
.page-hero p { color: #a89880; font-size: 1em; }

.section-title { font-size: 1.8em; font-weight: 800; color: #e0d6c8; display: flex; align-items: center; gap: 10px; }
.section-desc { color: #887766; font-size: 0.9em; margin: 0 0 28px; }

.nearby-section { max-width: 900px; margin: 0 auto; padding: 60px 20px 80px; }
.nearby-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
.nearby-card {
  display: flex; gap: 16px; background: rgba(26,22,18,0.6);
  border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; padding: 20px;
  transition: all 0.3s;
}
.nearby-card:hover { border-color: rgba(255,107,53,0.15); transform: translateY(-2px); }
.nearby-icon { color: #FF6B35; flex-shrink: 0; margin-top: 3px; }
.nearby-card h3 { color: #e0d6c8; font-size: 1em; margin: 0 0 4px; }
.nearby-dist { color: #FF6B35; font-size: 0.8em; margin: 0 0 6px; }
.nearby-desc { color: #a89880; font-size: 0.85em; margin: 0; line-height: 1.5; }

@media (max-width: 640px) { .nearby-grid { grid-template-columns: 1fr; } }
</style>