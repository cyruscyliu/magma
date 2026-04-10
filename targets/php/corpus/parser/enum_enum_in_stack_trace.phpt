<?php

enum Foo {
    case Bar;
}

function test($enum) {
    throw new Exception();
}

test(Foo::Bar);

?>