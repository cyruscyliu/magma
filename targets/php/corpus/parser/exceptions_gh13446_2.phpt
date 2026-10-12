<?php
$x = new \stdClass();
$handler = function ($ex) use (&$handler, $x) {
    $handler = null;
    var_dump($x);
};
unset($x);
set_exception_handler($handler);
throw new Exception('Unhandled');
?>