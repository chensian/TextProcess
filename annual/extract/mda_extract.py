#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/22 23:58
# @Author  : chesian
# @Site    :
# @File    : muti_extract.py
# @Software: PyCharm


"""
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 05 15:39:57 2017

@author: YYY
"""

import re
import os

import io_utils as io
from threadutil import *


# class TimeoutException(Exception):
#    print 'a timeout exception is detected'
#   """function run timeout"""

def Timeout(seconds):
    """超时装饰器，指定超时时间
    若被装饰的方法在指定的时间内未返回，则抛出Timeout异常"""

    def timeout_decorator(func):
        """真正的装饰器"""

        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

        def _(*args, **kwargs):
            result = []
            # create new args for _new_func, because we want to get the func return val to result list
            new_kwargs = {
                'oldfunc': func,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }
            thd = KThread(target=_new_func, kwargs=new_kwargs)
            thd.start()
            thd.join(seconds)
            alive = thd.isAlive()
            thd.kill()  # kill the child thread
            if alive:
                raise Exception(u'TimeoutException function run too long, timeout %d seconds.' % seconds)
            elif thd.exception is not None:
                #                print thd.exception.error_detail
                raise thd.exception
            return result[0]

        _.__name__ = func.__name__
        _.__doc__ = func.__doc__
        return _

    return timeout_decorator


# first_patterns = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
# [ \t\r\n\f\v] : denote empty,note there is a space
any_spaces_no_newline_pattern = '[ \t\r\f\v]'
# number_pattern = '([第（\(]*[一二三四五六七八九]{0,1}[ \t\r\f\v]*[一二三四五六七八九]{0,1}[\.、）\)章节])*[ \t\r\n\f\v]*'
# number_pattern = '([第（\(]{0,1}[一二三四五六七八九十百千万]{0,3}[ 章节\.、）\)]{0,1})*[ \t\r\n\f\v]{0,10}'
number_pattern = '([第（\(]{0,1}[一二三四五六七八九十百千万]{0,3}[ 章节\.、）\)]{0,1})*[ \t\r\n\f\v]{0,10}'
second_patterns = ['董事会报告', '公司业务概要', '管理层讨论与分析', '公司主要业务情况', '会计数据和财务指标摘要', '董事会关于公司报告期内经营情况的讨论与分析'
                                                                             '报告期内（总体）经营情况', '概述', '主营业务的范围及总体经营情况',
                   '公司经营情况', '股东大会情况简介', '董事会工作报告', '主营业务分析']

any_spaces_pattern = '[ \t\r\f\v]{0,10}'

fouth_patterns = ['监事会报告', '重要事项', '投资者关系', '监事会的工作情况', '监事会会议情况', '重大诉讼、仲裁和媒体普遍质疑的事项',
                  '监事会的会议情况及决议内容', '公司投资情况', '监事会工作报告']
# '((?!abc).)*'
# not including any '... page.no' format
chapter_suffix_pattern = '((?!(([ \t\r\n\f\v]{0,10}[\.\…\，\-]{2,200}[ \t\r\n\f\v]{0,10}[\d]{1,3}))))'

chapter_pattern = '([ \t\r\n\f\v]{0,10}[\.]{2,200}[ \t\r\n\f\v]{0,10}[\d]{1,3})'

c_id_pattern = '(\(cid\:\d{1,8}\))'

chinese_pattern = '[\u4e00-\u9fa5]+'

# denote string starts with a 2-10 characters
footnote_start_pattern = '\D{2,10}'  # no number
footnote_number_pattern = '[○零一二三四五六七八九十\d]{4}年{0,1}'
footnote_company_pattern = ['股份有限公司', '股份有限公司']
footnote_year_pattern = ['年度报告全文', '年年度报告']
extraction_timeout = 16


def filter_line(line_content):
    if len(line_content) > 0:

        return line_content
    else:
        return None


def load_file(filepath):
    file_content = []
    with open(filepath, 'rb') as fp:

        for line in fp:

            line = filter_line(line)

            if line:
                file_content.append(line)

    return file_content


