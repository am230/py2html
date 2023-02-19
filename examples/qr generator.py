import base64
import typing
from io import BytesIO

import qrcode
from flask import Flask, request
from py2js import js
from qrcode.image.pil import PilImage

from py2html.elements import body, button, div, head, html, img, input, title
from py2html.ext import SASS, Script, util

app = Flask(__name__)


this: object
window: object
fetch: object
JSON: object


class document:
    def getElementById(self, id: str): ...

class RequestData(typing.TypedDict):
    content: str


@util.api(app, '/api/generate', json=False, methods=['POST'])
def generate_qr():
    data: RequestData = request.json
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        image_factory=PilImage
    )
    qr.add_data(data['content'])
    qr.make(fit=True)

    image = qr.make_image(fill_color='#3da0b4', back_color="white")

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return b'data:image/png;base64,' + img_str


@app.route('/')
def index():
    @js
    def main():
        async def generate():
            data = document.getElementById('qr_data')
            image = document.getElementById('result')
            await generate_qr({
                'content': data.value
            })\
                .then(lambda response: response.text())\
                .then(lambda text: image.setAttribute('src', text))

    return html(lang='en')[
        util.cache(lambda: head[
            title['QR Code Generator'],
            SASS(href='styles_qr.scss'),
            Script[generate_qr],
            Script[main]
        ]),
        body[
            div(className='container')[
                div[
                    input(id='qr_data', name='qr_data', placeholder='data here'),
                    button(onclick='generate()')['>']
                ],
                img(id='result', src='', title='')
            ]
        ]
    ].render()


if __name__ == '__main__':
    app.run(debug=True, port=80)
