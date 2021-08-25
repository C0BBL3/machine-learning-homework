using LinearAlgebra
x = [0 1; 1 1; 2 1; 3 1;]
y = [0; 1; 4; 9]
x_transpose = transpose(x)
println("x_transpose ", x_transpose)
x_transpose_times_x = x_transpose * x
println("x_transpose_times_x ", x_transpose_times_x)
x_transpose_times_x_inverse = inv(x_transpose_times_x)
println("x_transpose_times_x_inverse ", x_transpose_times_x_inverse)
x_inverse = x_transpose_times_x_inverse * x_transpose
println("x_inverse ", x_inverse)
x_pseudo_inverse = pinv(x)
println("x_pseudo_inverse ", x_pseudo_inverse)

beta_inverse = x_inverse * y
println("beta_inverse ", beta_inverse)

beta_pseudo_inverse = x_pseudo_inverse * y
println("beta_pseudo_inverse ", beta_pseudo_inverse)