<script setup>
import { transport } from '../data/foodData.js'
import { MapPin, Train, Bus, Car, Clock, Phone } from '@lucide/vue'
</script>

<template>
  <section id="交通指南" class="transport-section">
    <div class="section-header">
      <h2 class="section-title"><span class="title-icon">&#128205;</span> 交通指南 & 夜市信息</h2>
    </div>
    <div class="transport-grid">
      <div class="info-card">
        <MapPin :size="22" class="info-icon" />
        <div><h4>地址</h4><p>{{ transport.address }}</p></div>
      </div>
      <div class="info-card">
        <Train :size="22" class="info-icon" />
        <div><h4>地铁</h4><p>{{ transport.subway }}</p></div>
      </div>
      <div class="info-card">
        <Bus :size="22" class="info-icon" />
        <div><h4>公交</h4><p>{{ transport.bus }}</p></div>
      </div>
      <div class="info-card">
        <Car :size="22" class="info-icon" />
        <div><h4>停车指引</h4><p>{{ transport.parking }}</p></div>
      </div>
      <div class="info-card">
        <Clock :size="22" class="info-icon" />
        <div><h4>营业时间</h4><p>{{ transport.hours }}</p></div>
      </div>
      <div class="info-card">
        <Phone :size="22" class="info-icon" />
        <div><h4>联系电话</h4><p>{{ transport.phone }}</p></div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.transport-section { max-width: 1280px; margin: 0 auto; padding: 80px 20px; }
.section-header { text-align: center; margin-bottom: 40px; }
.section-title { font-size: clamp(2em, 4vw, 2.6em); font-weight: 800; color: #FF6B35; display: flex; align-items: center; justify-content: center; gap: 12px; margin: 0; }

.transport-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px; }
.info-card {
  display: flex; gap: 16px; background: rgba(26,22,18,0.6);
  border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; padding: 20px;
  transition: all 0.3s;
}
.info-card:hover { border-color: rgba(255,107,53,0.15); }
.info-icon { color: #FF6B35; flex-shrink: 0; margin-top: 2px; }
.info-card h4 { color: #e0d6c8; font-size: 0.95em; margin: 0 0 4px; }
.info-card p { color: #a89880; font-size: 0.88em; margin: 0; line-height: 1.5; }

@media (max-width: 640px) { .transport-grid { grid-template-columns: 1fr; } }
</style>