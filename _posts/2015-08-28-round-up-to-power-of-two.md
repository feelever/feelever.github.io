---
layout: post
title: 'Round Up To Power Of Two'
date: '2015-08-28'
header-img: "img/post-bg-java.jpg"
tags:
     - java
author: 'Codeboy'
---

这个标题应该说明了我们要做什么了，中文的意思是找出一个2^n的数，使其不小于给出的数字。举个例子吧: 如果给一个数字63，那么我需要获取不小于63的数字，但是这个数字需要是2的n次方了，所以

- 63对应的是64(2^6)
- 64对应的依旧是64(2^6)
- 100对应的是128(2^7)

问题来了:
  
## 怎么快速的计算出这个结果呢？

可能首先浮现在我们眼前的可能是计算log或者一些其他的一些非位操作的算法，这些算法就不再次说明，来看一下JDK以及android的源码包中是怎么来计算的。

HashMap是一种常用的数据结果，底层是数组与链表的结合，为了能够使key尽量分布均匀，减少碰撞，HashMap的容量都是2^n，容量是2^n的另一个好处是在计算hashcode % size的时候可以使用与操作代替(实现远离可以google上查看)，当我们需要构造一个指定容量(记为sizeA)的HashMap时，HashMap帮我们计算出了不小于sizeA的SizeB，sizeB满足2^n。
具体实现在android的java.util.Collections中:

```
 /**
     * Returns the smallest power of two >= its argument, with several caveats:
     * If the argument is negative but not Integer.MIN_VALUE, the method returns
     * zero. If the argument is > 2^30 or equal to Integer.MIN_VALUE, the method
     * returns Integer.MIN_VALUE. If the argument is zero, the method returns
     * zero.
     *
     * @hide
     */
    public static int roundUpToPowerOfTwo(int i) {
        i--; // If input is a power of two, shift its high-order bit right.

        // "Smear" the high-order bit all the way to the right.
        i |= i >>> 1;
        i |= i >>> 2;
        i |= i >>> 4;
        i |= i >>> 8;
        i |= i >>> 16;

        return i + 1;
    }
```

而在JDK源码中的实现:

```
    private static int roundUpToPowerOf2(int number) {
        // assert number >= 0 : "number must be non-negative";
        return number >= MAXIMUM_CAPACITY
                ? MAXIMUM_CAPACITY
                : (number > 1) ? Integer.highestOneBit((number - 1) << 1) : 1;
    }

    public static int highestOneBit(int i) {
        // HD, Figure 3-1
        i |= (i >> 1);
        i |= (i >> 2);
        i |= (i >> 4);
        i |= (i >> 8);
        i |= (i >> 16);
        return i - (i >>> 1);
    }
```
虽然android中的java相关源码变动了部分，但是两者的实现基本是相同的，下面以上面一种为基准，阐述一下原理。
为了能够获取数字num对应的2^n对应的数值res，需要找出num对应二进制的最高位，如果num刚好满足2^n,即除最高位外其他位均是0，为了能够统一处理，将num首先减去1，这样如果res满足2^n,那么最高位现在处于原来的次高位，但是如果num不满足2^n，那么最高位不变,所以此时我们可以将num最高位(减1后新的最高位)后面的位全部置为1，然后加1即满足2^n,这样操作下来满足2^n的保持原样(num=res)，不满足2^n的num最后进了一位，也得到了结果。

操作中将最后为后面的位都置1也是非常妙的操作，使用最高位把次高位置为1，此时最高位与次高位都为1(num>>>1后与num或操作)，然后用最高位与次高位2位将次高位后面的2位置1，依次类推，由于HashMap定义的最大容量为2^30,所以最多只需5次操作，即可将最高位后面的位均置为1，非常的巧妙。




> 如有任何知识产权、版权问题或理论错误，还请指正。
>
> 转载请注明原作者及以上信息。
