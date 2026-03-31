<?php

readonly class Foo
{
}

$foo = new Foo();

try {
    $foo->bar = 1;
} catch (Error $exception) {
    echo $exception->getMessage() . "\n";
}

?>