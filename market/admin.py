from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from django.utils.safestring import mark_safe
from .models import Store, Certificate, StaffMember, Product, Review, JoinApplication, MerchantProfile, Event, TodaySpecial


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'rating', 'popularity', 'opening_hours')
    list_filter = ('category', 'spicy', 'vegetarian')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-popularity',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'issuer', 'issue_date')
    list_filter = ('issuer',)
    search_fields = ('name', 'store__name')


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'role', 'is_primary')
    list_filter = ('store', 'role', 'is_primary')
    search_fields = ('name', 'store__name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'price', 'is_recommended')
    list_filter = ('store', 'is_recommended', 'is_vegetarian')
    search_fields = ('name', 'store__name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'store', 'rating', 'food', 'created_at')
    list_filter = ('store', 'rating')
    search_fields = ('nickname', 'food', 'comment')
    ordering = ('-created_at',)


@admin.register(JoinApplication)
class JoinApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'application_type', 'status', 'created_at')
    list_filter = ('application_type', 'status')
    search_fields = ('name', 'phone', 'message')
    list_editable = ('status',)
    ordering = ('-created_at',)


@admin.register(MerchantProfile)
class MerchantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'store', 'phone', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'store')
    search_fields = ('user__username', 'store__name', 'phone')
    list_editable = ('is_approved',)




@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'tag', 'status', 'action_buttons', 'created_at')
    list_filter = ('tag', 'status')
    search_fields = ('title', 'description')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:event_id>/approve/', self.approve_view, name='market_event_approve'),
            path('<int:event_id>/publish/', self.publish_view, name='market_event_publish'),
            path('<int:event_id>/archive/', self.archive_view, name='market_event_archive'),
        ]
        return custom_urls + urls

    def approve_view(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.status = 'approved'; event.save()
        self.message_user(request, f'活动 "{event.title}" 已审批')
        return redirect(request.META.get('HTTP_REFERER', '../../'))

    def publish_view(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.status = 'published'; event.save()
        self.message_user(request, f'活动 "{event.title}" 已发布')
        return redirect(request.META.get('HTTP_REFERER', '../../'))

    def archive_view(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.status = 'archived'; event.save()
        self.message_user(request, f'活动 "{event.title}" 已下架')
        return redirect(request.META.get('HTTP_REFERER', '../../'))

    def action_buttons(self, obj):
        btns = []
        if obj.status != 'approved':
            btns.append(f'<a class="button" href="{obj.id}/approve/" style="background:#22c55e;color:#fff;padding:2px 10px;border-radius:3px;text-decoration:none;font-size:12px;margin-right:3px">审批</a>')
        if obj.status != 'published':
            btns.append(f'<a class="button" href="{obj.id}/publish/" style="background:#FF6B35;color:#fff;padding:2px 10px;border-radius:3px;text-decoration:none;font-size:12px;margin-right:3px">开启</a>')
        if obj.status != 'archived':
            btns.append(f'<a class="button" href="{obj.id}/archive/" style="background:#ef4444;color:#fff;padding:2px 10px;border-radius:3px;text-decoration:none;font-size:12px">下架</a>')
        return mark_safe(' '.join(btns))
    action_buttons.short_description = '操作'

@admin.register(TodaySpecial)
class TodaySpecialAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'store')
    search_fields = ('name', 'store__name')
