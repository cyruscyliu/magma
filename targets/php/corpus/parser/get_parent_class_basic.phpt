<?php

interface i {
    function test();
}

class foo implements i {
    function test() {
        var_dump(get_parent_class());
    }
}

class bar extends foo {
    function test_bar() {
        var_dump(get_parent_class($this));
    }
}

$bar = new bar;
$foo = new foo;

set_error_handler(function ($severity, $message, $file, $line) {
    throw new Exception($message);
});
try {
    $foo->test();
} catch (Exception $e) {
    echo $e->getMessage() . "\n";
}
set_error_handler(null);

$foo->test();
$bar->test();
$bar->test_bar();

var_dump(get_parent_class($bar));
var_dump(get_parent_class($foo));
var_dump(get_parent_class("bar"));
var_dump(get_parent_class("foo"));
var_dump(get_parent_class("i"));

try {
    get_parent_class("");
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}

try {
    get_parent_class("[[[[");
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}

try {
    get_parent_class(" ");
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}

var_dump(get_parent_class(new stdclass));

try {
    get_parent_class(array());
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}

try {
    get_parent_class(1);
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}

echo "Done\n";
?>