from telegraph import Telegraph
import os

telegraph = Telegraph(os.getenv('TELEGRAPH_API_KEY'))

def pagecreator(data):
    try:
        response = telegraph.create_page(
            '🌅Your weather forecast:',
            html_content=f'''<p>{data}</p>''')
        return response['url']
    except:
        return "pls try after some time"

