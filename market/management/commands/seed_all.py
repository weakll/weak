"""Comprehensive seed command for night market website."""
from django.core.management.base import BaseCommand
from market.models import Store, Product, Review, Event, TodaySpecial

STORES = [
    {"name":"老李炭烤羊肉串","slug":"lao-li-yang-rou-chuan","category":"肉类","description":"秘制孜然，炭火现烤，包头最火烧烤摊。","address":"包百美食街A区12号","rating":4.8,"opening_hours":"17:00-02:00","image_url":"https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=600&h=400&fit=crop","popularity":92,"waiting":"约5分钟","spicy":True,"vegetarian":False},
    {"name":"阿婆臭豆腐","slug":"a-po-chou-dou-fu","category":"素食","description":"外酥里嫩，秘制酱料，湖南祖传配方。","address":"包百美食街B区5号","rating":4.6,"image_url":"https://images.unsplash.com/photo-1625220194771-7ebdea0b70b9?w=600&h=400&fit=crop","popularity":88,"waiting":"约3分钟","spicy":True,"vegetarian":True},
    {"name":"台湾蚵仔煎","slug":"tai-wan-e-a-jian","category":"海鲜","description":"新鲜牡蛎配鸡蛋青菜，士林夜市同款配方。","address":"包百美食街C区2号","rating":4.5,"image_url":"https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=600&h=400&fit=crop","popularity":85,"waiting":"约8分钟","spicy":False,"vegetarian":False},
    {"name":"东北烤冷面","slug":"dong-bei-kao-leng-mian","category":"肉类","description":"哈尔滨老师傅手艺，劲道冷面配鸡蛋火腿。","address":"包百美食街A区18号","rating":4.7,"image_url":"https://images.unsplash.com/photo-1555126634-323283e090fa?w=600&h=400&fit=crop","popularity":90,"waiting":"约4分钟","spicy":True,"vegetarian":False},
    {"name":"老北京糖葫芦","slug":"lao-bei-jing-tang-hu-lu","category":"甜点","description":"三代传承，山楂裹糖衣，酸甜可口。","address":"包百美食街D区8号","rating":4.3,"image_url":"https://images.unsplash.com/photo-1551024601-bec78aea704b?w=600&h=400&fit=crop","popularity":78,"waiting":"即买即走","spicy":False,"vegetarian":True},
    {"name":"芒果绵绵冰","slug":"mang-guo-mian-mian-bing","category":"甜点","description":"台湾芒果搭配炼乳冰沙，夏日消暑圣品。","address":"包百美食街D区15号","rating":4.9,"image_url":"https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600&h=400&fit=crop","popularity":95,"waiting":"约3分钟","spicy":False,"vegetarian":True},
    {"name":"大肠包小肠","slug":"da-chang-bao-xiao-chang","category":"肉类","description":"糯米肠包裹碳烤香肠，经典台湾小吃。","address":"包百美食街A区25号","rating":4.6,"image_url":"https://images.unsplash.com/photo-1603073163308-9654c3fb70b5?w=600&h=400&fit=crop","popularity":87,"waiting":"约6分钟","spicy":False,"vegetarian":False},
    {"name":"铁板鱿鱼","slug":"tie-ban-you-yu","category":"海鲜","description":"整只大鱿鱼铁板煎烤，大连师傅手艺。","address":"包百美食街C区10号","rating":4.7,"image_url":"https://images.unsplash.com/photo-1625943553852-781c6dd46faa?w=600&h=400&fit=crop","popularity":91,"waiting":"约7分钟","spicy":True,"vegetarian":False},
    {"name":"秘制烤猪蹄","slug":"mi-zhi-kao-zhu-ti","category":"肉类","description":"先卤后烤，外皮焦香软糯，胶原蛋白满满。","address":"包百美食街B区12号","rating":4.5,"image_url":"https://images.unsplash.com/photo-1624373182399-7e0e5f5a1e1f?w=600&h=400&fit=crop","popularity":83,"waiting":"约10分钟","spicy":True,"vegetarian":False},
    {"name":"重庆酸辣粉","slug":"chong-qing-suan-la-fen","category":"素食","description":"正宗重庆味道，红薯粉劲道爽滑，酸辣开胃。","address":"包百美食街C区8号","rating":4.4,"image_url":"https://images.unsplash.com/photo-1555126634-323283e090fa?w=600&h=400&fit=crop","popularity":80,"waiting":"约5分钟","spicy":True,"vegetarian":True},
    {"name":"章鱼小丸子","slug":"zhang-yu-xiao-wan-zi","category":"海鲜","description":"外酥里嫩，整颗章鱼足，木鱼花跳舞。","address":"包百美食街D区3号","rating":4.3,"image_url":"https://images.unsplash.com/photo-1551024601-bec78aea704b?w=600&h=400&fit=crop","popularity":76,"waiting":"约3分钟","spicy":False,"vegetarian":False},
    {"name":"手工冰粉","slug":"shou-gong-bing-fen","category":"甜点","description":"手搓冰粉，红糖水搭配葡萄干山楂碎，清爽解腻。","address":"包百美食街D区20号","rating":4.2,"image_url":"https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600&h=400&fit=crop","popularity":72,"waiting":"即买即走","spicy":False,"vegetarian":True},
]

