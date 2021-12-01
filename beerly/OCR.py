import pytesseract
import re
import cv2

import pandas as pd
from rapidfuzz import process, fuzz

default_db = pd.read_csv('raw_data/dataset_light.csv')

def raw_extract (img):
    ''' raw extract from an image with tesseract'''

    extract = pytesseract.image_to_string(img)
    return extract

def list_from_ocr(extract):
    '''Extract a list of the beers from a raw tesseract extract'''

    # dict for accent and quotes removal
    normalMap = {
        'À': 'A',
        'Á': 'A',
        'Â': 'A',
        'Ã': 'A',
        'Ä': 'A',
        'à': 'a',
        'á': 'a',
        'â': 'a',
        'ã': 'a',
        'ä': 'a',
        'ª': 'A',
        'È': 'E',
        'É': 'E',
        'Ê': 'E',
        'Ë': 'E',
        'è': 'e',
        'é': 'e',
        'ê': 'e',
        'ë': 'e',
        'Í': 'I',
        'Ì': 'I',
        'Î': 'I',
        'Ï': 'I',
        'í': 'i',
        'ì': 'i',
        'î': 'i',
        'ï': 'i',
        'Ò': 'O',
        'Ó': 'O',
        'Ô': 'O',
        'Õ': 'O',
        'Ö': 'O',
        'ò': 'o',
        'ó': 'o',
        'ô': 'o',
        'õ': 'o',
        'ö': 'o',
        'º': 'O',
        'Ù': 'U',
        'Ú': 'U',
        'Û': 'U',
        'Ü': 'U',
        'ù': 'u',
        'ú': 'u',
        'û': 'u',
        'ü': 'u',
        'Ñ': 'N',
        'ñ': 'n',
        'Ç': 'C',
        'ç': 'c',
        '§': 'S',
        '³': '3',
        '²': '2',
        '¹': '1',
        '“': '',
        '"': '',
        '”': ''
    }
    normalize = str.maketrans(normalMap)

    # Remove empty lines
    extract_em = extract.replace('€', '\n')
    extract_lines = [
        line for line in extract_em.split('\n') if (line != '') & (line != ' ')
        & (line != '   ') & (line != '    ') & (line != '  ')
    ]
    extract_lines = [re.sub('\d,\d\d', '€', line) for line in extract_lines]
    extract_lines = [re.sub('\d.\d\d', '€', line) for line in extract_lines]

    # Remove accents
    extract_lines_acc = [line.translate(normalize) for line in extract_lines]

    # Remove non-beer sections (keeps lines from the first line that contains 'biere')
    indices_start = [
        i for i, s in enumerate(extract_lines_acc)
        if ('biere' in s.lower()) | ('bi ere' in s.lower())
    ]
    start = indices_start[0]
    rest_of_list = extract_lines_acc[start:]
    indices_stop = [
        i for i, s in enumerate(rest_of_list)
        if ('digestif' in s.lower()) | ('cafe' in s.lower())
        | ('service' in s.lower()) | ('sans alcool' in s.lower())
        | ('cb' in s.lower()) | ('faim' in s.lower())
    ]

    if indices_stop == []:
        indices_stop.append(-1)
    if indices_start == []:
        indices_start.append(0)

    start = indices_start[0] + 1
    stop = indices_stop[0] + start - 1

    extract_lines_stripped = extract_lines_acc[start:stop]

    # remove general keywords (bière locale, bière pression, bière bouteille, bière de saison)
    exc_list = [
        'pression', 'locale', 'bouteille', 'de saison', 'picon', 'monaco',
        'panache', 'cidre', 'cb', 'reglement', 'france', 'belgique', 'ecosse',
        'allemagne', 'hollande', 'prance', 'faim'
    ]

    extract_lines_post = [
        line for line in extract_lines_stripped
        if not any(word in line.lower() for word in exc_list)
    ]
    extract_lines_post_stripped = [
        re.sub('IPA', 'ipa', line) for line in extract_lines_post
    ]
    extract_lines_post_stripped = [
        line for line in extract_lines_post_stripped
        if not any(word.isupper() for word in line.split(' '))
    ]
    extract_lines_post_stripped = [
        re.sub('ipa', 'IPA', line) for line in extract_lines_post_stripped
    ]
    extract_lines_post_stripped = [
        re.sub('\d,\d\d', '', line) for line in extract_lines_post_stripped
    ]

    # remove price and quantities (often line splitted like 'beer - 3€' or 'beer ..........3€'), remove price tag, remove supp. chars
    extract_beers = [
        re.sub(' -.*', '', beer) for beer in extract_lines_post_stripped
    ]
    extract_beers = [re.sub(' \d\d\..*', '', beer) for beer in extract_beers]
    extract_beers = [re.sub(' \d\dd.*', '', beer) for beer in extract_beers]
    extract_beers = [re.sub('\..*', '', beer) for beer in extract_beers]
    extract_beers = [re.sub('..cl.*', '', beer) for beer in extract_beers]
    extract_beers = [re.sub('\d°.*', '', beer) for beer in extract_beers]
    extract_beers = [re.sub('\(.*', '', beer) for beer in extract_beers]
    extract_beers = [re.sub("'", ' ', beer) for beer in extract_beers]
    extract_beers = [re.sub('€.*', '', beer) for beer in extract_beers]
    extract_beers = [beer.strip(' ') for beer in extract_beers]
    extract_beers = [beer.lstrip('— ') for beer in extract_beers]
    extract_beers = [beer.lstrip('_') for beer in extract_beers]
    extract_beers = [beer for beer in extract_beers if len(beer) > 3]

    return extract_beers

