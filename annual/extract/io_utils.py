# -*- coding: utf-8 -*-
"""
Created on Sun May 07 21:56:02 2017

@author: YYY
"""
import os
import re
#c style, find the count of sub in string
def occurrences(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count


def format_dir(file_dir):
    '''
    if file_dir no endswith /, add it
    '''
    if not file_dir.endswith('/'):
        return file_dir + '/'
    else:
        return file_dir

def load_processed_files(filename):
    '''
    加载处理过的文件 filenames
    return set(filenames)
    '''
    processed_files = set()

    if not os.path.exists(filename):
        print 'index file not exists ', filename, ' return empty set'
        return processed_files
    
    with open(filename, 'rb') as logfile:
        for line in logfile:
            processed_files.add(line.strip())
    
    print 'load a ', len(processed_files), ' size set'
    return processed_files

    
def write_file(dest_dir, filename, content):
        
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)      
            
    with file(dest_dir + filename, "wb") as f:
         f.write(content)

def append_to_file(filename, content):
    
    with file(filename, 'a+') as f:
        f.write(content)
        #print content.decode('gbk')

def processed_file(new_file, processed_files, filename, content = None):
    processed_files.add(new_file)
    
    
    with open(filename, 'a') as logfile:
        if not content:
            logfile.write(new_file + '\n')
        else:
            logfile.write(content + '\n')
        
def generate_txt_name(filename):
    
    if '.PDF' in filename:
        return filename.replace('.PDF', '.txt')
        
    if '.pdf' in filename:
        return filename.replace('.pdf', '.txt')
        

def file_is_processed(new_file, processed_files):
    
    return new_file in processed_files

def get_publish_year(filepath):
    
    s_list = re.findall('2[0-9]{3}',filepath)
    
    if s_list:
        return s_list[0]
    else:
        return None
    
def get_stock_code(filepath):
    
    s_list = re.findall('[0-9]{6}', filepath)
    
    if s_list:
        return s_list[0]
    else:
        return None
    #for stock_code in s_list:
    #    print stock_code
    # last_slash = filepath.rfind('/')
    #
    # if last_slash < 0:
    #     print 'cannot find slash ', filepath
    # else:
    #     print last_slash
    #     last_2nd_slash = filepath.rfind('/',last_slash + 1)
    #
    #     if last_2nd_slash > 0:
    #
    #         print last_2nd_slash
    #         stock_code = filepath.substring(last_2nd_slash, last_slash)
    #
    #         print stock_code

def get_filename(filepath):

    if filepath.find('.PDF') > 0:
        last_slash = filepath.rfind('/')
        if last_slash > 0:
            return filepath[last_slash + 1:]
        else:
            return None
    else:
        return None
        
def insert_into_company_map(company_map, stock_code, publish_year, no_candidates, filepath):
    
    if stock_code and publish_year:
    
        stock_code = str(stock_code)
        publish_year = str(publish_year)
        #print stock_code, ' ', publish_year
        if stock_code not in company_map:
            company_map[stock_code] = {}

        company_map[stock_code][publish_year] = str(no_candidates)
            
            
def company_info_as_scv(stock_code, company_info, years_columns):
    
    content = []

    content.append(str(stock_code))

    for year in years_columns:
        if year in company_info:
            content.append(str(company_info[year]))
        else:
            content.append('0')
    
    return ','.join(content)
    

def company_map_as_csv_file(filepath, company_map, years_columns):
    
    with file(filepath, "wb") as f:
        
        
        columns = []
        columns.append('STOCK_CODE')
        for year in years_columns:
            columns.append(year)
            
        f.write(','.join(columns) + '\n')
        
        stock_codes = company_map.keys()
    
        stock_codes.sort()
        
        for stock_code in stock_codes:
            
            company_info = company_map[stock_code]

            
            line_info = company_info_as_scv(stock_code, company_info, years_columns)
            
            f.write(line_info + '\n')
    
        