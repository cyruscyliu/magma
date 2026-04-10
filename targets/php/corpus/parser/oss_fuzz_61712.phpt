<?php
#[AllowDynamicProperties]
class C {
    function error($_, $msg) {
        echo $msg, "\n";
        unset($this->a);
    }
}

$c = new C;
set_error_handler([$c, 'error']);
$c->a %= 10;
var_dump($c->a);
?>