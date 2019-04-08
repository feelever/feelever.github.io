---
layout: post
title: 'Get and Post'
date: '2014-10-03'
header-img: "img/post-bg-web.jpg"
tags:
     - web
author: 'Codeboy'
---

最近在做一些有关文件上传等的工作,遇到了以下的问题:

**将表单以post方式提交给一个有参数的url(如:res.php?param=aaa),这样的得到的结果将会是什么呢?**

下面就从几个例子将有关get与post的相关内容进行测试:

get(参数名字相同)
----
	<html>
	<body>
	<?php
	echo $_GET ['param'];
	?>
	    <form action="get_post_test.php?param=aaa" method="get">
	        <input type="text" name="param" value="bbb" /> 
	        <input type="submit" value="submit">
	    </form>
	</body>
	</html>
		
**input的value覆盖了url后面的值,获得了的param的为bbb.**

get(参数名字不相同)
----
	<html>
	<body>
	<?php
	echo $_GET ['param1'];
	echo "<br>";
	echo $_GET ['param2'];
	?>
	    <form action="get_post_test.php?param1=aaa" method="get">
	        <input type="text" name="param2" value="bbb" /> 
	        <input type="submit" value="submit">
	    </form>
	</body>
	</html>
	
**获取了param2的值,但是没有得到param1的值,说明以get方式提交将原先url的参数抹去了.**

post(参数名字相同)
----
	<html>
	<body>
	<?php
	echo "get=" . $_GET ['param'];
	echo "<br>";
	echo "post=" . $_POST ['param'];
	?>
	    <form action="get_post_test.php?param=aaa" method="post">
	        <input type="text" name="param" value="bbb" /> <input type="submit"
	            value="submit">
	    </form>
	</body>
	</html>
	
**输出的结果是get方式获得的是aaa, post方式获取的是bbb,说明此种情况下互不影响.get与post单独隔离开了.**

post(参数名字不相同)
----
	<html>
	<body>
	<?php
	echo "get=" . $_GET ['param2'];
	echo "<br>";
	echo "post=" . $_POST ['param1'];
	?>
	    <form action="get_post_test.php?param1=aaa" method="post">
	        <input type="text" name="param2" value="bbb" /> 
	        <input type="submit" value="submit">
	    </form>
	</body>
	</html>

**获取的参数全部为空,所以可以说php中get与post获取的参数是相互隔离的.**


***
**<span style="color:red; text-align:center;">传递post参数的时候可以附带将get的参数一块传递</span>**

***

*使用java进行文件上传的时候,可以正确的获取所有数据,即servlet里面可以使用request获取不论是post的表单数据或者是url后的get数据.毕竟servlet中获取参数的方法是一样的.*

> 如有任何知识产权、版权问题或理论错误，还请指正。
>
> 转载请注明原作者及以上信息。
