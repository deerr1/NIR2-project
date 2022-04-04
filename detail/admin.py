from django.db.models import Count, Sum, Min, Max, DateTimeField, F, ExpressionWrapper
from django.db.models.functions import Trunc
from django.contrib import admin
from django.contrib.auth.models import User, Group

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

@admin.register(models.Details)
class DetailsModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'vendore_code'
    ]
    search_fields = [
        'name',
        'vendore_code'
    ]

@admin.register(models.SupplierDetails)
class SupplierDetailsModelAdmin(admin.ModelAdmin):
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
        # 'cost'
    ]
    raw_id_fields = [
        'supplier',
        'detail'
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + tuple(['cost'])
        return self.readonly_fields

@admin.register(models.Purchases)
class PurchasesModelAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = [
        'suplier_detail',
        'quantity',
        'date'
    ]
    list_filter = [
        'suplier_detail__supplier__name',
        'date'
    ]
    search_fields = [
        'suplier_detail__detail__name',
        'quantity'
    ]
    raw_id_fields = [
        'suplier_detail' ,
    ]


@admin.register(models.PurchasesSummary)
class PurchasesSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/purchases_summary_change_list.html'
    date_hierarchy = 'date'
    list_filter = [
        'suplier_detail__supplier__name',
    ]


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