# e.g.
# ^((\d{2,10}(股份有限公司)|(股份有限公司)){0,1}([零一二三四五六七八九十\d]{2,4}(股份有限公司)|(股份有限公司)))$
def generate_footnote_patterns():
    # empty list
    content = []

    # the
    content.append('^(')  # .........1

    content.append('(')  # ..........2
    content.append(footnote_start_pattern)  # company name

    content.append('(')
    f_length = len(footnote_company_pattern)
    for f_id in xrange(f_length):
        f_pattern = footnote_company_pattern[f_id]

        content.append('(')  # ...................4
        content.append(f_pattern)
        # for f_char in f_pattern.decode('utf-8'):
        #    content.append(f_char.encode('utf-8'))

        content.append(')')  # ...................4

        if f_id < f_length - 1:
            content.append('|')

    content.append(')){0,1}')  # ........................2

    # content.append(any_spaces_pattern)

    content.append('(')  # ............................2
    content.append(footnote_number_pattern)

    content.append('(')
    c_length = len(footnote_year_pattern)
    for c_id in xrange(c_length):
        c_pattern = footnote_year_pattern[c_id]

        content.append('(')  # .....................3
        content.append(c_pattern)
        # for c_char in c_pattern.decode('utf-8'):
        #    content.append(c_char.encode('utf-8'))

        content.append(')')  # ....................3

        if c_id < c_length - 1:
            content.append('|')
    content.append(')')

    content.append(')')  # ...........................2
    content.append(')$')  # parath for ......1

    s = ''.join(content)

    # print s
    return s.decode('utf-8')


def generate_1_2_patterns():
    # generate empty list
    content = []

    # 1. the number pattern
    content.append('^(')  # .........1
    content.append(number_pattern)
    content.append('(')  # .........2

    # 2. pattern for chapter, section and so on
    s_p_len = len(second_patterns)
    for s_id in xrange(s_p_len):
        s_pattern = second_patterns[s_id]

        content.append('(')

        for p_char in s_pattern.decode('utf-8'):
            content.append(p_char.encode('utf-8'))
            content.append(any_spaces_pattern)

        content.append(')')

        if s_id < s_p_len - 1:
            content.append('|')

    content.append(')')  # parath ..........2

    # suffix such as '....' and so on
    content.append(chapter_suffix_pattern)
    content.append(')')  # parath for ......1

    s = ''.join(content)

    # print '\n'.join(content)
    # print s.decode('utf-8')
    return s.decode('utf-8')


def generate_3_4_patterns():
    content = []

    content.append('^(')
    content.append(number_pattern)
    content.append('(')

    s_p_len = len(fouth_patterns)
    for s_id in xrange(s_p_len):
        s_pattern = fouth_patterns[s_id]

        content.append('(')

        for p_char in s_pattern.decode('utf-8'):
            content.append(p_char.encode('utf-8'))
            content.append(any_spaces_pattern)

        content.append(')')

        if s_id < s_p_len - 1:
            content.append('|')

    content.append(')')  # parath for the
    content.append(chapter_suffix_pattern)
    content.append(')')  # parath for the whole re

    s = ''.join(content)

    return s.decode('utf-8')


# already ensure taht the sentence includes the pattern
# we only keep this pattern if its prefix and the suffix are not Chinese Character
# def refine_pattern(sentence, found_pattern):

# for each sentence, find whether the pattern exists
def find_patterns(sentences, sentence_indices, pattern):
    pattern_candidates = []
    for s_id, sentence in enumerate(sentences):

        # print 'processing sentence ', s_id , ' ', sentence
        sentence_start = sentence_indices[s_id]
        p_iter = pattern.finditer(sentence)

        for candidate in p_iter:
            pattern_candidates.append(
                (candidate.start() + sentence_start, candidate.end() + sentence_start, candidate.group(0)))

    return pattern_candidates


