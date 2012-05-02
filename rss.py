#! /usr/bin/env python

import datetime
import os

TITLE = '' #Site title goes here
URL = '' #Site URL goes here, e.g. http://www.example.com/

PAGEDIR = 'content/'
PAGEDIRLONG = '/var/www/' + PAGEDIR

with open('rss.xml', 'rb') as rssfile:
    rss_orig = rssfile.readlines()

rss_lines = []
for line in rss_orig:
    if '<guid>' in line and PAGEDIR in line:
        split_str = ''.join(['<guid>', URL, ,PAGEDIR])
        new_line  = line.split(split_str)[1].split('</guid>')[0]
        rss_lines.append(new_line)

all_page_list = [x for x in os.listdir(PAGEDIRLONG)]
page_list     = [entry for entry in all_page_list if entry not in rss_lines]

new_lines = []
for item in page_list:
    files = os.listdir(PAGEDIRLONG + item)
    html = [x for x in files if 'htm' in x][0]
    jpg = [x for x in files if 'jpg' in x][0]

    new_lines.extend([
        '\n'.join([
            '<item>',
            ''.join([
                '<title>',
                TITLE,
                ' - ',
                item,
                '</title>'
            ]),
            ''.join([
                URL,
                PAGEDIR,
                item,
                '/',
                html,
                '</link>'
            ]),
            ''.join([
                '<description>&lt;img src=&quot;',
                URL,
                PAGEDIR,
                item,
                '/',
                jpg,
                '&quot; title = &quot',
                TITLE,
                '&quot; alt=&quot;',
                TITLE,
                '&quot; /&gt;',
                '</description>'
            ]),
            ''.join([
                '<pubDate>',
                datetime.datetime.strftime(datetime.datetime.now(),
                                            '%a, %d %b %Y %H:%M:%S %z'),
                '</pubDate>'
            ]),
            ''.join([
                '<guid>',
                URL,,
                PAGEDIR,
                item,
                '</guid>'
            ]),
            '</item>'
        ])
    ])

if '<item>\n' in rss_orig:
    linesplit = rss_orig.index('<item>\n')
    top_lines = rss_orig[:linesplit]
    rss_orig = rss_orig[linesplit:]
else:
    top_lines = rss_orig
    rss_orig = []

if "</channel>" in top_lines:
    i = top_lines.index('</channel>')
    top_lines.pop(i)

if "</rss>" in top_lines:
    i = top_lines.index('</rss>')
    top_lines.pop(i)
    
new_rss = top_lines + new_lines + rss_orig

with open('rss.xml', 'w') as rssfile:
    rssfile.writelines(new_rss)
