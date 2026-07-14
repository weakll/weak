<script setup>
import { ref } from 'vue'
import { Briefcase, Store, Mail, Users, Gift, Star, Send } from '@lucide/vue'

const formData = ref({ name: '', phone: '', type: '摊位入驻', message: '' })
const submitted = ref(false)
const submitting = ref(false)
const formError = ref('')

const submitForm = async () => {
  if (!formData.value.name || !formData.value.phone) {
    formError.value = '请填写姓名和联系电话'
    return
  }
  formError.value = ''
  submitting.value = true
  try {
    const res = await fetch('/api/join/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: formData.value.name,
        phone: formData.value.phone,
        application_type: formData.value.type,
        message: formData.value.message,
      }),
    })
    const data = await res.json()
    if (data.success) {
      submitted.value = true
      formData.value = { name: '', phone: '', type: '摊位入驻', message: '' }
      setTimeout(() => { submitted.value = false }, 4000)
    } else {
      formError.value = data.message || '提交失败，请稍后重试'
    }
  } catch {
    formError.value = '网络错误，请稍后重试'
  } finally {
    submitting.value = false
  }
}

const jobList = [
  { title: '夜市运营经理', dept: '运营部', salary: '8K-12K', desc: '负责夜市日常运营管理，协调摊位商家，处理突发事件。', tags: ['全职', '3年经验'] },
  { title: '市场营销专员', dept: '市场部', salary: '6K-9K', desc: '策划并执行夜市线上线下推广活动，管理社交媒体账号。', tags: ['全职', '1年经验'] },
  { title: '兼职安保人员', dept: '安保部', salary: '时薪25元', desc: '夜市营业期间维护现场秩序，协助疏导人流。', tags: ['兼职', '无经验可'] },
]

const benefits = [
  { icon: Gift, title: '员工福利', desc: '免费工作餐、节日礼包、年度旅游' },
  { icon: Star, title: '晋升空间', desc: '完善的晋升体系，优秀者可升管理岗' },
  { icon: Users, title: '团队氛围', desc: '年轻活力的团队，定期团建活动' },
]

const stallTypes = ['摊位入驻', '求职应聘', '商务合作', '其他咨询']
</script>
<template>
  <div class="join-page">
    <div class="page-top-spacer"></div>

    <section class="join-hero">
      <h1>加入烟火美食街</h1>
      <p>和我们一起，点燃这座城市的烟火气</p>
    </section>

    <section class="join-reasons">
      <h2 class="section-title">为什么选择我们</h2>
      <div class="reasons-grid">
        <div class="reason-card">
          <h3>&#127881; 超高客流</h3>
          <p>日均客流量5000+，周末破万，摊位商业价值持续增长</p>
        </div>
        <div class="reason-card">
          <h3>&#128176; 低成本入驻</h3>
          <p>灵活的摊位租赁方案，月租低至2000元起，零转让费</p>
        </div>
        <div class="reason-card">
          <h3>&#128240; 流量扶持</h3>
          <p>官方账号矩阵推广，新摊位首月额外曝光资源倾斜</p>
        </div>
        <div class="reason-card">
          <h3>&#128293; 完善的配套设施</h3>
          <p>统一供水供电、垃圾处理、公共就餐区、安保监控全覆盖</p>
        </div>
      </div>
    </section>

    <section class="jobs-section">
      <h2 class="section-title">招贤纳士</h2>
      <p class="section-desc">寻找热爱美食、热爱烟火气的你</p>
      <div class="jobs-grid">
        <div class="job-card" v-for="job in jobList" :key="job.title">
          <div class="job-header">
            <h3>{{ job.title }}</h3>
            <span class="job-salary">{{ job.salary }}</span>
          </div>
          <p class="job-dept"><Briefcase :size="14" /> {{ job.dept }}</p>
          <p class="job-desc">{{ job.desc }}</p>
          <div class="job-tags">
            <span v-for="t in job.tags" :key="t" class="job-tag">{{ t }}</span>
          </div>
        </div>
      </div>

      <h2 class="section-title" style="margin-top:60px">员工福利</h2>
      <div class="benefits-grid">
        <div class="benefit-card" v-for="b in benefits" :key="b.title">
          <component :is="b.icon" :size="28" class="benefit-icon" />
          <h4>{{ b.title }}</h4>
          <p>{{ b.desc }}</p>
        </div>
      </div>
    </section>

    <section class="apply-section">
      <h2 class="section-title">摊位入驻 / 求职申请</h2>
      <p class="section-desc">留下联系方式，我们会在24小时内联系您</p>
      <div class="apply-form" v-if="!submitted">
        <p v-if="formError" class="form-error">{{ formError }}</p>
        <div class="form-row">
          <input v-model="formData.name" placeholder="您的姓名 / 品牌名称" class="form-input" />
          <input v-model="formData.phone" placeholder="联系电话" class="form-input" />
        </div>
        <div class="form-row">
          <select v-model="formData.type" class="form-input">
            <option v-for="t in stallTypes" :key="t" :value="t">{{ t }}</option>
          </select>
        </div>
        <textarea v-model="formData.message" placeholder="留言（可选）：简单介绍您的菜品或经验" class="form-textarea" rows="3"></textarea>
        <button class="form-btn" @click="submitForm" :disabled="submitting">
          <Send :size="18" /> {{ submitting ? '提交中...' : '提交申请' }}
        </button>
      </div>
      <div v-else class="apply-success">
        <span class="success-icon">&#10003;</span>
        <h3>提交成功！</h3>
        <p>我们会在24小时内与您联系，请保持电话畅通。</p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.join-page { min-height: 100vh; }
