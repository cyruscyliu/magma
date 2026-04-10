<?php
class Foo { }
$o = new Foo;

try {
    $o++;
} catch (\TypeError $e) {
    echo $e->getMessage(), PHP_EOL;
    var_dump($o);
}
try {
    $o--;
} catch (\TypeError $e) {
    echo $e->getMessage(), PHP_EOL;
    var_dump($o);
}
try {
    ++$o;
} catch (\TypeError $e) {
    echo $e->getMessage(), PHP_EOL;
    var_dump($o);
}
try {
    --$o;
} catch (\TypeError $e) {
    echo $e->getMessage(), PHP_EOL;
    var_dump($o);
}
?>