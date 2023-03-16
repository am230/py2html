import typing
from dataclasses import dataclass

from flask import Flask, request
from py2js import js

from py2html.elements import body, button, div, head, html, input, title
from py2html.ext import SASS, Script, util

app = Flask(__name__)


this: object
window: object
fetch: object
JSON: object


class document:
    def getElementById(self, id: str): ...


@dataclass
class Message:
    ip: str
    content: str


messages = []


class MessageData(typing.TypedDict):
    content: str


@util.api(app, '/api/message', methods=['POST'])
def send_message():
    data: MessageData = request.json
    messages.append(Message(request.remote_addr, data['content']))
    return {}


def message_component(message: Message):
    return div(className='message')[
        div(className='username')[
            message.ip
        ],
        message.content
    ]


@app.route('/')
# @util.timer
def index():
    @js
    def main():
        async def button_clicked():
            message = document.getElementById('message')
            await send_message({
                'content': message.value
            })
            message.value = ''
            window.location.reload()

    return html(lang='en')[
        util.cache(lambda: head[
            title['Form'],
            SASS(href='styles_form.scss'),
            Script[send_message],
            Script[main]
        ]),
        body[
            div[
                div[
                    input(id='message', name='message', placeholder='...'),
                    button(onclick='button_clicked()')['>']
                ],
                div(className='message_container')[
                    *map(message_component, messages)
                ]
            ]
        ]
    ].render()


if __name__ == '__main__':
    app.run(debug=True, port=80)