# test if a sentence's number is over ratio
def sentence_over_num_persentage(sentence, ratio=0.7):
    digit_num = 0.0

    # filter empty sentence
    if len(sentence) == 0:
        return True

    for chara in sentence:

        if chara.isdigit():
            digit_num += 1

    if (digit_num / len(sentence)) >= ratio:
        return True
    else:
        return False


# test if a sentence contains footnote
def filter_sentence_cids(sentence):
    # p_iter = cid_pattern.findall(sentence)

    new_sentence = re.sub(c_id_pattern, ' ', sentence)

    if new_sentence:
        new_sentence = new_sentence.strip()
        # else:
        # print len(sentence), ' to ', len(new_sentence)

    if (len(new_sentence) != len(sentence)):
        '''
        print 'from ', sentence
        print ' to ', new_sentence
        '''
        return new_sentence
    else:
        return sentence


# define if a sentence is a footnot
def sentence_is_footnote(sentence, footnote_pattern):
    # footnote_pattern = generate_footnote_patterns()

    # print footnote_pattern

    c_pattern = re.compile(footnote_pattern)

    p_iter = c_pattern.findall(sentence)

    if p_iter:
        # print 'footnote ', p_iter[0][0]
        return True
    else:
        return False


def filter_sentences(sentences, footnote_pattern, min_sentence_length=8):
    new_sentences = []
    for sentence in sentences:

        keep_it = True

        sentence = sentence.strip()

        if len(sentence) <= min_sentence_length:
            # print sentence, ' ', len(sentence)
            keep_it = False
        else:
            sentence = filter_sentence_cids(sentence)

            if len(sentence) <= min_sentence_length:
                keep_it = False
            else:
                if sentence_over_num_persentage(sentence):
                    # print 'skip sentence for number issue ', len(sentence)
                    # print sentence
                    keep_it = False

                if sentence_is_footnote(sentence, footnote_pattern):
                    keep_it = False

        if keep_it:
            '''
            if sentence.find('(cid:') != -1:
                print sentence
            '''

            new_sentences.append(sentence)

    return new_sentences


# the first part
# 1, 2, 3, 4 four parts consists of the whole pattern
# @Timeout(60)
def first_round_sentence_version(content, cn_words, debug=False):
    # 1. decode it by utf-8
    data = content.decode('utf-8')
    # data = content

    # 2. split it by new_line operator
    new_line = '\n'
    len_new_line = len(new_line)
    sentences = data.split(new_line)

    # prepare footnote pattern
    footnote_pattern = generate_footnote_patterns()

    sentences = filter_sentences(sentences, footnote_pattern)
    data = new_line.join(sentences)

    # print 'sentences ', len(sentences)

    # 3. build start and end index for each sentence, so if there are n sentences, the index size is n + 1
    # initialize the start position of the first sentence to be 0
    indices = []

    index_in_doc = 0
    indices.append(index_in_doc)
    for s_id, sentence in enumerate(sentences):
        # indices.append(len(sentence), len_new_line * s_id)
        index_in_doc += len(sentence)
        index_in_doc += len_new_line

        # print 'sid ', s_id, ' sentence =>', sentence, '<= len : ', len(sentence), ' ', index_in_doc

        # return
        indices.append(index_in_doc)

    # print len(data), ' ', indices[len(indices) - 1]

    # prepare start pattern
    f_s_patterns = generate_1_2_patterns()
    # print f_s_patterns
    start_pattern = re.compile(f_s_patterns)

    s_candidates = find_patterns(sentences, indices, start_pattern)

    if debug:
        print 's_candiadtes ', len(s_candidates)

    # prepare end pattern
    t_f_patterns = generate_3_4_patterns()
    end_pattern = re.compile(t_f_patterns)

    e_candidates = find_patterns(sentences, indices, end_pattern)

    if debug:
        print 'e_candiadtes ', len(e_candidates)

    candidates = []
    for s_start, s_end, s_group in s_candidates:

        for e_start, e_end, e_group in e_candidates:

            if s_end < e_start:

                sub_content = data[s_start: e_end]

                if debug:
                    print s_end, ' < ', e_start, ' ', len(sub_content)

                candidates.append((s_start, e_end, s_group, e_group, sub_content))

    return candidates


