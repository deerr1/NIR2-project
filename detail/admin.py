from django.db.models import Sum,  F
from django.db.models.functions import Trunc
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text

from detail import models

admin.site.site_header = 'Сайт учета деталей'
admin.site.site_title = 'Сайт учета деталей'
admin.site.site_url = None


admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(models.Supliers)
class SuplierModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'address',
        'phone_number'
    ]
    search_fields = [
        'name',
        'address',
        'phone_number'
    ]

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(models.Details)
class DetailsModelAdmin(admin.ModelAdmin):
    exclude  = ['is_active']
    list_display = [
        'name',
        'vendore_code'
    ]
    search_fields = [
        'name',
        'vendore_code'
    ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_active = True)

@admin.register(models.DeletedDetails)
class DeleteDetailsModelAdmin(admin.ModelAdmin):
    exclude  = ['is_active']
    readonly_fields = ['name', 'vendore_code']

    def has_view_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_active = False)

@admin.register(models.SupplierDetails)
class SupplierDetailsModelAdmin(admin.ModelAdmin):
    exclude  = ['is_active', 'deleted_datetime']
    list_display = [
        'supplier',
        'detail',
        'cost'
    ]
    list_filter = [
        'supplier__name'
    ]
    search_fields = [
        'supplier__name',
        'detail__name',
        'detail__vendore_code',
    ]
    raw_id_fields = [
        'supplier',
        'detail'
    ]

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)

    def delete_model(self, request, obj):
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id= ContentType.objects.get_for_model(obj).pk,
            object_id=obj.pk,
            object_repr=force_text(obj),
            action_flag=DELETION
        )
        obj.delete()

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + tuple(['supplier','detail','cost'])
        return self.readonly_fields

    def get_queryset(self, request):
        return super().get_queryset(request).filter(detail__is_active = True, is_active = True)

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(models.DeletedSupplierDetails)
class DeletedSupplierDetailsModelAdmin(admin.ModelAdmin):
    exclude  = ['is_active']
    readonly_fields = [
        'supplier',
        'detail',
        'cost',
        'deleted_datetime'
    ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_active = False)

@admin.register(models.Purchases)
class PurchasesModelAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/supplier_detatil_model_list.html'
    ordering = ('-date',)
    date_hierarchy = 'date'
    list_display = [
        'suplier_detail',
        'quantity',
        'sum',
        'date'
    ]
    list_filter = [
        'suplier_detail__supplier__name',
    ]
    raw_id_fields = [
        'suplier_detail' ,
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + tuple(['suplier_detail','quantity','date'])
        return self.readonly_fields

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(models.PurchasesSummary)
class PurchasesSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/purchases_summary_change_list.html'
    date_hierarchy = 'date'
    list_filter = [
        'suplier_detail__supplier__name',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total': Sum('quantity'),
            'total_sales': Sum(F('quantity') * F('suplier_detail__cost')),
        }

        response.context_data['summary'] = list(
            qs
            .values('suplier_detail__supplier__name')
            .annotate(**metrics)
            .order_by('suplier_detail__supplier__name')
        )

        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )
        return response
