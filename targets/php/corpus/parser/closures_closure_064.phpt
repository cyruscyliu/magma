<?php
function get_closure3($c) {
    return function () use ($c) {
        return $c();
    };
}
function throws() {
    throw new \Exception();
}
$throws = throws(...);
$closure1 = function() use ($throws) { $throws(); };
$closure2 = fn () => $closure1();
$closure3 = get_closure3($closure2);
\array_map(
    function ($item) use ($closure3) { $closure3(); },
    [1]
);
?>