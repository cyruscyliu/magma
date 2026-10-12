<?php

$i = 1;

$c = function ($p) use (&$i) {
    $self = Closure::getCurrent();
    var_dump($p, $i);
    $i++;
    if ($p < 10) {
        $self($p + 1);
    }
};

$c(1);
var_dump($i);

function fail() {
    Closure::getCurrent();
}

try {
    fail();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

function foo() {
    var_dump(Closure::getCurrent());
}

try {
    foo(...)();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>