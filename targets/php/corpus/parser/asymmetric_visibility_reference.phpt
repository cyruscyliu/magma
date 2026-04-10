<?php

class Foo {
    public private(set) int $bar = 0;

    public function test() {
        $bar = &$this->bar;
        $bar++;
    }
}

$foo = new Foo();

try {
    $bar = &$foo->bar;
    $bar++;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($foo->bar);

$foo->test();
var_dump($foo->bar);

?>