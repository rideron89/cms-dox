import re
import sqlite3
import sys
import time
import xml.etree.ElementTree as ET

def getTime():
    return int(round(time.time() * 1000))

def parseContent(input):
    # convert to utf-8
    output = ''.join([i if ord(i) < 128 else ' ' for i in input])

    # remove unnecessary sections
    output = re.sub(r'{{Languages\|\s({{[^}]+}}\s?)+\s*}}(\r\n|\r|\n)*', '', output, flags=re.M)

    # convert source links
    matches = re.search(r'{{#dotorgredirect: ([^}]+)}}(\r\n|\r|\n)*', output)
    if matches:
        output = output.replace(matches.group(0), '<sub>Source: <a href={0} target="_blank">{0}</a></sub><br />'.format(matches.group(1)))

    # replace characters that might interfere with database storage
    output = output.replace('\n;', '\n')
    output = output.replace('\'', '&#39;')
    output = output.replace('"', '&quot;')

    # replace headings formatting
    output = output.replace('=====\n', '</h5>')
    output = output.replace('=====', '<h5>')
    output = output.replace('====\n', '</h4>')
    output = output.replace('====', '<h4>')
    output = output.replace('===\n', '</h3>')
    output = output.replace('===', '<h3>')
    output = output.replace('==\n', '</h2>')
    output = output.replace('==', '<h2>')

    # replace extra newlines
    output = output.replace('\n\n', '<br /><br />')

    # # convert function links
    # matches = re.search('\[\[Function_Reference\/([_a-z]+)\|([^\]]+)\]\]', output)

    # if matches:
    #     replace_str = '<router-link to="/functions/' + matches.group(1) + '">' + matches.group(2) + '</router-link>'
    #     output = output.replace(matches.group(0), replace_str)

    # # convert action links
    # matches = re.search('\[\[Action_Reference\/([_a-z]+)\|([^\]]+)\]\]', output)

    # if matches:
    #     replace_str = '<router-link to="/actions/' + matches.group(1) + '">' + matches.group(2) + '</router-link>'
    #     output = output.replace(matches.group(0), replace_str)

    return output

def loadPages(root):
    data = []

    for page in root.findall('{http://www.mediawiki.org/xml/export-0.8/}page'):
        title = page.findall('{http://www.mediawiki.org/xml/export-0.8/}title')[0].text
        title = ''.join([i if ord(i) < 128 else ' ' for i in title])
        title = title.split('/')[-1]
        title = title.replace(' ', '_')

        revisions = page.findall('{http://www.mediawiki.org/xml/export-0.8/}revision')

        content = revisions[0].findall('{http://www.mediawiki.org/xml/export-0.8/}text')[0].text
        content = parseContent(content)

        data.append({ 'title': title, 'content': content })

    return data

def saveToDB(table_name, data):
    conn = sqlite3.connect('data/wordpress.sqlite')
    cur  = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS `{0}` (`title` text, `content` text)'.format(table_name))
    cur.execute('DELETE FROM `{0}`'.format(table_name))

    for row in data:
        try:
            cur.execute('INSERT INTO `{0}` VALUES ("{1}", \'{2}\')'.format(table_name, row['title'], row['content']))
        except:
            print 'Error during SQL Insertion:'
            print row['title']
            print row['content']

    conn.commit()
    conn.close()

def load(table_name, input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    data = loadPages(root)

    saveToDB(table_name, data)

    return data

def main(table_name, input_file):
    print 'Loading from "{0}" into table `{1}`...'.format(input_file, table_name)

    start = getTime()
    data  = load(table_name, input_file)
    end   = getTime()

    print 'Done. Generated {0} pages in {1}s'.format(len(data), (end - start) / 1000.0)

if __name__ == '__main__':
    main('actions', 'data/Actions-2017-11-02.xml')

    print ''

    main('functions', 'data/Functions-2017-10-30.xml')
