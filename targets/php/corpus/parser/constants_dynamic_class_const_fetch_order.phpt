<?php

class Foo {
    public const FOO = 'Foo';
}

function foo() {
    echo "foo()\n";
    return 'FOO';
}

function bar() {
    echo "bar()\n";
    return 'BAR';
}

function test($c) {
    try {
        echo $c(), "\n";
    } catch (Throwable $e) {
        echo $e->getMessage(), "\n";
    }
}

test(fn() => Foo::{foo()}::{bar()});
test(fn() => Foo::{bar()}::{foo()});

?>