import random
from typing import Optional

err_emoticons = [
    "(´,_ゝ`)",
    "(´ﾟдﾟ`)",
    "(´･_･`)",
    "(´-ι_-｀)",
    "(ㆆᴗㆆ)"
]

success_emotions = [
    "(*‘ v`*)",
    "(^u^)",
    "(ﾉ>ω<)ﾉ",
    "(*´∀`)~♥",
    "ξ( ✿＞◡❛)"
]


class Emoticon:

    @staticmethod
    def err(msg: Optional[str]):
        if msg is None:
            return ""
        return f"{msg} {random.choice(err_emoticons)}"

    @staticmethod
    def success(msg: Optional[str]):
        if msg is None:
            return ""
        return f"{msg} {random.choice(success_emotions)}"
