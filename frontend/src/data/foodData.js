export const stalls = [
  { id: 1, name: '老李炭烤羊肉串', slug: 'lao-li-yang-rou-chuan', category: "肉类", description: "秘制孜然，炭火现烤，肥瘦相间。", price: "¥15/5串", image: "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=400&h=300&fit=crop", spicy: true, vegetarian: false, popularity: 92, waiting: "约5分钟", lat: 40.6573, lng: 109.8408 },
  { id: 2, name: '阿婆臭豆腐', slug: 'a-po-chou-dou-fu', category: "素食", description: "外酥里嫩，秘制酱料，闻着臭吃着香。", price: "¥10/份", image: "https://images.unsplash.com/photo-1625220194771-7ebdea0b70b9?w=400&h=300&fit=crop", spicy: true, vegetarian: true, popularity: 88, waiting: "约3分钟", lat: 40.6571, lng: 109.8410 },
  { id: 3, name: '台湾蚵仔煎', slug: 'tai-wan-e-a-jian', category: "海鲜", description: "新鲜牡蛎搭配鸡蛋青菜，地道台湾味。", price: "¥18/份", image: "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=400&h=300&fit=crop", spicy: false, vegetarian: false, popularity: 85, waiting: "约8分钟", lat: 40.6574, lng: 109.8411 },
  { id: 4, name: '东北烤冷面', slug: 'dong-bei-kao-leng-mian', category: "肉类", description: "劲道冷面配鸡蛋火腿，刷上甜辣酱料。", price: "¥12/份", image: "https://images.unsplash.com/photo-1555126634-323283e090fa?w=400&h=300&fit=crop", spicy: true, vegetarian: false, popularity: 90, waiting: "约4分钟", lat: 40.6570, lng: 109.8413 },
  { id: 5, name: '老北京糖葫芦', slug: 'lao-bei-jing-tang-hu-lu', category: "甜点", description: "山楂裹糖衣，酸甜可口，童年回忆。", price: "¥8/串", image: "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=400&h=300&fit=crop", spicy: false, vegetarian: true, popularity: 78, waiting: "即买即走", lat: 40.6575, lng: 109.8415 },
  { id: 6, name: '芒果绵绵冰', slug: 'mang-guo-mian-mian-bing', category: "甜点", description: "新鲜芒果搭配炼乳冰沙，夏日消暑圣品。", price: "¥22/份", image: "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&h=300&fit=crop", spicy: false, vegetarian: true, popularity: 95, waiting: "约3分钟", lat: 40.6572, lng: 109.8416 },
  { id: 7, name: '大肠包小肠', slug: 'da-chang-bao-xiao-chang', category: "肉类", description: "糯米肠包裹碳烤香肠，蒜香四溢。", price: "¥16/份", image: "https://images.unsplash.com/photo-1603073163308-9654c3fb70b5?w=400&h=300&fit=crop", spicy: false, vegetarian: false, popularity: 87, waiting: "约6分钟", lat: 40.6569, lng: 109.8412 },
  { id: 8, name: '铁板鱿鱼', slug: 'tie-ban-you-yu', category: "海鲜", description: "整只鱿鱼铁板煎烤，刷上秘制酱料。", price: "¥20/份", image: "https://images.unsplash.com/photo-1625943553852-781c6dd46faa?w=400&h=300&fit=crop", spicy: true, vegetarian: false, popularity: 91, waiting: "约7分钟", lat: 40.6573, lng: 109.8414 },
]

export const events = [
  { id: 1, title: "每周五啤酒节", date: "每周五 19:00-23:00", desc: "指定摊位精酿啤酒买一送一，搭配烧烤更尽兴！", tag: "热门" },
  { id: 2, title: "周末现场乐队", date: "每周六/日 20:00-22:00", desc: "本地乐队驻唱，边吃边听 Live 音乐。", tag: "音乐" },
  { id: 3, title: "扫码集点换小吃", date: "长期活动", desc: "消费满5次送招牌小吃一份，扫码即可参与。", tag: "福利" },
  { id: 4, title: "七夕情侣套餐", date: "七夕节当天", desc: "限定双人套餐 ¥88，含两杯特调饮品。", tag: "限定" },
]

export const reviews = [
  { id: 1, nickname: "吃货小王", avatar: "W", rating: 5, food: "老李炭烤羊肉串", comment: "羊肉串太绝了！每次来必点，孜然味特别香，肉也很嫩。" },
  { id: 2, nickname: "美食猎人阿强", avatar: "A", rating: 5, food: "铁板鱿鱼", comment: "鱿鱼超大一只，酱料很入味，排队也值得！" },
  { id: 3, nickname: "甜品控小美", avatar: "M", rating: 4, food: "芒果绵绵冰", comment: "夏天来一碗太爽了，芒果超甜，份量也足。" },
  { id: 4, nickname: "夜宵达人", avatar: "Y", rating: 5, food: "东北烤冷面", comment: "正宗东北味儿！加蛋加肠，再来瓶啤酒完美。" },
  { id: 5, nickname: "本地老饕", avatar: "L", rating: 4, food: "台湾蚵仔煎", comment: "蚵仔新鲜，酱汁调得很好，跟在台湾吃的一个味道。" },
  { id: 6, nickname: "周末逛吃", avatar: "Z", rating: 5, food: "阿婆臭豆腐", comment: "闻着臭吃着真香！外皮炸得酥脆，里面嫩嫩的。" },
]

export const todaySpecial = {
  id: 1, name: "秘制蒜蓉烤生蚝", tag: "主厨特选", desc: "当日现捞大生蚝，搭配独门蒜蓉酱，炭火烤制，鲜嫩多汁。限量50份。", price: "¥28/半打", image: "https://images.unsplash.com/photo-1559737558-2f5a35f4523b?w=600&h=400&fit=crop"
}

export const transport = {
  address: "内蒙古包头市昆都仑区钢铁大街包百美食街",
  subway: "市内多路公交直达「包百大楼站」，步行1分钟",
  bus: "公交1路、5路、11路、25路、40路至「包百大楼站」下车",
  parking: "包百商圈停车场（¥5/小时）、钢铁大街路边停车位（步行3分钟）",
  hours: "每晚 17:00 – 凌晨 02:00（节假日照常营业）",
  phone: "0472-8888666",
}

export const foodRecommendations = [
  "来串炭烤羊肉串怎么样？",
  "试试铁板鱿鱼，超人气！",
  "芒果绵绵冰，消暑最佳！",
  "臭豆腐配啤酒，绝了！",
  "糖葫芦来一串，甜甜的～",
  "蚵仔煎，台湾地道味道！",
]