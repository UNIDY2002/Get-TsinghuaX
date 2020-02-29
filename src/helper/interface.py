import re
from os.path import join

from helper import version
from helper.grabber import User
from helper.searcher import Searcher


class Interface:
    def __init__(self, cookie: str):
        self.user = User(cookie)
        self.searcher = Searcher()
        self.searching = False

    def exec(self, command: str):
        stripped = command.strip()
        if ' ' in stripped:
            splitter = stripped.index(' ')
            header = stripped[0:splitter].lower()
            detail = stripped[splitter:].strip()
        else:
            header = stripped.lower()
            detail = ''
        if detail == '--help' and header != 'help':
            self.h(header)
        elif header == 'search':
            if self.searching:
                if detail == '':
                    self.searching = False
                    print('已退出搜索模式。')
                else:
                    print('请直接输入命令search以退出搜索模式。')
            else:
                self.searching = True
                print('已进入搜索模式。再次输入命令search即可退出搜索模式。')
                if detail != '':
                    self.s(detail)
        elif self.searching:
            self.s(command)
        else:
            if header == 'cookie':
                self.cookie(detail)
            elif header == 'gt':
                if detail == '':
                    self.gt()
                else:
                    self.h('gt')
            elif header == 'gc':
                if re.match('^[0-9]+$', detail):
                    self.gc(int(detail))
                else:
                    self.h('gc')
            elif header == 'gl':
                if re.match('^[0-9]+$', detail):
                    self.gl(int(detail))
                else:
                    self.h('gl')
            elif header == 'get':
                if detail == '.':
                    self.get()
                elif detail == '':
                    self.h('get')
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
                            self.h('get')
                    self.get(r)
            elif header == 's':
                if detail == '':
                    self.h('s')
                else:
                    self.s(detail)
            elif header == 'cd':
                if detail == '':
                    pass  # TODO
                else:
                    self.cd(detail)
            elif header == 'help':
                self.h(detail)
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

    def s(self, s: str):
        if self.searcher.path == '':
            print('正在当前目录下进行搜索...')
        else:
            print('正在目录 %s 下进行搜索...' % self.searcher.path)
        self.searcher.search(s,
                             lambda root, filename, line: print(root, filename, line, sep='\n'),
                             lambda root, filename, e: print("打开文件 %s 时发生异常：" % join(root, filename), e))

    def cd(self, directory: str):
        if self.searcher.cd(directory):
            if self.searcher.path == '':
                print('当前目录：磁盘根目录')
            else:
                print('当前目录：%s' % self.searcher.path)
        else:
            print('指定目录不存在。')

    @staticmethod
    def h(command: str):
        if command == '':
            print('''Get-TsinghuaX MOOC字幕抓取助手（版本号：%s）
你输入了命令"help"，因此你看到了全部命令的列表。
输入命令"help 命令名"，你可以进一步查看相应命令的用法。

gt      查看学期列表
gc      查看指定学期的课程列表
gl      查看指定课程的视频目录
get     批量下载指定视频的字幕
cookie  修改cookie

s       在字幕文件中搜索指定的字符串
search  进入/退出搜索模式''' % version)
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
                print('''gc: gc 学期号
    对于学期号指定的学期，获取相应的课程列表。
    
    例：
    >>> gc 1156
    8716    思想道德修养与法律基础 （2019秋）
    
    获得课程列表之后，你可以继续使用命令gl来获取视频目录。''')
            elif lower == 'gl':
                print('''gl: gl 课程号
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
                print('''get: get 参数片段... 或 get .
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
            elif lower == 's':
                print('''s: s 目标
    在当前目录下的全部文件中寻找目标字符串''')
            elif lower == 'search':
                print('''search: search
    进入/退出搜索模式
    进入搜索模式后，将直接对输入的内容进行搜索。''')
            else:
                print('未找到命令 %s' % command)


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
                      '    先进入 http://tsinghua.xuetangx.com 登录MOOC网站，\n'
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

        elif command.strip() != '':
            i = Interface(command)
    print('设置成功。输入help可查看更多帮助。')
    return i
