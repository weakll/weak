from django.core.management.base import BaseCommand
from market.models import Store, Certificate, StaffMember, Product, Review

SLUGS = [
    'lao-li-yang-rou-chuan',
    'a-po-chou-dou-fu',
    'tai-wan-e-a-jian',
    'dong-bei-kao-leng-mian',
    'lao-bei-jing-tang-hu-lu',
    'mang-guo-mian-mian-bing',
    'da-chang-bao-xiao-chang',
    'tie-ban-you-yu',
]

REVIEW_DATA = [
    {'nickname': '吃货小王', 'avatar': 'W', 'rating': 5, 'food': '老李炭烤羊肉串', 'comment': '羊肉串太绝了！每次来必点，孜然味特别香，肉也很嫩。'},
    {'nickname': '美食猎人阿强', 'avatar': 'A', 'rating': 5, 'food': '铁板鱿鱼', 'comment': '鱿鱼超大一只，酱料很入味，排队也值得！'},
    {'nickname': '甜品控小美', 'avatar': 'M', 'rating': 4, 'food': '芒果绵绵冰', 'comment': '夏天来一碗太爽了，芒果超甜，份量也足。'},
    {'nickname': '夜宵达人', 'avatar': 'Y', 'rating': 5, 'food': '东北烤冷面', 'comment': '正宗东北味儿！加蛋加肠，再来瓶啤酒完美。'},
    {'nickname': '本地老饕', 'avatar': 'L', 'rating': 4, 'food': '台湾蚵仔煎', 'comment': '蚵仔新鲜，酱汁调得很好，跟在台湾吃的一个味道。'},
    {'nickname': '周末逛吃', 'avatar': 'Z', 'rating': 5, 'food': '阿婆臭豆腐', 'comment': '闻着臭吃着真香！外皮炸得酥脆，里面嫩嫩的。'},
    {'nickname': '夜猫子', 'avatar': 'Y', 'rating': 5, 'food': '大肠包小肠', 'comment': '糯米肠很香，香肠烤得恰到好处，蒜蓉酱是灵魂！'},
    {'nickname': '甜牙齿', 'avatar': 'T', 'rating': 4, 'food': '老北京糖葫芦', 'comment': '糖衣薄脆，山楂酸酸甜甜，小时候的味道。'},
]

DETAILS = [
    {
        'certificates': [
            {'name': '食品经营许可证', 'issuer': '包头市昆都仑区市场监督管理局', 'issue_date': '2024-03-15', 'description': '合法经营许可'},
            {'name': '从业人员健康证', 'issuer': '包头市疾病预防控制中心', 'issue_date': '2025-01-10', 'description': '全部员工持证上岗'},
        ],
        'staff': [
            {'name': '主厨', 'bio': '从事烧烤行业15年，曾在内蒙古多家知名餐厅任职。', 'is_primary': True},
            {'name': '帮厨', 'bio': '负责食材准备和腌制工作。', 'is_primary': False},
        ],
        'details': ['秘制孜然羊肉串', '香辣羊肉筋', '烤羊腰子', '烤鸡翅'],
    },
    {
        'certificates': [
            {'name': '食品经营许可证', 'issuer': '包头市昆都仑区市场监督管理局', 'issue_date': '2024-06-20', 'description': '合法经营许可'},
        ],
        'staff': [
            {'name': '摊主', 'bio': '从湖南老家带来祖传臭豆腐配方，经营已8年。', 'is_primary': True},
        ],
        'details': ['经典臭豆腐', '炸豆腐泡', '香干炒辣椒'],
    },
    {
        'certificates': [
            {'name': '食品经营许可证', 'issuer': '包头市昆都仑区市场监督管理局', 'issue_date': '2023-11-05', 'description': '合法经营许可'},
        ],
        'staff': [
            {'name': '摊主', 'bio': '曾在台北士林夜市学习，还原地道台湾味。', 'is_primary': True},
        ],
        'details': ['经典蚵仔煎', '综合蚵仔煎(加虾仁)', '炸蚵仔酥'],
    },
    {
        'certificates': [
            {'name': '食品经营许可证', 'issuer': '包头市昆都仑区市场监督管理局', 'issue_date': '2024-01-18', 'description': '合法经营许可'},
        ],
        'staff': [
            {'name': '摊主', 'bio': '哈尔滨人，把正宗东北烤冷面带到了包头。', 'is_primary': True},
        ],
        'details': ['经典烤冷面', '加蛋加肠烤冷面', '芝士烤冷面', '豪华全家福烤冷面'],
    },
    {
        'certificates': [
            {'name': '食品经营许可证', 'issuer': '包头市昆都仑区市场监督管理局', 'issue_date': '2024-09-01', 'description': '合法经营许可'},
        ],
        'staff': [
            {'name': '老板', 'bio': '三代传承的糖葫芦手艺，用最传统的做法。', 'is_primary': True},
        ],
        'details': ['山楂糖葫芦', '草莓糖葫芦', '葡萄糖葫芦', '山药豆糖葫芦'],
    },
    {
        'certificates': [
            {'name': '食品经营许可证', 'issuer': '包头市昆都仑区市场监督管理局', 'issue_date': '2024-05-12', 'description': '合法经营许可'},
        ],
        'staff': [
            {'name': '老板', 'bio': '芒果控的福音，坚持只用当季新鲜芒果。', 'is_primary': True},
        ],
        'details': ['芒果绵绵冰', '芒果椰奶冰', '综合水果冰', '红豆抹茶冰'],
    },
    {
        'certificates': [
            {'name': '食品经营许可证', 'issuer': '包头市昆都仑区市场监督管理局', 'issue_date': '2024-07-22', 'description': '合法经营许可'},
        ],
        'staff': [
            {'name': '老板', 'bio': '在台湾夜市摆摊10年，带来最正宗大肠包小肠。', 'is_primary': True},
        ],
        'details': ['经典大肠包小肠', '蒜香大肠包小肠', '辣味大肠包小肠'],
    },
    {
        'certificates': [
            {'name': '食品经营许可证', 'issuer': '包头市昆都仑区市场监督管理局', 'issue_date': '2023-08-30', 'description': '合法经营许可'},
        ],
        'staff': [
            {'name': '摊主', 'bio': '从大连引进铁板鱿鱼技术，鱿鱼新鲜现做。', 'is_primary': True},
        ],
        'details': ['铁板大鱿鱼', '铁板鱿鱼须', '铁板鱿鱼串', '香辣铁板鱿鱼'],
    },
]

