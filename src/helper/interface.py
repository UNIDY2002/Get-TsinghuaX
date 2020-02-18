import re

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
        if header == 'cookie':
            self.cookie(detail)
        elif header == 'gt':
            self.gt()
        elif header == 'gc':
            self.gc(int(detail))
        elif header == 'gl':
            self.gl(int(detail))
        elif header == 'get':
            if detail == '.' or detail == '':
                self.get()
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
                self.get(r)

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


def instruct() -> Interface:
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
    return i
