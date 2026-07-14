<script setup>
import { ref, watch, onMounted } from 'vue'
import { Store, ShoppingBag, MessageSquareText, Plus, Pencil, Trash2, Save, X, LoaderCircle, Star, ExternalLink, LogOut } from '@lucide/vue'
import api from "../api"
import { useAuth } from '../composables/useAuth.js'

const { isLoggedIn, currentUser, openAuthModal } = useAuth()

const activeTab = ref('store')
const loading = ref(true)
const error = ref('')
const saved = ref('')

const store = ref(null)
const storeForm = ref({})
const editing = ref(false)

const products = ref([])
const storeReviews = ref([])
const showProductForm = ref(false)
const editingProduct = ref(null)
const productForm = ref({ name: '', description: '', price: '', is_recommended: false, spicy_level: 0, is_vegetarian: false })

onMounted(async () => {
  if (!isLoggedIn.value) { openAuthModal(); return }
  await loadData()
})

watch(isLoggedIn, async (val) => {
  if (val) { await loadData() }
})

const loadData = async () => {
  loading.value = true
  error.value = ''
  try {
    const [storeRes, prodRes] = await Promise.all([
      api.get('/merchant/profile/'),
      api.get('/merchant/products/'),
    ])
    store.value = storeRes.data
    storeForm.value = { ...storeRes.data }
    products.value = prodRes.data
    try {
      const { data: revData } = await api.get('/reviews/', { params: { store_id: store.value.id } })
      storeReviews.value = Array.isArray(revData) ? revData : []
      await loadReviews()
  } catch {}
  } catch (e) {
    if (e.response?.status === 403) {
      error.value = '您的商家账号未激活或未分配店铺，请联系管理员。'
    } else {
      error.value = '加载数据失败'
    }
  } finally {
    loading.value = false
  }
}

const saveStore = async () => {
  try {
    const { data } = await api.put('/merchant/profile/', storeForm.value)
    store.value = data
    editing.value = false
    saved.value = '店铺信息已保存'
    setTimeout(() => saved.value = '', 3000)
  } catch { error.value = '保存失败' }
}

const startAddProduct = () => {
  editingProduct.value = null
  productForm.value = { name: '', description: '', price: '', is_recommended: false, spicy_level: 0, is_vegetarian: false }
  showProductForm.value = true
}

const startEditProduct = (p) => {
  editingProduct.value = p.id
  productForm.value = { ...p }
  showProductForm.value = true
}

const saveProduct = async () => {
  try {
    if (editingProduct.value) {
      await api.put(`/api/merchant/products/${editingProduct.value}/`, productForm.value)
    } else {
      await api.post('/merchant/products/', productForm.value)
    }
    showProductForm.value = false
    editingProduct.value = null
    const { data } = await api.get('/merchant/products/')
    products.value = data
    saved.value = '商品已保存'
    setTimeout(() => saved.value = '', 3000)
  } catch { error.value = '保存商品失败' }
}


const loadReviews = async () => {
  if (!store.value?.id) return
  try {
    const { data } = await api.get('/reviews/', { params: { store_id: store.value.id } })
    storeReviews.value = Array.isArray(data) ? data : []
  } catch {}
}
const deleteProduct = async (id) => {
  if (!confirm('确定删除该商品？')) return
  try {
    await api.delete(`/api/merchant/products/${id}/`)
    products.value = products.value.filter(p => p.id !== id)
    saved.value = '商品已删除'
    setTimeout(() => saved.value = '', 3000)
  } catch { error.value = '删除失败' }
}
</script>

