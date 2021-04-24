## Juliaでシミュレーション高速化

---

### めっちゃたくさんランダムウォークがしたい！！！！！


---

#### 自己紹介(1/2)
数学科 M2  
解析学/確率解析/大規模相互作用系が好き  
翻訳レビューとか(ヨシ！係)  
(Juliaプログラミングクックブック  
IPythonデータサイエンス第二版)  
求職中

---

#### 自己紹介(2/2)

趣味等  
キーボード/キーキャップ集め  
好きなスイッチ:Gateron Clear(35g)  
好きなキット:Choco60, Attack25(∵左右分割は自明に体に良い)  
(明日の天キー行く方よろしくお願いします)


---


## やってること

- N個(>10000)のランダムウォークする粒子を考える |
- 2種類あって、異粒子とは相互作用を持つ |
- Pythonによる数値計算とシミュレーションの感染症モデルに少し似ている |

---


## なぜJuliaか？
- Python→遅い | 
- C++→読めない  |
- MATLAB→不便 | 
- ∴やっぱりJulia |

---

## 話すこと  
- 少しの変更で早くしたい |
- structureのバッドプラクティス  |
- マクロでちょっと早くなるかもしれない  |
- 初代秘伝のタレにならないために  |
- デバッグ等  |


---

## 話さないこと  

- 相互作用の具体的な決め方  |
- 理論的なこと(後日発表するので) |

---

### 少しの変更で早くしたい
- 型宣言する | 
- const使う |
- etc... |
```
x::Int8
const N = 10000
```

---

### structureでのバッドプラクティス

数直線上の原点に10000個粒子置きたいとき
```particle.jl
mutable struct particle
    x::Int8
end
```
Pythonっぽく生成
```.jl
@benchmark particles = [particle(0) for i in 1:10000]
```

---


結果
```result.jl
BenchmarkTools.Trial: 
  memory estimate:  234.45 KiB
  allocs estimate:  10002
  --------------
  minimum time:     44.139 μs (0.00% GC)
  median time:      52.413 μs (0.00% GC)
  mean time:        69.416 μs (19.93% GC)
  maximum time:     44.029 ms (99.74% GC)
  --------------
  samples:          10000
  evals/sample:     1
```

---

もっとよくなりそう  
undefのstructureの配列を作っておいて、あとから決めてみる  

```.jl
@benchmark particles = Array{particle}(undef, 10000)
```

```.jl
function generate_particle(particles)
    n = length(particles)
    for i in 1:n
        particles[i] = particle(0)
    end
    return particles
end
```

```.jl
@benchmark generate_particle(particles)
```

---
 
##### 結果


```
BenchmarkTools.Trial: 
  memory estimate:  78.20 KiB
  allocs estimate:  2
  --------------
  minimum time:     3.276 μs (0.00% GC)
  median time:      4.784 μs (0.00% GC)
  mean time:        7.513 μs (33.78% GC)
  maximum time:     5.444 ms (99.85% GC)
  --------------
  samples:          10000
  evals/sample:     8

  BenchmarkTools.Trial: 
  memory estimate:  156.25 KiB
  allocs estimate:  10000
  --------------
  minimum time:     38.285 μs (0.00% GC)
  median time:      39.740 μs (0.00% GC)
  mean time:        53.794 μs (18.21% GC)
  maximum time:     39.398 ms (99.73% GC)
  --------------
  samples:          10000
  evals/sample:     1

```



```
BenchmarkTools.Trial: 
  memory estimate:  156.25 KiB
  allocs estimate:  10000
  --------------
  minimum time:     27.323 μs (0.00% GC)
  median time:      29.851 μs (0.00% GC)
  mean time:        37.530 μs (16.71% GC)
  maximum time:     27.346 ms (99.78% GC)
  --------------
  samples:          10000
  evals/sample:     1
```




---

### マクロでちょっと早くなるかも知れない(1/2)
#### そのループ　早くなるかも　知れません　ならなかったら　許してください

---

##### マクロでちょっと早くなるかも知れない(1/2)
### @inbounds
#### 境界チェックを外して要素へのアクセスを早くする


---



```
A = rand(100)

function access_list(x, i)
    return x[i]
end

function access_list_inbounds(x, i)
    return @inbounds x[i]
end

@btime access_list(A, 1)

@btime access_list_inbounds(A, 1)

```
結構早くなる
```
16.956 ns (1 allocation: 16 bytes)

14.909 ns (1 allocation: 16 bytes)
```



