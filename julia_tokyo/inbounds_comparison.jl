using BenchmarkTools
x = [1, 2, 3]

f(x, i) = @inbounds x[i]

g(x, i) = x[i]


@btime f(x, 1)

@btime g(x, 1)
