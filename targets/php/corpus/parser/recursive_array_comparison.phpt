<?php
$a = [&$a];
try {
    $a === [[]];
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    [[]] === $a;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($a === $a);
?>