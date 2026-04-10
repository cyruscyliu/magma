<?php
class C {
    function errorHandle() {
        unset($this->a);
    }
}
$c = new C;
set_error_handler([$c,'errorHandle']);

$v = ($c->a--);
var_dump($c->a);
var_dump($v);
?>