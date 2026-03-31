<?php
function foo() {
    return "OK";
}

$foo = foo(...);

echo $foo();
?>