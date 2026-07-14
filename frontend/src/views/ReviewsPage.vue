<script setup>
import { ref, computed, onMounted } from 'vue'
import { Star, Star as StarFilled, MessageSquarePlus, Send, User, LoaderCircle } from '@lucide/vue'
import ReviewWall from '../components/ReviewWall.vue'
import { useAuth } from '../composables/useAuth.js'
import api from "../api"

const { isLoggedIn, currentUser, openAuthModal } = useAuth()

const stores = ref([])
const reviews = ref([])
const loading = ref(true)
const loadError = ref('')

const showForm = ref(false)
const newReview = ref({ store: '', food: '', rating: 5, comment: '' })
const submitted = ref(false)
const submitting = ref(false)

onMounted(async () => {
  try {
    const [storesRes, reviewsRes] = await Promise.all([
      api.get('/stores/'),
      api.get('/reviews/')
    ])
    stores.value = storesRes.data
    reviews.value = reviewsRes.data
  } catch {
    loadError.value = '加载数据失败，请刷新页面重试'
  } finally {
    loading.value = false
  }
})

const handleWriteReview = () => {
  if (!isLoggedIn.value) { openAuthModal(); return }
  showForm.value = true
}

const submitReview = async () => {
  if (!newReview.value.store || !newReview.value.comment) return
  submitting.value = true
  try {
    const { data } = await api.post('/reviews/submit/', {
      store: newReview.value.store,
      nickname: currentUser.value.username,
      rating: newReview.value.rating,
      food: newReview.value.food || '未指定美食',
      comment: newReview.value.comment,
    })
    if (data.success) {
      const res = await api.get('/reviews/')
      reviews.value = res.data
      submitted.value = true
      setTimeout(() => {
        submitted.value = false
        showForm.value = false
        newReview.value = { store: '', food: '', rating: 5, comment: '' }
      }, 3000)
    }
  } catch (e) {
    loadError.value = e.response?.data?.message || '提交失败，请稍后重试'
  } finally {
    submitting.value = false
  }
}

const avgRating = computed(() => {
  if (!reviews.value.length) return '0.0'
  return (reviews.value.reduce((s, r) => s + r.rating, 0) / reviews.value.length).toFixed(1)
})

const ratingDistribution = computed(() => {
  const total = reviews.value.length || 1
  const counts = [0, 0, 0, 0, 0, 0]
  reviews.value.forEach(r => { if (r.rating >= 1 && r.rating <= 5) counts[r.rating]++ })
  return [0, ...counts.slice(1).reverse().map(c => Math.round(c / total * 100))]
})
</script>

<template>
  <div class="reviews-page">
    <div class="page-top-spacer"></div>
    <section class="page-hero">
      <h1>食客点评</h1>
      <p>真实食客 · 真实评价</p>
    </section>

    <div v-if="loading" class="state-box">
      <LoaderCircle :size="32" class="spin" />
      <p>加载中...</p>
    </div>
    <div v-else-if="loadError" class="state-box error">
      <p>{{ loadError }}</p>
    </div>
    <template v-else>
      <section class="rating-overview">
        <div class="ro-stats">
          <div class="ro-big-num">{{ avgRating }}</div>
          <div class="ro-stars">
            <StarFilled v-for="i in 5" :key="i" :size="18" :fill="i <= Math.round(avgRating) ? '#FF6B35' : 'transparent'" :stroke="i <= Math.round(avgRating) ? '#FF6B35' : '#555'" />
          </div>
          <span class="ro-total">{{ reviews.length }} 条评价</span>
        </div>
        <div class="ro-bars">
          <div class="ro-bar-row" v-for="n in 5" :key="n">
            <span class="ro-label">{{ 6 - n }}星</span>
            <div class="ro-bar"><div class="ro-fill" :style="{ width: ratingDistribution[n] + '%' }"></div></div>
            <span class="ro-pct">{{ ratingDistribution[n] }}%</span>
          </div>
        </div>
      </section>

      <ReviewWall :reviews="reviews" />

      <section class="write-review">
        <button v-if="!showForm && !submitted" class="write-btn" :class="{ disabled: !isLoggedIn }" @click="handleWriteReview">
          <MessageSquarePlus :size="20" /> {{ isLoggedIn ? '我要点评' : '请先登录再点评' }}
        </button>
        <div v-if="showForm && !submitted" class="review-form" :class="{ disabled: submitting }">
          <div class="form-row">
            <div class="form-input disabled-input">
              <User :size="16" /> {{ currentUser?.username }}
            </div>
            <select v-model="newReview.store" class="form-input form-select">
              <option value="" disabled>选择要评价的店铺</option>
              <option v-for="s in stores" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
          <div class="form-row">
            <input v-model="newReview.food" placeholder="点了什么美食" class="form-input" />
          </div>
          <div class="form-stars">
            <span>评分：</span>
            <button v-for="n in 5" :key="n" class="star-btn" :disabled="submitting" @click="newReview.rating = n">
              <StarFilled :size="22" :fill="n <= newReview.rating ? '#FF6B35' : 'transparent'" :stroke="n <= newReview.rating ? '#FF6B35' : '#555'" />
            </button>
          </div>
          <textarea v-model="newReview.comment" placeholder="说说你的感受吧" class="form-textarea" rows="3"></textarea>
          <div class="form-actions">
            <button class="cancel-btn" @click="showForm = false" :disabled="submitting">取消</button>
            <button class="submit-btn" @click="submitReview" :disabled="submitting"><Send :size="16" /> {{ submitting ? '提交中...' : '提交评价' }}</button>
          </div>
        </div>
        <div v-if="submitted" class="submit-success">
          <span class="success-icon">&#10003;</span> 感谢你的评价！
        </div>
        <p v-if="!isLoggedIn && !showForm" class="login-tip">登录后才能发表评价哦</p>
      </section>
    </template>
  </div>
