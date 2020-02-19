import json
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup

from helper.io import save


class User:
    terms = None
    term = None
    courses = None
    course = None
    lessons = None

    def __init__(self, cookie: str):
        """
        Initializes the user with the given cookie.

        :param cookie: the cookie to initialize the user with
        """
        self.cookie = cookie

    def __connect(self, url: str) -> str:
        """
        Makes an HTTP request to the given url with the specified cookie, and returns the
        response body as a string.

        :param url: the url to connect to
        :return: the response body
        """
        headers = {
            'Cookie': self.cookie,
            'Referer': 'http://tsinghua.xuetangx.com/newcloud/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.130 Safari/537.36'
        }
        return urlopen(Request(url, headers=headers)).read().decode()

    def get_terms(self) -> list:
        """
        Gets the list of terms, saves it as the context and returns it to the caller.

        :return: the list of terms
                 Each term is a dictionary with the following keys: id and name.
        """
        result = self.__connect('http://tsinghua.xuetangx.com/newcloud/api/filter/manager/terms/')
        self.terms = json.loads(result)['list']
        return self.terms

    def get_courses(self, term_id: int) -> list:
        """
        Gets the list of courses, saves it as the context and returns it to the caller.

        :param term_id: the id of the corresponding term
        :return: the list of courses
                 Each course is a dictionary with the following keys: id, name, course_id,
                 thumbnail, status, credit, plat_id, term, start, end, term_start,
                 term_end, courseware_url, schedule, unsubscribe, downloadable, has_book,
                 creditcast, castcount, castliving and elective.

                 **NOTE THAT IT IS `id` RATHER THAN `course_id` THAT IS USED IN METHOD
                 `get_lessons` FOR COURSE IDENTIFICATION.**
        """
        for term in self.terms:
            if term['id'] == term_id:
                result = self.__connect('http://tsinghua.xuetangx.com/newcloud/api/studentcourse/?termid=%d' % term_id)
                self.courses = json.loads(result)['results']
                self.term = term
        return self.courses

    def get_lessons(self, course_id: int) -> list:
        """
        Gets the list of lessons, saves it as the context and returns it to the caller.

        :param course_id: the id of the corresponding course
        :return: the list of lessons
                 Actually, the return value is a list of units.
                 A unit is a pair of str and list. The str refers to the name of the unit,
                 and the list refers to the list of lessons in the unit.
                 Each lesson is a dictionary with the following keys: id, name and href.
        """
        for course in self.courses:
            if course['id'] == course_id:
                result = self.__connect('http://tsinghua.xuetangx.com%s' % course['courseware_url'])
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
                self.lessons = lessons
                self.course = course
                return lessons
        self.lessons = []
        return []

    def get_subtitle(self, r: list, on_beg=None, on_end=None, on_err=None):
        """
        Gets the subtitles of the requested lessons as are described in the given list,
        and saves them in the disk.

        :param r: the list of lessons to get subtitles from
        :param on_beg: the function to call on the beginning of each download
        :param on_end: the function to call on the end of each download
        :param on_err: the function to call on error of each download
        """
        for title, lesson_list in self.lessons:
            for lesson in lesson_list:
                index = lesson['id']
                if index in r:
                    if on_beg:
                        on_beg(lesson)
                    try:
                        result = self.__connect('http://tsinghua.xuetangx.com%s' % lesson['href'])
                        soup = BeautifulSoup(result, 'html.parser')
                        data = soup.find(id='seq_contents_0').contents[0]
                        start = data.index('data-transcript-translation-url') + 33
                        end = data.index('"', start)
                        result = self.__connect('http://tsinghua.xuetangx.com%s/zh' % data[start:end])
                        data = '\n'.join(json.loads(result)['text'])
                        save("%s/%s/%s" % (self.term['name'], self.course['name'], title), index, lesson['name'], data)
                        if on_end:
                            on_end(lesson)
                    except Exception as e:
                        if on_err:
                            on_err(lesson, e)