---

#### @inboundsの注意点

@inbounds無し
```
access_list(A, 101)
BoundsError: attempt to access 100-element Array{Float64,1} at index [101]

```
ちゃんとエラーを吐いてくれる

---

```
access_list_inbounds(A, 101)
0.0
```


140541771354176だったり2だったり0だったり落ちたりする  
意図しない値なのにエラー吐いてくれない

---

#### コマンドラインからも境界チェックを外せる
boundserror.jlを次のように決める
```boundserror.jl
x = [1, 2]
for i in 1:10
    println(x[i])
end
```


```
julia boundserror.jl
1
2
ERROR: LoadError: BoundsError: attempt to access 2-element Array{Int64,1} at index [3]
```


エラーを出してくれる



---




境界チェックを外す

```
julia --check-bounds=no  boundserror.jl
1
2
0
140541771354176
140541771401456
2
569348
2
2
0
```
エラー出してくれない

---

```
julia> @doc @inbounds
...
  │ Warning
  │
  │  Using @inbounds may return incorrect results/crashes/corruption
  │  for out-of-bounds indices. The user is responsible for checking it
  │  manually. Only use @inbounds when it is certain from the
  │  information locally available that all accesses are in bounds.
```
クラッシュすることもあるらしい

---

#### @inboundsの挙動を@code_nativeで見てみる(クックブックにある例)

```
julia> f(x) = x[1]
f (generic function with 1 method)

julia> g(x) = @inbounds x[1]
g (generic function with 1 method)
```

---

```
julia> @code_native f([1])
        .text
; ┌ @ REPL[1]:1 within `f'
; │┌ @ REPL[1]:1 within `getindex'
        cmpq    $0, 8(%rdi)
        je      L14
        movq    (%rdi), %rax
        movq    (%rax), %rax
; │└
        retq
L14:
        pushq   %rbp
        movq    %rsp, %rbp
; │ @ REPL[1]:1 within `f'
; │┌ @ array.jl:729 within `getindex'
        movq    %rsp, %rax
        leaq    -16(%rax), %rsi
        movq    %rsi, %rsp
        movq    $1, -16(%rax)
        movabsq $jl_bounds_error_ints, %rax
        movl    $1, %edx
        callq   *%rax
        nopw    %cs:(%rax,%rax)
; └└
```

---

```
julia> @code_native g([1])
        .text
; ┌ @ REPL[2]:1 within `g'
; │┌ @ REPL[2]:1 within `getindex'
        movq    (%rdi), %rax
        movq    (%rax), %rax
; │└
        retq
        nopw    (%rax,%rax)
; └
```

わからん...


---

