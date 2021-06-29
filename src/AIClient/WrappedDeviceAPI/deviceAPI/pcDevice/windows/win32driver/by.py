# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/pcDevice/windows/win32driver/by.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 7160 bytes
"""公共定义模块
"""
import re

class UIElementDescription(object):
    PROPERTY_SEP = '&&'
    OPERATORS = ['=', '~=']
    MATCH_FUNCS = {}
    MATCH_FUNCS['='] = lambda x, y: x == y
    MATCH_FUNCS['~='] = lambda string, pattern: re.search(pattern, string) != None

    def __init__(self, value):
        self._parsedValue = self._parse(value)

    def __str__(self):
        """返回格式化后的字符串
        """
        sep = ' ' + self.PROPERTY_SEP + ' '
        tmp = []
        for key in self._parsedValue:
            kv = '%s %s %s' % (key,
             self._parsedValue[key][0],
             isinstance(self._parsedValue[key][1], str) and '"%s"' % self._parsedValue[key][1] or self._parsedValue[key][1])
            tmp.append(kv)

        return sep.join(tmp)

    def _parse(self, value):
        if not value.strip():
            return {}
        props = value.split(self.PROPERTY_SEP)
        parsed_locators = {}
        for prop_str in props:
            prop_str = prop_str.strip()
            if len(prop_str) == 0:
                raise Exception('%s 中含有空的属性。' % value)
            parsed_props = self._parse_property(prop_str)
            parsed_locators.update(parsed_props)

        return parsed_locators

    def _parse_property(self, prop_str):
        """解析property字符串，返回解析后结构
        
                           例如将 "ClassName='Dialog' " 解析返回 {ClassName: ['=', 'Dialog']}
        """
        parsed_pattern = '([\\w\\-]+)\\s*([=~!<>]+)\\s*["\'](.*)["\']'
        match_object = re.match(parsed_pattern, prop_str)
        if match_object is None:
            parsed_pattern = '([\\w\\-]+)\\s*([=~!<>]+)\\s*((?:-?0x[0-9a-fA-F]+|-?[0-9]+))'
            match_object = re.match(parsed_pattern, prop_str)
            if match_object is None:
                raise Exception('属性(%s)不符合QPath语法' % prop_str)
            prop_name, operator, prop_value = match_object.groups()
            if operator not in self.OPERATORS:
                raise Exception('QPath不支持操作符：%s' % operator)
            if prop_value.find('0x') != -1:
                prop_value = int(prop_value, 16)
            else:
                prop_value = int(prop_value)
            return {prop_name: [operator, prop_value]}
        else:
            prop_name, operator, prop_value = match_object.groups()
            if operator not in self.OPERATORS:
                raise Exception('QPath不支持操作符：%s' % operator)
            return {prop_name: [operator, prop_value]}

    def loads(self):
        """获取解释后的数值
        """
        return self._parsedValue

    @classmethod
    def dumps(cls, attrs):
        inst = cls('')
        rlt = {}
        for key in list(attrs.keys()):
            rlt[key] = [
             '=', attrs[key]]

        inst._parsedValue = rlt
        return inst


class QPath(object):
    __doc__ = 'Query Path类，使用QPath字符串定位UI控件\n    \n    QPath的定义：\n    Qpath ::= Seperator UIElementDescription Qpath\n    Seperator ::= 路径分隔符，任意的单个字符\n    UIElementDescription ::= UIElementProperty [&& UIElementProperty]\n    UIElementProperty ::= UIProperty | RelationProperty | IndexProperty\n    UIProperty ::= Property Operator “Value”\n    RelationProperty ::= MaxDepth = Integer(最大搜索子孙深度， 若不写，则代表搜索所有子孙。 数值从1开始)\n    IndexProperty ::= Index = Integer(Integer:找到的多个控件中的第几个（数值从0开始）)\n    \n    Operator ::= \'=\' | \'~=\' (\'=\' 表示精确匹配; \'~=\' 表示用正则表达式匹配) \n     \n    UI控件基本上都是由树形结构组织起来的。为了方便定位树形结构的节点，QPath采用了路径结构\n         的字符串形式。 QPath以第一个字符为路径分隔符，如 "/Node1/Node2/Node3"和 “|Node1|Node2|Node3"\n         是一样的路径，都表示先找到Node1，再在Node1的子孙节点里找Node2，然后在Node2的子孙节点里\n         找Node3。而定位每个Node需要改节点的多个属性以"&&"符号连接起来, 形成\n    "/Property1=\'value1\' && property2~=\'value2\' && ..."的形式，其中"~="表示正则匹配。\n    "MaxDepth"表示该节点离祖先节点的最大深度，    如果没有明确指定时默认取值为\'1\',即直接父子关系。\n    QPath还支持"Index”属性，用于当找到多个节点时指定选择第几个节点。\n    \n         例子：\n    Qpath ="/ ClassName=\'TxGuiFoundation\' && Caption~=\'QQ\\d+\' && Index=\'0\'\n            / Name=\'mainpanel\' && MaxDepth=\'10\'"\n    '
    PROPERTY_SEP = '&&'

    def __init__(self, value):
        """Contructor
        
        :type value: string
        :param value: QPath字符串   
        """
        if not isinstance(value, str):
            raise Exception('输入的QPath(%s)不是字符串!' % value)
        self._strqpath = value
        self._path_sep, self._parsed_qpath = self._parse(value)
        self._error_qpath = None

    def _parse(self, qpath_string):
        """解析qpath，并返回QPath的路径分隔符和解析后的结构
        
           "| ClassName='Dialog' && Caption~='SaveAs' | UIType='GF' && ControlID='123' && Instanc='-1'"
           => [{'ClassName': ['=', 'Dialog'], 'Caption': ['~=', 'SaveAs']}, 
               {'UIType': ['=', 'GF'], 'ControlID': ['=', '123'], 'Index': ['=', '-1']}]
        
        :param qpath_string: qpath 字符串
        :return: (seperator, parsed_qpath)
        """
        qpath_string = qpath_string.strip()
        seperator = qpath_string[0]
        locators = qpath_string[1:].split(seperator)
        parsed_qpath = []
        for locator in locators:
            parsed_locators = UIElementDescription(locator).loads()
            parsed_qpath.append(parsed_locators)

        return (seperator, parsed_qpath)

    def __str__(self):
        """返回格式化后的QPath字符串
        """
        qpath_str = ''
        for locator in self._parsed_qpath:
            qpath_str += self._path_sep + ' '
            delimit_str = ' ' + self.PROPERTY_SEP + ' '
            locator_str = delimit_str.join(["%s %s '%s'" % (key, locator[key][0], locator[key][1]) for key in locator])
            qpath_str += locator_str

        return qpath_str

    def loads(self, level=-1):
        """获取解释后的数值
        """
        if level == -1:
            return self._parsed_qpath
        if level >= 0:
            return self._parsed_qpath[level]
        raise ValueError('error parameter level:%s' % level)

    def get_parsed_qpath(self):
        """获取解析后的数据

        :return:
        """
        return self._parsed_qpath


class XPath(object):

    def __init__(self, value):
        self._value = value

    def loads(self):
        return self._value