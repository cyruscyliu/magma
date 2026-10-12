<?php
function number() {
    return 6;
}

// We need to use a function to trick the optimizer *not* to optimize the array to a constant
$x = [number() => 0, ...[1, 1, 1]];
print_r($x);
?>