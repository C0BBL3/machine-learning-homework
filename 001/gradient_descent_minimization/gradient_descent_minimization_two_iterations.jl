derivatives = Dict('x' => (dx(coords) = 4.0 * coords['x']), 'y' => (dy(coords) = 6.0 * coords['y']))
best_coords = Dict('x' => 0.0, 'y' => 0.0) # f(x,y) = 1
current_coords = Dict('x' => 1.0, 'y' => 2.0) # f(x,y) = 15

function descend(current_coords, learning_rate = 0.001)
    new_coords = Dict(cart => pos for (cart, pos) in current_coords)

    for cart in keys(current_coords)
        println("\n\tcart ", cart)
        println("\n\t\tderivatives[cart](current_coords) ", derivatives[cart](current_coords))
        println("\t\tderivatives[cart](current_coords) * learning_rate ", derivatives[cart](current_coords) * learning_rate)
        new_coords[cart] -= derivatives[cart](current_coords) * learning_rate
    end

    println("\n\tnew_coords ", new_coords)
    return new_coords
end

function f(coords) 
    return 1 + 2 * coords['x'] ^ 2 + 3 * coords['y'] ^ 2
end

for i = 1:2
    println("\niteration ", i)
    global current_coords = descend(current_coords)
end