#!/usr/bin/env python3
# coding: utf-8

'''POC 执行入口'''

import sys

from CScanPoc.lib.api.common import create_cmd_parser
from CScanPoc.lib.core.log import CSCAN_LOGGER as logger
from CScanPoc.lib.core.log import setup_cscan_poc_logger
from CScanPoc.lib.utils.indexing import find_poc


def create_parser():
    '''创建命令行解析'''

    parser = create_cmd_parser()
    parser.add_argument('--poc-id', dest='poc_id', required=False,
                        help='要执行的 POC 的 ID')

    return parser


def main():
    '''POC 执行入口'''
    args = None
    parser = create_parser()
    try:
        args = parser.parse_args()
    except:
        logger.exception('解析错误')
        raise
    if not args.poc_id:
        parser.print_usage()
        logger.warning('参数解析错误: poc-id 为空')
        return
    if not args.url:
        parser.print_usage()
        logger.warning('参数解析错误: url 为空')
        return
    setup_cscan_poc_logger(verbose=args.verbose,
                           very_verbose=args.very_verbose)
    (poc_id, index_dir) = (args.poc_id, args.index_dir)

    poc = None
    try:
        logger.debug('查找 POC[id=%s] index_dir=%s', poc_id, index_dir)
        poc = find_poc(poc_id, index_dir)
    except:
        logger.exception('POC[id=%s, index_dir=%s]加载失败，退出执行',
                         poc_id, index_dir)
        raise

    try:
        poc.run(args=args)
    except:
        logger.exception('%s执行异常', poc)


if __name__ == '__main__':
    try:
        main()
    except:
        sys.exit(1)
