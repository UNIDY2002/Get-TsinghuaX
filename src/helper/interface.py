import re

from helper import version
from helper.grabber import User


class Interface:
    def __init__(self, cookie: str):
        self.user = User(cookie)

    def exec(self, command: str):
        command = command.strip()
        if ' ' in command:
            splitter = command.index(' ')
            header = command[0:splitter].lower()
            detail = command[splitter:].strip()
        else:
            header = command.lower()
            detail = ''
        if detail == '--help' and header != 'help':
            h(header)
        else:
            if header == 'cookie':
                self.cookie(detail)
            elif header == 'gt':
                if detail == '':
                    self.gt()
                else:
                    h('gt')
            elif header == 'gc':
                if re.match('^[0-9]+$', detail):
                    self.gc(int(detail))
                else:
                    h('gc')
            elif header == 'gl':
                if re.match('^[0-9]+$', detail):
                    self.gl(int(detail))
                else:
                    h('gl')
            elif header == 'get':
                if detail == '.':
                    self.get()
                elif detail == '':
                    h('get')
                else:
                    r = []
                    for frag in detail.split(','):
                        frag = re.sub('\\s', '', frag)
                        if re.match('^[0-9]+$', frag):
                            r.append(int(frag))
                        elif re.match('^[0-9]+-[0-9]+$', frag):
                            s = frag.split('-')
                            beg = int(s[0])
                            end = int(s[1])
                            if beg <= end:
                                r.extend(range(beg, end + 1))
                        else:
                            h('get')
                    self.get(r)
            elif header == 'help':
                h(detail)
            elif header != '':
                print('未找到命令 %s' % header)

    def cookie(self, cookie: str):
        self.user.cookie = cookie

    def gt(self):
        print('\n'.join(map(lambda term: "%-8d%s" % (term['id'], term['name']), self.user.get_terms())))

    def gc(self, term_id: int):
        print('\n'.join(map(lambda course: "%-8d%s" % (course['id'], course['name']), self.user.get_courses(term_id))))

    def gl(self, course_id: int):
        lessons = self.user.get_lessons(course_id)
        for title, lesson_list in lessons:
            print(title)
            print('\n'.join(map(lambda lesson: "    %-4d%s" % (lesson['id'], lesson['name']), lesson_list)))

    def get(self, r: list = range(0, 1000)):  # Assumes that there are no more than 1000 lessons
        self.user.get_subtitle(r,
                               lambda lesson: print('正在下载 %s ...' % lesson['name']),
                               lambda lesson: print('下载成功'),
                               lambda lesson, e: print('下载失败'))


def h(command: str):
    if command == '':
        print('''Get-TsinghuaX MOOC字幕抓取助手（版本号：%s）
你输入了命令"help"，因此你看到了全部命令的列表。
输入命令"help 命令名"，你可以进一步查看相应命令的用法。

gt      查看学期列表
gc      查看指定学期的课程列表
gl      查看指定课程的视频目录
get     批量下载指定视频的字幕
cookie  修改cookie''' % version)
    else:
        lower = command.lower()
        if lower == 'gt':
            print('''gt: gt
    查看所有学期的列表。
    
    例：
    >>> gt
    1641    2020春
    1156    2019秋
    796     2019春
    371     2018秋
    153     2018春
    24      2017秋
    
    获得学期列表之后，你可以继续使用命令gc来获取课程列表。''')
        elif lower == 'gc':
            print('''gc: gc [学期号]
    对于学期号指定的学期，获取相应的课程列表。
    
    例：
    >>> gc 1156
    8716    思想道德修养与法律基础 （2019秋）
    
    获得课程列表之后，你可以继续使用命令gl来获取视频目录。''')
        elif lower == 'gl':
            print('''gl: gl [课程号]
    对于课程号指定的课程，获取相应的课程目录。
    
    例：
    >>> gl 8716
    绪论
        0   开篇的话
        1   0.1 认识大学生活特点，提高独立生活能力
        2   0.2 树立新的学习理念，养成优良的学风
        3   0.3 确立成才目标，塑造新的形象
    第一章 人生的青春之问
        4   第一节 树立正确的人生观
    ...
    
    获得视频目录之后，你可以继续使用命令get来下载视频字幕。''')
        elif lower == 'get':
            print('''get: get [参数片段 ...] 或 get .
    下载参数片段列表指定的视频字幕，或一次性下载课程的全部字幕。
    
    说明：
    参数片段之间用,隔开。
    每个参数片段为以下两种形式之一：
      - 序号
      - 始序号-末序号
    其中，“始序号-末序号”是闭区间。
    
    注：所有符号均为半角字符。
    
    例：
    >>> get 0, 2-4, 6
        # 下载0、2、3、4、6号视频的字幕
    >>> get .
        # 下载全部视频的字幕''')
        elif lower == 'cookie':
            print('''cookie: cookie 字符串
    将cookie设置为指定字符串''')


def instruct() -> Interface:
    print('Get-TsinghuaX MOOC字幕抓取助手（版本号：%s）' % version)
    i = None
    while i is None:
        print('请输入cookies（输入help查看帮助）：')
        command = input('>>> ').strip()

        if command.lower() == 'help':
            while command not in {'0', '1', '2'}:
                print('您的操作系统是：\n'
                      '    0   Windows\n'
                      '    1   Mac\n'
                      '    2   Linux')
                command = input('>>> ').strip()
            os = int(command)

            if os == 2:
                print('我认为您具备独立完成以下操作的能力：\n'
                      '    先进入 http://tsinghua.xuetangx.com/ 登录MOOC网站，\n'
                      '    然后获取该站点下的cookie值即可。')
                continue

            command = ''
            while command not in {'0', '1', '2'}:
                print('您的浏览器是：\n'
                      '    0   谷歌 Chrome\n'
                      '    1   火狐 Firefox\n'
                      '    2   苹果 Safari')
                command = input('>>> ').strip()
            browser = int(command)

            print('先进入 http://tsinghua.xuetangx.com/ 登录MOOC网站，')
            hint = [
                '然后在该页面按下组合键Ctrl + Shift + J，',
                '然后在该页面按下组合键Ctrl + Shift + K，',
                '然后在该页面按下组合键Ctrl + Alt + C，',
                '然后在该页面按下组合键⌘⌥J',
                '然后在该页面按下组合键⌘⌥K',
                '然后在该页面按下组合键⌘⌥C'
            ]
            print(hint[os * 3 + browser])
            print('在跳出的Console（控制台）对话框中，输入命令')
            print('document.cookie')
            print('将得到的一长串结果（不含首末引号）粘贴在这里即可。')

        else:
            i = Interface(command)
    print('设置成功。输入help可查看更多帮助。')
    return i