class Command(BaseCommand):
    help = '播种夜市摊位初始数据'

    def handle(self, *args, **options):
        stalls = [
            {'name': '老李炭烤羊肉串', 'slug': SLUGS[0], 'category': '肉类', 'description': '秘制孜然，炭火现烤，肥瘦相间。', 'address': '包百美食街A区12号', 'rating': 4.8, 'opening_hours': '17:00-02:00', 'phone': '0472-1234567', 'image_url': 'https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=600&h=400&fit=crop', 'popularity': 92, 'waiting': '约5分钟', 'spicy': True, 'vegetarian': False},
            {'name': '阿婆臭豆腐', 'slug': SLUGS[1], 'category': '素食', 'description': '外酥里嫩，秘制酱料，闻着臭吃着香。', 'address': '包百美食街B区5号', 'rating': 4.6, 'opening_hours': '17:00-01:00', 'phone': '0472-1234568', 'image_url': 'https://images.unsplash.com/photo-1625220194771-7ebdea0b70b9?w=600&h=400&fit=crop', 'popularity': 88, 'waiting': '约3分钟', 'spicy': True, 'vegetarian': True},
            {'name': '台湾蚵仔煎', 'slug': SLUGS[2], 'category': '海鲜', 'description': '新鲜牡蛎搭配鸡蛋青菜，地道台湾味。', 'address': '包百美食街C区2号', 'rating': 4.5, 'opening_hours': '17:30-01:30', 'phone': '0472-1234569', 'image_url': 'https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=600&h=400&fit=crop', 'popularity': 85, 'waiting': '约8分钟', 'spicy': False, 'vegetarian': False},
            {'name': '东北烤冷面', 'slug': SLUGS[3], 'category': '肉类', 'description': '劲道冷面配鸡蛋火腿，刷上甜辣酱料。', 'address': '包百美食街A区18号', 'rating': 4.7, 'opening_hours': '17:00-02:00', 'phone': '0472-1234570', 'image_url': 'https://images.unsplash.com/photo-1555126634-323283e090fa?w=600&h=400&fit=crop', 'popularity': 90, 'waiting': '约4分钟', 'spicy': True, 'vegetarian': False},
            {'name': '老北京糖葫芦', 'slug': SLUGS[4], 'category': '甜点', 'description': '山楂裹糖衣，酸甜可口，童年回忆。', 'address': '包百美食街D区8号', 'rating': 4.3, 'opening_hours': '17:00-23:00', 'phone': '0472-1234571', 'image_url': 'https://images.unsplash.com/photo-1551024601-bec78aea704b?w=600&h=400&fit=crop', 'popularity': 78, 'waiting': '即买即走', 'spicy': False, 'vegetarian': True},
            {'name': '芒果绵绵冰', 'slug': SLUGS[5], 'category': '甜点', 'description': '新鲜芒果搭配炼乳冰沙，夏日消暑圣品。', 'address': '包百美食街D区15号', 'rating': 4.9, 'opening_hours': '17:00-02:00', 'phone': '0472-1234572', 'image_url': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600&h=400&fit=crop', 'popularity': 95, 'waiting': '约3分钟', 'spicy': False, 'vegetarian': True},
            {'name': '大肠包小肠', 'slug': SLUGS[6], 'category': '肉类', 'description': '糯米肠包裹碳烤香肠，蒜香四溢。', 'address': '包百美食街A区25号', 'rating': 4.6, 'opening_hours': '17:00-01:00', 'phone': '0472-1234573', 'image_url': 'https://images.unsplash.com/photo-1603073163308-9654c3fb70b5?w=600&h=400&fit=crop', 'popularity': 87, 'waiting': '约6分钟', 'spicy': False, 'vegetarian': False},
            {'name': '铁板鱿鱼', 'slug': SLUGS[7], 'category': '海鲜', 'description': '整只鱿鱼铁板煎烤，刷上秘制酱料。', 'address': '包百美食街C区10号', 'rating': 4.7, 'opening_hours': '17:00-02:00', 'phone': '0472-1234574', 'image_url': 'https://images.unsplash.com/photo-1625943553852-781c6dd46faa?w=600&h=400&fit=crop', 'popularity': 91, 'waiting': '约7分钟', 'spicy': True, 'vegetarian': False},
        ]

        for i, stall in enumerate(stalls):
            store, created = Store.objects.update_or_create(slug=stall['slug'], defaults=stall)
            if created:
                self.stdout.write(self.style.SUCCESS(f'创建店铺: {store.name}'))
            detail = DETAILS[i]
            for cert in detail['certificates']:
                Certificate.objects.get_or_create(store=store, name=cert['name'], defaults=cert)
            for staff_ in detail['staff']:
                StaffMember.objects.get_or_create(
                    store=store,
                    name=f'{store.name}员工{staff_["name"]}',
                    defaults={'role': staff_['name'], 'bio': staff_['bio'], 'is_primary': staff_['is_primary']}
                )
            for j, prod_name in enumerate(detail['details']):
                Product.objects.get_or_create(
                    store=store,
                    name=prod_name,
                    defaults={
                        'description': f'{store.name} 招牌商品 - {prod_name}',
                        'price': f'¥{10+j*5}/份',
                        'is_recommended': (j == 0),
                        'image_url': store.image_url,
                    }
                )
            self.stdout.write(self.style.SUCCESS(f'已为 {store.name} 创建证书、人员和商品'))

        # 播种评价数据
        store_map = {s.name: s for s in Store.objects.all()}
        review_count = 0
        for rv in REVIEW_DATA:
            store = store_map.get(rv['food'])
            if store:
                Review.objects.get_or_create(
                    store=store,
                    nickname=rv['nickname'],
                    defaults={
                        'avatar': rv['avatar'],
                        'rating': rv['rating'],
                        'food': rv['food'],
                        'comment': rv['comment'],
                    }
                )
                review_count += 1
        self.stdout.write(self.style.SUCCESS(f'创建评价: {review_count} 条'))

        # 今日特价商品
        special_store = store_map.get('老李炭烤羊肉串')
        if special_store:
            Product.objects.get_or_create(
                store=special_store,
                name='秘制蒜蓉烤生蚝',
                defaults={
                    'description': '今日特价：当日现捞大生蚝，搭配独门蒜蓉酱，炭火烤制，鲜嫩多汁。限量50份。',
                    'price': '¥28/半打',
                    'image_url': 'https://images.unsplash.com/photo-1559737558-2f5a35f4523b?w=600&h=400&fit=crop',
                    'is_recommended': True,
                }
            )
            self.stdout.write(self.style.SUCCESS('创建今日特价商品: 秘制蒜蓉烤生蚝'))

        self.stdout.write(self.style.SUCCESS('数据播种完成！'))
