#!/usr/bin/python3
"""
=============================== Markdown to HTML ===================================
"""
from sys import argv, stderr
import fnmatch
import re


def inline_tags(line, group):
    md_inline = {"**": "b", "__": "em"}
    line = line.replace(group, "<" + md_inline[group] + ">", 1)
    line = line.replace(group, "<" + "/" + md_inline[group] + ">", 1)
    return line

def markdown_to_html(argv):

    # Check if you write the argument
    if len(argv) < 3 or not fnmatch.fnmatchcase(argv[1], "*.md") \
            or not fnmatch.fnmatchcase(argv[2], "*.html"):
        stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    try:
        # Variables
        md = {1: "h1", 2: "h2", 3: "h3", 4: "h4", 5: "h5", 6: "h6", "-": "ul", "*": "ol"}
        Identifier = 0
        paragraph = 0
        inline = re.compile(".*([**].*[**]|[__].*[__]).*")

        # check if the file exist read and write file.
        with open(argv[2], "w+") as file_html, open(argv[1], "r") as file_md:
            readme = file_md.readlines()
            for i, line in enumerate(readme):
                while inline.match(line):
                    # print("called!")
                    match = inline.match(line)
                    # print(match, group)
                    line = inline_tags(line, match.group(1))
                    # print(line)

                # Change '#' with heading tag
                if len(line) - len(line.lstrip("#")) > 0:
                    tag = md[len(line) - len(line.lstrip("#"))]
                    # String without '#'
                    line = line.lstrip("# ")
                    # String without '\n'
                    line = line.rstrip("\n ")
                    file_html.write("<{}>".format(tag) + line + "</{}>\n".format(tag))

                #  Unordered and Ordered listing
                elif len(line)-len(line.lstrip('-*')) > 0:
                    # tag <ul>
                    tag = md[line[0]]
                    # String without '*- '
                    String_li = line.lstrip("*- ")
                    # String without '\n'
                    String_li = String_li.rstrip("\n ")

                    # write in html file tag <ul> or <ol> Start
                    if Identifier != 1:
                        file_html.write("<{}>\n".format(tag))
                        Identifier = 1

                    # write in html file tag <li> Start and final
                    file_html.write("<li>" + String_li + "</li>" + "\n")

                    # write in html file final tag </ul> or <ol>
                    if i == len(readme) - 1 or readme[i + 1][0] != line[0]:
                        file_html.write("</{}>\n".format(tag))
                        Identifier = 0

                # Paragraph  and single line break
                elif line.split(" ")[0] not in md:
                    if line[0] != "\n":
                        if paragraph != 1:
                            file_html.write("<p>\n")
                            paragraph = 1
                        file_html.write(line)
                        # if next line is part of the paragraph
                        if i != len(readme) - 1 and readme[i + 1][0] != "\n" and readme[i + 1][0] not in md:
                            file_html.write("<br/>\n")
                        else:
                            file_html.write("</p>\n")
                            paragraph = 0
        exit(0)
    except IOError:
        stderr.write("Missing {}\n".format(argv[1]))
    exit(1)


if __name__ == '__main__':
    markdown_to_html(argv)