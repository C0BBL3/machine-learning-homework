avg = []
for i = 1:10
    start_time = time_ns()

    array =  [1 0 0;  1 1 1;  1 2 4]
    x = [1 0;  1 1;  1 2]
    y = [0;  1;  4]

    coeffs = Dict("beta_0" => 0.0, "beta_1" => 2.0)
    coeff_order = ["beta_0", "beta_1"]

    function regression_function(coeffs, inputs)
        return sum([coeffs[coeff] * term for (coeff, term) in zip(coeff_order, inputs)])
    end

    function rss(coeffs)
        return sum([(regression_function(coeffs, row[1:(length(y) - 1)]) - row[length(y)]) ^ 2 for row in eachrow(array)]) 
    end

    function calc_gradient(coeffs, learning_rate = 0.001)
        gradient = Dict()
        temp = Dict(beta => coeff for (beta, coeff) in coeffs)
        for key in coeff_order
            temp[key] += learning_rate
            plus_prediction = rss(temp)
            temp[key] -= 2 * learning_rate
            minus_prediction = rss(temp)
            temp[key] += learning_rate
            push!(gradient, key => (plus_prediction - minus_prediction) / (2 * learning_rate))
        end
        return gradient
    end

    function descend(coeffs, learning_rate = 0.001)
        gradient = calc_gradient(coeffs, learning_rate)
        for key in coeff_order
            coeffs[key] -= gradient[key] * learning_rate
        end
        return coeffs
    end

    for i = 1:10000
        coeffs = descend(coeffs)
    end

    append!(avg, time_ns() - start_time)
end

print("Julia: ", sum(avg) / 1000000000 / 10)