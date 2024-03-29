import argparse
from itertools import chain
from collections import Counter

# Arguments.
parser = argparse.ArgumentParser(description=
  'Read corpora, and generate'
  ' (1) Vocabulary file, sorted by frequency.'
  ' (2) Alphabet file.'
  ' (3) Frequencey file, containing frequencies of each word. ',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    '--corpus_prefix',
    type=str,
    required=True,
    help='Corpora prefix. '
    'The input path will be "<corpus_prefix>.<lang_extension>.<lang>", '
    'and the output path will be "<corpus_prefix>.<lang_extension>.<info>.<lang>". '
    'If any field is missing, it will be ignored.'
)
parser.add_argument(
    '--lang_extensions',
    type=str,
    help='Language extensions. See documentation of --corpus_prefix for details.',
    nargs='+',
    default=['stanford.clean', 'clean']
)
parser.add_argument(
    '--langs',
    type=str,
    help='Language suffixes. See documentation of --corpus_prefix for details.',
    nargs='+',
    default=['ara', 'eng']
)
parser.add_argument(
    '--freq_delim',
    type=str,
    help='String to use as a delimiter between words and their respective '
    'counts in the frequency file.',
    default=' '
)
args = parser.parse_args()

def preprocess_args():
  assert len(args.langs) == len(args.lang_extensions)
  args.lang_extensions = {lang: lang_extension for lang, lang_extension in zip(args.langs, args.lang_extensions)}

def main():
  preprocess_args()
  for lang in args.langs:
    lang_extension = args.lang_extensions[lang]
    print('Processing language %s.' % lang)

    # Extract Info.
    print('Extracting Vocabulary.')
    with open('.'.join(filter(None, [args.corpus_prefix, lang_extension, lang]))) as input_file:
      vocab_freq = dict(Counter(chain.from_iterable(map(lambda sentence: sentence.split(), input_file))))
    print('Sorting vocab by frequency.')
    vocab_freq = sorted(vocab_freq.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print('Writing info.')
    # Write info.
    for name, info in [
      ('alphabet', sorted(list(set(c for word, _ in vocab_freq for c in word)))),
      ('vocab', map(lambda kv: kv[0], vocab_freq)),
      ('freq', map(lambda kv: args.freq_delim.join((kv[0], str(kv[1]))), vocab_freq))]:
      with open('.'.join(filter(None, [args.corpus_prefix, lang_extension, name, lang])), 'w') as output_file:
        output_file.write('\n'.join(info))

if __name__ == '__main__':
  main()
