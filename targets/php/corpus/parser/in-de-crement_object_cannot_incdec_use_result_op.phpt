<?php
class Foo { }
$o = new Foo;

try {
    $y = $o++;
} catch (\TypeError $e) {
    echo $e->getMessage(), PHP_EOL;
    var_dump($o);
}
try {
    $y = $o--;
} catch (\TypeError $e) {
    echo $e->getMessage(), PHP_EOL;
    var_dump($o);
}
try {
    $y = ++$o;
} catch (\TypeError $e) {
    echo $e->getMessage(), PHP_EOL;
    var_dump($o);
}
try {
    $y = --$o;
} catch (\TypeError $e) {
    echo $e->getMessage(), PHP_EOL;
    var_dump($o);
}
?>