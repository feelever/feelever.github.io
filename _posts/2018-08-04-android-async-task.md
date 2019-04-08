---
layout: post
title: 'Andorid AsyncTask解析'
date: '2018-08-04'
header-img: "img/post-bg-android.jpg"
tags:
     - android
author: 'Codeboy'
---

## 前言

AsyncTask 在Android开发中是一个经常用到的类，允许用户在工作线程上完成后台计算等任务，之后将结果同步UI线程，比起 Thread 和  Handler 模型使用起来方便一些。

AsyncTask 使用起来如此方便了，那么有什么需要注意的问题么？看一段AsyncTask官网的介绍文档：

```
When first introduced, AsyncTasks were executed serially on a single background thread. Starting with Build.VERSION_CODES.DONUT, this was changed to a pool of threads allowing multiple tasks to operate in parallel. Starting with Build.VERSION_CODES.HONEYCOMB, tasks are executed on a single thread to avoid common application errors caused by parallel execution.

If you truly want parallel execution, you can invoke executeOnExecutor(java.util.concurrent.Executor, Object[]) with THREAD_POOL_EXECUTOR.
```

可以看出，从 Android1.6 到  Android2.2 之间，AsyncTask是并行执行的，从HONEYCOMB(2.3)开始，为了避免并行执行造成的通用应用错误，任务的执行方式修改为串行。



## 分析

我们从最新的Android 8.0中分析一下AsyncTask：

```java
/**
 * An {@link Executor} that can be used to execute tasks in parallel.
 */
public static final Executor THREAD_POOL_EXECUTOR;

static {
    ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(
            CORE_POOL_SIZE, MAXIMUM_POOL_SIZE, KEEP_ALIVE_SECONDS, TimeUnit.SECONDS,
            sPoolWorkQueue, sThreadFactory);
    threadPoolExecutor.allowCoreThreadTimeOut(true);
    THREAD_POOL_EXECUTOR = threadPoolExecutor;
}
```

AsyncTask中定义了一个线程池，在我们执行execute(params)的时候的操作如下：

```java
@MainThread
public final AsyncTask<Params, Progress, Result> execute(Params... params) {
    return executeOnExecutor(sDefaultExecutor, params);
}
```

```java
@MainThread
public final AsyncTask<Params, Progress, Result> executeOnExecutor(Executor exec,
        Params... params) {
    if (mStatus != Status.PENDING) {
        switch (mStatus) {
            case RUNNING:
                throw new IllegalStateException("Cannot execute task:"
                        + " the task is already running.");
            case FINISHED:
                throw new IllegalStateException("Cannot execute task:"
                        + " the task has already been executed "
                        + "(a task can be executed only once)");
        }
    }

    mStatus = Status.RUNNING;

	//之前前的准备工作
    onPreExecute();

    mWorker.mParams = params;
    //真正添加任务并执行
    exec.execute(mFuture);

    return this;
}
```

其中Executor传递了一个sDefaultExecutor，sDefaultExecutor的定义如下:

```java
private static volatile Executor sDefaultExecutor = SERIAL_EXECUTOR;
public static final Executor SERIAL_EXECUTOR = new SerialExecutor();
//串行执行器
private static class SerialExecutor implements Executor {
    final ArrayDeque<Runnable> mTasks = new ArrayDeque<Runnable>();
    Runnable mActive;

    public synchronized void execute(final Runnable r) {
        //将任务加入队列中
        mTasks.offer(new Runnable() {
            public void run() {
                try {
                    r.run();
                } finally {
                    scheduleNext();
                }
            }
        });
        //如果首次添加，执行任务
        if (mActive == null) {
            scheduleNext();
        }
    }

    protected synchronized void scheduleNext() {
        if ((mActive = mTasks.poll()) != null) {
            THREAD_POOL_EXECUTOR.execute(mActive);
        }
    }
}
```

这里应该比较明确了，默认的executor使用的 SerialExecutor，而 SerialExecutor 的 execute 中的逻辑也很简单，直接添加队列，如果第一次添加的话，从队列中取出一个任务执行，进而达到了串行执行的结果。

到此，AsyncTask 为什么串行执行已经分析完毕。



## 使用

当前主流的应用，如手机淘宝、支付宝等的最低支持版本均已经是4.0，所以在开发中，系统的默认的AsyncTask的执行时串行的，我们可以进行修改。上面分析中也有提到，在AsyncTask执行execute方法的时候，使用了默认的Executor，我们可以使用AsyncTask中提供的另外一个方法 executeOnExecutor 指定线程池来执行，需要注意的一点是AsyncTask提供了线程池的 AsyncTask.THREAD_POOL_EXECUTOR ，我们可以使用这个线程池，但是这个线程池的参数中的队列长度是128，线程池拒绝策略采用的 AbortPolicy  ，任务超出线程池可承受范围(MAXIMUM_POOL_SIZE + POOL_SIZE)时，将会发生异常。

