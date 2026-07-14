<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { stalls } from '../data/foodData.js'
import { X } from '@lucide/vue'

const PLACEHOLDER = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%232a1f14'/%3E%3Cstop offset='50%25' style='stop-color:%233a2a18'/%3E%3Cstop offset='100%25' style='stop-color:%232a1f14'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='400' height='300' fill='url(%23g)'/%3E%3C/svg%3E"
const onImgError = (e) => { if (e.target.src !== PLACEHOLDER) e.target.src = PLACEHOLDER }

const router = useRouter()
const mapContainer = ref(null)
const selectedStall = ref(null)
let map = null
let markers = []

// 2. 自定义圆形彩色标记：清晰可辨，按类别区分颜色
const catStyles = {
  '肉类': { bg: '#e74c3c', label: '肉' },
  '海鲜': { bg: '#3498db', label: '鲜' },
  '素食': { bg: '#2ecc71', label: '素' },
  '甜点': { bg: '#f39c12', label: '甜' },
}

const createIcon = (cat) => {
  const s = catStyles[cat] || { bg: '#FF6B35', label: '食' }
  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="background:${s.bg};width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 10px rgba(0,0,0,0.5);border:3px solid rgba(255,255,255,0.9);cursor:pointer;transition:transform 0.2s"><span style="color:#fff;font-size:13px;font-weight:700;line-height:1">${s.label}</span></div>`,
    iconSize: [40, 40],
    iconAnchor: [20, 20],
    popupAnchor: [0, -22],
  })
}

onMounted(async () => {
  await nextTick()
  if (!mapContainer.value) return

  // 1. 限制缩放范围 minZoom:15 / maxZoom:19
  map = L.map(mapContainer.value, {
    center: [40.6572, 109.8411],
    zoom: 17,
    minZoom: 15,
    maxZoom: 19,
    zoomControl: false,
    attributionControl: false,
  })

  // 3. OSM 标准瓦片 + CSS 滤镜实现深色主题，加载更快
  L.tileLayer('https://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}', {
    maxZoom: 19,
    className: 'dark-tiles',
  }).addTo(map)

  L.control.zoom({ position: 'bottomright' }).addTo(map)
  L.control.attribution({ position: 'bottomleft', prefix: false }).addTo(map)

  stalls.forEach((s) => {
    const marker = L.marker([s.lat, s.lng], { icon: createIcon(s.category) })
      .addTo(map)
      .on('click', () => { selectedStall.value = s })
    markers.push(marker)
  })

  L.circle([40.6572, 109.8411], {
    radius: 40,
    color: '#FF6B35',
    fillColor: '#FF6B35',
    fillOpacity: 0.15,
    weight: 2,
    dashArray: '6 4',
  }).addTo(map).bindPopup('<b>包百美食街</b>')
})

onUnmounted(() => {
  if (map) { map.remove(); map = null }
  markers = []
})

const closePopup = () => { selectedStall.value = null }
</script>

<template>
  <section id="今日推荐" class="map-section">
    <div class="section-header">
      <h2 class="section-title"><span class="title-icon">&#128506;</span> 店铺目录</h2>
      <p class="section-desc">包百美食街 · 点击摊位图标查看详细信息</p>
    </div>
    <div class="map-wrapper">
      <div ref="mapContainer" class="map-container"></div>

      <div v-if="selectedStall" class="map-popup" @click.self="closePopup">
        <div class="popup-card">
          <button class="popup-close" @click="closePopup"><X :size="18" /></button>
          <button class="popup-link" @click="router.push('/store/' + selectedStall.slug); closePopup()">查看店铺详情 →</button>
          <img :src="selectedStall.image" :alt="selectedStall.name" class="popup-img" @error="onImgError" />
          <div class="popup-body">
            <h3>{{ selectedStall.name }}</h3>
            <p>{{ selectedStall.description }}</p>
            <div class="popup-meta">
              <span class="popup-price">{{ selectedStall.price }}</span>
              <span>&#9201; 排队{{ selectedStall.waiting }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.map-section { max-width: 1280px; margin: 0 auto; padding: 80px 20px; }
.section-header { text-align: center; margin-bottom: 32px; }
.section-title { font-size: clamp(2em, 4vw, 2.6em); font-weight: 800; color: #FF6B35; display: flex; align-items: center; justify-content: center; gap: 12px; margin: 0 0 8px; }
.section-desc { color: #a89880; font-size: 1.1em; }

.map-wrapper { position: relative; }
.map-container {
  width: 100%; height: 520px; border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.06); overflow: hidden;
  background: #1a1a1a;
}

.map-popup { position: absolute; inset: 0; background: rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: center; z-index: 1000; border-radius: 16px; }
.popup-card { background: #1e1a16; border: 1px solid rgba(255,107,53,0.3); border-radius: 12px; max-width: 340px; width: 90%; overflow: hidden; position: relative; }
.popup-link { display: block; width: 100%; background: rgba(255,107,53,0.12); border: 1px solid rgba(255,107,53,0.3); color: #FF6B35; padding: 10px; border-radius: 8px; cursor: pointer; font-size: 0.85em; margin-top: 12px; text-align: center; font-weight: 600; transition: all 0.2s; }
.popup-link:hover { background: rgba(255,107,53,0.25); }
.popup-close { position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.6); border: none; color: #fff; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 1; }
.popup-img { width: 100%; height: 180px; object-fit: cover; }
.popup-body { padding: 16px; }
.popup-body h3 { color: #FF6B35; margin: 0 0 8px; font-size: 1.1em; }
.popup-body p { color: #a89880; font-size: 0.85em; margin: 0 0 12px; line-height: 1.5; }
.popup-meta { display: flex; gap: 16px; color: #887766; font-size: 0.85em; }
.popup-price { color: #FF6B35; font-weight: 700; }

@media (max-width: 640px) { .map-container { height: 400px; } }
</style>

<style>
.dark-tiles {
  filter: invert(1) hue-rotate(180deg) brightness(0.85) saturate(0.5);
}
.leaflet-container { background: #1a1a1a; font-family: inherit; }
.custom-marker { background: none !important; border: none !important; }
.custom-marker:hover div { transform: scale(1.2) !important; }
.leaflet-control-zoom a {
  background: rgba(30,26,22,0.9) !important; color: #e0d6c8 !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
}
.leaflet-control-zoom a:hover { background: rgba(255,107,53,0.3) !important; }
.leaflet-control-attribution {
  background: rgba(0,0,0,0.5) !important; color: #888 !important; font-size: 10px !important;
}
.leaflet-control-attribution a { color: #ffaa00 !important; }
.leaflet-popup-content-wrapper {
  background: #1e1a16 !important; color: #e0d6c8 !important;
  border-radius: 8px !important; border: 1px solid rgba(255,107,53,0.2) !important;
}
.leaflet-popup-tip { background: #1e1a16 !important; }
</style>