---
layout: post
title: '实用的陌生Shell命令'
date: '2015-08-31'
header-img: "img/post-bg-unix.jpg"
tags:
     - linux
     - osx
author: 'Codeboy'
---

有一些不经常的使用的bash命令可以帮我们省去写很多的脚本, 汇总如下:

### realpath

获取文件的真实路径

	➜  ls
	haha
	➜  realpath haha
	/Volumes/Extra/Tmp/test/haha
	➜   
	➜  echo "`pwd`/haha"        
	/Users/YD/Tmp/test/haha

### rename
批量重命名, -s '替换前的串' '替换后的串'，可以多次使用-s

	➜  ls
	heha1 heha2 heha3 heha4 heha5 heha6 heha7 heha8 heha9
	➜  rename -s 'he' 'code' -s 'ha' 'boy' *
	➜  
	➜  ls 
	codeboy1 codeboy2 codeboy3 codeboy4 codeboy5 codeboy6 codeboy7 codeboy8 codeboy9
	

### cd -
回到上一次目录

### man ascii 
显示ascii(省略部分)

	➜  man ascii

	ASCII(7)             BSD Miscellaneous Information Manual             ASCII(7)

	NAME
	     ascii -- octal, hexadecimal and decimal ASCII character sets

	DESCRIPTION

	     The decimal set:

	       0 nul    1 soh    2 stx    3 etx    4 eot    5 enq    6 ack    7 bel
	       8 bs     9 ht    10 nl    11 vt    12 np    13 cr    14 so    15 si
	      16 dle   17 dc1   18 dc2   19 dc3   20 dc4   21 nak   22 syn   23 etb
	      24 can   25 em    26 sub   27 esc   28 fs    29 gs    30 rs    31 us
	      32 sp    33  !    34  "    35  #    36  $    37  %    38  &    39  '
	      40  (    41  )    42  *    43  +    44  ,    45  -    46  .    47  /
	      48  0    49  1    50  2    51  3    52  4    53  5    54  6    55  7
	      56  8    57  9    58  :    59  ;    60  <    61  =    62  >    63  ?
	      64  @    65  A    66  B    67  C    68  D    69  E    70  F    71  G
	      72  H    73  I    74  J    75  K    76  L    77  M    78  N    79  O
	      80  P    81  Q    82  R    83  S    84  T    85  U    86  V    87  W
	      88  X    89  Y    90  Z    91  [    92  \    93  ]    94  ^    95  _
	      96  `    97  a    98  b    99  c   100  d   101  e   102  f   103  g
	     104  h   105  i   106  j   107  k   108  l   109  m   110  n   111  o
	     112  p   113  q   114  r   115  s   116  t   117  u   118  v   119  w
	     120  x   121  y   122  z   123  {   124  |   125  }   126  ~   127 del

### 不定时更新...
---

> 如有任何知识产权、版权问题或理论错误，还请指正。
>
> 转载请注明原作者及以上信息。