#### @code_llvmで見てみる
```
julia> @code_llvm f([1])

;  @ REPL[2]:1 within `f'
define i64 @julia_f_12234(%jl_value_t addrspace(10)* nonnull align 16 dereferenceable(40)) {
top:
; ┌ @ array.jl:729 within `getindex'
   %1 = addrspacecast %jl_value_t addrspace(10)* %0 to %jl_value_t addrspace(11)*
   %2 = bitcast %jl_value_t addrspace(11)* %1 to %jl_array_t addrspace(11)*
   %3 = getelementptr inbounds %jl_array_t, %jl_array_t addrspace(11)* %2, i64 0,
i32 1
   %4 = load i64, i64 addrspace(11)* %3, align 8
   %5 = icmp eq i64 %4, 0
   br i1 %5, label %oob, label %idxend

oob:                                              ; preds = %top
   %6 = alloca i64, align 8
   store i64 1, i64* %6, align 8
   %7 = addrspacecast %jl_value_t addrspace(10)* %0 to %jl_value_t addrspace(12)*
   call void @jl_bounds_error_ints(%jl_value_t addrspace(12)* %7, i64* nonnull %6, i64 1)
   unreachable

idxend:                                           ; preds = %top
   %8 = bitcast %jl_value_t addrspace(11)* %1 to i64 addrspace(13)* addrspace(11)*
   %9 = load i64 addrspace(13)*, i64 addrspace(13)* addrspace(11)* %8, align 8
   %10 = load i64, i64 addrspace(13)* %9, align 8
; └
  ret i64 %10
}
```

---

```
julia> @code_llvm g([1])

;  @ REPL[1]:1 within `g'
define i64 @julia_g_12239(%jl_value_t addrspace(10)* nonnull align 16 dereferenceable(40)) {
top:
; ┌ @ array.jl:729 within `getindex'
   %1 = addrspacecast %jl_value_t addrspace(10)* %0 to %jl_value_t addrspace(11)*
   %2 = bitcast %jl_value_t addrspace(11)* %1 to i64 addrspace(13)* addrspace(11)*
   %3 = load i64 addrspace(13)*, i64 addrspace(13)* addrspace(11)* %2, align 8
   %4 = load i64, i64 addrspace(13)* %3, align 8
; └
  ret i64 %4
}

```

@code_nativeより雰囲気がわかる気がする(気がする)  
(oob=out of boundsで境界見てる)

---

##### マクロでちょっと早くなるかも知れない(2/2)
### @simdつかう
```vectors.jl
a = zeros(100000)
b = rand(Int8, 100000)
c = rand(Int8, 100000)
d = rand(Int8, 100000)
```
を全部足したい場合を考える

---

```sum.jl
function sum_vectors(a, b, c, d)
    n = length(a)
    for i in 1:n
        a[i] = b[i] + c[i] + d[i]
    end
end

```

```sum_simd.jl
function sum_vectors_simd(a, b, c, d)
    n = length(a)
    @inbounds @simd for i in 1:n
        a[i] = b[i] + c[i] + d[i]
    end
end
```

---

#### 図ってみる

```results.jl
@benchmark sum_vectors(a, b, c, d)
BenchmarkTools.Trial: 
  memory estimate:  0 bytes
  allocs estimate:  0
  --------------
  minimum time:     125.474 μs (0.00% GC)
  median time:      125.556 μs (0.00% GC)
  mean time:        136.913 μs (0.00% GC)
  maximum time:     987.026 μs (0.00% GC)
  --------------
  samples:          10000
  evals/sample:     1
```

---

```results.jl
@benchmark sum_vectors_simd(a, b, c, d)
BenchmarkTools.Trial: 
  memory estimate:  0 bytes
  allocs estimate:  0
  --------------
  minimum time:     37.890 μs (0.00% GC)
  median time:      37.996 μs (0.00% GC)
  mean time:        40.743 μs (0.00% GC)
  maximum time:     534.254 μs (0.00% GC)
  --------------
  samples:          10000
  evals/sample:     1

```

---
#### 早くなってる
- とりあえずforの前に@simdつけておけばよいのでは？ |
- いいえ |

---

```simple_sum.jl
function usual_sum(n)
    z = 0
    for i in 1:n
        z = z + i
        end
    return z
end

@btime usual_sum(1000)
```

```
1.638 ns
```

---


```simd_sum.jl
function useless_simd(n)
    z = 0
    @inbounds @simd for i in 1:n
        z = z + i
        end
    return z
end

@btime useless_simd(1000)
```

```
1.693 ns (0 allocations: 0 bytes)
```




---


### 秘伝のタレ予防(1/2)

- JuliaFormatter使う | 
- Python教徒を引き込みたいのでindent=4にしてみる |
```
shell> cat awful_indent.jl
function say_hello()
	           println("hello")
                                  end


				  say_hello()
```
---


formatかける(overwrite=false)

```
julia> format_file("awful_indent.jl", indent = 4, margin = 81, overwrite = false, verbose = false, always_for_in = false)
shell> cat -n awful_indent_fmt.jl
function say_hello()
    println("hello")
end


say_hello()
```

---

### 秘伝のタレ予防(2/2)
コメントを大量に書く(忘れるので)

```
"""
関数の目的
"""

function hoge(x)...
```



---

### デバッグ等
ssh先で作業する時  
- ProgressMeter.jlを使う(画面埋めないように) |
- logging使う |

---

#### logging
ssh先での作業の時,接続先の情報など記録しておく

```
@info Sys.MACHINE
@warn "警告文かく"
run(`lscpu`)
@show ARGS PROGRAM_FILE
```

---

##### GPUの有無でコードを変える
```
try CuDevice(0)
    prinln("GPUでやりたい処理")
    catch
    println("GPUない\nCPUのみでやりたい処理")
end
```

---
### 参考
Julia High Performance(Second Edition)

[Loggingの公式ドキュメント](https://docs.julialang.org/en/v1/stdlib/Logging/)

Juliaプログラミングクックブック

[Juliaのコードを更に高速化する方法](https://myenigma.hatenablog.com/entry/2017/08/22/093953)

Pythonによる数値計算とシミュレーション