# from lxml.html import fromstring
# from py2xml import util

# print(util.generate_code(fromstring('''
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta http-equiv="X-UA-Compatible" content="IE=edge">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>py2html<title>
# </head>
# <body>
#     <h1>Hello, Py2HTML!</h1>
# </body>
# </html>
# ''')))

from py2html.elements import html, head, body, meta, title, h1


print(
    html(lang="en")[
        head[
            meta(charset="UTF-8"),
            meta({"http-equiv": "X-UA-Compatible", "content": "IE=edge"}),
            meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            title["py2html"]
        ],
        body[
            h1[
                "Hello, Py2HTML!"
            ]
        ]
    ].render()
)