.page-top-spacer { height: 80px; }

.join-hero {
  text-align: center; padding: 60px 20px;
  background: linear-gradient(135deg, rgba(255,107,53,0.08), transparent);
}
.join-hero h1 { font-size: 2.6em; font-weight: 800; color: #FF6B35; margin: 0 0 8px; letter-spacing: 3px; }
.join-hero p { color: #a89880; font-size: 1.1em; }

.join-reasons, .jobs-section { max-width: 1100px; margin: 0 auto; padding: 60px 20px; }
.section-title { font-size: 2em; font-weight: 800; color: #FF6B35; text-align: center; margin: 0 0 8px; }
.section-desc { color: #a89880; font-size: 1em; text-align: center; margin-bottom: 32px; }

.reasons-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 32px; }
.reason-card {
  background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.04);
  border-radius: 12px; padding: 28px; transition: all 0.3s;
}
.reason-card:hover { border-color: rgba(255,107,53,0.2); transform: translateY(-2px); }
.reason-card h3 { color: #e0d6c8; font-size: 1.1em; margin: 0 0 8px; }
.reason-card p { color: #a89880; font-size: 0.9em; margin: 0; line-height: 1.6; }

.jobs-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; margin-top: 32px; }
.job-card {
  background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.04);
  border-radius: 12px; padding: 24px; transition: all 0.3s;
}
.job-card:hover { border-color: rgba(255,107,53,0.2); }
.job-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.job-header h3 { color: #e0d6c8; font-size: 1.05em; margin: 0; }
.job-salary { color: #FF6B35; font-weight: 700; font-size: 0.9em; }
.job-dept { display: flex; align-items: center; gap: 6px; color: #887766; font-size: 0.8em; margin: 0 0 8px; }
.job-desc { color: #a89880; font-size: 0.85em; margin: 0 0 12px; line-height: 1.5; }
.job-tags { display: flex; gap: 8px; }
.job-tag { background: rgba(255,107,53,0.1); color: #FF6B35; padding: 2px 10px; border-radius: 10px; font-size: 0.75em; }

.benefits-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 32px; }
.benefit-card { text-align: center; background: rgba(26,22,18,0.4); border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; padding: 28px 20px; }
.benefit-icon { color: #FF6B35; margin-bottom: 12px; }
.benefit-card h4 { color: #e0d6c8; font-size: 1em; margin: 0 0 6px; }
.benefit-card p { color: #a89880; font-size: 0.85em; margin: 0; }

.apply-section { max-width: 700px; margin: 0 auto; padding: 60px 20px 80px; }
.apply-form { display: flex; flex-direction: column; gap: 14px; margin-top: 32px; }
.form-error { color: #ef4444; font-size: 0.85em; text-align: center; margin: 0; }
.form-row { display: flex; gap: 14px; }
.form-input {
  flex: 1; padding: 12px 16px; background: rgba(26,22,18,0.8); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px; color: #e0d6c8; font-size: 0.95em; outline: none;
  transition: border-color 0.2s;
}
.form-input:focus { border-color: #FF6B35; }
.form-textarea {
  padding: 12px 16px; background: rgba(26,22,18,0.8); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px; color: #e0d6c8; font-size: 0.95em; outline: none; resize: vertical;
  font-family: inherit;
}
.form-textarea:focus { border-color: #FF6B35; }
.form-btn {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  background: linear-gradient(135deg, #FF6B35, #f0932b); color: #fff;
  border: none; border-radius: 50px; padding: 14px 32px; font-size: 1em;
  font-weight: 600; cursor: pointer; transition: all 0.3s; align-self: center;
  box-shadow: 0 4px 16px rgba(255,107,53,0.3);
}
.form-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 24px rgba(255,107,53,0.5); }
.form-btn:disabled { opacity: 0.6; cursor: default; transform: none; box-shadow: none; }

.apply-success { text-align: center; padding: 60px 0; }
.success-icon { font-size: 3em; color: #22c55e; }
.apply-success h3 { color: #e0d6c8; margin: 16px 0 8px; }
.apply-success p { color: #a89880; }

@media (max-width: 768px) {
  .reasons-grid, .benefits-grid { grid-template-columns: 1fr; }
  .form-row { flex-direction: column; }
  .join-hero h1 { font-size: 1.8em; }
}
@media (max-width: 640px) { .jobs-grid { grid-template-columns: 1fr; } }
</style>
