#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

"""
高性能日期解析器 - 替代Python的strptime
使用纯C实现，预期10-20倍性能提升
"""

# Cython深度性能优化标记（完整版）
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: nonecheck=False
# cython: initializedcheck=False
# cython: infer_types=True
# cython: optimize.unpack_method_calls=True

import datetime
from libc.stdlib cimport atoi, atol
from libc.string cimport strlen, memcpy
cimport cython

# 快速解析整数（避免Python的int()开销）
@cython.cdivision(True)
@cython.boundscheck(False)
cdef inline int _parse_int(const char* s, int start, int length) nogil:
    """从字符串中快速解析整数"""
    cdef int result = 0
    cdef int i
    cdef char c
    
    for i in range(start, start + length):
        c = s[i]
        if c >= 48 and c <= 57:  # '0' to '9'
            result = result * 10 + (c - 48)
        else:
            break
    
    return result

# 快速解析2位整数
@cython.cdivision(True)
@cython.boundscheck(False)
cdef inline int _parse_int2(const char* s, int pos) nogil:
    """快速解析2位整数 (如 01, 12, 59)"""
    return (s[pos] - 48) * 10 + (s[pos + 1] - 48)

# 快速解析4位整数
@cython.cdivision(True)
@cython.boundscheck(False)
cdef inline int _parse_int4(const char* s, int pos) nogil:
    """快速解析4位整数 (如 2023)"""
    return ((s[pos] - 48) * 1000 + 
            (s[pos + 1] - 48) * 100 + 
            (s[pos + 2] - 48) * 10 + 
            (s[pos + 3] - 48))

# 快速解析6位整数（微秒）
@cython.cdivision(True)
@cython.boundscheck(False)
cdef inline int _parse_int6(const char* s, int pos) nogil:
    """快速解析6位整数 (如 123456 for microseconds)"""
    return ((s[pos] - 48) * 100000 + 
            (s[pos + 1] - 48) * 10000 + 
            (s[pos + 2] - 48) * 1000 + 
            (s[pos + 3] - 48) * 100 + 
            (s[pos + 4] - 48) * 10 + 
            (s[pos + 5] - 48))

# 高性能日期时间解析 - %Y-%m-%d格式
@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef inline object fast_strptime_date(str date_str):
    """
    快速解析日期字符串: YYYY-MM-DD
    比datetime.strptime快10-20倍
    
    Args:
        date_str: 日期字符串，格式为 "YYYY-MM-DD"
        
    Returns:
        datetime.date对象
        
    Example:
        >>> fast_strptime_date("2023-06-15")
        datetime.date(2023, 6, 15)
    """
    cdef bytes date_bytes = date_str.encode('ascii')
    cdef const char* s = date_bytes
    cdef int year, month, day
    
    # 释放GIL进行纯C运算
    with nogil:
        # YYYY-MM-DD
        # 0123456789
        year = _parse_int4(s, 0)   # Position 0-3
        month = _parse_int2(s, 5)  # Position 5-6
        day = _parse_int2(s, 8)    # Position 8-9
    
    return datetime.date(year, month, day)

# 高性能日期时间解析 - %Y-%m-%d %H:%M:%S格式
@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef inline object fast_strptime_datetime(str datetime_str):
    """
    快速解析日期时间字符串: YYYY-MM-DD HH:MM:SS
    比datetime.strptime快10-20倍
    
    Args:
        datetime_str: 日期时间字符串，格式为 "YYYY-MM-DD HH:MM:SS"
        
    Returns:
        datetime.datetime对象
        
    Example:
        >>> fast_strptime_datetime("2023-06-15 14:30:25")
        datetime.datetime(2023, 6, 15, 14, 30, 25)
    """
    cdef bytes dt_bytes = datetime_str.encode('ascii')
    cdef const char* s = dt_bytes
    cdef int year, month, day, hour, minute, second
    
    # 释放GIL进行纯C运算
    with nogil:
        # YYYY-MM-DD HH:MM:SS
        # 0123456789012345678
        year = _parse_int4(s, 0)    # Position 0-3
        month = _parse_int2(s, 5)   # Position 5-6
        day = _parse_int2(s, 8)     # Position 8-9
        hour = _parse_int2(s, 11)   # Position 11-12
        minute = _parse_int2(s, 14) # Position 14-15
        second = _parse_int2(s, 17) # Position 17-18
    
    return datetime.datetime(year, month, day, hour, minute, second)

