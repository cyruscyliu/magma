<?php

#[AllowDynamicProperties]
class C {
    public $a {
        get => 42;
    }
}

$obj = new C();
$b = &$obj->b;
unset($b);
echo json_encode($obj);

?>