<?php

foreach (array(array(1,2), array(3,4)) as list($a, )) {
    var_dump($a);
}

echo "Array of strings:\n";
$array = [['a', 'b'], 'c', 'd'];

foreach($array as list(, $a)) {
   var_dump($a);
}

echo "Array of ints:\n";
$array = [[5, 6], 10, 20];

foreach($array as list(, $a)) {
   var_dump($a);
}

echo "Array of nulls:\n";
$array = [[null, null], null, null];

foreach($array as list(, $a)) {
   var_dump($a);
}

?>