<template>
  <div class="merchant-page">
    <div class="page-top-spacer"></div>

    <section class="page-hero">
      <h1><Store :size="28" /> 商家中心</h1>
      <p>管理你的店铺信息和商品</p>
    </section>

    <div v-if="!isLoggedIn" class="state-box"><p>请先登录</p></div>
    <div v-else-if="loading" class="state-box"><LoaderCircle :size="32" class="spin" /><p>加载中...</p></div>
    <div v-else-if="error" class="state-box error"><p>{{ error }}</p></div>
    <div v-else-if="store" class="dashboard">
      <div class="tab-bar">
        <button :class="{ active: activeTab === 'store' }" @click="activeTab = 'store'"><Store :size="16" /> 店铺信息</button>
        <button :class="{ active: activeTab === 'products' }" @click="activeTab = 'products'"><ShoppingBag :size="16" /> 商品管理</button>
        <button :class="{ active: activeTab === 'reviews' }" @click="activeTab = 'reviews'"><MessageSquareText :size="16" /> 评价查看</button>
      </div>

      <div v-if="saved" class="saved-msg">{{ saved }}</div>

      <div v-if="activeTab === 'store'" class="tab-content">
        <div class="section-header">
          <h2>店铺信息</h2>
          <button v-if="!editing" class="action-btn" @click="editing = true"><Pencil :size="14" /> 编辑</button>
        </div>
        <div class="info-grid" v-if="!editing">
          <div class="info-item"><label>店铺名称</label><span>{{ store.name }}</span></div>
          <div class="info-item"><label>分类</label><span>{{ store.category }}</span></div>
          <div class="info-item"><label>描述</label><span>{{ store.description }}</span></div>
          <div class="info-item"><label>地址</label><span>{{ store.address }}</span></div>
          <div class="info-item"><label>营业时间</label><span>{{ store.opening_hours }}</span></div>
          <div class="info-item"><label>联系电话</label><span>{{ store.phone }}</span></div>
        </div>
        <div v-else class="edit-form">
          <div class="form-row">
            <label>店铺名称</label><input v-model="storeForm.name" class="form-input" />
          </div>
          <div class="form-row">
            <label>描述</label><textarea v-model="storeForm.description" class="form-textarea" rows="3"></textarea>
          </div>
          <div class="form-row">
            <label>地址</label><input v-model="storeForm.address" class="form-input" />
          </div>
          <div class="form-row">
            <label>营业时间</label><input v-model="storeForm.opening_hours" class="form-input" />
          </div>
          <div class="form-row">
            <label>联系电话</label><input v-model="storeForm.phone" class="form-input" />
          </div>
          <div class="form-actions">
            <button class="cancel-btn" @click="editing = false"><X :size="14" /> 取消</button>
            <button class="save-btn" @click="saveStore"><Save :size="14" /> 保存</button>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'products'" class="tab-content">
        <div class="section-header">
          <h2>商品列表 ({{ products.length }})</h2>
          <button class="action-btn" @click="startAddProduct"><Plus :size="14" /> 添加商品</button>
        </div>
        <div v-if="showProductForm" class="edit-form">
          <div class="form-row"><label>商品名</label><input v-model="productForm.name" class="form-input" /></div>
          <div class="form-row"><label>描述</label><textarea v-model="productForm.description" class="form-textarea" rows="2"></textarea></div>
          <div class="form-row"><label>价格</label><input v-model="productForm.price" class="form-input" placeholder="¥15/份" /></div>
          <div class="form-row"><label>图片URL</label><input v-model="productForm.image_url" class="form-input" placeholder="输入图片链接地址" /></div>
          <div class="form-row checkbox-row">
            <label><input type="checkbox" v-model="productForm.is_recommended" /> 招牌推荐</label>
            <label><input type="checkbox" v-model="productForm.is_vegetarian" /> 素食</label>
          </div>
          <div class="form-row"><label>辣度 (0-3)</label><input v-model.number="productForm.spicy_level" type="number" min="0" max="3" class="form-input short" /></div>
          <div class="form-actions">
            <button class="cancel-btn" @click="showProductForm = false"><X :size="14" /> 取消</button>
            <button class="save-btn" @click="saveProduct"><Save :size="14" /> 保存</button>
          </div>
        </div>
        <div class="product-list" v-if="products.length">
          <div class="prod-card" v-for="p in products" :key="p.id">
            <img v-if="p.image_url" :src="p.image_url" :alt="p.name" class="prod-thumb" @error="p.image_url = null" />
            <div class="prod-info">
              <h4>{{ p.name }} <span v-if="p.is_recommended" class="tag">招牌</span></h4>
              <p>{{ p.description }}</p>
              <span class="prod-price">{{ p.price }}</span>
            </div>
            <div class="prod-actions">
              <button class="icon-btn" @click="startEditProduct(p)" title="编辑"><Pencil :size="14" /></button>
              <button class="icon-btn danger" @click="deleteProduct(p.id)" title="删除"><Trash2 :size="14" /></button>
            </div>
          </div>
        </div>
        <div v-else class="empty-hint">还没有添加商品，点击上方添加</div>
      </div>

      <div v-if="activeTab === 'reviews'" class="tab-content">
        <div class="section-header"><h2>顾客评价</h2></div>
        <p class="section-desc">这里是顾客对您店铺的评价，你可以在前台店铺详情页查看完整内容。</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.merchant-page { min-height: 100vh; max-width: 900px; margin: 0 auto; padding: 0 20px 80px; }
