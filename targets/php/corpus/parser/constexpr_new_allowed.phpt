<?php

#[SomeAttribute(new stdClass)]
class Test {
    public function __construct(
        public $prop = new stdClass,
    ) {
        var_dump($prop);
    }
}

function test($param = new stdClass) {
    static $var = new stdClass;
    var_dump($param, $var);
}

const TEST = new stdClass;

new Test;
test();
var_dump(TEST);

?>