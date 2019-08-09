# safepoint
## 场景
* Running interpreted：interpeter dispatch table强行要求其检验安全点；
* Running in native code:使用一种叫做serialization page的内存记录法处理本地调用后返回os::serialize_thread_states()
* Running compiled Code:Safepoint Polling page实现
* Blocked：safepoint未结束前不允许返回
* In VM or Transitioning between states：等待其转换状态的时候block。
##
```
assert(myThread->is_VM_thread(), "Only VM thread may execute a safepoint");
Threads_lock->lock();//通过快速锁和自旋锁进行快速锁定，不用重锁
    TryFast();//如果嗅探到可以执行成功则返回
    TrySpin(); //SpinPause(),delay *= 1 + 1/Exponent;Delay += 1 + (Delay/4); Delay &= 0x7FF ;
RuntimeService::record_safepoint_begin();
```