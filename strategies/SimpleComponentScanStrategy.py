# coding: utf-8

from CScanPoc import ABStrategy
from CScanPoc.lib.utils.indexing import iter_pocs_of_component


class SimpleComponentScanStrategy(ABStrategy):
    '''组件 POC 按序扫描策略'''

    def __init__(self, component_name=None):
        ABStrategy.__init__(self)
        self.component_name = component_name

    @property
    def author(self):
        return 'lotuc'

    @property
    def strategy_id(self):
        return 'simple-component-scan-strategy'

    @property
    def name(self):
        return '简单组件扫描策略'

    @property
    def description(self):
        return '此策略在给定组件名后，选定组件相关的所有 POC 对对应资产进行扫描'

    @property
    def pocs(self):
        if self.component_name is None:
            return []
        return iter_pocs_of_component(self.component_name, self.index_dir)


if __name__ == '__main__':
    SimpleComponentScanStrategy('CmsEasy').run()
