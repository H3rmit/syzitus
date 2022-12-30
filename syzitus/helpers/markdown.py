from .get import *

from mistletoe.span_token import SpanToken
from mistletoe.block_token import BlockToken
from mistletoe.html_renderer import HTMLRenderer
import os.path
from re import compile as re_compile, sub as re_sub

from flask import g

#preprocess re

enter_re=re_compile("(\n\r?\w+){3,}")



# add token/rendering for @username mentions


class UserMention(SpanToken):

    pattern = re_compile("(^|\s|\n)@(\w{3,25})")
    parse_inner = False

    def __init__(self, match_obj):
        self.target = (match_obj.group(1), match_obj.group(2))


class BoardMention(SpanToken):

    pattern = re_compile("(^|\s|\n)\+(\w{3,25})")
    parse_inner = False

    def __init__(self, match_obj):

        self.target = (match_obj.group(1), match_obj.group(2))

class ChatMention(SpanToken):

    pattern = re_compile("(^|\s|\n)#(\w{3,25})")
    parse_inner = False

    def __init__(self, match_obj):

        self.target = (match_obj.group(1), match_obj.group(2))
        
class Emoji(SpanToken):
    
    pattern=re_compile(":([A-Za-z0-9_-]+):")
    parse_inner=False
    
    def __init__(self, match_obj):
        self.target=match_obj.group(1)


class Spoiler(SpanToken):

    pattern=re_compile("(>!|<s>|\|\|)(.+?)(\|\||</s>|!<)")
    parse_inner=True

    def __init__(self, match_obj):

        self.target=match_obj.group(2)


class CodeBlockLanguage(BlockToken):
    pattern=re_compile("```(\w+)\n(.+)\n```")
    parse_inner=False

    def __init__(self, match_obj):
        self.target=(match_obj.group(1), match_obj.group(1))



# class OpMention(SpanToken):

#     pattern = re_compile("(^|\W|\s)@([Oo][Pp])\b")
#     parse_inner = False

#     def __init__(self, match_obj):
#         self.target = (match_obj.group(1), match_obj.group(2))


class CustomRenderer(HTMLRenderer):

    def __init__(self, **kwargs):
        super().__init__(UserMention,
                         BoardMention,
                         #ChatMention,
                         Emoji,
                         Spoiler,
                         CodeBlockLanguage
                         )

        for i in kwargs:
            self.__dict__[i] = kwargs[i]

    def render_user_mention(self, token):
        space = token.target[0]
        target = token.target[1]

        user = get_user(target, graceful=True)


        try:
            if g.user.admin_level == 0 and g.v.any_block_exists(user):
                return f"{space}@{target}"
        except BaseException:
            pass

        if (not user or (user.is_banned and not user.unban_utc) or user.is_deleted):
            return f"{space}@{target}"

        return f'{space}<a href="{user.permalink}" class="d-inline-block mention-user" data-original-name="{user.original_username}"><img src="{user.dynamic_profile_url}" class="profile-pic-20 mr-1">@{user.username}</a>'

    def render_board_mention(self, token):
        space = token.target[0]
        target = token.target[1]

        board = get_guild(target, graceful=True)

        if not board or board.is_banned:
            return f"{space}+{target}"
        else:
            return f'{space}<a href="{board.permalink}" class="d-inline-block"><img src="{board.dynamic_profile_url}" class="profile-pic-20 mr-1">+{board.name}</a>'

    def render_chat_mention(self, token):
        space = token.target[0]
        target = token.target[1]

        board = get_guild(target, graceful=True)

        if not board or board.is_banned:
            return f"{space}#{target}"
        else:
            return f'{space}<a href="{board.permalink}/chat" class="d-inline-block"><img src="/+{board.name}/pic/profile" class="profile-pic-20 mr-1">#{board.name}</a>'

    def render_emoji(self, token):
        
        name=token.target
        
        if os.path.isfile(f"{app.config['RUQQUSPATH']}/assets/images/emojis/{name}"):
            
            return f'<span data-toggle="tooltip" title=":{name}:"><img class="emoji" src="/assets/images/emojis/{name}"></span>'
        
        elif g.user.has_premium and os.path.isfile(f"{app.config['RUQQUSPATH']}/assets/images/primojis/{name}"):
            
            return f'<span data-toggle="tooltip" title=":{name}:"><img class="emoji" src="/assets/images/primojis/{name}"></span>'

        else:
            return f":{name}:"
        
    def render_spoiler(self, token):

        return f'<span class="spoiler">{token.target}</span>'

    def render_code_block_language(self, token):

        language=token.target[0]
        code=token.target[1]

        return f'<pre class="prettyprint lang-{language.lower()}>{code}</pre>">'
    
def preprocess(text):

    text=text.lstrip().rstrip()
    
    text=re_sub(enter_re, "\n\n", text)

    text=re_sub("(\u200b|\u200c|\u200d)",'', text)
    
    return text
    
