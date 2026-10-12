<?php

class Box {
    public ?Test $value;
}

class Test {
    function __destruct() {
        global $box;
        $box->value = null;
    }
}

function test($box) {
    var_dump($box->value = new Test);
}

$box = new Box();
$box->value = new Test;
test($box);
// Second call tests the cache slot path
test($box);

?>