def fuzzy_matching(beer, df = default_db):
    ''' get the match of a beer in a database'''
    df = default_db
    # fill brewery names
    df['brewery_name'].fillna(' ', inplace=True)

    # set 3 fuzzy scorers
    choices = df['beer_brewery'].unique()
    s1 = process.extract(beer,
                         choices,
                         limit=15,
                         scorer=fuzz.partial_ratio)

    s2 = process.extract(beer,
                         choices,
                         limit=15,
                         scorer=fuzz.partial_token_set_ratio)

    s3 = process.extract(beer,
                         choices,
                         limit=15,
                         scorer=fuzz.token_set_ratio)

    # create a df with the results of the 3 scorers, sum scores per beer
    df_fuzz = pd.DataFrame(s1).append(s2).append(s3).rename(columns={
        0: 'beer_brewery',
        1: 'Score'
    })

    df_fuzz_gpb = df_fuzz.groupby('beer_brewery').agg({
        'Score': 'sum'
    }).reset_index().sort_values(by='Score', ascending=False)

    # get top score beer (=> most probable match)
    return df_fuzz_gpb['beer_brewery'].iloc[0]

def match_all_beers(list_from_ocr, df):
    ''' uses the fuzzy_matching function to match all beers from a list.
    Returns name_from_ocr, beer_id, beer_name'''

    matches = [fuzzy_matching(beer, df) for beer in list_from_ocr]
    df_match = pd.DataFrame({
        'name_from_ocr': list_from_ocr,
        'beer_brewery': matches
    })
    df = default_db
    df_return = df_match.merge(df, on = 'beer_brewery', how = 'left')

    df_return = df_return[[
        'name_from_ocr', 'brewery_name', 'beer_name', 'beer_id'
    ]]
    return df_return

def quick_preproc(df = default_db):
    ''' Preprocessing of the df for name = main'''
    df = default_db
    df['brewery_name'].fillna(' ', inplace = True)
    df['beer_brewery'] = df['brewery_name'] + ' - ' + df['beer_name']
    return df

if __name__ == '__main__':
    df = quick_preproc()
    print(match_all_beers(['kwak', 'paulaner', 'coors light', 'grimbergen blanche'], df))
    match_all_beers(['kwak', 'paulaner', 'coors light', 'grimbergen blanche'],
                    df).to_csv('test_from_ocr.csv', index = None)
