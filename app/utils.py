import re

def markup_to_html(text):
    #image
    pattern=re.compile(r'\*img\*(.*?)\*img\*')
    text=pattern.sub(r'<img src="static/upload/\1">',text)
    #bold
    pattern=re.compile(r'\*b\*(.*?)\*b\*')
    text=pattern.sub(r'<strong>\1</strong>',text)
    #italic
    pattern=re.compile(r'\*i\*(.*?)\*i\*')
    text=pattern.sub(r'<em>\1</em>',text)
    #underline
    pattern=re.compile(r'\*u\*(.*?)\*u\*')
    text=pattern.sub(r'<u>\1</u>',text)
    #linebreak
    # text=re.sub(r'\n','<br>',text)
    return text

img_size=(1280,800)
thumbnail_size=(120,90)