# the first part
# 1, 2, 3, 4 four parts consists of the whole pattern
@Timeout(120)
def first_round(content, cn_words, debug=True):
    data = content.decode('utf-8')

    f_s_patterns = generate_1_2_patterns()

    if debug:
        print 'finish f_s_patterns '

    # print f_s_patterns
    start_pattern = re.compile(f_s_patterns)

    if debug:
        print 'finish start pattern'

    s_iter = start_pattern.finditer(data)

    if debug:
        print 'finish s_iter ', len(start_pattern.findall(data))

    t_f_patterns = generate_3_4_patterns()

    if debug:
        print 'finish t_f_patterns '

    end_pattern = re.compile(t_f_patterns)

    if debug:
        print 'finish end_pattern '

    e_iter = end_pattern.finditer(data)

    if debug:
        print 'finish e_iter ', len(end_pattern.findall(data))

    candidates = []

    starts = []

    for s_id, start in enumerate(s_iter):
        if debug:
            print 'starts ', s_id, ' ', start.start(), ' ', start.end(), ' ', start.group(0)
        starts.append((start.start(), start.end(), start.group(0)))

    print 'end starts '

    ends = []

    for e_id, end in enumerate(e_iter):

        if debug:
            print 'ends ', e_id, ' ', end.start(), ' ', end.end(), ' ', end.group(0)
        ends.append((end.start(), end.end(), end.group(0)))

    for s_start, s_end, s_index in starts:

        for e_start, e_end, e_index in ends:

            if s_end < e_start:

                sub_content = data[s_start: e_end]

                candidates.append((s_start, e_end, s_index, e_index, sub_content))

                if debug:
                    print start.end(), ' < ', end.start(), ' ', len(sub_content)
    return candidates


def prepare_cn_words():
    # cn_words = re.compile(u'[\u4e00-\u9fa5]+')
    cn_words = re.compile('[\u4e00-\u9fa5]+')
    # cn_punctuations =re.compile(u'[\u3000-\u303f\ufb00-\ufffd]+')
    return cn_words


def list_as_str(file_content):
    s = '\n'.join(file_content)
    # s = unicode(s)
    return s


def load_file_as_str(filepath):
    file_content = load_file(filepath)

    file_content = list_as_str(file_content)

    return file_content


def test_re():
    filepath = u'D:/data/cc/AStock/parsed/000001/S深发展A：2006年年度报告.txt'

    file_content = load_file(filepath)

    file_content = list_as_str(file_content)

    chapter_suffix = re.compile(chapter_pattern)

    c_iter = chapter_suffix.finditer(file_content)

    for c in c_iter:
        print c.group(0)


def form_candidates_as_str(filepath, candidates):
    content_list = []

    content_list.append(filepath.decode('gbk'))
    for start, end, start_str, end_str, content in candidates:
        content_list.append(str(start) + ': ' + start_str)
        content_list.append(str(end) + ': ' + end_str)
        content_list.append('=========================================')
        content_list.append(content)
        content_list.append('=========================================')

    return '\n'.join(content_list)


def find_mean_volume_from_candiates(candidates):
    if not candidates:
        return 0

    size = 0.0

    for start, end, start_str, end_str, content in candidates:
        size = size + len(content)

    return size / len(candidates)


