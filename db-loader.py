import sqlite3
import sys
import time
import xml.etree.ElementTree as ET

def getTime():
    return int(round(time.time() * 1000))

def parseContent(input):
    char_mappings = {
        '\'': '&#39;',
        '"': '&quot;',
    }

    # convert to utf-8
    output = ''.join([i if ord(i) < 128 else ' ' for i in input])

    output = output.replace('\n;', '\n')

    for key in char_mappings:
        output = output.replace(key, char_mappings[key])

    # headings mappings
    output = output.replace('=====\n', '</h5>')
    output = output.replace('=====', '<h5>')
    output = output.replace('====\n', '</h4>')
    output = output.replace('====', '<h4>')
    output = output.replace('===\n', '</h3>')
    output = output.replace('===', '<h3>')
    output = output.replace('==\n', '</h2>')
    output = output.replace('==', '<h2>')

    output = output.replace('\n\n', '<br /><br />')

    return output

def loadPages(root):
    data = []

    for page in root.findall('{http://www.mediawiki.org/xml/export-0.8/}page'):
        title = page.findall('{http://www.mediawiki.org/xml/export-0.8/}title')[0].text
        title = ''.join([i if ord(i) < 128 else ' ' for i in title])
        title = title.replace('Function Reference/', '')
        title = title.replace(' ', '_')

        revisions = page.findall('{http://www.mediawiki.org/xml/export-0.8/}revision')

        content = revisions[0].findall('{http://www.mediawiki.org/xml/export-0.8/}text')[0].text
        content = parseContent(content)

        data.append({ 'title': title, 'content': content })

    return data

def saveToDB(data):
    conn = sqlite3.connect('data/wordpress.sqlite')
    cur  = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS `functions` (`title` text, `content` text)')
    cur.execute('DELETE FROM `functions`')

    for row in data['functions']:
        cur.execute('INSERT INTO `functions` VALUES ("{0}", "{1}")'.format(row['title'], row['content']))

    conn.commit()
    conn.close()

def main(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    data = { 'functions': loadPages(root) }

    saveToDB(data)

    return data

if __name__ == '__main__':
    print 'Loading from "{0}...'.format(sys.argv[1])

    start = getTime()
    data  = main(sys.argv[1])
    end   = getTime()

    print 'Done. Generated {0} pages in {1}s'.format(len(data['functions']), (end - start) / 1000.0)
