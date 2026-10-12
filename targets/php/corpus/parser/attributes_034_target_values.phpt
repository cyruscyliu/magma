<?php

function showFlag(string $name, int $value) {
    $all = Attribute::TARGET_ALL;
    $and = $all & $value;
    echo "Attribute::$name = $value ($all & $value === $and)\n";
}

showFlag("TARGET_CLASS", Attribute::TARGET_CLASS);
showFlag("TARGET_FUNCTION", Attribute::TARGET_FUNCTION);
showFlag("TARGET_METHOD", Attribute::TARGET_METHOD);
showFlag("TARGET_PROPERTY", Attribute::TARGET_PROPERTY);
showFlag("TARGET_CLASS_CONSTANT", Attribute::TARGET_CLASS_CONSTANT);
showFlag("TARGET_PARAMETER", Attribute::TARGET_PARAMETER);
showFlag("TARGET_CONSTANT", Attribute::TARGET_CONSTANT);
showFlag("IS_REPEATABLE", Attribute::IS_REPEATABLE);

$all = Attribute::TARGET_CLASS | Attribute::TARGET_FUNCTION
    | Attribute::TARGET_METHOD | Attribute::TARGET_PROPERTY
    | Attribute::TARGET_CLASS_CONSTANT | Attribute::TARGET_PARAMETER
    | Attribute::TARGET_CONSTANT;
var_dump($all, Attribute::TARGET_ALL, $all === Attribute::TARGET_ALL);

?>