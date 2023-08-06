from django.contrib import admin

from diary.models import DailyReport, FoodInReport, Products

admin.site.register(Products)


@admin.register(FoodInReport)
class FoodInReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'weight', 'report', 'report_type',)


@admin.register(DailyReport)
class DailyReport(admin.ModelAdmin):
    list_display = ('id', 'user', 'date',)