PRODUCTS = {
    "lao-li-yang-rou-chuan": ["秘制孜然羊肉串|15|1", "香辣羊肉筋|18|0", "烤羊腰子|25|0", "烤鸡翅|10|0"],
    "a-po-chou-dou-fu": ["经典臭豆腐|12|1", "炸豆腐泡|10|0", "香干炒辣椒|15|0"],
    "tai-wan-e-a-jian": ["经典蚵仔煎|18|1", "综合蚵仔煎(加虾仁)|25|0", "炸蚵仔酥|22|0"],
    "dong-bei-kao-leng-mian": ["经典烤冷面|10|1", "加蛋加肠烤冷面|15|0", "芝士烤冷面|18|0", "豪华全家福烤冷面|25|0"],
    "lao-bei-jing-tang-hu-lu": ["山楂糖葫芦|8|1", "草莓糖葫芦|12|0", "葡萄糖葫芦|10|0", "山药豆糖葫芦|8|0"],
    "mang-guo-mian-mian-bing": ["芒果绵绵冰|28|1", "芒果椰奶冰|25|0", "综合水果冰|30|0", "红豆抹茶冰|22|0"],
    "da-chang-bao-xiao-chang": ["经典大肠包小肠|15|1", "蒜香大肠包小肠|18|0", "辣味大肠包小肠|18|0"],
    "tie-ban-you-yu": ["铁板大鱿鱼|20|1", "铁板鱿鱼须|15|0", "铁板鱿鱼串|12|0", "香辣铁板鱿鱼|22|0"],
    "mi-zhi-kao-zhu-ti": ["秘制烤猪蹄|18|1", "香辣烤猪蹄|20|0", "蒜蓉烤猪蹄|20|0"],
    "chong-qing-suan-la-fen": ["招牌酸辣粉|12|1", "肥肠酸辣粉|18|0", "杂酱酸辣粉|15|0"],
    "zhang-yu-xiao-wan-zi": ["经典章鱼小丸子(6粒)|15|1", "芝士章鱼小丸子|18|0", "芥末章鱼小丸子|16|0"],
    "shou-gong-bing-fen": ["经典红糖冰粉|8|1", "水果冰粉|12|0", "玫瑰冰粉|10|0"],
}

REVIEWS = [
    "lao-li-yang-rou-chuan|吃货小王|5|秘制孜然羊肉串|羊肉串太绝了！每次来必点",
    "lao-li-yang-rou-chuan|美食猎人阿强|5|香辣羊肉筋|羊筋有嚼劲，辣得够味",
    "a-po-chou-dou-fu|周末逛吃|5|经典臭豆腐|闻着臭吃着真香！外皮炸得酥脆",
    "tai-wan-e-a-jian|本地老饕|4|经典蚵仔煎|跟在台湾吃的一个味道",
    "dong-bei-kao-leng-mian|夜宵达人|5|经典烤冷面|正宗东北味儿！加蛋加肠",
    "mang-guo-mian-mian-bing|甜品控小美|5|芒果绵绵冰|夏天来一碗太爽了",
    "mang-guo-mian-mian-bing|约会达人|5|综合水果冰|颜值超高，拍照好看",
    "da-chang-bao-xiao-chang|夜市老粉|5|经典大肠包小肠|蒜蓉酱是灵魂",
    "tie-ban-you-yu|海鲜控|5|铁板大鱿鱼|鱿鱼超大一只，排队也值得",
    "mi-zhi-kao-zhu-ti|美容养颜|5|秘制烤猪蹄|满满的胶原蛋白！",
    "chong-qing-suan-la-fen|辣妹子|4|招牌酸辣粉|酸辣够味，粉条劲道",
    "zhang-yu-xiao-wan-zi|小朋友妈妈|5|经典章鱼小丸子|孩子每次来必点",
    "shou-gong-bing-fen|解腻专家|4|经典红糖冰粉|清爽解腻",
    "lao-li-yang-rou-chuan|公司聚餐|5|秘制孜然羊肉串|每周五公司聚餐必来",
]