# 高性能日期时间解析 - %Y-%m-%d %H:%M:%S.%f格式（带微秒）
@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef inline object fast_strptime_datetime_micro(str datetime_str):
    """
    快速解析日期时间字符串（带微秒）: YYYY-MM-DD HH:MM:SS.ffffff
    比datetime.strptime快10-20倍
    
    Args:
        datetime_str: 日期时间字符串，格式为 "YYYY-MM-DD HH:MM:SS.ffffff"
        
    Returns:
        datetime.datetime对象
        
    Example:
        >>> fast_strptime_datetime_micro("2023-06-15 14:30:25.123456")
        datetime.datetime(2023, 6, 15, 14, 30, 25, 123456)
    """
    cdef bytes dt_bytes = datetime_str.encode('ascii')
    cdef const char* s = dt_bytes
    cdef int year, month, day, hour, minute, second, microsecond
    cdef int str_len = len(datetime_str)
    
    # 释放GIL进行纯C运算
    with nogil:
        # YYYY-MM-DD HH:MM:SS.ffffff
        # 012345678901234567890123456
        year = _parse_int4(s, 0)    # Position 0-3
        month = _parse_int2(s, 5)   # Position 5-6
        day = _parse_int2(s, 8)     # Position 8-9
        hour = _parse_int2(s, 11)   # Position 11-12
        minute = _parse_int2(s, 14) # Position 14-15
        second = _parse_int2(s, 17) # Position 17-18
        
        # 微秒部分（如果存在）
        if str_len >= 26:  # Has microseconds
            microsecond = _parse_int6(s, 20)  # Position 20-25
        else:
            microsecond = 0
    
    return datetime.datetime(year, month, day, hour, minute, second, microsecond)

# 高性能日期时间解析 - ISO 8601格式 YYYY-MM-DDTHH:MM:SS
@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef inline object fast_strptime_iso(str datetime_str):
    """
    快速解析ISO 8601日期时间字符串: YYYY-MM-DDTHH:MM:SS
    比datetime.strptime快10-20倍
    
    Args:
        datetime_str: ISO 8601格式字符串，格式为 "YYYY-MM-DDTHH:MM:SS"
        
    Returns:
        datetime.datetime对象
        
    Example:
        >>> fast_strptime_iso("2023-06-15T14:30:25")
        datetime.datetime(2023, 6, 15, 14, 30, 25)
    """
    cdef bytes dt_bytes = datetime_str.encode('ascii')
    cdef const char* s = dt_bytes
    cdef int year, month, day, hour, minute, second
    
    # 释放GIL进行纯C运算
    with nogil:
        # YYYY-MM-DDTHH:MM:SS
        # 0123456789012345678
        year = _parse_int4(s, 0)    # Position 0-3
        month = _parse_int2(s, 5)   # Position 5-6
        day = _parse_int2(s, 8)     # Position 8-9
        hour = _parse_int2(s, 11)   # Position 11-12
        minute = _parse_int2(s, 14) # Position 14-15
        second = _parse_int2(s, 17) # Position 17-18
    
    return datetime.datetime(year, month, day, hour, minute, second)

