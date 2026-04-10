<?php
class A {
    public const self CONST1 = C;
}

try {
    define("C", new A());
} catch (Error $exception) {
    echo $exception->getMessage() . "\n";
}
?>