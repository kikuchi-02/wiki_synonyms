from typing import Generator

import MeCab

# mecab = MeCab.Tagger('-Ochasen')
mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
# UnicodeDecodeErrorを避けることが出来る
mecab.parse('')


def extract_nouns(sentence: str) -> Generator[str, None, None]:
    parsed = (m.split() for m in mecab.parse(sentence).split('\n'))
    noun = map(lambda x: x[0],
               filter(lambda x: x and x[-1].startswith('名詞'), parsed))
    yield from noun
