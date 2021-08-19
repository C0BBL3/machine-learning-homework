using LinearAlgebra

avg = []
for i = 1:10
    start_time = time_ns()
    x = [1 0; 1 1; 1 2; 1 3;]
    x_inverse = pinv(x)
    y = [0; 1; 4; 9]
    beta = x_inverse * y
    append!(avg, (time_ns() - start_time))
end

println("julia: ", sum(avg) / 1000000000 / 10)