# Get-TsinghuaX

The subtitle grabber for TsinghuaX MOOC platform.

Chinese-version README follows the English-version.

[点击链接跳转至中文使用说明](#中文使用说明)

## Usage

### Interactive user interface

Run `main.py` to launch the interactive user interface.

For Windows users, you can also get the `.exe` file in the [release](https://github.com/UNIDY2002/Get-TsinghuaX/releases) page.

#### Login

In current version, simulated-login is not available, so an alternative method of using cookie to login is applied.

To get the cookie to login:

1. Manually login at [http://tsinghua.xuetangx.com/](http://tsinghua.xuetangx.com/) in your browser.
2. Open the developer's tool, and switch to `console` page.
3. Enter command `document.cookie`.

And the cookie shall be returned by the `console` of your browser.

#### Main

Commands currently available are listed as below:

- `gt`
  - Get the term list.
- `gc ${term_id}`
  - Get the course list of the specified term.
- `gl ${course_id}`
  - Get the lesson list of the specified course.
- `get ${param_fragment...}` or `get .`
  - Get the subtitles as are described in the `param_fragment` list, or get all the subtitles of the specified course.
- `cookie ${data}`
  - Reset the cookie data.

Detailed descriptions can be obtained at runtime by entering `help ${command_name}` .

### Core library

An easy way of getting the core library is simply including the `helper` package in your project.

I might probably upload the package to PyPI later on.

#### __init__.py

Currently, it only has a version data.

#### grabber.py

The module related to grabbing data from TsinghuaX.

```python
class User:
 |
 | # Context
 |-- terms    # Current term list
 |-- term     # Current term
 |-- courses  # Current course list
 |-- course   # Current course
 |-- lessons  # Current lesson list
 |
 | # Login-related
 |-- cookie   # Defined in __init__
 |
 | # Public methods
 |-- get_terms(self) -> list
 |-- get_courses(self, term_id: int) -> list
 |-- get_lessons(self, course_id: int) -> list
 |-- get_subtitle(self, r: list, on_beg=None, on_end=None, on_err=None)
 |            # on_beg, on_end and on_err serve as callback functions
 |
 | # Private method
 |-- __connect(self, url: str) -> str
```

Documents are available in the source file.

#### interface.py

The module related to the interactive user interface.

Each instantiated interface wraps in it a logged-in user.

**Of course, it is not a necessity that you import this module in your own project.**

```python
class Interface:
 |
 |-- user     # Defined in __init__
 |
 |-- exec(self, command: str)
 |
 |-- gt(self)
 |-- gc(self, term_id: int)
 |-- gl(self, course_id: int)
 |-- get(self, r: list = range(0, 1000))
 |-- cookie(self, cookie: str)

h(command: str)

instruct() -> Interface
```

#### io.py

This module serves as a inner util module.

Currently, only a method `save(path: str, walk_id: int, name: str, data: str)` is included.

This method creates a file at `path` with the filename of `"%03d. %s.txt" % (walk_id, name)` and writes `data` into it.

#### searcher.py

There is nothing in it yet.


## Dependencies
 - beautifulsoup4

## Changelog

- v0.1.0
  - First release.
  - Support the core function of grabbing the subtitles, along with term-list and course-list query.

## License

// TODO

## 中文使用说明

这是Get-TsinghuaX MOOC字幕抓取助手。

在这份说明中，我将介绍交互式用户界面的使用方法。至于如何在自己的项目中使用核心库，请参阅[英文说明](#Core-library)。

### 开始使用

#### 直接下载可执行文件

[下载页面](https://github.com/UNIDY2002/Get-TsinghuaX/releases)

目前仅支持Windows系统。

#### 执行Python源代码

运行`main.py`来启动交互式用户界面。

你可能需要先安装`beautifulsoup4`第三方库。

### 登录

由于我还没搞定模拟登录，目前只能通过手动设置cookie凑合一下。

获取cookie的步骤如下：

1. 进入[http://tsinghua.xuetangx.com/](http://tsinghua.xuetangx.com/)登录MOOC网站；
2. 打开开发者工具，进入`Console`（控制台）页面；
3. 输入命令`document.cookie`，即可得到cookie值（不含首末引号）。

### 主体部分

以下是当前可用的全部命令：

- `gt`：查看学期列表
- `gc`：查看指定学期的课程列表
- `gl`：查看指定课程的视频目录
- `get`：批量下载指定视频的字幕
- `cookie`：修改cookie

你可以在运行时输入`help 命令名称`来查看相应命令的具体用法。

### 示例

```
>>> gt
1641    2020春
1156    2019秋
796     2019春
371     2018秋
153     2018春
24      2017秋
>>> gc 1156
8716    思想道德修养与法律基础 （2019秋）
>>> gl 8716
绪论
    0   开篇的话
    1   0.1 认识大学生活特点，提高独立生活能力
    2   0.2 树立新的学习理念，养成优良的学风
    3   0.3 确立成才目标，塑造新的形象
第一章 人生的青春之问
    4   第一节 树立正确的人生观
...
>>> get 0, 2-4, 6
    # 下载0、2、3、4、6号视频的字幕
>>> get .
    # 下载全部视频的字幕
```
