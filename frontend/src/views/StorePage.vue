<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from "../api"
import {
  Star, MapPin, Clock, Phone, Award, Users,
  ShoppingBag, X, ChevronLeft, Flame, Leaf, LoaderCircle,
  Image as ImageIcon, Send, MessageSquarePlus
} from '@lucide/vue'
import { useAuth } from '../composables/useAuth.js'

const { currentUser, isLoggedIn, openAuthModal } = useAuth()
const route = useRoute()
const router = useRouter()
const slug = route.params.slug

const store = ref(null)
const loading = ref(true)
const error = ref('')
const lightbox = ref(null)

onMounted(async () => {
  try {
    const { data } = await api.get(`/stores/${slug}/`)
    store.value = data
    loadStoreReviews()
  } catch {
    error.value = '店铺信息加载失败，请稍后重试'
  } finally {
    loading.value = false
  }
})

const openLightbox = (url) => { lightbox.value = url }
const closeLightbox = () => { lightbox.value = null }
const goBack = () => { router.back() }

const ratingStars = (r) => Array.from({ length: 5 }, (_, i) => i < Math.round(r || 0))

// 图片轮播
const currentImage = ref(0)
const galleryImages = computed(() => {
  if (!store.value) return []
  const images = [store.value.image_url]
  store.value.products?.forEach(p => {
    if (p.image_url && !images.includes(p.image_url)) images.push(p.image_url)
  })
  return images
})
const prevImage = () => {
  currentImage.value = (currentImage.value - 1 + galleryImages.value.length) % galleryImages.value.length
}
const nextImage = () => {
  currentImage.value = (currentImage.value + 1) % galleryImages.value.length
}

// 评价列表（分页）
const allReviews = ref([])
const visibleCount = ref(5)
const reviewLoading = ref(false)
const reviewError = ref('')

const loadStoreReviews = async () => {
  if (!store.value?.id) return
  reviewLoading.value = true
  reviewError.value = ''
  try {
    const { data } = await api.get('/reviews/', { params: { store_id: store.value.id } })
    allReviews.value = Array.isArray(data) ? data : []
  } catch {
    reviewError.value = '加载评价失败'
  } finally {
    reviewLoading.value = false
  }
}

const loadMoreReviews = () => { visibleCount.value += 5 }

const visibleReviews = computed(() => allReviews.value.slice(0, visibleCount.value))

// 评价提交
const showReviewForm = ref(false)
const reviewForm = ref({ rating: 5, food: '', comment: '' })
const reviewSubmitting = ref(false)
const reviewSubmitted = ref(false)

const toggleReviewForm = () => {
  if (!isLoggedIn.value) { openAuthModal(); return }
  showReviewForm.value = !showReviewForm.value
}

const submitStoreReview = async () => {
  if (!reviewForm.value.comment) return
  reviewSubmitting.value = true
  try {
    const { data } = await api.post('/reviews/submit/', {
      store: store.value.id,
      nickname: currentUser.value.username,
      rating: reviewForm.value.rating,
      food: reviewForm.value.food || '未指定美食',
      comment: reviewForm.value.comment,
    })
    if (data.success) {
      reviewForm.value = { rating: 5, food: '', comment: '' }
      reviewSubmitted.value = true
      showReviewForm.value = false
      loadStoreReviews()
      setTimeout(() => { reviewSubmitted.value = false }, 3000)
    }
  } catch {
    reviewError.value = '提交失败，请稍后重试'
  } finally {
    reviewSubmitting.value = false
  }
}
</script>

