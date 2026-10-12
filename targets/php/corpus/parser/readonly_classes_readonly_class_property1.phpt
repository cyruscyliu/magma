<?php

readonly class Foo
{
    public int $bar;

    public function __construct() {
        $this->bar = 1;
    }
}

$foo = new Foo();

try {
    $foo->bar = 2;
} catch (Error $exception) {
    echo $exception->getMessage() . "\n";
}

?>