<?php

// Not packed
$a = ["k" => 0, 1 => 1, 2, 3, 4, 5, 6];
foreach ($a as $k => &$v) {
    if ($k == 1) {
        // force that it'll be rehashed by adding enough holes
        unset($a[4], $a[5]);
        // actually make the array larger than 8 elements to trigger rehash
        $a[] = 8; $a[] = 9; $a[] = 10;

    }
    // observe the iteration jumping from key 1 to key 6, skipping keys 2 and 3
    echo "$k => $v\n";
}

?>