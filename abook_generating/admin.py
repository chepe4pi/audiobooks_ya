from constance import config
from django.contrib import admin

from abook_generating.models import ABookGeneration


class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('status', 'generated_file', 'error_log')

    fieldsets = [
        ('-', {
            'fields': ('speaker', "book_text", "book_name", 'lang', 'gender', "status", 'generated_file', 'error_log'),
            'description': '<div class="help">SPEAKERS: {}</div>'.format(config.SPEAKERS),
        }),
    ]


admin.site.register(ABookGeneration, BookAdmin)