EVENTS = [
    {"title":"优惠券派送","date":"即日起至8月底","description":"关注公众号领取5元优惠券","tag":"福利","status":"published","is_past":False},
    {"title":"七夕情侣套餐","date":"七夕节当天","description":"全场情侣套餐享8折优惠","tag":"限定","status":"published","is_past":False},
    {"title":"扫码集点换小吃","date":"长期活动","description":"集满6枚印章兑换小吃","tag":"福利","status":"published","is_past":False},
    {"title":"周末现场乐队","date":"每周六/日","description":"中心广场现场乐队表演","tag":"音乐","status":"published","is_past":False},
    {"title":"每周五啤酒节","date":"每周五","description":"指定啤酒买二送一","tag":"热门","status":"published","is_past":False},
    {"title":"美食摄影大赛","date":"7月-8月","description":"上传美食照片赢大奖","tag":"热门","status":"published","is_past":False},
    {"title":"元旦跨年狂欢","date":"2025/12/31","description":"跨年夜营业至凌晨3点","tag":"热门","status":"archived","is_past":True},
    {"title":"春季美食节","date":"2026年4月","description":"春季限定美食","tag":"限定","status":"archived","is_past":True},
    {"title":"端午粽子节","date":"2026年6月","description":"购买任意商品送粽子","tag":"福利","status":"archived","is_past":True},
]

TODAY_SPECIALS = [
    {"store":"lao-li-yang-rou-chuan","name":"秘制蒜蓉烤生蚝","description":"当日现捞大生蚝，搭配蒜蓉酱","price":"¥28/半打","tag":"主厨特选","active":True},
    {"store":"a-po-chou-dou-fu","name":"臭豆腐全家福","description":"经典臭豆腐+炸豆腐泡+香干","price":"¥25/份","tag":"限时优惠","active":True},
    {"store":"mang-guo-mian-mian-bing","name":"芒果绵绵冰买一送一","description":"芒果绵绵冰买一份送一份","price":"¥28/2份","tag":"买一送一","active":True},
]

class Command(BaseCommand):
    help = "Seed all night market data"

    def handle(self, *args, **options):
        self._seed_stores()
        self._seed_events()
        self._seed_specials()
        self.stdout.write(self.style.SUCCESS(f"Done: Stores={Store.objects.count()} Products={Product.objects.count()} Reviews={Review.objects.count()} Events={Event.objects.count()} Specials={TodaySpecial.objects.count()}"))

    def _seed_stores(self):
        for s in STORES:
            copy = dict(s)
            slug = copy.pop("slug")
            store, created = Store.objects.update_or_create(slug=slug, defaults=copy)
            if slug in PRODUCTS:
                for pdata in PRODUCTS[slug]:
                    parts = pdata.split("|")
                    Product.objects.update_or_create(
                        store=store, name=parts[0],
                        defaults={"price":"¥"+parts[1]+"/份","is_recommended":parts[2]=="1","description":store.name+" - "+parts[0],"image_url":store.image_url}
                    )
        for rdata in REVIEWS:
            parts = rdata.split("|")
            try:
                store = Store.objects.get(slug=parts[0])
                Review.objects.update_or_create(
                    store=store, nickname=parts[1],
                    defaults={"rating":int(parts[2]),"food":parts[3],"comment":parts[4]}
                )
            except Store.DoesNotExist:
                pass

    def _seed_events(self):
        Event.objects.all().delete()
        for e in EVENTS:
            Event.objects.create(**e)

    def _seed_specials(self):
        TodaySpecial.objects.all().delete()
        for t in TODAY_SPECIALS:
            try:
                s = Store.objects.get(slug=t["store"])
                TodaySpecial.objects.create(store=s, name=t["name"], description=t["description"], price=t["price"], tag=t["tag"], is_active=t["active"])
            except Store.DoesNotExist:
                pass
