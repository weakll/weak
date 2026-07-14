<script setup>
import { Star } from '@lucide/vue'

const props = defineProps({
  reviews: { type: Array, default: () => [] }
})

const ratingStars = (r) => {
  const arr = []
  for (let i = 0; i < 5; i++) arr.push(i < r)
  return arr
}
</script>

<template>
  <section class="reviews-section">
    <div v-if="props.reviews.length" class="reviews-grid">
      <div class="review-card" v-for="r in props.reviews" :key="r.id">
        <div class="review-header">
          <img v-if="r.avatar && r.avatar.length > 2" :src="r.avatar" class="review-avatar-img" :alt="r.nickname || r.name" />
          <div v-else class="review-avatar">{{ r.avatar || (r.nickname || r.name)?.[0] || '?' }}</div>
          <div>
            <h4 class="review-name">{{ r.nickname || r.name }}</h4>
            <p class="review-store-name" v-if="r.store_name">&#127963; {{ r.store_name }}</p>
            <div class="review-stars">
              <Star v-for="(on, i) in ratingStars(r.rating)" :key="i" :size="14" :fill="on ? '#FF6B35' : 'transparent'" :stroke="on ? '#FF6B35' : '#555'" />
            </div>
          </div>
        </div>
        <p class="review-food" v-if="r.food">&#127858; {{ r.food }}</p>
        <p class="review-comment">{{ r.comment }}</p>
      </div>
    </div>
    <div v-else class="empty-state">
      <p>快来第一个点评吧&#65374;</p>
    </div>
  </section>
</template>

<style scoped>
.reviews-section { max-width: 1280px; margin: 0 auto; padding: 0 20px 80px; }
.reviews-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 20px; }
.review-card {
  background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.04);
  border-radius: 12px; padding: 20px; transition: all 0.3s;
}
.review-card:hover { border-color: rgba(255,107,53,0.15); transform: translateY(-2px); }
.review-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.review-avatar {
  width: 40px; height: 40px; border-radius: 50%;
  background: linear-gradient(135deg, #FF6B35, #f0932b);
  color: #fff; display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 1em; flex-shrink: 0;
}
.review-avatar-img { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
.review-name { color: #e0d6c8; font-size: 0.95em; margin: 0 0 4px; }
.review-store-name { color: #887766; font-size: 0.75em; margin: 0 0 4px; line-height: 1.3; }
.review-stars { display: flex; gap: 2px; }
.review-food { color: #FF6B35; font-size: 0.82em; margin: 0 0 8px; }
.review-comment { color: #a89880; font-size: 0.88em; margin: 0; line-height: 1.6; }

.empty-state { text-align: center; padding: 60px 0; color: #887766; font-size: 1.1em; }

@media (max-width: 640px) { .reviews-grid { grid-template-columns: 1fr; } }
</style>
