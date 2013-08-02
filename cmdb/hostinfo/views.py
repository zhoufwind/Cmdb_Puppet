# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Host, HostGroup 

try:
    import json
except ImportError,e:
    import simplejson as json

def collect(request):
    req = request
    if req.POST:
        vendor = req.POST.get('Product_Name')
        sn = req.POST.get('Serial_Number')
        product = req.POST.get('Manufacturer')
        cpu_model = req.POST.get('Model_Name')
        cpu_num = req.POST.get('Cpu_Cores')
        cpu_vendor = req.POST.get('Vendor_Id')
        memory_part_number = req.POST.get('Part_Number')
        memory_manufacturer = req.POST.get('Manufacturer')
        memory_size = req.POST.get('Size')
        #uuid = req.POST.get('UUID')
        identity = req.POST.get('identity')
        device_model = req.POST.get('Device_Model')
        device_version = req.POST.get('Firmware_Version')
        device_sn = req.POST.get('Serial_Number')
        device_size = req.POST.get('User_Capacity')
        osver = req.POST.get('os_version')
        hostname = req.POST.get('os_name')
        os_release = req.POST.get('os_release')
        ipaddrs = req.POST.get('Ipaddr')
        mac = req.POST.get('Device')
        link = req.POST.get('Link')
        mask = req.POST.get('Mask')
        device = req.POST.get('Device')
 
        host = Host()
        host.hostname = hostname
        host.product = product
        host.cpu_num = cpu_num
        host.cpu_model = cpu_model
        host.cpu_vendor = cpu_vendor
        host.memory_part_number = memory_part_number
        host.memory_manufacturer = memory_manufacturer
        host.memory_size = memory_size
        host.device_model = device_model
        host.device_version = device_version
        host.device_sn = device_sn
        host.device_size = device_size
        host.osver = osver
        host.os_release = os_release
        host.vendor = vendor
        #host.uuid = uuid
        host.identity = identity
        host.sn = sn
        host.ipaddr = ipaddrs 
        host.save()
       
        #for ip in ipaddrs.split(';'):
        #    o_ip = IPaddr()
        #    o_ip.ipaddr = ip
        #    o_ip.host = host
        #    o_ip.save()
          
        return HttpResponse('OK')
    else:
        return HttpResponse('no post data')

def gethosts(req):
    d = []
    hostgroups = HostGroup.objects.all()
    for hg in hostgroups:
        ret_hg = {'hostgroup':hg.name,'members':[]}
        members = hg.members.all()
        for h in members:
            ret_h = {'hostname':h.hostname,
                'ipaddr':h.ipaddr,
                'identity':h.identity
            }
            ret_hg['members'].append(ret_h)
        d.append(ret_hg)
    ret = {'status':0,'data':d,'message':'ok'}
    return HttpResponse(json.dumps(ret))

def getHostByIdentity(req):
    try:
        identity = req.GET['hostidentity']
    except:
        return HttpResponse(json.dumps({'status':-1,'message':'no option'}))
  
    try:
        host = Host.objects.get(identity=identity)
    except:
        return HttpResponse(json.dumps({'status':-2,'message':'no host'}))
  
    data = {'hostname':host.hostname,'hostgroups':[hg.name for hg in host.hostgroup_set.all()]}
    return HttpResponse(json.dumps(data))
