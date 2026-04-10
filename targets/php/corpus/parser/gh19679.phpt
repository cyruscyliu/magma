<?php
function test() {
    $a = PHP_INT_MIN+1;
    $b = 0;
    while ($b++ < 3) {
        $a = (int) ($a-- - $b - 1);
    }
    return $a;
}
var_dump(test() == PHP_INT_MIN);
?>