import re

_no_period_re = re.compile(r'(No[.])(?=[ ]?[0-9])')
_percent_re = re.compile(r'([ ]?[%])')
_half_re = re.compile('([0-9]½)|(½)')
_url_re = re.compile(r'([a-zA-Z])\.(com|gov|org)')


# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
    ('mrs', 'misess'),
    ('ms', 'miss'),
    ('mr', 'mister'),
    ('dr', 'doctor'),
    ('st', 'saint'),
    ('co', 'company'),
    ('jr', 'junior'),
    ('maj', 'major'),
    ('gen', 'general'),
    ('drs', 'doctors'),
    ('rev', 'reverend'),
    ('lt', 'lieutenant'),
    ('hon', 'honorable'),
    ('sgt', 'sergeant'),
    ('capt', 'captain'),
    ('esq', 'esquire'),
    ('ltd', 'limited'),
    ('col', 'colonel'),
    ('ft', 'fort'),
    ('sen', 'senator'),
    ('etc', 'et cetera'),
]]

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations_vi = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
    ('btc', 'ban tổ chức'),
    ('clb', 'câu lạc bộ'),
    ('htx', 'hợp tác xã'),
    ('nxb', 'nhà xuất bản'),
    ('ôb', 'ông bà'),
    ('tp', 'thành phố'),
    ('tt', 'tổng thống'),
    ('ttg', 'thủ tướng'),
    ('tw', 'trung ương'),
    ('ubnd', 'ủy ban nhân dân'),
    ('bch', 'ban chấp hành'),
    ('chxhcnvn', 'cộng hòa xã hội chủ nghĩa việt nam'),
    ('mtdtgpmnvn', 'mặt trận dân tộc giải phóng miền nam việt nam'),
    ('qdnd', 'quân đội nhân dân việt nam'),
    ('qđnd', 'quân đội nhân dân việt nam'),
    ('vn', 'việt nam'),
    ('qlvnch', 'quân lực việt nam cộng hòa'),
    ('vnqdđ', 'việt nam quốc dân đảng'),
    ('vnqdd', 'việt nam quốc dân đảng'),
    ('vnch', 'việt nam cộng hòa'),
    ('vndcch', 'việt nam dân chủ cộng hòa'),
    ('lhq', 'liên Hợp quốc'),
    ('thpt', 'trung học phổ thông'),
    ('thcs', 'trung học cơ sở'),
    ('đ/c', 'địa chỉ'),
    ('k/g', 'kính gửi'),
    ('th/g', 'thân gửi'),
    ('v/v', 'về việc'),
    ('tr', 'trang'),
    ('dc', 'được'),
    ('đc', 'được'),
    ('cty', 'công ty'),
    ('ngta', 'người ta'),
    ('tv', 'ti vi'),
]]


def _expand_no_period(m):
    word = m.group(0)
    if word[0] == 'N':
        return 'Number'
    return 'number'


def _expand_percent(m):
    return ' percent'


def _expand_half(m):
    word = m.group(1)
    if word is None:
        return 'half'
    return word[0] + ' and a half'


def _expand_urls(m):
    return f'{m.group(1)} dot {m.group(2)}'


def normalize_abbreviations(text):
    text = re.sub(_no_period_re, _expand_no_period, text)
    text = re.sub(_percent_re, _expand_percent, text)
    text = re.sub(_half_re, _expand_half, text)
    text = re.sub('&', ' and ', text)
    text = re.sub('@', ' at ', text)
    text = re.sub(_url_re, _expand_urls, text)

    for regex, replacement in _abbreviations:
        text = re.sub(regex, replacement, text)
    return text

def expand_abbreviations_vi(text):
    for regex, replacement in _abbreviations_vi:
        text = re.sub(regex, replacement, text)
    return text