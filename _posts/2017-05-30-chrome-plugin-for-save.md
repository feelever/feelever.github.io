---
layout: post
title: 'Chrome内容保存插件 - Just One File'
date: '2017-05-30'
header-img: "img/post-bg-web.jpg"
tags:
     - web
author: 'Codeboy'
---

随着互联网的发展，当前我们可以方便的在网站中找到各种各样的资源，尽管现在网络已经无处不在，但是有些时候我们仍然需要保存一些信息到本地，于是开发一个Chrome插件的想法产生了。

## 初衷

- 所见即所存

> 目前很多网站都是动态产生的，而浏览器保存的是网页源码， 看到的和保存的内容是可能不一样的，特别是在没有网络的情况下打开。
> 
> 

- 去除无用信息

> 很多网站页面中充满了广告等不相关的元素，这些元素影响了信息的查看，去除了后将提升阅读体验。
> 

## 分析

- 针对第一个问题，可以直接保存浏览器当前的dom树，这样就可以达到所见即所存了。
- 针对第二个问题，目前像chrome等浏览器已经可以非常方便的操作dom中的元素了，删除、增加、修改都可以快速的完成。

## 实施
有了思路后，就可以根据Chrome插件开发的步骤开始制作插件了，考虑到动画等动态性的内容并不是那么的重要，所以在保存页面的时候，去除了所有引入的js和js代码，这样做的另一个好处是减少文件大小。 

## 后续
- 目前尚未对引入的css进行合并，直接注入到页面中，可以完全不依赖网络，下个版本改进。
- 保留一些动画等元素。

## 下载
[https://chrome.google.com/webstore/detail/just-one-file/opofajlgipfljhhlfhcpmhhjckjaacia?hl=zh-CN&authuser=1](https://chrome.google.com/webstore/detail/just-one-file/opofajlgipfljhhlfhcpmhhjckjaacia?hl=zh-CN&authuser=1)