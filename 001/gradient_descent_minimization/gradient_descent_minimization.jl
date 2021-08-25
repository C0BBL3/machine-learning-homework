avg = []
for i = 1:10
    start_time = time_ns()

    derivatives = Dict('x' => (dx(coords) = 4 * coords['x']), 'y' => (dy(coords) = 6 * coords['y']))
    best_coords = Dict('x' => 0, 'y' => 0) # f(x,y) = 1
    current_coords = Dict('x' => 1, 'y' => 2) # f(x,y) = 15

    function descend(current_coords, learning_rate = 0.001)
        new_coords = Dict(cart => pos for (cart, pos) in current_coords)

        for cart in keys(current_coords)
            new_coords[cart] -= derivatives[cart](current_coords) * learning_rate
        end

        return new_coords
    end

    function f(coords) 
        return 1 + 2 * coords['x'] ^ 2 + 3 * coords['y'] ^ 2
    end

    while float(f(current_coords)) > float(f(best_coords)) # or for _ in range(10000)
        current_coords = descend(current_coords)
    end

    append!(avg, (time_ns() - start_time))
end

println("Julia: ", sum(avg) / 1000000000 / 10)