```java
private static final int CORE_POOL_SIZE = Math.max(2, Math.min(CPU_COUNT - 1, 4));
private static final int MAXIMUM_POOL_SIZE = CPU_COUNT * 2 + 1;
private static final int KEEP_ALIVE_SECONDS = 30;

//线程池队列
private static final BlockingQueue<Runnable> sPoolWorkQueue =
        new LinkedBlockingQueue<Runnable>(128);
```



如果我们使用这个线程池，添加了比较多的耗时任务，将会crash，测试代码如下：

```java
package me.codeboy.test;

import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;

import java.util.concurrent.LinkedBlockingDeque;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class MainActivity extends AppCompatActivity {
    private static final int CPU_COUNT = Runtime.getRuntime().availableProcessors();
    private static final int CORE_POOL_SIZE = Math.max(2, Math.min(CPU_COUNT - 1, 4));
    private static final int MAXIMUM_POOL_SIZE = CPU_COUNT * 2 + 1;
    private static final int KEEP_ALIVE_SECONDS = 30;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(
                CORE_POOL_SIZE, MAXIMUM_POOL_SIZE, KEEP_ALIVE_SECONDS, TimeUnit.SECONDS,
                new LinkedBlockingDeque<>(128));
        for (int i = 0; i < 200; i++) {
            new AsyncTask<Integer, Void, Void>() {
                @Override
                protected void onPostExecute(Void aVoid) {
                    super.onPostExecute(aVoid);

                }

                @Override
                protected Void doInBackground(Integer... params) {
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    if (params != null || params.length > 0) {
                        Log.e(MainActivity.this.getClass().getSimpleName(), "" + params[0]);
                    }
                    return null;
                }
            }.executeOnExecutor(threadPoolExecutor, i);
        }
    }
}
```

错误信息：

```

java.lang.RuntimeException: Unable to start activity ComponentInfo{me.codeboy.test/me.codeboy.test.MainActivity}: java.util.concurrent.RejectedExecutionException: Task android.os.AsyncTask$3@a1014c4 rejected from java.util.concurrent.ThreadPoolExecutor@2c4bfad[Running, pool size = 9, active threads = 9, queued tasks = 128, completed tasks = 0]
   at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:2817)
   at android.app.ActivityThread.handleLaunchActivity(ActivityThread.java:2892)
   at android.app.ActivityThread.-wrap11(Unknown Source:0)
   at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1593)
   at android.os.Handler.dispatchMessage(Handler.java:105)
   at android.os.Looper.loop(Looper.java:164)
   at android.app.ActivityThread.main(ActivityThread.java:6541)
   at java.lang.reflect.Method.invoke(Native Method)
   at com.android.internal.os.Zygote$MethodAndArgsCaller.run(Zygote.java:240)
   at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:767)
Caused by: java.util.concurrent.RejectedExecutionException: Task android.os.AsyncTask$3@a1014c4 rejected from java.util.concurrent.ThreadPoolExecutor@2c4bfad[Running, pool size = 9, active threads = 9, queued tasks = 128, completed tasks = 0]
   at java.util.concurrent.ThreadPoolExecutor$AbortPolicy.rejectedExecution(ThreadPoolExecutor.java:2078)
   at java.util.concurrent.ThreadPoolExecutor.reject(ThreadPoolExecutor.java:843)
   at java.util.concurrent.ThreadPoolExecutor.execute(ThreadPoolExecutor.java:1389)
   at android.os.AsyncTask.executeOnExecutor(AsyncTask.java:651)
   at me.codeboy.test.MainActivity.onCreate(MainActivity.java:50)
   at android.app.Activity.performCreate(Activity.java:6975)
   at android.app.Instrumentation.callActivityOnCreate(Instrumentation.java:1213)
   at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:2770)
   at android.app.ActivityThread.handleLaunchActivity(ActivityThread.java:2892) 
   at android.app.ActivityThread.-wrap11(Unknown Source:0) 
   at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1593) 
   at android.os.Handler.dispatchMessage(Handler.java:105) 
   at android.os.Looper.loop(Looper.java:164) 
   at android.app.ActivityThread.main(ActivityThread.java:6541) 
   at java.lang.reflect.Method.invoke(Native Method) 
   at com.android.internal.os.Zygote$MethodAndArgsCaller.run(Zygote.java:240) 
   at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:767) 
```

避免的方法是可以将队列大小加大或者不限制大小，在不限制大小的时候，如果MAXIMUM_POOL_SIZE和CORE_POOL_SIZE不同，那么MAXIMUM_POOL_SIZE将失去意义。




> 如有任何知识产权、版权问题或理论错误，还请指正。
>
> 转载请注明原作者及以上信息。
