<?php

class Test {
    public $prop {
        get { echo "get called\n"; }
        set { echo "set called with $value\n"; }
    }
}

$test = new Test;
try {
    $test->{'$prop::get'}();
} catch (\Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    $test->{'$prop::set'}('foo');
} catch (\Error $e) {
    echo $e->getMessage(), "\n";
}

?>