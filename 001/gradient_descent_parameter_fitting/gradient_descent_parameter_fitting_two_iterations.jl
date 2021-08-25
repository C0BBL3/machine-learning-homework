
array =  [1 0 0;  1 1 1;  1 2 4]
x = [1 0;  1 1;  1 2]
y = [0;  1;  4]

coeffs = Dict("beta_0" => 0.0, "beta_1" => 2.0)
coeff_order = ["beta_0", "beta_1"]

function regression_function(coeffs, inputs)
    return sum([coeffs[coeff] * term for (coeff, term) in zip(coeff_order, inputs)])
end

function rss(coeffs)
    println("\n\t\t\trss ", [(regression_function(coeffs, row[1:(length(y) - 1)]) - row[length(y)]) ^ 2 for row in eachrow(array)] , "\n")
    return sum([(regression_function(coeffs, row[1:(length(y) - 1)]) - row[length(y)]) ^ 2 for row in eachrow(array)]) 
end

function calc_gradient(coeffs, learning_rate = 0.001)
    gradient = Dict()
    temp = Dict(beta => coeff for (beta, coeff) in coeffs)
    for key in coeff_order
        println("\n\tkey ", key)
        println("\n\t\ttemp[key] + learning_rate ", temp[key] + learning_rate)
        temp[key] += learning_rate
        plus_prediction = rss(temp)
        println("\t\tplus_prediction ", plus_prediction)
        println("\t\ttemp[key] + learning_rate ", temp[key] - 2 * learning_rate)
        temp[key] -= 2 * learning_rate
        minus_prediction = rss(temp)
        println("\t\tminus_prediction ", minus_prediction)
        temp[key] += learning_rate
        println("\t\t(plus_prediction - minus_prediction) ", (plus_prediction - minus_prediction))
        println("\t\t(plus_prediction - minus_prediction) / (2 * learning_rate) ", (plus_prediction - minus_prediction) / (2 * learning_rate))
        push!(gradient, key => (plus_prediction - minus_prediction) / (2 * learning_rate))
    end
    return gradient
end

function descend(coeffs, learning_rate = 0.001)
    gradient = calc_gradient(coeffs, learning_rate)
    for key in coeff_order
        coeffs[key] -= gradient[key] * learning_rate
    end
    println("\n\tnew_coeffs ", coeffs)
    return coeffs
end

for i = 1:2
    println("\niteration ", i)
    global coeffs = descend(coeffs)
end