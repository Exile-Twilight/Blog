from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from blog.base_admin import BaseOwnerAdmin
from blog.custom_site import custom_site


# Register your models here.
class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', "post_count")
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    inlines = [PostInline]


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    # @classmethod
    # def test(cls, field, request, params, model, admin_view, field_path):
    #     return field.name == 'category'
    #
    # def __init__(self, field, request, params, model, model_admin, field_path):
    #     super().__init__(field, request, params, m
    #     odel, model_admin, field_path)
    #     self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


# manager.register(CategoryOwnerFilter, take_priority=True)


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    list_display = ['title', 'category', 'status',
                    'created_time', 'operator', 'pv', 'uv']
    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']

    actions_on_top = False
    actions_on_bottom = True

    save_on_top = False

    exclude = ['owner']

    form = PostAdminForm
    # fields = [
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag'
    # ]
    # form_layout = (
    #     Fieldset(
    #         '基础信息',
    #         Row("title", "category"),
    #         'status',
    #         'tag',
    #     ),
    #     Fieldset(
    #         '内容信息',
    #         'desc',
    #         'content'
    #     )
    # )

    fieldsets = (
                    '基础配置', {
                        'description': '基础配置描述',
                        'fields': (
                            ('title', 'category'),
                            'status',
                        ),
                    }
                ),
    ('内容', {
        'fields': (
            'desc',
            'content',
        ),
    }),
    ('内容', {
        'field': (
            'desc',
            'content',
        ),
    }),
    ('额外信息', {
        'classes': ('wide',),
        'fields': ('tag',),
    })

    # filter_vertical = ['tag']

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:app_blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)

    # @property
    # def media(self):
    #     media = super().media
    #     media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
    #     media.add_css({
    #         'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),
    #     })
    #     return media
    class Media:
        css = {
            'all': ['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css']
        }
        js = ['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js']


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
