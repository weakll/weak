<script setup>
import { MapPin, Phone, Mail, Clock, Store, Star, TrendingUp, Award, Target, Heart, Briefcase, Users, Gift, Send } from '@lucide/vue'
import { ref } from 'vue'
const formData = ref({ name: '', phone: '', type: '摊位入驻', message: '' })
const submitted = ref(false)

const submitForm = async () => {
  if (!formData.value.name || !formData.value.phone) return
  try {
    await axios.post('/api/join/', formData.value)
    submitted.value = true
    formData.value = { name: '', phone: '', type: '摊位入驻', message: '' }
    setTimeout(() => { submitted.value = false }, 4000)
  } catch {
    submitted.value = false
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

const timeline = [
  { year: '2010', title: '夜市成立', desc: '十几位下岗工人与小吃摊主在钢铁大街自发聚集，形成了最初的烟火美食街雏形。' },
  { year: '2013', title: '初具规模', desc: '摊位数量增至20家，开始统一管理，成为附近居民夜间觅食的首选之地。' },
  { year: '2015', title: '规模扩大', desc: '突破30家摊位，引入规范管理，获得"包头市特色夜市"称号。' },
  { year: '2018', title: '夜经济名片', desc: '入选包头市夜经济重点项目，日均客流突破2000人，成为城市夜生活文化符号。' },
  { year: '2020', title: '品牌升级', desc: '统一招牌设计和卫生标准，新增公共就餐区，日均客流突破3000人。' },
  { year: '2023', title: '全新面貌', desc: '摊位总数突破50家，引入线上点单系统，与多家旅游平台达成合作。' },
  { year: '2026', title: '持续精彩', desc: '被评为包头市夜经济示范街区，月均客流超15万人次。' },
]

const partners = [
  '包头市旅游局', '昆都仑区管委会', '内蒙古美食协会',
  '大众点评', '美团外卖', '滴滴出行', '抖音生活服务'
]

const stats = [
  { icon: Store, value: '50+', label: '特色摊位' },
  { icon: Star, value: '15年', label: '经营历史' },
  { icon: TrendingUp, value: '5K+', label: '日均客流' },
  { icon: Award, value: '示范区', label: '官方认证' },
]
</script>

<template>
  <div class="about-page">
    <div class="page-top-spacer"></div>
    <section class="about-hero">
      <h1>关于烟火美食街</h1>
      <p class="about-sub">始于2010年 · 包头最富烟火气的夜市美食街</p>
      <div class="hero-stats">
        <div class="hero-stat" v-for="s in stats" :key="s.label">
          <component :is="s.icon" :size="22" />
          <strong>{{ s.value }}</strong>
          <span>{{ s.label }}</span>
        </div>
      </div>
    </section>

    <section class="about-content">
      <div class="about-card">
        <h3><span class="card-icon">&#127753;</span> 我们的故事</h3>
        <p>烟火美食街成立于2010年，从最初十几个路边摊发展到如今汇聚50多家特色美食的大型夜市。我们坚持"地道、新鲜、实惠"的理念，为食客们提供最正宗的各地小吃。每一串羊肉、每一碗冰沙、每一口臭豆腐，承载的都是包头这座城市最真实的味道。</p>
        <p>每年接待超过150万人次食客，从本地老饕到外地游客，从深夜加班族到周末聚会团，烟火美食街早已成为包头的城市名片。</p>
      </div>
      <div class="about-card">
        <h3><span class="card-icon">&#127919;</span> 我们的使命</h3>
        <p>让每一位来到烟火美食街的食客都能找到属于自己的那一味。我们不仅是美食的聚集地，更是城市夜生活的文化符号、无数人深夜觅食的情感寄托。</p>
        <p><strong>核心理念：</strong>地道食材、明码标价、卫生安全、热情服务。每一口食物都承载着摊主的匠心与诚意。</p>
      </div>
    </section>

    <section class="timeline-section">
      <h2 class="section-title"><TrendingUp :size="24" /> 发展历程</h2>
      <div class="timeline">
        <div class="tl-item" v-for="(t, i) in timeline" :key="t.year">
          <div class="tl-year">{{ t.year }}</div>
          <div class="tl-dot"></div>
          <div class="tl-body">
            <h3>{{ t.title }} <span v-if="i === 0" class="tl-badge">起点</span><span v-if="i === timeline.length - 1" class="tl-badge now">现在</span></h3>
            <p>{{ t.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="partners-section">
      <h2 class="section-title"><Heart :size="24" /> 合作伙伴</h2>
      <p class="section-desc">感谢以下机构与企业对烟火美食街的长期支持</p>
      <div class="partners-grid">
        <span class="partner-tag" v-for="p in partners" :key="p">{{ p }}</span>
      </div>
    </section>


    <section class="join-section">
      <h2 class="section-title"><Users :size="24" /> 加入我们</h2>
      <p class="section-desc">和我们一起，点燃这座城市的烟火气</p>
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
          <h3>&#128293; 配套设施</h3>
          <p>统一供水供电、垃圾处理、公共就餐区、安保监控全覆盖</p>
        </div>
      </div>

      <h2 class="section-title" style="margin-top:56px"><Briefcase :size="24" /> 招贤纳士</h2>
      <div class="jobs-grid">
        <div class="job-card" v-for="job in jobList" :key="job.title">
          <div class="job-header">
            <h3>{{ job.title }}</h3>
            <span class="job-salary">{{ job.salary }}</span>
          </div>
          <p class="job-dept"><Briefcase :size="14" /> {{ job.dept }}</p>
          <p class="job-desc">{{ job.desc }}</p>
          <div class="job-tags"><span v-for="t in job.tags" :key="t" class="job-tag">{{ t }}</span></div>
        </div>
      </div>

      <div class="benefits-grid">
        <div class="benefit-card" v-for="b in benefits" :key="b.title">
          <component :is="b.icon" :size="28" class="benefit-icon" />
          <h4>{{ b.title }}</h4>
          <p>{{ b.desc }}</p>
        </div>
      </div>

      <h2 class="section-title" style="margin-top:56px"><Store :size="24" /> 摊位入驻 / 求职申请</h2>
      <p class="section-desc">留下联系方式，我们会在24小时内联系您</p>
      <div class="apply-form" v-if="!submitted">
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
        <button class="form-btn" @click="submitForm"><Send :size="18" /> 提交申请</button>
      </div>
      <div v-else class="apply-success">
        <span class="success-icon">&#10003;</span>
        <h3>提交成功！</h3>
        <p>我们会在24小时内与您联系，请保持电话畅通。</p>
      </div>
    </section>
    <section class="contact-section">
      <h2 class="section-title"><MapPin :size="24" /> 联系我们</h2>
      <div class="contact-card">
        <div class="contact-row"><MapPin :size="18" /> <span>内蒙古包头市昆都仑区钢铁大街包百美食街</span></div>
        <div class="contact-row"><Phone :size="18" /> <span>0472-8888666</span></div>
        <div class="contact-row"><Mail :size="18" /> <span>contact@yanhuo-foodstreet.com</span></div>
        <div class="contact-row"><Clock :size="18" /> <span>每晚 17:00 – 凌晨 02:00（节假日照常营业）</span></div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.about-page { min-height: 100vh; }
.page-top-spacer { height: 80px; }
.about-hero { text-align: center; padding: 40px 20px 48px; background: linear-gradient(135deg, rgba(255,107,53,0.1), rgba(255,107,53,0.02), transparent); }
.about-hero h1 { font-size: 2.4em; font-weight: 800; color: #FF6B35; margin: 0 0 8px; letter-spacing: 4px; }
.about-sub { color: #a89880; font-size: 1.1em; }
.hero-stats { display: flex; justify-content: center; gap: 48px; margin-top: 36px; flex-wrap: wrap; }
.hero-stat { display: flex; flex-direction: column; align-items: center; gap: 6px; color: #FF6B35; }
.hero-stat strong { font-size: 1.8em; color: #e0d6c8; font-weight: 800; }
.hero-stat span { font-size: 0.82em; color: #887766; }

.section-title { font-size: 1.6em; font-weight: 800; color: #e0d6c8; display: flex; align-items: center; justify-content: center; gap: 10px; margin: 0 0 12px; }
.section-desc { color: #887766; font-size: 0.9em; text-align: center; }

.about-content { max-width: 900px; margin: 0 auto; padding: 40px 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.about-card { background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.04); border-radius: 14px; padding: 32px; transition: border-color 0.3s; }
.about-card:hover { border-color: rgba(255,107,53,0.15); }
.about-card h3 { color: #FF6B35; font-size: 1.2em; margin: 0 0 14px; display: flex; align-items: center; gap: 8px; }
.card-icon { font-size: 1.2em; }
.about-card p { color: #a89880; font-size: 0.93em; margin: 0 0 10px; line-height: 1.7; }
.about-card p:last-child { margin-bottom: 0; }

.timeline-section { max-width: 700px; margin: 0 auto; padding: 60px 20px; }
.timeline { position: relative; padding-left: 100px; margin-top: 36px; }
.timeline::before { content: ''; position: absolute; left: 72px; top: 0; bottom: 0; width: 2px; background: rgba(255,107,53,0.2); }
.tl-item { position: relative; margin-bottom: 32px; }
.tl-year { position: absolute; left: -94px; top: -2px; font-size: 1.2em; font-weight: 800; color: #FF6B35; width: 60px; text-align: right; }
.tl-dot { position: absolute; left: -23px; top: 4px; width: 14px; height: 14px; border-radius: 50%; background: #FF6B35; box-shadow: 0 0 12px rgba(255,107,53,0.5); border: 3px solid #14120e; }
.tl-body h3 { color: #e0d6c8; font-size: 1.05em; margin: 0 0 6px; display: flex; align-items: center; gap: 8px; }
.tl-badge { background: rgba(255,107,53,0.15); color: #FF6B35; padding: 1px 8px; border-radius: 8px; font-size: 0.7em; font-weight: 600; }
.tl-badge.now { background: rgba(34,197,94,0.15); color: #22c55e; }
.tl-body p { color: #a89880; font-size: 0.88em; margin: 0; line-height: 1.6; }

.partners-section { max-width: 800px; margin: 0 auto; padding: 60px 20px; }
.partners-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin-top: 24px; }
.partner-tag { background: rgba(255,107,53,0.06); border: 1px solid rgba(255,107,53,0.2); color: #c0a880; padding: 10px 24px; border-radius: 8px; font-size: 0.9em; transition: all 0.25s; cursor: default; }
.partner-tag:hover { background: rgba(255,107,53,0.15); color: #FF6B35; }

.contact-section { max-width: 800px; margin: 0 auto; padding: 40px 20px 80px; }
.contact-card { background: rgba(26,22,18,0.6); border: 1px solid rgba(255,107,53,0.12); border-radius: 14px; padding: 28px 36px; text-align: left; max-width: 500px; margin: 24px auto 0; }
.contact-row { display: flex; align-items: center; gap: 12px; color: #c0a880; font-size: 0.92em; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.contact-row:last-child { border-bottom: none; }
.contact-row svg { color: #FF6B35; flex-shrink: 0; }

@media (max-width: 768px) {
  .about-content { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .hero-stats { gap: 24px; }
  .hero-stat strong { font-size: 1.4em; }
  .timeline { padding-left: 70px; }
  .timeline::before { left: 52px; }
  .tl-year { left: -64px; width: 50px; text-align: right; font-size: 1em; }
  .tl-dot { left: -11px; }
  .about-hero h1 { font-size: 1.8em; }
  .contact-card { padding: 22px 24px; }
}

.join-section { max-width: 1100px; margin: 0 auto; padding: 60px 20px; }
.reasons-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 28px; }
.reason-card { background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; padding: 28px; transition: all 0.3s; }
.reason-card:hover { border-color: rgba(255,107,53,0.2); transform: translateY(-2px); }
.reason-card h3 { color: #e0d6c8; font-size: 1.1em; margin: 0 0 8px; }
.reason-card p { color: #a89880; font-size: 0.9em; margin: 0; line-height: 1.6; }
.jobs-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 28px; }
.job-card { background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; padding: 24px; transition: all 0.3s; }
.job-card:hover { border-color: rgba(255,107,53,0.2); }
.job-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.job-header h3 { color: #e0d6c8; font-size: 1.05em; margin: 0; }
.job-salary { color: #FF6B35; font-weight: 700; font-size: 0.9em; }
.job-dept { display: flex; align-items: center; gap: 6px; color: #887766; font-size: 0.8em; margin: 0 0 8px; }
.job-desc { color: #a89880; font-size: 0.85em; margin: 0 0 12px; line-height: 1.5; }
.job-tags { display: flex; gap: 8px; }
.job-tag { background: rgba(255,107,53,0.1); color: #FF6B35; padding: 2px 10px; border-radius: 10px; font-size: 0.75em; }
.benefits-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 28px; }
.benefit-card { text-align: center; background: rgba(26,22,18,0.4); border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; padding: 28px 20px; }
.benefit-icon { color: #FF6B35; margin-bottom: 12px; }
.benefit-card h4 { color: #e0d6c8; font-size: 1em; margin: 0 0 6px; }
.benefit-card p { color: #a89880; font-size: 0.85em; margin: 0; }
.apply-form { display: flex; flex-direction: column; gap: 14px; margin-top: 28px; }
.form-row { display: flex; gap: 14px; }
.form-input { flex: 1; padding: 12px 16px; background: rgba(26,22,18,0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #e0d6c8; font-size: 0.95em; outline: none; transition: border-color 0.2s; }
.form-input:focus { border-color: #FF6B35; }
.form-textarea { padding: 12px 16px; background: rgba(26,22,18,0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #e0d6c8; font-size: 0.95em; outline: none; resize: vertical; font-family: inherit; }
.form-textarea:focus { border-color: #FF6B35; }
.form-btn { display: flex; align-items: center; justify-content: center; gap: 8px; background: linear-gradient(135deg, #FF6B35, #f0932b); color: #fff; border: none; border-radius: 50px; padding: 14px 32px; font-size: 1em; font-weight: 600; cursor: pointer; transition: all 0.3s; align-self: center; box-shadow: 0 4px 16px rgba(255,107,53,0.3); }
.form-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 24px rgba(255,107,53,0.5); }
.apply-success { text-align: center; padding: 60px 0; }
.apply-success .success-icon { font-size: 3em; color: #22c55e; }
.apply-success h3 { color: #e0d6c8; margin: 16px 0 8px; }
.apply-success p { color: #a89880; }
</style>