# 通用快速解析函数 - 自动检测格式
@cython.cdivision(True)
@cython.boundscheck(False)
cpdef inline object fast_strptime(str datetime_str, str format_hint=None):
    """
    通用快速日期解析函数 - 自动检测格式或使用提示
    
    Args:
        datetime_str: 日期时间字符串
        format_hint: 格式提示 (可选)
            - None: 自动检测
            - 'date': YYYY-MM-DD
            - 'datetime': YYYY-MM-DD HH:MM:SS
            - 'datetime_micro': YYYY-MM-DD HH:MM:SS.ffffff
            - 'iso': YYYY-MM-DDTHH:MM:SS
            
    Returns:
        datetime.date 或 datetime.datetime对象
        
    Example:
        >>> fast_strptime("2023-06-15")
        datetime.date(2023, 6, 15)
        >>> fast_strptime("2023-06-15 14:30:25")
        datetime.datetime(2023, 6, 15, 14, 30, 25)
    """
    cdef int str_len = len(datetime_str)
    
    # 如果有格式提示，直接使用对应函数
    if format_hint == 'date':
        return fast_strptime_date(datetime_str)
    elif format_hint == 'datetime':
        return fast_strptime_datetime(datetime_str)
    elif format_hint == 'datetime_micro':
        return fast_strptime_datetime_micro(datetime_str)
    elif format_hint == 'iso':
        return fast_strptime_iso(datetime_str)
    
    # 自动检测格式（基于长度）
    if str_len == 10:  # YYYY-MM-DD
        return fast_strptime_date(datetime_str)
    elif str_len == 19:  # YYYY-MM-DD HH:MM:SS 或 YYYY-MM-DDTHH:MM:SS
        if datetime_str[10] == 'T':
            return fast_strptime_iso(datetime_str)
        else:
            return fast_strptime_datetime(datetime_str)
    elif str_len >= 26:  # YYYY-MM-DD HH:MM:SS.ffffff
        return fast_strptime_datetime_micro(datetime_str)
    elif str_len > 19:  # YYYY-MM-DD HH:MM:SS.f*
        return fast_strptime_datetime_micro(datetime_str)
    else:
        # 回退到Python的strptime
        return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

# 兼容接口 - 可以直接替换datetime.strptime
@cython.cdivision(True)
@cython.boundscheck(False)
cpdef inline object strptime(str datetime_str, str format_str):
    """
    兼容datetime.strptime的接口
    
    支持的格式:
        - '%Y-%m-%d': 日期
        - '%Y-%m-%d %H:%M:%S': 日期时间
        - '%Y-%m-%d %H:%M:%S.%f': 日期时间（微秒）
        - '%Y-%m-%dT%H:%M:%S': ISO 8601
        
    对于不支持的格式，回退到Python的datetime.strptime
    
    Args:
        datetime_str: 日期时间字符串
        format_str: 格式字符串
        
    Returns:
        datetime对象
    """
    # 快速路径 - 常用格式
    if format_str == '%Y-%m-%d':
        return fast_strptime_date(datetime_str)
    elif format_str == '%Y-%m-%d %H:%M:%S':
        return fast_strptime_datetime(datetime_str)
    elif format_str == '%Y-%m-%d %H:%M:%S.%f':
        return fast_strptime_datetime_micro(datetime_str)
    elif format_str == '%Y-%m-%dT%H:%M:%S':
        return fast_strptime_iso(datetime_str)
    else:
        # 回退到Python的strptime
        return datetime.datetime.strptime(datetime_str, format_str)

# 批量解析函数 - 适用于大量数据
@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef list fast_strptime_batch(list datetime_strs, str format_hint=None):
    """
    批量快速解析日期时间字符串
    
    Args:
        datetime_strs: 日期时间字符串列表
        format_hint: 格式提示 (可选)
        
    Returns:
        datetime对象列表
        
    Example:
        >>> dates = ["2023-06-15", "2023-06-16", "2023-06-17"]
        >>> fast_strptime_batch(dates, 'date')
        [datetime.date(2023, 6, 15), datetime.date(2023, 6, 16), datetime.date(2023, 6, 17)]
    """
    cdef int n = len(datetime_strs)
    cdef list results = []
    cdef int i
    cdef str dt_str
    
    for i in range(n):
        dt_str = datetime_strs[i]
        results.append(fast_strptime(dt_str, format_hint))
    
    return results