def form_median_candidate_as_str(filepath, candidates, mean_volume):
    content_list = []

    num_candidates = len(candidates)

    index = (num_candidates - 1) // 2
    # odd

    ids = []

    if num_candidates <= 0:
        print 'empty list '
    elif num_candidates == 1:
        ids.append(0)
    elif (num_candidates % 2):
        ids.append(index)
    else:
        ids.append(index)
        ids.append(index + 1)

    choosen_volume = 0

    if ids:
        content_list.append(filepath.decode('gbk'))

        if len(ids) == 1:
            for c_id in ids:
                start, end, start_str, end_str, content = candidates[c_id]

                content_list.append(str(start) + ': ' + start_str)
                content_list.append(str(end) + ': ' + end_str)
                content_list.append('=========================================')
                content_list.append(content)
                content_list.append('=========================================')

                choosen_volume = len(content)
        elif len(ids) == 2:
            min_abs = 0
            min_id = -1

            # iteration used to find the c_id with min_abs
            for c_id in ids:

                start, end, start_str, end_str, content = candidates[c_id]

                if min_id == -1:
                    min_id = c_id
                    min_abs = abs(len(content) - mean_volume)
                else:
                    tmp_abs = abs(len(content) - mean_volume)

                    if tmp_abs < min_abs:
                        min_abs = tmp_abs
                        min_id = c_id

            start, end, start_str, end_str, content = candidates[min_id]
            content_list.append(str(start) + ': ' + start_str)
            content_list.append(str(end) + ': ' + end_str)
            content_list.append('=========================================')
            content_list.append(content)
            content_list.append('=========================================')

            choosen_volume = len(content)

        else:
            print 'median with ids longer than 3'
            choosen_volume = 0

        return '\n'.join(content_list), choosen_volume


# several heuristic rules
# 1. number of lines < 5
# 2. number of characters < 250
def filter_candidates(candidates, min_newline_number=5, min_volume=250):
    new_candidates = []

    # rule 1: if the count of newline is smaller than 10, filter it

    for candidate in candidates:

        keep_it = True
        start, end, start_str, end_str, content = candidate

        # number of lines check
        if io.occurrences(content, '\n') < min_newline_number:
            keep_it = False

        if len(content) < min_volume:
            keep_it = False

        if keep_it:
            new_candidates.append(candidate)

            # number of characters

    return new_candidates

    # except TimeoutException, toe:
    #     #timeout process
    #     print 'add file ', (src_dir + filename).decode('gbk'), ' to log and timeout file'
    #     io.processed_file(src_dir + filename, processed_files, timeout_file)


