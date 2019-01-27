# Striped64理解

## 关键

* table为延迟加载的基于一个Cell类的并发累加器
* table拓容为2的倍数,且不允许超过cpu个数
* Cell的hash原则为线程基于一个probe的hashcode策略，
* Cell的目的是减少cas的无效处理场景
* Cell通过sun.misc.Contented进行long padding
* probe的目的是减少线程的hash碰撞问题
* cell拓容采用spinlock方案保证安全
* 因为生命周期短，可重用，Cell对应的线程销毁之后cell不会被销毁；
  
## 流程

```mermaid
graph LR
st(start)-->ge[get probe]
ge-->co{exist table?}
co--yes-->sub(create table)
sub-->ifcell{cell null}
ifcell--yes-->ifspin{cell busy}
ifcell--no-->ifcon{uncoented}
ifcon--yes-->adv(adv probe)
ifcon--no-->uc{update cell}
uc--success-->ed[release lock]
uc--failed-->cp{over cpu num}
cp--yes-->sc(stop collide)
cp--no-->ec(collide can)
cp-->cb(get lock)
cb-->sc2[set cells]
sc2-->el[release lock]
el-->ed
ifspin--yes-->cc2(create cell)
cc2-->fout[update cell]
co--no-->co2{exits cell}
co2--no-->cc[create cell]
cc-->ed
co2--yes-->fout
fout-->ed
ed-->ends[end]
```