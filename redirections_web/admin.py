from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .models import QRCodePlugin


class FieldsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'thumbnail',
        'qrcode_link',
        'name',
        'start_date',
        'end_date',
        'activate',
        'created_at',
        'updated_at'
    ]
    list_filter = [
        ('activate', admin.BooleanFieldListFilter)
    ]


    def thumbnail(self, obj):
        if obj.qr_code:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="auto" >'.format(
                    url=obj.qr_code.url.split("/media/")[-1]
                )
            )

    
    def qrcode_link(self, obj):
        return format_html('<a href="{url}">{url}</a>', url=obj.qr_code_link)
    

admin.site.register(QRCodePlugin, FieldsAdmin)
