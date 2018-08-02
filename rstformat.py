#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


class RstFormat(object):
    """ mysql ddl => .rst


        This is Test
        =============

        +-------------+------------+--------------+
        |字段名        |意义        |类型           |
        +=============+============+==============+
        |inst_id      |机构id      |bigint(20)    |
        +-------------+------------+--------------+

    """

    def __init__(self, source, prefix='.'):
        """source: {
                'table_name':     'institution',
                'table_comment':  '机构表',
                'columns':    [('inst_id', '机构Id'， 'bigint(20)')  ....]
           }

           prefix: target dir to store .rst
        """

        self.tableName = source['table_name']
        self.comment = source['table_comment']
        self.columns = source['columns']

        self.head_1 = '字段名'
        self.head_2 = '意义'
        self.head_3 = '类型'
        self.length_1 = 30
        self.length_2 = 100
        self.length_3 = 20
        self.prefix = prefix

    def to_rst(self):

        if not os.path.exists(self.prefix):
            os.mkdir(self.prefix)

        path = f'{self.prefix}/{self.tableName}.rst'

        with open(path, 'wb') as f:
            result = self.make_up_string()
            f.write(result.encode('utf-8'))

    def make_up_string(self):
        # title
        title = f"{self.tableName}({self.comment})"
        title_line = '=' * (self.get_length(title) + 2)

        table_line = '+' + '-' * self.length_1 + '+' + '-' * self.length_2 + '+' + '-' * self.length_3 + '+'

        # heads
        heads = '|' + self.head_1 + ' ' * (self.length_1 - self.get_length(self.head_1)) + \
                '|' + self.head_2 + ' ' * (self.length_2 - self.get_length(self.head_2)) + \
                '|' + self.head_3 + ' ' * (self.length_3 - self.get_length(self.head_3)) + '|'
        heads_line = '+' + '=' * self.length_1 + '+' + '=' * self.length_2 + '+' + '=' * self.length_3 + '+'

        # columns
        columns_str = ""

        for column in self.columns:
            name = column[0]
            comment = column[1]
            comment = comment.replace('\n', ' ').replace('\r', '').replace('\t', ' ')
            comment = self.ch2en(comment)

            _type = column[2]

            column_str = self.make_column_str(name, comment, _type)

            columns_str += column_str
            columns_str += '\n'
            columns_str += table_line
            columns_str += '\n'

        return title + '\n' + title_line + '\n\n' + table_line + '\n' + heads + '\n' + heads_line + '\n' + columns_str

    def make_column_str(self, name, comment, _type):

        comment_len = self.get_length(comment)
        if comment_len > self.length_2:

            rows = int(comment_len / self.length_2) + 1 if comment_len % self.length_2 \
                else int(comment_len / self.length_2)

            _length = len(comment)

            start = int(_length / rows * 1)
            end = int(_length / rows * 2)
            string = '|' + name + ' ' * (self.length_1 - self.get_length(name)) + \
                     '|' + comment[:start] + ' ' * (self.length_2 - self.get_length(comment[:start])) + \
                     '|' + _type + ' ' * (self.length_3 - self.get_length(_type)) + '|'

            index = 1
            while end <= _length:
                string += '\n'
                string += '|' + ' ' * self.length_1 + \
                          '|' + comment[start:end] + ' ' * (self.length_2 - self.get_length(comment[start:end])) + \
                          '|' + ' ' * self.length_3 + '|'

                index += 1
                start = int(_length / rows * index)
                end = int(_length / rows * (index + 1))
            return string


        else:
            return '|' + name + ' ' * (self.length_1 - self.get_length(name)) + \
                   '|' + comment + ' ' * (self.length_2 - self.get_length(comment)) + \
                   '|' + _type + ' ' * (self.length_3 - self.get_length(_type)) + '|'

    def ch2en(self, string):
        """ 中文标点换成英文标点"""
        return string.replace('，', ',').replace('“','"').\
                      replace('‘','\'').replace('：', ':').\
                      replace('？','?').replace('；', ';').\
                      replace('”', '\'')


    def get_length(self, string):
        row_l = len(string)
        utf8_l = len(string.encode('utf-8'))
        return int((utf8_l - row_l) / 2) + row_l
