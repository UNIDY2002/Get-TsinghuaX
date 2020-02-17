from helper.grabber import User


class Interface:
    def __init__(self, username, password):
        self.user = User(username, password)

    def execute(self, command):
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

    def cookie(self, cookie):
        self.user.cookie = cookie

    def gt(self):
        print('\n'.join(map(lambda term: "%-8d%s" % (term['id'], term['name']), self.user.get_terms())))

    def gc(self, term_id):
        print('\n'.join(map(lambda course: "%-8d%s" % (course['id'], course['name']), self.user.get_courses(term_id))))

    def gl(self, course_id):
        lessons = self.user.get_lessons(course_id)
        for title, lesson_list in lessons:
            print(title)
            print('\n'.join(map(lambda lesson: "    %-4d%s" % (lesson['id'], lesson['name']), lesson_list)))
