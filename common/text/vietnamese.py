import re
from pathlib import Path

valid_symbols_vi = ['ɪ', '6', 'm', 'ă', 'iə', 'ɤ', 'k͡p', 'ʷe', 'ʐw', 'fw', 'hw', 'tʃ', 'bw', 'ʷɤ̆', "'", 't', 'u', 'ʷi', '2', 'r', 'v', 'jw', 'g', 'ɛ', 'ɛ_1', 'ə', 'ɯ', 'cw', 'ɛu', 'ʈ', 'd', 'ʤ', 'l_ɔ_ŋ͡m_1', 'j', 'tʰw', 'ɲw', '5', 'ʐ', 'ʂ', 'ɣw', 'ɔ', 'ʒ', 'ŋw', 'eo', 'sw', 'ʧ', 'p', 'vw', 'ŋ', 'ɣ', 'ʷă', 'o', 'ʷɛ', 'i', 'zw', '4', 'tw', 'mw', '3', 's', 'f', '1', 'ʃ', 'ɲ', 'æ', 'ʂw', 'ɯə', 'h', 'b', 'k', 'dw', 'ʈw', 'c', 'a', 'ʷiu', 'ʷiə', 'l', 'w', 'θ', 'ʌ', 'xw', 'uə', 'ʊ', 'e', 'nw', 'ð', 'n', 'lw', 'tʰ', 'kw', 'x', 'ŋ͡m', 'z', 'ʂ_ɔ_1', 'iɛ', 'ʷa', 'ɤ̆']

valid_symbol_set = set(valid_symbols_vi)

_alt_re = re.compile(r'\([0-9]+\)')

def _get_pronunciation(s):
  parts = s.strip().split(' ')
  for part in parts:
    if part not in valid_symbol_set:
      return None
  return ' '.join(parts)

def _parse_vnipa(file):
  cmudict = {}
  for line in file:
    if len(line):
      parts = line.split('  ')
      word = re.sub(_alt_re, '', parts[0])
      pronunciation = _get_pronunciation(parts[1])
      if pronunciation:
        if word in cmudict:
          cmudict[word].append(pronunciation)
        else:
          cmudict[word] = [pronunciation]
  return cmudict

class VNDict:
  '''Thin wrapper around vnIPA data, mostly from CMUDict wrapper. http://www.speech.cs.cmu.edu/cgi-bin/cmudict'''
  def __init__(self, file_or_path="cmudict/vnIPA.dict", keep_ambiguous=True):
    self._entries = {}
    self.heteronyms = []
    if file_or_path is not None:
      self.initialize(file_or_path, keep_ambiguous)

  def initialize(self, file_or_path, keep_ambiguous=True):
    if isinstance(file_or_path, str):
      if not Path(file_or_path).exists():
        raise FileNotFoundError
      print(file_or_path)
      with open(file_or_path, encoding='utf-8') as f:
        entries = _parse_vnipa(f)

    else:
      entries = _parse_vnipa(file_or_path)


    if not keep_ambiguous:
      entries = {word: pron for word, pron in entries.items() if len(pron) == 1}
    self._entries = entries

  def __len__(self):
    if len(self._entries) == 0:
      raise ValueError("VNDict not initialized")
    return len(self._entries)

  def lookup(self, word):
    '''Returns list of IPA pronunciations of the given word.'''
    if len(self._entries) == 0:
      raise ValueError("VNDict not initialized")
    return self._entries.get(word.lower())