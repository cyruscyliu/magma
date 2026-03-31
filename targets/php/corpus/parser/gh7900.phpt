<?php

$x = fn(): never => throw new \Exception('Here');

try {
    var_dump($x());
} catch (\Exception $e) {
    echo $e->getMessage(), "\n";
}

try {
    assert((fn(): never => 42) && false);
} catch (\Error $e) {
    echo $e->getMessage(), "\n";
}

?>