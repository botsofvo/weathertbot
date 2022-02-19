from telegraph import Telegraph
import os
from dotenv import load_dotenv

load_dotenv()
telegraph = Telegraph(os.getenv('TELEGRAPH_API_KEY'))

def pagecreator(data):
    try:
        response = telegraph.create_page(
            '🌅Your weather forecast:',
            html_content=f'''{data}''',author_name="@weatherforecast4ubot",author_url="https://t.me/weatherforecast4ubot")
        return response['path']
    except:
        raise
        return "pls try after some time"
        
       
if __name__=="__main__":
    print(pagecreator("hello world"))