</template>

<style scoped>
.reviews-page { min-height: 100vh; }
.state-box { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 20px; color: #887766; gap: 12px; }
.state-box.error { color: #ef4444; }
.spin { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.page-hero { text-align: center; padding: 40px 20px; background: linear-gradient(135deg, rgba(255,107,53,0.06), transparent); }
.page-hero p { color: #a89880; font-size: 1em; }
.rating-overview { max-width: 800px; margin: 0 auto; padding: 40px 20px; display: flex; gap: 40px; align-items: center; }
.ro-stats { text-align: center; flex-shrink: 0; }
.ro-big-num { font-size: 3.5em; font-weight: 800; color: #FF6B35; line-height: 1; }
.ro-stars { display: flex; gap: 3px; justify-content: center; margin: 8px 0; }
.ro-total { color: #887766; font-size: 0.85em; }
.ro-bars { flex: 1; display: flex; flex-direction: column; gap: 6px; }
.ro-bar-row { display: flex; align-items: center; gap: 8px; }
.ro-label { color: #a89880; font-size: 0.8em; width: 30px; text-align: right; }
.ro-bar { flex: 1; height: 8px; background: rgba(255,255,255,0.06); border-radius: 4px; overflow: hidden; }
.ro-fill { height: 100%; background: #FF6B35; border-radius: 4px; }
.ro-pct { color: #887766; font-size: 0.78em; width: 36px; }

.write-review { max-width: 600px; margin: 0 auto; padding: 0 20px 80px; text-align: center; }
.login-tip { color: #665544; font-size: 0.85em; margin-top: 16px; }
.write-btn { display: inline-flex; align-items: center; gap: 8px; background: transparent; border: 1px solid rgba(255,107,53,0.4); color: #FF6B35; padding: 12px 28px; border-radius: 50px; cursor: pointer; font-size: 0.95em; transition: all 0.3s; }
.write-btn:hover { background: rgba(255,107,53,0.1); }
.write-btn.disabled { border-color: rgba(255,255,255,0.1); color: #887766; cursor: not-allowed; }
.write-btn.disabled:hover { background: transparent; }
.review-form { display: flex; flex-direction: column; gap: 14px; margin-top: 20px; }
.review-form.disabled { opacity: 0.6; pointer-events: none; }
.form-row { display: flex; gap: 14px; }
.form-input { flex: 1; padding: 12px 16px; background: rgba(26,22,18,0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #e0d6c8; font-size: 0.95em; outline: none; }
.form-input:focus { border-color: #FF6B35; }
.form-select { cursor: pointer; appearance: auto; }
.form-select option { background: #1e1a16; color: #e0d6c8; padding: 8px; }
.disabled-input { display: flex; align-items: center; gap: 8px; color: #887766; font-size: 0.9em; }
.form-stars { display: flex; align-items: center; gap: 4px; }
.form-stars span { color: #a89880; font-size: 0.9em; margin-right: 8px; }
.star-btn { background: none; border: none; cursor: pointer; padding: 0; transition: transform 0.15s; }
.star-btn:hover { transform: scale(1.15); }
.star-btn:disabled { cursor: default; }
.form-textarea { padding: 12px 16px; background: rgba(26,22,18,0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #e0d6c8; font-size: 0.95em; outline: none; resize: vertical; font-family: inherit; }
.form-textarea:focus { border-color: #FF6B35; }
.form-actions { display: flex; gap: 12px; justify-content: center; }
.cancel-btn { background: transparent; border: 1px solid rgba(255,255,255,0.1); color: #887766; padding: 10px 24px; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
.cancel-btn:hover { border-color: #ef4444; color: #ef4444; }
.cancel-btn:disabled { cursor: default; opacity: 0.5; }
.submit-btn { display: flex; align-items: center; gap: 6px; background: linear-gradient(135deg, #FF6B35, #f0932b); color: #fff; border: none; padding: 10px 24px; border-radius: 8px; cursor: pointer; font-weight: 600; transition: all 0.3s; }
.submit-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(255,107,53,0.3); }
.submit-btn:disabled { opacity: 0.6; cursor: default; transform: none; box-shadow: none; }
.submit-success { padding: 30px; color: #22c55e; font-size: 1.1em; text-align: center; }
.success-icon { font-size: 1.5em; margin-right: 6px; }

@media (max-width: 640px) {
  .rating-overview { flex-direction: column; }
  .form-row { flex-direction: column; }
  .form-select { width: 100%; }
}
</style>
