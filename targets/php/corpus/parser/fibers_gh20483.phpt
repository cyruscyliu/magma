<?php
$callback = function () {};
$fiber = new Fiber($callback);
try {
    $fiber->start();
} catch (Exception $e) {
    echo $e->getMessage() . "\n";
}
?>