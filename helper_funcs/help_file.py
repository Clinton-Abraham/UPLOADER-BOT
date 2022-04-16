import emoji
import re

def deEmojify(string):
    string = emoji.get_emoji_regexp().sub(u'', string)
    return re.sub(" +", " ", string)
