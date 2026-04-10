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
$v = ($c->a--);
var_dump($c->a);
var_dump($v);
?>