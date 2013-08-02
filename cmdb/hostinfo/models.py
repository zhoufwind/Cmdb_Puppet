from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import paramiko

# Create your models here.

class Host(models.Model):
    """store host information"""
    vendor = models.CharField(max_length=30,null=True)
    sn = models.CharField(max_length=30,null=True)
    product = models.CharField(max_length=30,null=True)
    cpu_model = models.CharField(max_length=50,null=True)
    cpu_num = models.CharField(max_length=2,null=True)
    cpu_vendor = models.CharField(max_length=30,null=True)
    memory_part_number = models.CharField(max_length=30,null=True)
    memory_manufacturer = models.CharField(max_length=30,null=True)
    memory_size = models.CharField(max_length=20,null=True)
    device_model = models.CharField(max_length=30,null=True)
    device_version = models.CharField(max_length=30,null=True)
    device_sn = models.CharField(max_length=30,null=True)
    device_size = models.CharField(max_length=30,null=True)
    osver = models.CharField(max_length=30,null=True)
    hostname = models.CharField(max_length=30,null=True)
    os_release = models.CharField(max_length=30,null=True)
    ipaddr = models.IPAddressField(max_length=15)
    #uuid = models.CharField(max_length=50,null=True)
    identity = models.CharField(max_length=50,null=True)
 
    def __unicode__(self):
        return '%s,%s' % (self.hostname,self.ipaddr)
    
#class IPaddr(models.Model):
#     ipaddr = models.IPAddressField()
#     host = models.ForeignKey('Host')

class HostGroup(models.Model):
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(Host)

@receiver(pre_save,sender=Host)
def mod_handler(sender,**kwargs):
    data = str(kwargs['instance'])
    host, ip = data.split(',')
    user = 'root'
    passwd = '123456'
    port = 22
    connectExec(ip,port,user,passwd,host)

def connectExec(ip,port,user,passwd,host):
    ssh = paramiko.SSHClient()
    paramiko.util.log_to_file('/var/tmp/connectExec.log')
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip,port=port,username=user,password=passwd)
    ssh.exec_command('echo %s %s >> /etc/hosts' % (ip,host))
    ssh.exec_command("sed -i 's/^HOSTNAME.*/HOSTNAME=%s/' /etc/sysconfig/network" % host)
    ssh.close()
