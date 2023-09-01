import os
import urllib.request
import csv
from html.parser import HTMLParser
import shutil

files = [
    "D:/830程序设计基础/作业1网页/副教授-数字媒体与设计艺术学院.html",
    "D:/830程序设计基础/作业1网页/讲师-数字媒体与设计艺术学院.htm",
    "D:/830程序设计基础/作业1网页/教授-数字媒体与设计艺术学院.htm"
]
output = "teacher_info.csv"

base_urls = [
    'file:///D:/830%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%E5%9F%BA%E7%A1%80/%E4%BD%9C%E4%B8%9A1%E7%BD%91%E9%A1%B5/%E5%89%AF%E6%95%99%E6%8E%88-%E6%95%B0%E5%AD%97%E5%AA%92%E4%BD%93%E4%B8%8E%E8%AE%BE%E8%AE%A1%E8%89%BA%E6%9C%AF%E5%AD%A6%E9%99%A2_files/',
    'file:///D:/830程序设计基础/作业1网页/讲师-数字媒体与设计艺术学院_files/',
    'file:///D:/830程序设计基础/作业1网页/教授-数字媒体与设计艺术学院_files/'
]


# 下载图片
def download_images(files, base_urls):
    class TeacherImageParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.teacher_images = []

        def handle_starttag(self, tag, attrs):
            if tag == 'img':
                for attr in attrs:
                    if attr[0] == 'src' and '.jpg' in attr[1]:
                        self.teacher_images.append(attr[1].split('/')[-1])

        def get_teacher_images(self):
            return self.teacher_images

    for file, base_url in zip(files, base_urls):
        with open(file, 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()

        parser = TeacherImageParser()
        parser.feed(html_content)

        for image in parser.get_teacher_images():
            image_url = base_url + image
            try:
                urllib.request.urlretrieve(image_url, image)
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    print(f"图片 {image_url} 不存在")
                else:
                    print(f"下载图片 {image_url} 时发生错误: {e}")
            except urllib.error.URLError as e:
                print(f"下载图片 {image_url} 时发生错误: {e}")


# 爬取并处理教师信息
def crawl_html_files(files):
    class Parser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.data = []
            self.is_name = False
            self.is_department = False

        def handle_starttag(self, tag, attrs):
            if tag == 'span':
                for attr in attrs:
                    if attr[1] == 'name':
                        self.is_name = True
                    elif attr[1] == 'iden':
                        self.is_department = True

        def handle_endtag(self, tag):
            if tag == 'span':
                self.is_name = False
                self.is_department = False

        def handle_data(self, data):
            if self.is_name:
                self.data.append(("Department", data.strip(), title))
            elif self.is_department and self.data:
                self.data[-1] = (self.data[-1][1], data.strip(), self.data[-1][2])

    data = []
    for file in files:
        title = file.split('-')[0].replace("D:/830程序设计基础/作业1网页/", "")
        parser = Parser()
        with open(file, 'r', encoding='utf-8') as html_file:
            parser.feed(html_file.read())
        data.extend(parser.data)
    return data


def write_csv(data, output):
    with open(output, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Name", "Department", "Title"])
        writer.writerows(data)


download_images(files, base_urls)
data = crawl_html_files(files)
write_csv(data, output)

# 爬取并处理教师姓名
def get_teacher_names(files):
    class Parser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.names = []
            self.is_name = False

        def handle_starttag(self, tag, attrs):
            if tag == 'span':
                for attr in attrs:
                    if attr[1] == 'name':
                        self.is_name = True

        def handle_endtag(self, tag):
            if tag == 'span':
                self.is_name = False

        def handle_data(self, data):
            if self.is_name:
                self.names.append(data.strip())

    names = []
    for file in files:
        parser = Parser()
        with open(file, 'r', encoding='utf-8') as html_file:
            parser.feed(html_file.read())
        names.extend(parser.names)
    return names

names = get_teacher_names(files)
stroage_paths = ['Photo']
for name in names:
    stroage_path = 'D:\\831程序设计实践\\' + name + '.jpg'
    stroage_paths.append(stroage_path)

# 写入储存路径
def write_column(csv_file, column_data):
    # 打开CSV文件并读取数据
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
    # 将列数据添加到数据列表中
    for i in range(len(data)):
        data[i].append(column_data[i])
    # 写入更新后的数据到CSV文件
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

temp_csv = 'D:/831程序设计实践/teacher_info.csv'  # CSV文件路径
column_data = stroage_paths  # 要写入的列数据
write_column(temp_csv, column_data)




