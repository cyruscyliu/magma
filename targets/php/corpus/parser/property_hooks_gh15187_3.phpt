<?php

class C {
    public $a { set {} }
    public int $b;
    public int $c = 1;
    public $d = 2;
}

$c = new C();

foreach ($c as $k => &$v) {
    var_dump($v);
    if ($k === 'c') {
        try {
            $v = 'foo';
        } catch (Error $e) {
            echo $e->getMessage(), "\n";
        }
    }
    if ($k === 'd') {
        $v = 'foo';
    }
}

var_dump($c);

?>