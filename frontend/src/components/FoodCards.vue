<script setup>
import api from "../api"

import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Flame, Leaf, Star } from '@lucide/vue'

const PLACEHOLDER = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%232a1f14'/%3E%3Cstop offset='50%25' style='stop-color:%233a2a18'/%3E%3Cstop offset='100%25' style='stop-color:%232a1f14'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='400' height='300' fill='url(%23g)'/%3E%3C/svg%3E"
const props = defineProps({
  searchText: { type: String, default: "" },
  sortBy: { type: String, default: "popularity" },
})

const onImgError = (e) => { if (e.target.src !== PLACEHOLDER) e.target.src = PLACEHOLDER }

const router = useRouter()
const activeCat = ref('全部')
const cats = ['全部', '肉类', '海鲜', '素食', '甜点']



const setCat = (c) => { activeCat.value = c }

const allStalls = ref([])

const filtered = computed(() => {
  let result = allStalls.value
  if (activeCat.value !== '全部') {
    result = result.filter(s => s.category === activeCat.value)
  }
  const q = props.searchText.trim().toLowerCase()
  if (q) {
    result = result.filter(s =>
      s.name.toLowerCase().includes(q) ||
      s.description.toLowerCase().includes(q) ||
      s.category.toLowerCase().includes(q)
    )
  }
  if (props.sortBy === 'name') {
    result = [...result].sort((a, b) => a.name.localeCompare(b.name))
  } else {
    result = [...result].sort((a, b) => b.popularity - a.popularity)
  }
  return result
})

onMounted(async () => {
  try {
    const { data } = await api.get('/stores/')
    allStalls.value = Array.isArray(data) ? data : []
  } catch {}
})
</script>

<template>
  <section id="美食地图" class="food-cards-section">
    <div class="section-header">
      <h2 class="section-title">
        <span class="title-icon">&#127858;</span>
        特色美食
      </h2>
      <p class="section-desc">烟火气里寻美味，总有一款适合你</p>
    </div>

    <div class="filter-bar">
      <button v-for="c in cats" :key="c" class="filter-btn" :class="{ active: activeCat === c }" @click="setCat(c)">
        {{ c }}
      </button>
    </div>

    <div class="cards-grid">
      <div class="food-card" v-for="s in filtered" :key="s.id" @click="router.push('/store/' + s.slug)" style="cursor:pointer">
        <div class="card-img-wrap">
          <img :src="s.image_url" :alt="s.name" class="card-img" loading="lazy" @error="onImgError" />
          <div class="card-badges">
            <span v-if="s.spicy" class="badge spicy"><Flame :size="12" /> 辣</span>
            <span v-if="s.vegetarian" class="badge veg"><Leaf :size="12" /> 素</span>
          </div>
          <div class="card-popularity">
            <Star :size="12" fill="#FF6B35" stroke="none" />
            {{ s.popularity }}%推荐
          </div>
        </div>
        <div class="card-body">
          <h3 class="card-name">{{ s.name }}</h3>
          <p class="card-desc">{{ s.description }}</p>
          <div class="card-footer">
            <span class="card-price">{{ s.price }}</span>
            <span class="card-wait">&#9201; {{ s.waiting }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.food-cards-section {
  max-width: 1280px; margin: 0 auto; padding: 80px 20px;
}
.section-header { text-align: center; margin-bottom: 32px; }
.section-title {
  font-size: clamp(2em, 4vw, 2.6em); font-weight: 800; color: #FF6B35;
  display: flex; align-items: center; justify-content: center; gap: 12px;
  margin: 0 0 8px;
}
.title-icon { font-size: 0.9em; }
.section-desc { color: #a89880; font-size: 1.1em; }

.filter-bar { display: flex; justify-content: center; gap: 10px; margin-bottom: 40px; flex-wrap: wrap; }
.filter-btn {
  padding: 8px 22px; border-radius: 20px; border: 1px solid rgba(255,107,53,0.3);
  background: transparent; color: #c0a880; cursor: pointer; font-size: 0.9em;
  transition: all 0.3s;
}
.filter-btn:hover, .filter-btn.active {
  background: rgba(255,107,53,0.2); border-color: #FF6B35; color: #FF6B35;
}

.cards-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 24px;
}
.food-card {
  background: rgba(26,22,18,0.8); border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px; overflow: hidden; transition: all 0.3s;
}
.food-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(255,107,53,0.15); border-color: rgba(255,107,53,0.2); }
.card-img-wrap { position: relative; height: 200px; overflow: hidden; }
.card-img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; }
.food-card:hover .card-img { transform: scale(1.08); }
.card-badges { position: absolute; top: 10px; left: 10px; display: flex; gap: 6px; }
.badge {
  display: flex; align-items: center; gap: 3px; padding: 3px 8px;
  border-radius: 10px; font-size: 0.7em; font-weight: 600;
}
.badge.spicy { background: rgba(239,68,68,0.8); color: #fff; }
.badge.veg { background: rgba(34,197,94,0.8); color: #fff; }
.card-popularity {
  position: absolute; top: 10px; right: 10px; display: flex; align-items: center; gap: 3px;
  background: rgba(20,18,14,0.8); color: #FF6B35; padding: 3px 10px;
  border-radius: 10px; font-size: 0.75em; font-weight: 600;
}
.card-body { padding: 16px 20px 20px; }
.card-name { font-size: 1.1em; color: #e0d6c8; margin: 0 0 8px; font-weight: 700; }
.card-desc { font-size: 0.85em; color: #a89880; margin: 0 0 14px; line-height: 1.5; }
.card-footer { display: flex; justify-content: space-between; align-items: center; }
.card-price { color: #FF6B35; font-weight: 700; font-size: 1.1em; }
.card-wait { color: #887766; font-size: 0.8em; }

@media (max-width: 640px) {
  .cards-grid { grid-template-columns: 1fr; }
}
</style>
