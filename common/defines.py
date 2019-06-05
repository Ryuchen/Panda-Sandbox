#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-05-31 17:59
# @Author : ryuchen
# @File : defines.py
# @Desc :
# ==================================================

REG_NONE = 0
REG_SZ = 1
REG_EXPAND_SZ = 2
REG_BINARY = 3
REG_DWORD_LITTLE_ENDIAN = 4
REG_DWORD = 4
REG_DWORD_BIG_ENDIAN = 5

# Windows specific process rights
# https://msdn.microsoft.com/en-us/library/ms684880(v=vs.85).aspx
WIN_PROCESS_QUERY_INFORMATION = 0x0400

# Windows specific error codes
# https://msdn.microsoft.com/en-us/library/windows/desktop
# /ms683189(v=vs.85).aspx
WIN_ERR_STILL_ALIVE = 259
