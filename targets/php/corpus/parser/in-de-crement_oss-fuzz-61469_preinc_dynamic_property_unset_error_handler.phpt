<?php
class C {
    function errorHandle() {
        unset($this->a);
    }
}
$c = new C;
set_error_handler([$c,'errorHandle']);
(++$c->a);
var_dump($c->a);
?>