.page-top-spacer { height: 80px; }
.page-hero { text-align: center; padding: 40px 20px; }
.hero-row { display: flex; align-items: center; justify-content: center; gap: 16px; flex-wrap: wrap; }
.view-store-link { display: inline-flex; align-items: center; gap: 4px; background: rgba(255,107,53,0.1); border: 1px solid rgba(255,107,53,0.25); color: #FF6B35; padding: 5px 14px; border-radius: 20px; font-size: 0.78em; text-decoration: none; transition: all 0.2s; }
.view-store-link:hover { background: rgba(255,107,53,0.2); }
.page-hero h1 { font-size: 2em; font-weight: 800; color: #FF6B35; display: flex; align-items: center; justify-content: center; gap: 10px; margin: 0 0 6px; }
.page-hero p { color: #a89880; }
.state-box { display: flex; flex-direction: column; align-items: center; padding: 80px 20px; color: #887766; gap: 12px; }
.state-box.error { color: #ef4444; }
.spin { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.tab-bar { display: flex; gap: 4px; margin-bottom: 24px; background: rgba(26,22,18,0.6); border-radius: 10px; padding: 4px; }
.tab-bar button { flex: 1; padding: 10px; background: none; border: none; color: #887766; border-radius: 8px; cursor: pointer; font-size: 0.85em; display: flex; align-items: center; justify-content: center; gap: 6px; transition: all 0.2s; }
.tab-bar button.active { background: rgba(255,107,53,0.15); color: #FF6B35; }
.tab-bar button:hover:not(.active) { color: #c0a880; }

.saved-msg { text-align: center; color: #22c55e; padding: 8px; font-size: 0.85em; margin-bottom: 12px; background: rgba(34,197,94,0.1); border-radius: 8px; }
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
.section-header h2 { color: #e0d6c8; font-size: 1.3em; font-weight: 700; margin: 0; }
.action-btn { display: inline-flex; align-items: center; gap: 4px; background: rgba(255,107,53,0.12); border: 1px solid rgba(255,107,53,0.3); color: #FF6B35; padding: 6px 14px; border-radius: 8px; cursor: pointer; font-size: 0.8em; transition: all 0.2s; }
.action-btn:hover { background: rgba(255,107,53,0.2); }

.info-grid { display: grid; gap: 14px; }
.info-item { display: flex; gap: 16px; padding: 14px 18px; background: rgba(26,22,18,0.4); border: 1px solid rgba(255,255,255,0.04); border-radius: 10px; }
.info-item label { color: #887766; font-size: 0.82em; min-width: 70px; flex-shrink: 0; }
.info-item span { color: #e0d6c8; font-size: 0.9em; }

.edit-form { background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 20px; display: flex; flex-direction: column; gap: 14px; }
.form-row { display: flex; flex-direction: column; gap: 4px; }
.form-row label { color: #a89880; font-size: 0.82em; }
.form-input { padding: 10px 14px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #e0d6c8; font-size: 0.9em; outline: none; }
.form-input:focus { border-color: #FF6B35; }
.form-input.short { max-width: 100px; }
.form-textarea { padding: 10px 14px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #e0d6c8; font-size: 0.9em; outline: none; resize: vertical; font-family: inherit; }
.form-textarea:focus { border-color: #FF6B35; }
.checkbox-row { flex-direction: row; gap: 20px; }
.checkbox-row label { display: flex; align-items: center; gap: 6px; color: #e0d6c8; font-size: 0.85em; cursor: pointer; }
.form-actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 4px; }
.cancel-btn { background: transparent; border: 1px solid rgba(255,255,255,0.1); color: #887766; padding: 8px 18px; border-radius: 8px; cursor: pointer; font-size: 0.85em; display: flex; align-items: center; gap: 4px; }
.cancel-btn:hover { border-color: #ef4444; color: #ef4444; }
.save-btn { background: linear-gradient(135deg, #FF6B35, #f0932b); color: #fff; border: none; padding: 8px 18px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.85em; display: flex; align-items: center; gap: 4px; }

.product-list { display: flex; flex-direction: column; gap: 10px; }
.prod-card { display: flex; align-items: center; justify-content: space-between; background: rgba(26,22,18,0.4); border: 1px solid rgba(255,255,255,0.04); border-radius: 10px; padding: 14px 18px; }
.prod-info h4 { color: #e0d6c8; font-size: 0.95em; margin: 0 0 4px; display: flex; align-items: center; gap: 6px; }
.tag { background: #FF6B35; color: #fff; font-size: 0.6em; padding: 1px 6px; border-radius: 4px; font-weight: 600; }
.prod-info p { color: #a89880; font-size: 0.8em; margin: 0 0 4px; }
.prod-price { color: #FF6B35; font-weight: 600; font-size: 0.85em; white-space: nowrap; }
.prod-actions { display: flex; gap: 6px; align-items: center; }
.prod-thumb { width: 60px; height: 60px; object-fit: cover; border-radius: 8px; flex-shrink: 0; }
.icon-btn { background: none; border: 1px solid rgba(255,255,255,0.08); color: #887766; border-radius: 6px; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; }
.icon-btn:hover { border-color: #FF6B35; color: #FF6B35; }
.icon-btn.danger:hover { border-color: #ef4444; color: #ef4444; }
.empty-hint { text-align: center; padding: 40px 0; color: #665544; font-size: 0.9em; }
.section-desc { color: #887766; font-size: 0.85em; text-align: center; }
.review-list { display: flex; flex-direction: column; gap: 10px; }
.review-card { background: rgba(26,22,18,0.4); border: 1px solid rgba(255,255,255,0.04); border-radius: 10px; padding: 14px 16px; }
.review-head { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.review-avatar { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,107,53,0.25); color: #FF6B35; display: flex; align-items: center; justify-content: center; font-size: 0.85em; font-weight: 700; flex-shrink: 0; }
.review-name { color: #e0d6c8; font-size: 0.85em; font-weight: 600; }
.review-stars { display: flex; gap: 1px; margin-top: 2px; }
.review-food { color: #FF6B35; font-size: 0.78em; margin: 0 0 6px; }
.review-comment { color: #a89880; font-size: 0.82em; margin: 0; line-height: 1.5; }
</style>



