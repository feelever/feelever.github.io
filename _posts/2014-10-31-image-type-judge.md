---
layout: post
title: '图片格式判断'
date: '2014-10-31'
header-img: "img/home-bg.jpg"
tags:
     - discover
author: 'Codeboy'
---

Linux/Unix下系统判断文件类型并不依据文件名，也即不会根据文件后缀来判断文件的类型。从网上下载了一个图片，没有后缀，希望能够正确判断出格式，以便于共享到其他平台，该怎么办呢？

不同文件类型的文件头部信息不同，比较流行的图片的格式有jpg，png, gif等，下面列出jpg，png，gif文件头(16进制)：

	JPEG(jpg) 文件头： FFD8FF
	PNG(png) 文件头：  89504E47
	GIF(gif) 文件头：  47494638

有了文件头，判断文件就很容易了.读取图片文件头部信息，之后进行比较即可。有很多已有的编辑器可以直接读取文件的二进制信息，下面使用xxd进行二进制信息读取并判断：

	#!/bin/bash
	#judge image file type

	#判断是否只有一个参数
	if [ $# != 1 ]
	 then 
	  echo "parameter error"
	else
	  ## 读取前3个字节与前4个字节对应的16进制
	  len3=`xxd -p -l 3 $1`
	  len4=`xxd -p -l 4 $1`
	  if [ $len3 == "ffd8ff" ]
	    then
	      echo "The type is jpg" 
	  elif [ $len4 == "89504e47" ]
	    then
	       echo "The type is png"
	  elif [ $len4 == "47494638" ]
	    then
	       echo "The type is gif"
	  else
	       echo "The type is others"
	   fi
	fi


脚本保存后，可以直接运行测试没有扩展名字的图片文件。

> 如有任何知识产权、版权问题或理论错误，还请指正。
>
> 转载请注明原作者及以上信息。