def parse_all_files(company_map, processed_files, cn_words, src_dir, dest_dir, log_file='extract/back_log.dat',
                    error_file='extract/no_candidates.dat', timeout_file='extract/timeout.dat', suffix='txt'):
    # 1. the statistic file
    csv_file = 'extract/statistics.csv'
    # extract_dir = dest_dir + '/extract/'
    # dest_dir = dest_dir + '/all/'


    # print 'nb'
    if processed_files is None:
        print 'loading ', log_file
        processed_files = io.load_processed_files(log_file)

    timeout_files = io.load_processed_files(timeout_file)

    if cn_words is None:
        print 'prepare cn words'
        cn_words = prepare_cn_words()

    src_dir = io.format_dir(src_dir)
    dest_dir = io.format_dir(dest_dir)

    print 'extract from ', src_dir, ' to ', dest_dir
    if (not os.path.exists(src_dir)) or (not os.path.isdir(src_dir)):
        print 'error, source dir ' + src_dir + '  not exists!'
        return

    dir_list = []

    # dir_set = {}

    for filename in sorted(os.listdir(src_dir)):

        src_file = os.path.join(src_dir, filename)

        print 'processing ->', src_file.decode('gbk'), '<-'

        # check file is exists

        if os.path.isdir(src_file):
            # print 'dir ' + (src_dir+filename).decode('gbk')
            # recursively backup this folder
            # back_up_dir_memory(src_dir + filename, dest_dir + filename, log_file = log_file)
            dir_list.append((src_dir + filename, dest_dir + filename, log_file, error_file, timeout_file))

        elif os.path.isfile(src_file):
            # print 'process file ' + (src_dir+filename).decode('gbk')

            stock_code = io.get_stock_code(src_dir)
            publish_year = io.get_publish_year(filename)

            # print stock_code, ' ', publish_year

            if suffix is '*' or filename.find(suffix) != -1:

                count = -1

                if io.file_is_processed(src_dir + filename, timeout_files):
                    print 'timeout file skip ', (src_dir + filename).decode('gbk')

                elif not io.file_is_processed(src_dir + filename, processed_files):

                    # print src_file.__class__
                    # return
                    mean_volume = 0
                    median_volume = 0

                    file_content = load_file_as_str(src_file)
                    print 'computing candiadtes for ', (src_dir + filename).decode('gbk')
                    try:
                        # 1. extract the candidates
                        candidates = first_round_sentence_version(file_content, cn_words)

                        # 2. filter the candidates by some rules: eg, less than 10 lines
                        candidates = filter_candidates(candidates)

                        count = len(candidates)

                        if count <= 0:
                            io.processed_file(src_dir + filename, processed_files, error_file)

                    except Exception, e:
                        print 'unknown exception ', e
                        io.processed_file(src_dir + filename, processed_files, timeout_file)

                        # count = t_cmd.timeout(timeout = extraction_timeout)(first_round)(file_content, cn_words)
                        # func()

                    if True and candidates:
                        mean_volume = find_mean_volume_from_candiates(candidates)
                        median_str, median_volume = form_median_candidate_as_str(src_dir + filename, candidates,
                                                                                 mean_volume)
                        io.write_file(dest_dir, filename, median_str.encode('utf-8'))

                        # all_str = form_candidates_as_str(src_dir + filename, candidates)
                        # io.write_file(dest_dir, filename, all_str.encode('utf-8'))

                    io.processed_file(src_dir + filename, processed_files, log_file)
                    print (src_dir + filename).decode('gbk'), ' candidates count ', count

                    io.insert_into_company_map(company_map, stock_code, publish_year, count,
                                               (src_dir + filename).decode('gbk'))

                    io.append_to_file(csv_file,
                                      (src_dir + filename) + ',' + str(count) + ',' + str(mean_volume) + ',' + str(
                                          median_volume) + '\n')
                else:
                    print (src_dir + filename).decode('gbk'), ' is processed already, skip'

            else:
                print (src_dir + filename).decode('gbk'), ' file type not match ', suffix

        else:
            print 'case ??? ', (src_dir + filename).decode('gbk')

    for (cp_src_dir, cp_dest_dir, cp_log_file, cp_error_file, cp_timeout_file) in dir_list:
        parse_all_files(company_map, processed_files, cn_words, cp_src_dir, cp_dest_dir, cp_log_file, cp_error_file,
                        cp_timeout_file, suffix=suffix)


def test():
    # filepath = u'D:/data/cc/AStock/parsed/000001/S深发展A：2006年年度报告.txt'
    # filepath = u'D:/data/cc/AStock/second_parse/600072/江南重工：2007年年度报告.txt'

    # src_dir = u'D:/data/cc/AStock/second_parse/600072/'

    src_dir = u'D:/data/cc/AStock/parsed/000001/'

    files = sorted(os.listdir(src_dir))

    cn_words = prepare_cn_words()
    for s_file in files:

        # print filepath

        # if u'中船股份：2007年年度报告.txt' in s_file:
        if u'S深发展A：2006年年度报告.txt' in s_file:
            print src_dir + s_file

            file_content = load_file_as_str(src_dir + s_file)

            candidates = first_round(file_content, cn_words)

            print 'find candidates by v1 ', len(candidates)

            candidates = first_round_sentence_version(file_content, cn_words)

            print 'find candidates v2 ', len(candidates)

            # print filepath.__class__, ' ', filepath.encode('utf-8').__class__

    print 'finished process '


def test_dir():
    company_map = {}
    parse_all_files(company_map, None, None, 'G:/Stock/ARTEXT/', 'G:/Stock/median/')

    years_columns = [str(year) for year in range(1999, 2017)]
    io.company_map_as_csv_file('extract/compnay_map.csv', company_map, years_columns)


if __name__ == '__main__':
    test_dir()