<template>
  <div class="store-page">
    <div class="page-top-spacer"></div>

    <div v-if="loading" class="state-box">
      <LoaderCircle :size="32" class="spin" />
      <p>加载中...</p>
    </div>
    <div v-else-if="error" class="state-box error">
      <p>{{ error }}</p>
      <button @click="router.go(0)" class="retry-btn">重新加载</button>
    </div>

    <template v-else-if="store">
      <button class="back-btn" @click="goBack"><ChevronLeft :size="20" /> 返回</button>

      <section class="store-hero">
        <img :src="store.image_url" :alt="store.name" class="store-cover" />
        <div class="store-hero-info">
          <h1>{{ store.name }}</h1>
          <div class="store-meta">
            <span class="store-cat">{{ store.category }}</span>
            <span class="store-rating"><Star :size="16" fill="#FF6B35" stroke="none" /> {{ store.rating }}</span>
          </div>
          <p class="store-desc">{{ store.description }}</p>
          <div class="store-contact">
            <span><MapPin :size="14" /> {{ store.address }}</span>
            <span><Clock :size="14" /> {{ store.opening_hours }}</span>
            <span v-if="store.phone"><Phone :size="14" /> {{ store.phone }}</span>
          </div>
        </div>
      </section>

      <section class="gallery-section" v-if="galleryImages.length > 1">
        <h2><ImageIcon :size="22" /> 店铺图集</h2>
        <div class="gallery-carousel">
          <button class="carousel-btn carousel-prev" @click="prevImage" aria-label="上一张">&lsaquo;</button>
          <div class="carousel-viewport" @click="openLightbox(galleryImages[currentImage])">
            <img :src="galleryImages[currentImage]" :alt="store.name" class="carousel-img" />
            <span class="carousel-counter">{{ currentImage + 1 }} / {{ galleryImages.length }}</span>
          </div>
          <button class="carousel-btn carousel-next" @click="nextImage" aria-label="下一张">&rsaquo;</button>
        </div>
        <div class="carousel-dots">
          <span v-for="(img, i) in galleryImages" :key="i" class="carousel-dot" :class="{ active: i === currentImage }" @click="currentImage = i"></span>
        </div>
      </section>

      <section class="cert-section" v-if="store.certificates?.length">
        <h2><Award :size="22" /> 经营证书</h2>
        <div class="cert-grid">
          <div class="cert-card" v-for="c in store.certificates" :key="c.id">
            <h3>{{ c.name }}</h3>
            <p class="cert-issuer">颁发：{{ c.issuer }}</p>
            <p class="cert-date" v-if="c.issue_date">日期：{{ c.issue_date }}</p>
            <p class="cert-desc" v-if="c.description">{{ c.description }}</p>
          </div>
        </div>
      </section>
      <div v-else class="empty-hint">老板还没有上传证书～</div>

      <section class="staff-section" v-if="store.staff?.length">
        <h2><Users :size="22" /> 经营人员</h2>
        <div class="staff-grid">
          <div class="staff-card" v-for="s in store.staff" :key="s.id">
            <div class="staff-avatar">{{ s.name[0] }}</div>
            <div class="staff-info">
              <h3>{{ s.name }} <span class="staff-role">{{ s.role }}</span></h3>
              <p>{{ s.bio }}</p>
            </div>
          </div>
        </div>
      </section>
      <div v-else class="empty-hint">暂无人员信息</div>

      <section class="products-section" v-if="store.products?.length">
        <h2><ShoppingBag :size="22" /> 售卖商品</h2>
        <div class="products-grid">
          <div class="product-card" v-for="p in store.products" :key="p.id">
            <div class="product-img-wrap">
              <img v-if="p.image_url" :src="p.image_url" :alt="p.name" class="product-img" />
              <div class="product-badges">
                <span v-if="p.spicy_level" class="badge spicy"><Flame :size="10" /> {{ '&#127798;'.repeat(p.spicy_level) }}</span>
                <span v-if="p.is_vegetarian" class="badge veg"><Leaf :size="10" /> 素</span>
              </div>
            </div>
            <div class="product-body">
              <h3>{{ p.name }} <span v-if="p.is_recommended" class="rec-tag">招牌</span></h3>
              <p v-if="p.description" class="product-desc">{{ p.description }}</p>
              <div class="product-price">{{ p.price }}</div>
            </div>
          </div>
        </div>
      </section>
      <div v-else class="empty-hint">老板还没有上架商品～</div>

      <section class="reviews-section">
        <h2><MessageSquarePlus :size="22" /> 食客评价 <span class="review-count">({{ allReviews.length }})</span></h2>
        <div class="review-actions">
          <button class="write-review-btn" @click="toggleReviewForm">
            <Send :size="16" /> {{ isLoggedIn ? '写评价' : '登录后评价' }}
          </button>
        </div>
        <div v-if="showReviewForm" class="store-review-form">
          <div class="form-stars">
            <span>评分：</span>
            <button v-for="n in 5" :key="n" class="star-btn" :disabled="reviewSubmitting" @click="reviewForm.rating = n">
              <Star :size="22" :fill="n <= reviewForm.rating ? '#FF6B35' : 'transparent'" :stroke="n <= reviewForm.rating ? '#FF6B35' : '#555'" />
            </button>
          </div>
          <input v-model="reviewForm.food" placeholder="点了什么美食" class="form-input" />
          <textarea v-model="reviewForm.comment" placeholder="说说你的感受吧" class="form-textarea" rows="3"></textarea>
          <div class="form-actions">
            <button class="cancel-btn" @click="showReviewForm = false" :disabled="reviewSubmitting">取消</button>
            <button class="submit-btn" @click="submitStoreReview" :disabled="reviewSubmitting">
              <Send :size="16" /> {{ reviewSubmitting ? '提交中...' : '提交评价' }}
            </button>
          </div>
        </div>
        <div v-if="reviewSubmitted" class="submit-success">
          <span class="success-icon">&#10003;</span> 评价已提交！
        </div>
        <div v-if="reviewLoading" class="reviews-loading">
          <LoaderCircle :size="20" class="spin" />
        </div>
        <div v-else-if="reviewError" class="reviews-error">{{ reviewError }}</div>
        <div v-else-if="visibleReviews.length" class="reviews-list">
          <div class="review-item" v-for="r in visibleReviews" :key="r.id">
            <div class="review-avatar">{{ r.nickname[0] }}</div>
            <div class="review-info">
              <div class="review-top">
                <span class="review-name">{{ r.nickname }}</span>
                <div class="review-stars">
                  <Star v-for="n in 5" :key="n" :size="12" :fill="n <= r.rating ? '#FF6B35' : 'transparent'" :stroke="n <= r.rating ? '#FF6B35' : '#555'" />
                </div>
              </div>
              <p class="review-food" v-if="r.food">&#127858; {{ r.food }}</p>
              <p class="review-comment">{{ r.comment }}</p>
            </div>
          </div>
        </div>
        <div v-else class="empty-hint">暂无评价，快来第一个点评吧～</div>
        <button v-if="visibleCount < allReviews.length" class="load-more-btn" @click="loadMoreReviews">
          加载更多评价 ({{ allReviews.length - visibleCount }})
        </button>
      </section>
    </template>

    <Teleport to="body">
      <div v-if="lightbox" class="lightbox" @click="closeLightbox">
        <button class="lightbox-close" @click="closeLightbox"><X :size="24" /></button>
        <img :src="lightbox" class="lightbox-img" @click.stop />
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.store-page { min-height: 100vh; max-width: 1100px; margin: 0 auto; padding: 0 20px 80px; color: #e0d6c8; }
.page-top-spacer { height: 80px; }

.state-box { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 120px 20px; color: #887766; gap: 12px; }
.state-box.error { color: #ef4444; }
.retry-btn { background: rgba(255,107,53,0.12); border: 1px solid rgba(255,107,53,0.3); color: #FF6B35; border-radius: 8px; padding: 8px 20px; cursor: pointer; margin-top: 8px; }
.spin { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.back-btn { display: inline-flex; align-items: center; gap: 4px; background: none; border: 1px solid rgba(255,255,255,0.08); color: #a89880; border-radius: 8px; padding: 8px 16px; cursor: pointer; margin-bottom: 20px; transition: all 0.2s; font-size: 0.9em; }
.back-btn:hover { border-color: #FF6B35; color: #FF6B35; }

.store-hero { display: flex; gap: 28px; background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.04); border-radius: 16px; overflow: hidden; }
.store-cover { width: 360px; height: 260px; object-fit: cover; flex-shrink: 0; }
.store-hero-info { flex: 1; padding: 24px; display: flex; flex-direction: column; justify-content: center; gap: 10px; }
.store-hero-info h1 { font-size: 1.8em; font-weight: 800; color: #FF6B35; margin: 0; }
.store-meta { display: flex; gap: 12px; align-items: center; }
.store-cat { background: rgba(255,107,53,0.12); color: #FF6B35; padding: 3px 12px; border-radius: 10px; font-size: 0.8em; font-weight: 600; }
.store-rating { display: flex; align-items: center; gap: 4px; color: #FF6B35; font-weight: 600; }
.store-desc { color: #a89880; font-size: 0.95em; margin: 0; line-height: 1.6; }
.store-contact { display: flex; flex-wrap: wrap; gap: 14px; color: #887766; font-size: 0.82em; }
.store-contact span { display: flex; align-items: center; gap: 4px; }

section { margin-top: 48px; }
section h2 { font-size: 1.5em; font-weight: 800; display: flex; align-items: center; gap: 8px; color: #e0d6c8; margin: 0 0 20px; }
.review-count { font-weight: 400; color: #887766; font-size: 0.7em; }

/* 图集轮播 */
.gallery-section { margin-top: 48px; }
.gallery-carousel { position: relative; display: flex; align-items: center; gap: 12px; }
.carousel-viewport { flex: 1; border-radius: 12px; overflow: hidden; cursor: pointer; position: relative; aspect-ratio: 16/9; background: #1a1a1a; }
.carousel-img { width: 100%; height: 100%; object-fit: cover; transition: opacity 0.3s; }
.carousel-counter { position: absolute; bottom: 10px; right: 10px; background: rgba(0,0,0,0.6); color: #fff; padding: 3px 10px; border-radius: 10px; font-size: 0.8em; }
.carousel-btn { background: rgba(20,18,16,0.8); border: 1px solid rgba(255,255,255,0.1); color: #e0d6c8; border-radius: 50%; width: 40px; height: 40px; font-size: 1.5em; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0; transition: all 0.2s; }
.carousel-btn:hover { background: rgba(255,107,53,0.2); border-color: #FF6B35; color: #FF6B35; }
.carousel-dots { display: flex; justify-content: center; gap: 8px; margin-top: 12px; }
.carousel-dot { width: 8px; height: 8px; border-radius: 50%; background: #555; cursor: pointer; transition: all 0.2s; }
.carousel-dot.active { background: #FF6B35; width: 20px; border-radius: 4px; }

.cert-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }
.cert-card { background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; padding: 20px; }
.cert-card h3 { color: #FF6B35; font-size: 1em; margin: 0 0 8px; }
.cert-issuer, .cert-date { color: #887766; font-size: 0.82em; margin: 0 0 2px; }
.cert-desc { color: #a89880; font-size: 0.85em; margin: 8px 0 0; }

.staff-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
.staff-card { display: flex; gap: 16px; background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; padding: 20px; }
.staff-avatar { width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #FF6B35, #f0932b); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 1.2em; font-weight: 700; flex-shrink: 0; }
.staff-info h3 { color: #e0d6c8; font-size: 1em; margin: 0 0 6px; }
.staff-role { color: #FF6B35; font-size: 0.85em; font-weight: 400; }
.staff-info p { color: #a89880; font-size: 0.85em; margin: 0; line-height: 1.5; }

.products-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
.product-card { background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; overflow: hidden; transition: all 0.3s; }
.product-card:hover { transform: translateY(-2px); border-color: rgba(255,107,53,0.15); }
.product-img-wrap { position: relative; height: 150px; background: #1a1a1a; overflow: hidden; }
.product-img { width: 100%; height: 100%; object-fit: cover; }
.product-badges { position: absolute; top: 6px; left: 6px; display: flex; gap: 4px; }
.badge { display: flex; align-items: center; gap: 2px; padding: 2px 6px; border-radius: 6px; font-size: 0.65em; font-weight: 600; }
.badge.spicy { background: rgba(239,68,68,0.7); color: #fff; }
.badge.veg { background: rgba(34,197,94,0.7); color: #fff; }
.product-body { padding: 12px 14px 16px; }
.product-body h3 { color: #e0d6c8; font-size: 0.9em; margin: 0 0 4px; display: flex; align-items: center; gap: 6px; }
.rec-tag { background: #FF6B35; color: #fff; font-size: 0.7em; padding: 1px 6px; border-radius: 4px; font-weight: 600; }
.product-desc { color: #a89880; font-size: 0.78em; margin: 0 0 8px; line-height: 1.4; }
.product-price { color: #FF6B35; font-weight: 700; }

.reviews-section { }
.review-actions { margin-bottom: 16px; }
.write-review-btn { display: inline-flex; align-items: center; gap: 6px; background: rgba(255,107,53,0.12); border: 1px solid rgba(255,107,53,0.3); color: #FF6B35; border-radius: 20px; padding: 8px 20px; cursor: pointer; font-size: 0.85em; font-weight: 600; transition: all 0.2s; }
.write-review-btn:hover { background: rgba(255,107,53,0.2); }
.store-review-form { background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 20px; margin-bottom: 20px; display: flex; flex-direction: column; gap: 12px; }
.store-review-form .form-input, .store-review-form .form-textarea { padding: 10px 14px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #e0d6c8; font-size: 0.9em; outline: none; font-family: inherit; }
.store-review-form .form-input:focus, .store-review-form .form-textarea:focus { border-color: #FF6B35; }
.store-review-form .form-textarea { resize: vertical; min-height: 60px; }
.store-review-form .form-stars { display: flex; align-items: center; gap: 4px; }
.store-review-form .form-stars span { color: #a89880; font-size: 0.85em; margin-right: 8px; }
.store-review-form .star-btn { background: none; border: none; cursor: pointer; padding: 0; transition: transform 0.15s; }
.store-review-form .star-btn:hover { transform: scale(1.15); }
.store-review-form .form-actions { display: flex; gap: 10px; justify-content: flex-end; }
.store-review-form .cancel-btn { background: transparent; border: 1px solid rgba(255,255,255,0.1); color: #887766; padding: 8px 18px; border-radius: 8px; cursor: pointer; font-size: 0.85em; }
.store-review-form .cancel-btn:hover { border-color: #ef4444; color: #ef4444; }
.store-review-form .submit-btn { display: flex; align-items: center; gap: 6px; background: linear-gradient(135deg, #FF6B35, #f0932b); color: #fff; border: none; padding: 8px 18px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.85em; transition: all 0.2s; }
.store-review-form .submit-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(255,107,53,0.3); }
.submit-success { color: #22c55e; padding: 20px; text-align: center; }

.reviews-list { display: flex; flex-direction: column; gap: 12px; }
.review-item { display: flex; gap: 12px; background: rgba(26,22,18,0.4); border: 1px solid rgba(255,255,255,0.02); border-radius: 10px; padding: 16px; }
.review-avatar { width: 36px; height: 36px; border-radius: 50%; background: rgba(255,107,53,0.3); color: #FF6B35; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.9em; flex-shrink: 0; }
.review-info { flex: 1; }
.review-top { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
.review-name { color: #e0d6c8; font-size: 0.9em; font-weight: 600; }
.review-stars { display: flex; gap: 1px; }
.review-food { color: #FF6B35; font-size: 0.82em; margin: 4px 0; }
.review-comment { color: #a89880; font-size: 0.85em; margin: 0; line-height: 1.5; }

.empty-hint { text-align: center; padding: 40px 0; color: #665544; font-size: 0.9em; }
.reviews-loading { text-align: center; padding: 20px; }
.reviews-error { color: #ef4444; text-align: center; padding: 20px; }
.load-more-btn { display: block; margin: 20px auto 0; background: transparent; border: 1px solid rgba(255,255,255,0.08); color: #a89880; padding: 10px 24px; border-radius: 8px; cursor: pointer; font-size: 0.85em; transition: all 0.2s; }
.load-more-btn:hover { border-color: #FF6B35; color: #FF6B35; }

.lightbox { position: fixed; inset: 0; z-index: 3000; background: rgba(0,0,0,0.9); display: flex; align-items: center; justify-content: center; padding: 40px; }
.lightbox-img { max-width: 90vw; max-height: 90vh; border-radius: 8px; }
.lightbox-close { position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.1); border: none; color: #fff; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; cursor: pointer; }

@media (max-width: 768px) {
  .store-hero { flex-direction: column; }
  .store-cover { width: 100%; height: 200px; }
  .store-hero-info h1 { font-size: 1.4em; }
}
</style>
