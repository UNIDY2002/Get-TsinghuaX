from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import json


class User:
    terms = None
    courses = None
    lessons = None

    def __init__(self, username, password):
        self.cookie = ""

    def get_terms(self):
        url = 'http://tsinghua.xuetangx.com/newcloud/api/filter/manager/terms/'
        headers = {
            'Cookie': self.cookie,
            'Referer': 'http://tsinghua.xuetangx.com/newcloud/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.130 Safari/537.36'
        }
        result = urlopen(Request(url, headers=headers)).read().decode()
        self.terms = json.loads(result)['list']
        return self.terms

    def get_courses(self, term_id):
        url = 'http://tsinghua.xuetangx.com/newcloud/api/studentcourse/?termid=%d' % term_id
        headers = {
            'Cookie': self.cookie,
            'Referer': 'http://tsinghua.xuetangx.com/newcloud/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.130 Safari/537.36'
        }
        result = urlopen(Request(url, headers=headers)).read().decode()
        self.courses = json.loads(result)['results']
        return self.courses

    def get_lessons(self, course_id):
        for course in self.courses:
            if course['id'] == course_id:
                url = 'http://tsinghua.xuetangx.com/courses/%s/courseware' % course['course_id']
                headers = {
                    'Cookie': self.cookie,
                    'Referer': 'http://tsinghua.xuetangx.com/newcloud/',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/79.0.3945.130 Safari/537.36'
                }
                result = urlopen(Request(url, headers=headers)).read().decode()
                soup = BeautifulSoup(result, 'html.parser')
                contents = soup.find(id='accordion').contents[1].contents[1::2]
                walk_id = 0
                lessons = []
                for unit in contents:
                    unit_title = unit.contents[1].get_text(strip=True)
                    unit_lessons_original = unit.contents[3].contents[1::2]
                    unit_lessons_parsed = []
                    for lesson in unit_lessons_original:
                        details = lesson.contents[1]
                        lesson_href = details['href']
                        lesson_name = details.contents[1].get_text(strip=True)
                        unit_lessons_parsed.append({'id': walk_id, 'name': lesson_name, 'href': lesson_href})
                        walk_id = walk_id + 1
                    lessons.append((unit_title, unit_lessons_parsed))
                    # print(unit_lessons_parsed)
                self.lessons = lessons
                return lessons
        return []
