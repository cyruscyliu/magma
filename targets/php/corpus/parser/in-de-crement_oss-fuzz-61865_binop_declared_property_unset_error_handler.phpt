<?php
class C {
    public $a;
    function errorHandler($errno, $errstr) {
        unset($this->a);
    }
}
$c = new C;
set_error_handler([$c,'errorHandler']);
unset($c->a);
$c->a += 5;
var_dump($c->a);
?>