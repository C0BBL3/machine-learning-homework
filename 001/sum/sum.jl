avg = []
for i = 1:10
    start_time = time_ns()
    sum_ = sum(1:100000)
    append!(avg, (time_ns() - start_time))
end

println("Julia: ", sum(avg) / 1000000000 / 10)