#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 11:36:40 2019

@author: kenkuo
"""

import math
import time
import multiprocessing

def goldbach(T):
    
    s=T[0]
    e=T[1]
    
    if s<4:
        s=4
    if s%2==1:
        s+=1
    
    for i in range(s,e+1,2):
        isGoldbach=False
        for j in range(i//2+1):
            if isprime(j):
                k=i-j
                if isprime(k):
                    isGoldbach=True
                    print('%d=%d+%d' %(i,j,k))
#                    if i%((e-s)//10)==0:
#                        print('%d=%d+%d' %(i,j,k))
                    break
        if not isGoldbach:
            print('哥德巴赫猜想失敗')
            break

def isprime(n):
    
    if n<=1:
        return False
    for i in range(2,int(math.sqrt(n))+1):
        if n%i==0:
            return False
    return True

def subRange(N,cpu_cnt):
    num_list=[[i+1,i+N//cpu_cnt] for i in range(4,N,N//cpu_cnt)]
    num_list[0][0]=4
    if num_list[cpu_cnt-1][1]>N:
        num_list[cpu_cnt-1][1]=N
    return num_list

def main():
    N=10**5
    cpu_count=multiprocessing.cpu_count()
    #單程式測試
    print("單程式測試")
    start=time.clock()
    results=goldbach([4,N])
    for sample in results:
        print('%d=%d+%d' %sample)
    print("單程式耗時:%d s" %(time.clock()-start))

    #多程式測試
    print("多程式測試")
    pool=multiprocessing.Pool(cpu_count)
    sepList=subRange(N,cpu_count)
    start=time.clock()
    results=pool.map(goldbach,sepList)
    pool.close()
    pool.join()
    for result in results:
        for sample in result:
            print('%d=%d+%d' %sample)
    print("多程式耗時:%d s" %(time.clock()-start))

    

if __name__=='__main__':
    main()