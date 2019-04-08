---
layout: post
title: 'IOS UIWebView 优化'
date: '2015-09-27'
header-img: "img/post-bg-iphone.jpg"
tags:
     - ios
     - web
author: 'Codeboy'
---

native体验好，但是每一次修正bug后都需要发版(特例除外)；web开发快，维护成本低，体验上比native上差一点。web方面怎么减少与native的差距的呢？一个很重要的优化就是尽可能较少网络传输。下面看一下ios开发中怎么减少UIWebView的网络数据传输。

加载网页时需要加载页面以及页面相关的资源(js,css,img)，一般来说页面会经常的变动，但是大部分js,css,img都不会随网页的升级变化而变化，我们可以将这一部分不会变动的资源放置在客户端，在客户端发起请求时进行拦截，将本地资源提供给UIWebView。

	操作步骤:
	1 分析资源的变动
	2 实现拦截协议
	3 注册拦截协议
	
### 1 分析资源的变动
	
分析哪些资源是不会改变的，哪些是会改变的，将不会改变的提取，例如jquery，bootstrap等。

### 2 实现拦截协议

实现自己的URLProtocol,假设我们要使用本地的bootstrap.min.js, bootstrap.min.css ,icon.png .

    //  CBInterceptURLProtocol.swift
    //  拦截器
    //  Created by lyd on 9/25/15.
    //  Copyright © 2015 lyd. All rights reserved.
    //
    
    import Foundation
    
    //资源拦截
    class CBInterceptURLProtocol: NSURLProtocol {
        static var res:Dictionary<String,String> = [:]  //资源文件
        static var type:Dictionary<String,String> = [:]  //资源类型
        
        // 初始化数据
        class func initData(){
            CBInterceptURLProtocol.res["bootstrap.min.css"] = "res/css"
            CBInterceptURLProtocol.res["bootstrap.min.js"] = "res/js"
            CBInterceptURLProtocol.res["icon.png"] = "res/img"
            
            CBInterceptURLProtocol.type["bootstrap.min.css"] = "text/css"
            CBInterceptURLProtocol.type["bootstrap.min.js"] = "application/javascript"
            CBInterceptURLProtocol.type["icon.png"] = "image/png"
        }
        
        //拦截请求
        override class func canInitWithRequest(request: NSURLRequest) -> Bool {
            if CBInterceptURLProtocol.res.isEmpty {
                CBInterceptURLProtocol.initData()
            }
            
            let requestUrl = request.URL!.absoluteString
            for key in CBInterceptURLProtocol.res.keys{
                if requestUrl.hasSuffix(key) {
                    //返回true代表要使用本协议进行处理
                    return true
                }
            }
            //不使用该协议处理
            return false
        }
        
        <!--返回源请求-->
        override class func canonicalRequestForRequest(request: NSURLRequest) -> NSURLRequest{
            return request
        }
        
        //替换请求
        override func startLoading(){
            
            let path:NSString = self.request.URL!.path!
            
            var name:String!
            for key in CBInterceptURLProtocol.res.keys {
                if path.hasSuffix(key){
                    name = key ;
                    break ;
                }
            }
            
            if CBInterceptURLProtocol.res.indexForKey(name) == nil{
                return;
            }
            
            let dir = CBInterceptURLProtocol.res[name]
            let urlPath = NSBundle.mainBundle().pathForResource(name, ofType: nil, inDirectory:dir)
            let url = NSURL.fileURLWithPath(urlPath!)
            
            let type = CBInterceptURLProtocol.type[name]
            
            let data = NSData(contentsOfURL:url)
            
            let response = NSURLResponse(URL: url, MIMEType: type, expectedContentLength: data!.length, textEncodingName: "UTF-8")
            self.client!.URLProtocol(self, didReceiveResponse: response, cacheStoragePolicy: .NotAllowed)
            self.client!.URLProtocol(self, didLoadData: data!)
            self.client!.URLProtocolDidFinishLoading(self)
        }
        
        //加载结束不做特殊处理
        override func stopLoading() {
            
        }
    }
   
    
 实现自己的URLProtocol需要重写以下方法:
 
 - **canInitWithRequest**  决定是否拦截请求，不拦截的话交还给系统默认处理单元
 - **canonicalRequestForRequest** 拦截后的请求操作
 - **startLoading**  开始加载请求时的操作
 - **stopLoading**  加载结束的操作

    
### 3 注册拦截协议

进行了本地拦截，接着就是将拦截协议进行注册，在AppDelegate中加入以下代码

	 func application(application: UIApplication, didFinishLaunchingWithOptions launchOptions: [NSObject: AnyObject]?) -> Bool {
        NSURLProtocol.registerClass(CBInterceptURLProtocol)
        return true
    }


**经过几步的进行，已经可以将一些不变资源进行本地存储，并提供给UIWebView，网络流量也减少了很多。**


> 如有任何知识产权、版权问题或理论错误，还请指正。
>
> 转载请注明原作者及以上信息。
