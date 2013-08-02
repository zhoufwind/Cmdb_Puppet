#from models import Host, IPaddr
from models import Host, HostGroup
from django.contrib import admin


class HostAdmin(admin.ModelAdmin):
    list_display = ['vendor',
        'sn',
        'product',
        'cpu_model',
        'cpu_num',
        'cpu_vendor',
        'memory_part_number',
        'memory_manufacturer',
        'memory_size',
        'device_model',
        'device_version',
        'device_sn',
        'device_size',
        'osver',
        'hostname',
        'os_release',
        'ipaddr',
        'identity'
        ]

#class IPaddrAdmin(admin.ModelAdmin):
#    list_display = ['ipaddr',
#        'host'
#    ]

class HostGroupAdmin(admin.ModelAdmin):
    list_display = ['name',]

admin.site.register(HostGroup,HostGroupAdmin)
admin.site.register(Host, HostAdmin)
#admin.site.register(IPaddr, IPaddrAdmin)
