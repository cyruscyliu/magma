<?php

class Foo {
    public private(set) array $bars = [];

    public function addBar($bar) {
        $this->bars[] = $bar;
    }
}

$foo = new Foo();

try {
    $foo->bars[] = 'baz';
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($foo->bars);

$foo->addBar('baz');
var_dump($foo->bars);

?>